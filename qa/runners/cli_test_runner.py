#!/usr/bin/env python3
"""
Diverga QA Protocol v3.0 - True Automated Testing via CLI

Executes real AI conversations using CLI tools (Claude Code, OpenCode, Codex)
to capture actual AI responses instead of simulated templates.

Key differences from v2.x (simulation):
- v2.x: Uses RESPONSE_TEMPLATES dict with hardcoded responses
- v3.0: Uses subprocess to call CLI tools and capture real AI responses

Usage:
    python cli_test_runner.py --scenario QUAL-002 --cli claude
    python cli_test_runner.py --scenario META-002 --cli claude --output qa/reports/sessions
    python cli_test_runner.py --scenario QUAL-002 --dry-run  # Test without API calls
"""

import argparse
import json
import os
import re
import subprocess
import sys
import uuid
import yaml
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Turn:
    """A single conversation turn."""
    number: int
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str
    checkpoints_detected: List[str] = field(default_factory=list)
    agents_detected: List[str] = field(default_factory=list)
    vs_options: List[Dict] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestSession:
    """Complete test session result."""
    scenario_id: str
    cli_tool: str
    session_id: str
    start_time: str
    end_time: Optional[str] = None
    turns: List[Turn] = field(default_factory=list)
    checkpoints: List[Dict] = field(default_factory=list)
    agents_invoked: List[str] = field(default_factory=list)
    validation_results: Dict[str, Any] = field(default_factory=dict)
    status: str = "running"
    error: Optional[str] = None


