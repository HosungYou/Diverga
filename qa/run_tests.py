#!/usr/bin/env python3
"""
Diverga QA Protocol v2.0 - Test Runner and Evaluator

Main entry point for running QA tests and generating reports.

Usage:
    python run_tests.py --all                    # Run all protocol tests
    python run_tests.py --evaluate-extracted ... # Evaluate extracted conversation
    python run_tests.py --report ...             # Generate report from results
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
import yaml

# Add runners to path
sys.path.insert(0, str(Path(__file__).parent))
from runners.extract_conversation import (
    ConversationExtractor,
    ConversationEvaluator,
    ExtractionResult,
)


@dataclass
class TestResult:
    """Single test result."""
    scenario_id: str
    passed: bool
    checks: list
    summary: dict
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    errors: list = field(default_factory=list)


@dataclass
class TestReport:
    """Complete test report."""
    generated_at: str
    total_scenarios: int
    passed: int
    failed: int
    pass_rate: float
    results: list
    summary: dict


class DivergaQARunner:
    """
    QA Test Runner for Diverga plugin.

    Orchestrates test execution, evaluation, and report generation.
    """

    PROTOCOL_DIR = Path(__file__).parent / "protocol"
    REPORTS_DIR = Path(__file__).parent / "reports"

    def __init__(self, verbose: bool = False):
        """Initialize runner."""
        self.verbose = verbose
        self.results: list[TestResult] = []

    def run_all(self) -> TestReport:
        """
        Run all protocol tests.

        Note: This validates protocol YAML files, not actual conversations.
        For real conversation testing, use evaluate_extracted().
        """
        print("=" * 60)
        print("Diverga QA Protocol v2.0 - Protocol Validation")
        print("=" * 60)
        print()

        protocol_files = list(self.PROTOCOL_DIR.glob("test_*.yaml"))

        if not protocol_files:
            print("No protocol files found in:", self.PROTOCOL_DIR)
            return self._generate_report()

        for protocol_file in protocol_files:
            self._validate_protocol(protocol_file)

        return self._generate_report()

    def _validate_protocol(self, protocol_path: Path) -> None:
        """Validate a protocol YAML file structure."""
        scenario_id = protocol_path.stem.replace("test_", "").upper()
        print(f"Validating: {scenario_id}...")

        try:
            with open(protocol_path, 'r', encoding='utf-8') as f:
                protocol = yaml.safe_load(f)

            checks = []

            # Check required fields
            required_fields = [
                'scenario_id', 'name', 'paradigm', 'agents_involved',
                'language', 'conversation_flow', 'checkpoints_expected'
            ]
            for field in required_fields:
                passed = field in protocol
                checks.append({
                    'name': f'Required field: {field}',
                    'passed': passed,
                    'details': ['Present' if passed else 'Missing']
                })

            # Check conversation flow structure
            flow = protocol.get('conversation_flow', [])
            if flow:
                for i, turn in enumerate(flow):
                    turn_valid = all(k in turn for k in ['turn', 'user', 'expected_behavior'])
                    if not turn_valid:
                        checks.append({
                            'name': f'Turn {i+1} structure',
                            'passed': False,
                            'details': ['Missing required keys']
                        })

            # Check checkpoints
            checkpoints = protocol.get('checkpoints_expected', [])
            for cp in checkpoints:
                cp_valid = all(k in cp for k in ['id', 'level'])
                if not cp_valid:
                    checks.append({
                        'name': f'Checkpoint {cp.get("id", "unknown")}',
                        'passed': False,
                        'details': ['Missing level or id']
                    })

            # Check agents format
            agents = protocol.get('agents_involved', [])
            if not isinstance(agents, list) or len(agents) == 0:
                checks.append({
                    'name': 'Agents list',
                    'passed': False,
                    'details': ['Must be non-empty list']
                })

            all_passed = all(c['passed'] for c in checks)

            result = TestResult(
                scenario_id=scenario_id,
                passed=all_passed,
                checks=checks,
                summary={
                    'total_checks': len(checks),
                    'passed': sum(1 for c in checks if c['passed']),
                    'failed': sum(1 for c in checks if not c['passed'])
                }
            )
            self.results.append(result)

            status = "PASS" if all_passed else "FAIL"
            print(f"  [{status}] {protocol.get('name', scenario_id)}")
            if self.verbose and not all_passed:
                for check in checks:
                    if not check['passed']:
                        print(f"    - {check['name']}: {check['details']}")

        except Exception as e:
            result = TestResult(
                scenario_id=scenario_id,
                passed=False,
                checks=[],
                summary={'error': str(e)},
                errors=[str(e)]
            )
            self.results.append(result)
            print(f"  [ERROR] {e}")

    def evaluate_extracted(
        self,
        extracted_path: str,
        expected_path: str
    ) -> TestResult:
        """
        Evaluate an extracted conversation against expected scenario.

        Args:
            extracted_path: Path to extracted conversation YAML/JSON
            expected_path: Path to expected scenario YAML

        Returns:
            TestResult with evaluation details
        """
        print("=" * 60)
        print("Diverga QA Protocol v2.0 - Conversation Evaluation")
        print("=" * 60)
        print()

        # Load extracted conversation
        with open(extracted_path, 'r', encoding='utf-8') as f:
            if extracted_path.endswith('.json'):
                extracted_data = json.load(f)
            else:
                extracted_data = yaml.safe_load(f)

        # Convert to ExtractionResult if dict
        if isinstance(extracted_data, dict):
            # Create a minimal ExtractionResult-like object
            class ExtractedResult:
                def __init__(self, data):
                    self.session_id = data.get('session_id', 'unknown')
                    self.scenario_id = data.get('scenario_id')
                    self.language = data.get('language', 'unknown')
                    self.total_turns = data.get('total_turns', len(data.get('turns', [])))
                    self.turns = data.get('turns', [])
                    self.checkpoints = data.get('checkpoints', [])
                    self.agents_invoked = data.get('agents_invoked', [])
                    self.metrics = data.get('metrics', {})

            extracted = ExtractedResult(extracted_data)
        else:
            extracted = extracted_data

        # Run evaluation
        evaluator = ConversationEvaluator(extracted, expected_path)
        eval_result = evaluator.evaluate()

        scenario_id = eval_result.get('scenario_id', extracted.scenario_id or 'unknown')

        result = TestResult(
            scenario_id=scenario_id,
            passed=eval_result.get('passed', False),
            checks=eval_result.get('checks', []),
            summary=eval_result.get('summary', {})
        )
        self.results.append(result)

        # Print results
        status = "PASS" if result.passed else "FAIL"
        print(f"Scenario: {scenario_id}")
        print(f"Status: [{status}]")
        print()
        print("Checks:")
        for check in result.checks:
            check_status = "✓" if check['passed'] else "✗"
            print(f"  {check_status} {check['name']}")
            for detail in check.get('details', []):
                print(f"      {detail}")
        print()
        print(f"Summary: {result.summary}")

        return result

    def evaluate_session(
        self,
        session_path: str,
        expected_path: str,
        scenario_id: Optional[str] = None
    ) -> TestResult:
        """
        Extract and evaluate a Claude Code session in one step.

        Args:
            session_path: Path to Claude Code session JSONL
            expected_path: Path to expected scenario YAML
            scenario_id: Optional scenario ID

        Returns:
            TestResult with evaluation details
        """
        print("Extracting conversation...")

        extractor = ConversationExtractor(session_path, scenario_id)
        extracted = extractor.extract()

        print(f"Extracted {extracted.total_turns} turns")
        print(f"Language: {extracted.language}")
        print(f"Checkpoints: {len(extracted.checkpoints)}")
        print(f"Agents: {len(extracted.agents_invoked)}")
        print()

        # Save extraction
        output_dir = self.REPORTS_DIR / "real-transcripts"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{scenario_id or extracted.session_id}.yaml"
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(asdict(extracted), f, default_flow_style=False, allow_unicode=True)
        print(f"Saved extraction: {output_file}")

        # Evaluate
        return self.evaluate_extracted(str(output_file), expected_path)

    def _generate_report(self) -> TestReport:
        """Generate test report from results."""
        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed
        pass_rate = (passed / len(self.results) * 100) if self.results else 0

        report = TestReport(
            generated_at=datetime.now().isoformat(),
            total_scenarios=len(self.results),
            passed=passed,
            failed=failed,
            pass_rate=round(pass_rate, 1),
            results=[asdict(r) for r in self.results],
            summary={
                'protocol_version': '2.0',
                'test_type': 'real_conversation',
                'total': len(self.results),
                'passed': passed,
                'failed': failed,
            }
        )

        return report

    def save_report(
        self,
        report: TestReport,
        output_dir: str,
        format: str = 'yaml'
    ) -> Path:
        """
        Save report to file.

        Args:
            report: TestReport to save
            output_dir: Output directory
            format: Output format ('yaml', 'json', 'html')

        Returns:
            Path to saved report
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qa_report_{timestamp}"

        if format == 'html':
            filepath = output_path / f"{filename}.html"
            self._generate_html_report(report, filepath)
        elif format == 'json':
            filepath = output_path / f"{filename}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(asdict(report), f, indent=2, ensure_ascii=False)
        else:
            filepath = output_path / f"{filename}.yaml"
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(asdict(report), f, default_flow_style=False, allow_unicode=True)

        print(f"\nReport saved: {filepath}")
        return filepath

    def _generate_html_report(self, report: TestReport, filepath: Path) -> None:
        """Generate HTML report."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Diverga QA Report - {report.generated_at}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; }}
        h1 {{ color: #1a1a2e; }}
        .summary {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .pass {{ color: #28a745; }}
        .fail {{ color: #dc3545; }}
        .scenario {{ border: 1px solid #dee2e6; border-radius: 8px; margin: 10px 0; padding: 15px; }}
        .scenario-header {{ font-weight: bold; font-size: 1.1em; }}
        .check {{ margin: 5px 0; padding: 5px 10px; }}
        .check-pass {{ background: #d4edda; }}
        .check-fail {{ background: #f8d7da; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #dee2e6; padding: 10px; text-align: left; }}
        th {{ background: #f8f9fa; }}
    </style>
</head>
<body>
    <h1>Diverga QA Protocol v2.0 Report</h1>

    <div class="summary">
        <h2>Summary</h2>
        <p>Generated: {report.generated_at}</p>
        <p>Total Scenarios: {report.total_scenarios}</p>
        <p>Passed: <span class="pass">{report.passed}</span></p>
        <p>Failed: <span class="fail">{report.failed}</span></p>
        <p>Pass Rate: <strong>{report.pass_rate}%</strong></p>
    </div>

    <h2>Scenario Results</h2>
"""

        for result in report.results:
            status_class = 'pass' if result['passed'] else 'fail'
            status_text = 'PASS' if result['passed'] else 'FAIL'

            html += f"""
    <div class="scenario">
        <div class="scenario-header">
            <span class="{status_class}">[{status_text}]</span> {result['scenario_id']}
        </div>
"""
            for check in result.get('checks', []):
                check_class = 'check-pass' if check['passed'] else 'check-fail'
                html += f"""
        <div class="check {check_class}">
            {'✓' if check['passed'] else '✗'} {check['name']}
        </div>
"""
            html += """    </div>
"""

        html += """
</body>
</html>
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Diverga QA Protocol v2.0 - Test Runner'
    )

    # Mode selection
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--all', '-a',
        action='store_true',
        help='Run all protocol validations'
    )
    mode_group.add_argument(
        '--evaluate-extracted',
        action='store_true',
        help='Evaluate extracted conversation against expected'
    )
    mode_group.add_argument(
        '--evaluate-session',
        action='store_true',
        help='Extract and evaluate Claude Code session'
    )

    # Input/output paths
    parser.add_argument(
        '--input', '-i',
        help='Path to extracted conversation or session JSONL'
    )
    parser.add_argument(
        '--expected', '-e',
        help='Path to expected scenario YAML'
    )
    parser.add_argument(
        '--scenario-id', '-s',
        help='Scenario ID for matching'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output directory for reports'
    )
    parser.add_argument(
        '--report-format', '-f',
        choices=['yaml', 'json', 'html'],
        default='yaml',
        help='Report format (default: yaml)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    runner = DivergaQARunner(verbose=args.verbose)

    if args.all:
        report = runner.run_all()

    elif args.evaluate_extracted:
        if not args.input or not args.expected:
            parser.error("--evaluate-extracted requires --input and --expected")
        runner.evaluate_extracted(args.input, args.expected)
        report = runner._generate_report()

    elif args.evaluate_session:
        if not args.input or not args.expected:
            parser.error("--evaluate-session requires --input and --expected")
        runner.evaluate_session(args.input, args.expected, args.scenario_id)
        report = runner._generate_report()

    # Print summary
    print()
    print("=" * 60)
    print(f"TOTAL: {report.total_scenarios} scenarios")
    print(f"PASSED: {report.passed}")
    print(f"FAILED: {report.failed}")
    print(f"PASS RATE: {report.pass_rate}%")
    print("=" * 60)

    # Save report if output specified
    if args.output:
        runner.save_report(report, args.output, args.report_format)

    # Exit with appropriate code
    sys.exit(0 if report.failed == 0 else 1)


if __name__ == '__main__':
    main()