class CLITestRunner:
    """
    CLI-based automated test runner for Diverga QA Protocol v3.0.

    Executes actual CLI commands to get real AI responses, unlike the
    v2.x simulator which uses hardcoded response templates.
    """

    SUPPORTED_CLIS = ['claude', 'opencode', 'codex']
    PROTOCOL_DIR = Path(__file__).parent.parent / "protocol"
    DEFAULT_TIMEOUT = 300  # 5 minutes per turn

    def __init__(
        self,
        scenario_id: str,
        cli_tool: str = 'claude',
        verbose: bool = False,
        dry_run: bool = False,
        timeout: int = 300
    ):
        self.scenario_id = scenario_id
        self.cli_tool = cli_tool
        self.verbose = verbose
        self.dry_run = dry_run
        self.timeout = timeout

        if cli_tool not in self.SUPPORTED_CLIS:
            raise ValueError(f"Unsupported CLI: {cli_tool}. Supported: {self.SUPPORTED_CLIS}")

        self.protocol = self._load_protocol()
        self.session_id = str(uuid.uuid4())
        self.session = TestSession(
            scenario_id=scenario_id,
            cli_tool=cli_tool,
            session_id=self.session_id,
            start_time=datetime.now().isoformat()
        )

        # Track conversation state
        self._turn_count = 0
        self._is_first_turn = True

    def _load_protocol(self) -> dict:
        """Load protocol YAML file."""
        # Convert scenario ID to file name (e.g., QUAL-002 -> test_qual_002.yaml)
        scenario_lower = self.scenario_id.lower().replace('-', '_')
        protocol_file = self.PROTOCOL_DIR / f"test_{scenario_lower}.yaml"

        if not protocol_file.exists():
            raise FileNotFoundError(f"Protocol not found: {protocol_file}")

        with open(protocol_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _build_claude_command(self, message: str, is_first_turn: bool) -> List[str]:
        """Build Claude Code CLI command."""
        # Escape special characters for shell
        # Use direct list format to avoid shell escaping issues
        if is_first_turn:
            # First turn: Start new session with Diverga skill
            prefix = "/diverga:research-coordinator\n\n"
            full_message = prefix + message
            return [
                'claude',
                '-p', full_message,
                '--output-format', 'text',
                '--allowedTools', 'Read,Glob,Grep,Task,WebSearch,WebFetch'
            ]
        else:
            # Subsequent turns: Continue conversation
            return [
                'claude',
                '-p', message,
                '--continue',
                '--output-format', 'text'
            ]

    def _build_opencode_command(self, message: str) -> List[str]:
        """Build OpenCode CLI command."""
        return ['opencode', 'run', message]

    def _build_codex_command(self, message: str) -> List[str]:
        """Build Codex CLI command."""
        return ['codex', 'exec', message]

    def _execute_cli(self, message: str) -> str:
        """Execute CLI command and capture response."""
        is_first = self._is_first_turn

        if self.cli_tool == 'claude':
            cmd = self._build_claude_command(message, is_first)
        elif self.cli_tool == 'opencode':
            cmd = self._build_opencode_command(message)
        elif self.cli_tool == 'codex':
            cmd = self._build_codex_command(message)
        else:
            raise ValueError(f"Unsupported CLI: {self.cli_tool}")

        if self.verbose:
            print(f"  [CMD] {' '.join(cmd[:3])}...")

        if self.dry_run:
            # Return mock response for dry run
            return self._get_dry_run_response(message, is_first)

        try:
            # Execute command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=Path(__file__).parent.parent.parent  # Diverga root
            )

            if result.returncode != 0:
                error_msg = f"CLI returned non-zero: {result.returncode}\nStderr: {result.stderr}"
                if self.verbose:
                    print(f"  [ERROR] {error_msg}")
                raise RuntimeError(error_msg)

            self._is_first_turn = False
            return result.stdout

        except subprocess.TimeoutExpired:
            raise TimeoutError(f"CLI command timed out after {self.timeout}s")
        except FileNotFoundError:
            raise RuntimeError(f"CLI tool '{self.cli_tool}' not found. Is it installed?")

    def _get_dry_run_response(self, message: str, is_first_turn: bool) -> str:
        """Generate mock response for dry run mode."""
        turn = self._turn_count + 1

        # Detect expected checkpoint from protocol
        conversation_flow = self.protocol.get('conversation_flow', [])
        expected_checkpoint = ""
        if turn <= len(conversation_flow):
            expected = conversation_flow[turn - 1].get('expected_behavior', {})
            if expected.get('checkpoint'):
                expected_checkpoint = f"\n\n🔴 CHECKPOINT: {expected['checkpoint']}\n\n옵션을 선택해 주세요:\n[A] 옵션 A (T=0.50)\n[B] 옵션 B (T=0.40) ⭐\n[C] 옵션 C (T=0.35)"

        return f"""[DRY RUN] Turn {turn} Response

This is a simulated response for dry run mode.
Message received: {message[:100]}...

Paradigm Detection: {self.protocol.get('paradigm', 'unknown')}
Language: {self.protocol.get('language', 'English')}
{expected_checkpoint}

---
DRY RUN MODE: No actual API calls made.
To run with real AI responses, remove --dry-run flag.
"""

    def _detect_checkpoints(self, response: str) -> List[str]:
        """Detect checkpoint markers in response."""
        checkpoints = []

        # Pattern matching for checkpoint markers
        # Note: Responses may include markdown bold markers (**) around checkpoint IDs
        patterns = [
            # With emoji + optional bold markers
            r'🔴\s*CHECKPOINT[:\s]+\*?\*?(CP_\w+)\*?\*?',
            r'🟠\s*CHECKPOINT[:\s]+\*?\*?(CP_\w+)\*?\*?',
            r'🟡\s*CHECKPOINT[:\s]+\*?\*?(CP_\w+)\*?\*?',
            # Plain text with optional bold
            r'CHECKPOINT[:\s]+\*?\*?(CP_\w+)\*?\*?',
            r'\*\*CHECKPOINT\*\*[:\s]+\*?\*?(CP_\w+)\*?\*?',
            # Without CP_ prefix (fallback)
            r'🔴\s*CHECKPOINT[:\s]+\*?\*?(\w+)\*?\*?',
            r'🟠\s*CHECKPOINT[:\s]+\*?\*?(\w+)\*?\*?',
            r'🟡\s*CHECKPOINT[:\s]+\*?\*?(\w+)\*?\*?',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            checkpoints.extend(matches)

        # Normalize: Ensure CP_ prefix
        normalized = []
        for cp in set(checkpoints):
            if not cp.upper().startswith('CP_'):
                cp = f"CP_{cp.upper()}"
            else:
                cp = cp.upper()
            normalized.append(cp)

        return list(set(normalized))

    def _detect_agents(self, response: str) -> List[str]:
        """
        Detect agent invocations in response.

        Note: Agent detection depends on CLI capabilities:
        - Claude Code: Full Diverga plugin support, agents are invoked via Task tool
        - Codex: No plugin system, agents cannot be invoked (only mentioned in text)
        - OpenCode: Limited plugin support
        """
        agents = []

        # Various agent reference patterns
        patterns = [
            # Diverga agent patterns
            r'diverga:([a-z]\d+)',  # diverga:a1, diverga:c5
            r'([A-Z]\d+)-[A-Za-z]+',  # A1-ResearchQuestionRefiner
            r'Agent[:\s]+([A-Z]\d+-[A-Za-z]+)',
            r'([A-Z]\d+)\s+에이전트',  # Korean pattern
            r'Task.*subagent_type.*diverga:(\w+)',
            # Direct agent ID patterns (with optional bold)
            r'\*?\*?([A-Z]\d+)\*?\*?\s*[-:]\s*[A-Za-z]+',
            # Agent mentions in bullet points
            r'[-•]\s*\*?\*?([A-Z]\d+)\*?\*?',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            agents.extend(matches)

        # Normalize agent IDs (uppercase, like A1, C5, D1)
        normalized = []
        for agent in set(agents):
            agent_upper = agent.upper()
            # Only accept valid agent patterns (letter + digit)
            if re.match(r'^[A-Z]\d+$', agent_upper):
                normalized.append(agent_upper)
            elif '-' in agent:
                # Extract ID from full name like A1-ResearchQuestionRefiner
                agent_id = agent.split('-')[0].upper()
                if re.match(r'^[A-Z]\d+$', agent_id):
                    normalized.append(agent_id)

        return list(set(normalized))

    def _extract_vs_options(self, response: str) -> List[Dict]:
        """Extract VS methodology options with T-Scores."""
        options = []

        # Pattern: [A] Option Label (T=0.50)
        pattern = r'\[([A-Z])\]\s*([^(]+?)\s*\(T\s*=\s*(\d+\.?\d*)\)'
        matches = re.findall(pattern, response)

        for match in matches:
            options.append({
                'option': match[0],
                'label': match[1].strip(),
                't_score': float(match[2])
            })

        return options

    def run(self) -> TestSession:
        """Execute the complete test scenario."""
        print(f"\n{'='*60}")
        print(f"Diverga QA Protocol v3.0 - True Automated Testing")
        print(f"Scenario: {self.scenario_id}")
        print(f"CLI Tool: {self.cli_tool}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print(f"{'='*60}\n")

        conversation_flow = self.protocol.get('conversation_flow', [])

        try:
            for turn_spec in conversation_flow:
                self._turn_count += 1
                turn_num = turn_spec.get('turn', self._turn_count)
                user_message = turn_spec.get('user', '').strip()
                user_type = turn_spec.get('user_type', 'UNKNOWN')
                expected = turn_spec.get('expected_behavior', {})

                if not user_message:
                    continue

                print(f"[Turn {turn_num}] {user_type}")
                if self.verbose:
                    print(f"  User: {user_message[:60]}...")

                # Record user turn
                user_turn = Turn(
                    number=turn_num,
                    role='user',
                    content=user_message,
                    timestamp=datetime.now().isoformat(),
                    metadata={'user_type': user_type}
                )
                self.session.turns.append(user_turn)

                # Execute CLI and get response
                print(f"  Sending to {self.cli_tool}...")
                response = self._execute_cli(user_message)
                print(f"  Received: {len(response)} chars")

                # Analyze response
                checkpoints = self._detect_checkpoints(response)
                agents = self._detect_agents(response)
                vs_options = self._extract_vs_options(response)

                # Record assistant turn
                assistant_turn = Turn(
                    number=turn_num,
                    role='assistant',
                    content=response,
                    timestamp=datetime.now().isoformat(),
                    checkpoints_detected=checkpoints,
                    agents_detected=agents,
                    vs_options=vs_options,
                    metadata={'expected': expected}
                )
                self.session.turns.append(assistant_turn)

                # Update session-level aggregates
                for cp in checkpoints:
                    self.session.checkpoints.append({
                        'checkpoint': cp,
                        'turn': turn_num,
                        'timestamp': datetime.now().isoformat()
                    })
                self.session.agents_invoked.extend(agents)

                print(f"  ✓ Completed (CP: {len(checkpoints)}, Agents: {len(agents)})")

            # Finalize session
            self.session.end_time = datetime.now().isoformat()
            self.session.agents_invoked = list(set(self.session.agents_invoked))
            self.session.status = "completed"
            self.session.validation_results = self._validate_session()

        except Exception as e:
            self.session.status = "failed"
            self.session.error = str(e)
            print(f"\n[ERROR] {e}")

        # Print summary
        print(f"\n{'='*60}")
        print(f"Test {'Completed' if self.session.status == 'completed' else 'Failed'}: {self.scenario_id}")
        print(f"Turns: {len([t for t in self.session.turns if t.role == 'user'])}")
        print(f"Checkpoints: {len(self.session.checkpoints)}")
        print(f"Agents: {len(self.session.agents_invoked)}")
        print(f"{'='*60}\n")

        return self.session

    def _validate_session(self) -> Dict[str, Any]:
        """Validate session against protocol expectations."""
        expected_checkpoints = [
            cp['id'] for cp in self.protocol.get('checkpoints_expected', [])
        ]
        found_checkpoints = [cp['checkpoint'] for cp in self.session.checkpoints]

        expected_agents = self.protocol.get('agents_involved', [])

        # Run verification huddle if enabled in protocol
        verification_huddle = self._run_verification_huddle()

        return {
            'checkpoints': {
                'expected': expected_checkpoints,
                'found': found_checkpoints,
                'missing': [cp for cp in expected_checkpoints if cp not in found_checkpoints],
                'compliance': len([cp for cp in expected_checkpoints if cp in found_checkpoints]) / max(len(expected_checkpoints), 1) * 100
            },
            'agents': {
                'expected': expected_agents,
                'found': self.session.agents_invoked,
                'match_rate': len(set(expected_agents) & set(self.session.agents_invoked)) / max(len(expected_agents), 1) * 100
            },
            'turns': {
                'expected_min': int(self.protocol.get('expected_turns', '1').split('-')[0]) if isinstance(self.protocol.get('expected_turns'), str) else self.protocol.get('expected_turns', 1),
                'actual': len([t for t in self.session.turns if t.role == 'user']),
            },
            'verification_huddle': verification_huddle
        }

    def _run_verification_huddle(self) -> Dict[str, Any]:
        """
        VERIFICATION HUDDLE: Confirm responses are from real AI, not simulation.

        Checks:
        1. NO_SIMULATION_MARKERS: No [DRY RUN], [SIMULATED] markers
        2. RESPONSE_LENGTH_VARIANCE: Response lengths vary naturally
        3. TIMESTAMP_VARIANCE: Response times vary naturally
        4. CONTEXT_AWARENESS: AI references specific user input
        5. UNIQUE_SESSION_ID: Valid UUID session ID
        6. DYNAMIC_CONTENT: Content shows reasoning, not templates
        """
        results = {
            'enabled': True,
            'passed': True,
            'checks': {},
            'summary': ''
        }

        assistant_turns = [t for t in self.session.turns if t.role == 'assistant']

        if not assistant_turns:
            results['passed'] = False
            results['summary'] = 'No assistant responses to verify'
            return results

        # Check 1: NO_SIMULATION_MARKERS
        simulation_markers = ['[DRY RUN]', '[SIMULATED]', 'DRY RUN MODE:',
                              'simulated response', 'This is a simulated']
        marker_found = False
        for turn in assistant_turns:
            for marker in simulation_markers:
                if marker.lower() in turn.content.lower():
                    marker_found = True
                    break

        results['checks']['NO_SIMULATION_MARKERS'] = {
            'passed': not marker_found,
            'detail': 'No simulation markers found' if not marker_found else 'SIMULATION MARKERS DETECTED!'
        }

        # Check 2: RESPONSE_LENGTH_VARIANCE
        lengths = [len(t.content) for t in assistant_turns]
        if len(lengths) >= 2:
            length_variance = max(lengths) - min(lengths)
            # Real AI should have at least 200 char variance across responses
            variance_ok = length_variance > 200
        else:
            variance_ok = True
            length_variance = 0

        results['checks']['RESPONSE_LENGTH_VARIANCE'] = {
            'passed': variance_ok,
            'detail': f'Length variance: {length_variance} chars (min: {min(lengths) if lengths else 0}, max: {max(lengths) if lengths else 0})'
        }

        # Check 3: TIMESTAMP_VARIANCE
        timestamps = []
        for turn in assistant_turns:
            try:
                ts = datetime.fromisoformat(turn.timestamp)
                timestamps.append(ts)
            except:
                pass

        if len(timestamps) >= 2:
            intervals = []
            for i in range(1, len(timestamps)):
                interval = (timestamps[i] - timestamps[i-1]).total_seconds()
                intervals.append(interval)

            # Check if intervals vary (not all identical)
            if len(set(intervals)) > 1 or len(intervals) == 1:
                timestamp_ok = True
            else:
                timestamp_ok = False
        else:
            timestamp_ok = True
            intervals = []

        results['checks']['TIMESTAMP_VARIANCE'] = {
            'passed': timestamp_ok,
            'detail': f'Response intervals: {[f"{i:.1f}s" for i in intervals]}' if intervals else 'Single response'
        }

        # Check 4: CONTEXT_AWARENESS
        user_turns = [t for t in self.session.turns if t.role == 'user']
        context_references = 0

        for user_turn in user_turns[:3]:  # Check first 3 user messages
            user_keywords = [w for w in user_turn.content.split() if len(w) > 4][:5]
            for assistant_turn in assistant_turns:
                for keyword in user_keywords:
                    if keyword.lower() in assistant_turn.content.lower():
                        context_references += 1
                        break

        context_ok = context_references >= min(len(user_turns), 2)

        results['checks']['CONTEXT_AWARENESS'] = {
            'passed': context_ok,
            'detail': f'{context_references} context references found'
        }

        # Check 5: UNIQUE_SESSION_ID
        try:
            uuid.UUID(self.session.session_id)
            uuid_ok = True
        except:
            uuid_ok = False

        results['checks']['UNIQUE_SESSION_ID'] = {
            'passed': uuid_ok,
            'detail': f'Session ID: {self.session.session_id[:8]}...'
        }

        # Check 6: DYNAMIC_CONTENT
        # Real AI responses should have varied sentence structures
        dynamic_ok = True
        for turn in assistant_turns:
            # Check for template-like repetitive patterns
            if turn.content.count('This is a simulated') > 0:
                dynamic_ok = False
            if turn.content.count('Paradigm Detection:') > 3:
                dynamic_ok = False

        results['checks']['DYNAMIC_CONTENT'] = {
            'passed': dynamic_ok,
            'detail': 'Content appears dynamic' if dynamic_ok else 'Template patterns detected'
        }

        # Calculate overall pass/fail
        all_passed = all(check['passed'] for check in results['checks'].values())
        results['passed'] = all_passed

        passed_count = sum(1 for check in results['checks'].values() if check['passed'])
        total_count = len(results['checks'])

        if all_passed:
            results['summary'] = f'✅ VERIFICATION PASSED ({passed_count}/{total_count} checks)'
        else:
            failed_checks = [name for name, check in results['checks'].items() if not check['passed']]
            results['summary'] = f'❌ VERIFICATION FAILED ({passed_count}/{total_count}): {", ".join(failed_checks)}'

        return results

    def save_results(self, output_dir: str) -> Path:
        """Save test results to session folder."""
        output_path = Path(output_dir) / self.session.scenario_id
        output_path.mkdir(parents=True, exist_ok=True)

        # 1. Save conversation transcript (Markdown)
        self._save_transcript(output_path)

        # 2. Save raw JSON
        self._save_raw_json(output_path)

        # 3. Save test result YAML
        self._save_result_yaml(output_path)

        # 4. Save README
        self._save_readme(output_path)

        print(f"Results saved to: {output_path}")
        return output_path

    def _save_transcript(self, output_path: Path):
        """Save human-readable conversation transcript."""
        transcript_file = output_path / 'conversation_transcript.md'

        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(f"# {self.session.scenario_id} Test Session Transcript\n\n")
            f.write(f"**CLI Tool**: {self.session.cli_tool}\n")
            f.write(f"**Session ID**: {self.session.session_id}\n")
            f.write(f"**Start Time**: {self.session.start_time}\n")
            f.write(f"**End Time**: {self.session.end_time or 'N/A'}\n")
            f.write(f"**Status**: {self.session.status}\n\n")
            f.write("---\n\n")

            for turn in self.session.turns:
                role_icon = "👤 USER" if turn.role == 'user' else "🤖 ASSISTANT"
                f.write(f"## Turn {turn.number}: {role_icon}\n\n")
                f.write(f"{turn.content}\n\n")

                if turn.checkpoints_detected:
                    f.write(f"**Checkpoints Detected**: {', '.join(turn.checkpoints_detected)}\n\n")
                if turn.agents_detected:
                    f.write(f"**Agents Detected**: {', '.join(turn.agents_detected)}\n\n")
                if turn.vs_options:
                    f.write("**VS Options**:\n")
                    for opt in turn.vs_options:
                        f.write(f"- [{opt['option']}] {opt['label']} (T={opt['t_score']})\n")
                    f.write("\n")

                f.write("---\n\n")

    def _save_raw_json(self, output_path: Path):
        """Save raw session data as JSON."""
        raw_file = output_path / 'conversation_raw.json'

        raw_data = {
            'scenario_id': self.session.scenario_id,
            'cli_tool': self.session.cli_tool,
            'session_id': self.session.session_id,
            'start_time': self.session.start_time,
            'end_time': self.session.end_time,
            'status': self.session.status,
            'error': self.session.error,
            'total_turns': len([t for t in self.session.turns if t.role == 'user']),
            'checkpoints': self.session.checkpoints,
            'agents_invoked': self.session.agents_invoked,
            'validation_results': self.session.validation_results,
            'turns': [asdict(t) for t in self.session.turns]
        }

        with open(raw_file, 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)

    def _save_result_yaml(self, output_path: Path):
        """Save test result summary as YAML."""
        result_file = output_path / f'{self.session.scenario_id}_test_result.yaml'

        validation = self.session.validation_results
        status = "PASSED" if validation.get('checkpoints', {}).get('compliance', 0) >= 80 else "FAILED"

        test_result = {
            'scenario_id': self.session.scenario_id,
            'name': self.protocol.get('name', ''),
            'test_date': datetime.now().strftime('%Y-%m-%d'),
            'test_mode': 'cli_automated' if not self.dry_run else 'dry_run',
            'cli_tool': self.session.cli_tool,
            'status': status if self.session.status == 'completed' else 'ERROR',
            'error': self.session.error,
            'metrics': {
                'total_turns': len([t for t in self.session.turns if t.role == 'user']),
                'checkpoints_found': len(self.session.checkpoints),
                'checkpoint_compliance': f"{validation.get('checkpoints', {}).get('compliance', 0):.1f}%",
                'agents_invoked': len(self.session.agents_invoked),
            },
            'validation': validation,
            'checkpoints': [
                {'id': cp['checkpoint'], 'turn': cp['turn'], 'status': 'TRIGGERED'}
                for cp in self.session.checkpoints
            ],
            'agents': [{'agent': a} for a in self.session.agents_invoked]
        }

        with open(result_file, 'w', encoding='utf-8') as f:
            yaml.dump(test_result, f, default_flow_style=False, allow_unicode=True)

    def _save_readme(self, output_path: Path):
        """Save README with session overview."""
        readme_file = output_path / 'README.md'

        validation = self.session.validation_results
        status_icon = "✅" if self.session.status == 'completed' else "❌"

        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(f"# {self.session.scenario_id} Test Session\n\n")
            f.write(f"**Scenario**: {self.protocol.get('name', '')}\n")
            f.write(f"**Test Date**: {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write(f"**CLI Tool**: {self.session.cli_tool}\n")
            f.write(f"**Status**: {status_icon} {self.session.status.upper()}\n\n")

            if self.session.error:
                f.write(f"**Error**: {self.session.error}\n\n")

            f.write("---\n\n")
            f.write("## Session Contents\n\n")
            f.write("| File | Description |\n")
            f.write("|------|-------------|\n")
            f.write("| `conversation_transcript.md` | Human-readable conversation with AI |\n")
            f.write("| `conversation_raw.json` | Raw JSON data including all metadata |\n")
            f.write(f"| `{self.session.scenario_id}_test_result.yaml` | Test evaluation and metrics |\n\n")

            f.write("## Metrics Summary\n\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            f.write(f"| Total Turns | {len([t for t in self.session.turns if t.role == 'user'])} |\n")
            f.write(f"| Checkpoints Found | {len(self.session.checkpoints)} |\n")
            f.write(f"| Checkpoint Compliance | {validation.get('checkpoints', {}).get('compliance', 0):.1f}% |\n")
            f.write(f"| Agents Invoked | {len(self.session.agents_invoked)} |\n\n")

            f.write("## Checkpoints\n\n")
            if self.session.checkpoints:
                f.write("| Checkpoint | Turn | Status |\n")
                f.write("|------------|------|--------|\n")
                for cp in self.session.checkpoints:
                    f.write(f"| {cp['checkpoint']} | {cp['turn']} | ✅ Triggered |\n")
            else:
                f.write("No checkpoints detected in this session.\n")

            f.write("\n## Agents Invoked\n\n")
            if self.session.agents_invoked:
                for agent in self.session.agents_invoked:
                    f.write(f"- {agent}\n")
            else:
                f.write("No agents detected in this session.\n")

            # Add Verification Huddle section
            verification = validation.get('verification_huddle', {})
            if verification.get('enabled'):
                f.write("\n## 🔍 VERIFICATION HUDDLE\n\n")
                f.write(f"**Result**: {verification.get('summary', 'N/A')}\n\n")

                if verification.get('checks'):
                    f.write("| Check | Status | Detail |\n")
                    f.write("|-------|--------|--------|\n")
                    for check_name, check_result in verification['checks'].items():
                        status = "✅ PASS" if check_result['passed'] else "❌ FAIL"
                        detail = check_result.get('detail', '')[:50]
                        f.write(f"| {check_name} | {status} | {detail} |\n")

                f.write("\n### Verification Huddle Purpose\n\n")
                f.write("This huddle confirms the test used **real AI API calls**, not simulation:\n\n")
                f.write("- **NO_SIMULATION_MARKERS**: No `[DRY RUN]` or template markers\n")
                f.write("- **RESPONSE_LENGTH_VARIANCE**: Natural response length variation\n")
                f.write("- **TIMESTAMP_VARIANCE**: Natural response timing\n")
                f.write("- **CONTEXT_AWARENESS**: AI references user-specific input\n")
                f.write("- **UNIQUE_SESSION_ID**: Valid unique session identifier\n")
                f.write("- **DYNAMIC_CONTENT**: Non-templated, reasoning-based content\n")


def main():
    parser = argparse.ArgumentParser(
        description='Diverga QA v3.0 - True Automated Testing via CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with Claude Code (default)
  python cli_test_runner.py --scenario QUAL-002

  # Run with specific CLI tool
  python cli_test_runner.py --scenario META-002 --cli claude

  # Dry run (no API calls)
  python cli_test_runner.py --scenario QUAL-002 --dry-run

  # Verbose output
  python cli_test_runner.py --scenario QUAL-002 -v

  # Custom output directory
  python cli_test_runner.py --scenario QUAL-002 --output ./my-reports
        """
    )

    parser.add_argument(
        '--scenario', '-s',
        required=True,
        help='Scenario ID (e.g., QUAL-002, META-002)'
    )
    parser.add_argument(
        '--cli', '-c',
        default='claude',
        choices=['claude', 'opencode', 'codex'],
        help='CLI tool to use (default: claude)'
    )
    parser.add_argument(
        '--output', '-o',
        default='qa/reports/sessions',
        help='Output directory (default: qa/reports/sessions)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Dry run mode (no actual API calls)'
    )
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=300,
        help='Timeout per turn in seconds (default: 300)'
    )

    args = parser.parse_args()

    try:
        runner = CLITestRunner(
            scenario_id=args.scenario,
            cli_tool=args.cli,
            verbose=args.verbose,
            dry_run=args.dry_run,
            timeout=args.timeout
        )

        session = runner.run()
        result_path = runner.save_results(args.output)

        # Exit code based on status
        if session.status == 'completed':
            compliance = session.validation_results.get('checkpoints', {}).get('compliance', 0)
            if compliance >= 80:
                print(f"\n✅ Test PASSED: {result_path}")
                sys.exit(0)
            else:
                print(f"\n⚠️ Test completed but low compliance ({compliance:.1f}%): {result_path}")
                sys.exit(1)
        else:
            print(f"\n❌ Test FAILED: {session.error}")
            sys.exit(2)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(3)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(4)


if __name__ == '__main__':
    main()
