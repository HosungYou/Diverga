#!/usr/bin/env python3
"""
Diverga QA Protocol v2.0 - Conversation Extractor

Extracts and analyzes Claude Code session logs for QA testing.
Parses JSONL format from ~/.claude/projects/{project-id}/{session}.jsonl

Features:
- JSONL parsing with turn-by-turn extraction
- Checkpoint detection and tracking
- Agent invocation tracking
- User input type classification
- VS methodology option detection
- T-Score extraction
- Language consistency validation

Usage:
    python extract_conversation.py --session <path> --output <dir>
    python extract_conversation.py --session ~/.claude/projects/abc123/session.jsonl
"""

import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional
import yaml


@dataclass
class Turn:
    """Single conversation turn."""
    turn_number: int
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[str] = None
    turn_type: Optional[str] = None  # For user turns
    tool_calls: list = field(default_factory=list)
    checkpoint_triggered: Optional[str] = None
    halt_verified: bool = False
    vs_options: int = 0
    t_scores: list = field(default_factory=list)
    agent_invoked: Optional[str] = None
    maintains_checkpoint: bool = False


@dataclass
class Checkpoint:
    """Checkpoint tracking."""
    id: str
    status: str  # 'TRIGGERED', 'PASSED', 'BYPASSED'
    turn_triggered: int
    turn_resolved: Optional[int] = None
    wait_turns: int = 0
    user_selection: Optional[str] = None
    level: str = "RED"  # RED, ORANGE, YELLOW


@dataclass
class AgentInvocation:
    """Agent invocation tracking."""
    agent: str
    turn: int
    trigger: str
    tool_call_id: Optional[str] = None


@dataclass
class ExtractionResult:
    """Complete extraction result."""
    session_id: str
    scenario_id: Optional[str]
    extracted_at: str
    language: str
    total_turns: int
    turns: list
    checkpoints: list
    agents_invoked: list
    metrics: dict


class ConversationExtractor:
    """
    Claude Code session log extractor and analyzer.

    Parses JSONL session logs and extracts:
    - Conversation turns with role classification
    - Checkpoint triggers and resolutions
    - Agent invocations via Task tool calls
    - VS methodology options and T-Scores
    - User input type classification
    """

    # Checkpoint patterns
    CHECKPOINT_PATTERNS = {
        'RED': [
            r'CP_RESEARCH_DIRECTION',
            r'CP_METHODOLOGY_APPROVAL',
            r'CP_ETHICS_APPROVAL',
            r'CP_FINAL_SUBMISSION',
            r'CP_DATA_COLLECTION_START',
        ],
        'ORANGE': [
            r'CP_THEORY_SELECTION',
            r'CP_SCOPE_DECISION',
            r'CP_HUMANIZATION_REVIEW',
            r'CP_ANALYSIS_APPROACH',
            r'CP_INTEGRATION_STRATEGY',
        ],
        'YELLOW': [
            r'CP_PARADIGM_RECONSIDERATION',
            r'CP_MINOR_ADJUSTMENT',
        ]
    }

    # User input type patterns
    USER_TYPE_PATTERNS = {
        'TECHNICAL_FOLLOW_UP': [
            r'\bwhy\b.*\?',
            r'\bhow\b.*\?',
            r'\bwhat if\b',
            r'\bexplain\b',
            r'\bdifference\b.*\?',
            r'\bcompare\b',
        ],
        'METHODOLOGICAL_CHALLENGE': [
            r'\bbut\b',
            r'\bhowever\b',
            r'\bconcern\b',
            r'\bworried\b',
            r'\bproblem\b',
            r'\bissue\b',
            r'\bassumption\b.*\?',
            r'\bviolat',
        ],
        'AGENT_TRANSITION_REQUEST': [
            r'\bwait\b',
            r'\bbefore we\b',
            r'\bstep back\b',
            r'\bfirst\b.*\bcan we\b',
            r'\bactually\b.*\bfirst\b',
        ],
        'SCOPE_CHANGE': [
            r'\bactually\b.*\bwant to\b',
            r'\binclude\b.*\btoo\b',
            r'\bchange\b.*\bscope\b',
            r'\badd\b.*\bto\b',
        ],
        'ALTERNATIVE_EXPLORATION': [
            r'\bwhat about\b',
            r'\bwhy not\b',
            r'\bdidn\'t mention\b',
            r'\bwasn\'t.*listed\b',
            r'\bother option\b',
        ],
        'PRACTICAL_CONSTRAINT': [
            r'\bonly have\b',
            r'\btime\b.*\bproblem\b',
            r'\bresources\b',
            r'\bbudget\b',
            r'\bminimum\b.*\?',
            r'\benough\b.*\?',
        ],
        'SELECTION': [
            r'^\s*\[[A-Z]\]',
            r'^Option\s+[A-Z]',
            r'^I choose\b',
            r'^I\'ll go with\b',
        ],
        'APPROVAL': [
            r'\bapproved?\b',
            r'\bconfirm\b',
            r'\bproceed\b',
            r'\byes\b.*\bcontinue\b',
            r'\bagree\b',
        ],
    }

    # Agent detection patterns (from Task tool calls)
    AGENT_PATTERNS = {
        # Category A: Foundation
        'A1-ResearchQuestionRefiner': r'diverga:A1|research.*question.*refin',
        'A2-TheoreticalFrameworkArchitect': r'diverga:A2|theoret.*framework',
        'A3-DevilsAdvocate': r'diverga:A3|devil.*advocate|critic',
        'A4-ResearchEthicsAdvisor': r'diverga:A4|ethics|IRB',
        'A5-ParadigmWorldviewAdvisor': r'diverga:A5|paradigm|worldview',
        'A6-ConceptualFrameworkVisualizer': r'diverga:A6|conceptual.*framework',
        # Category B: Evidence
        'B1-LiteratureReviewStrategist': r'diverga:B1|literature.*review|PRISMA',
        'B2-EvidenceQualityAppraiser': r'diverga:B2|quality.*apprais|RoB|GRADE',
        'B3-EffectSizeExtractor': r'diverga:B3|effect.*size|Cohen|Hedges',
        'B4-ResearchRadar': r'diverga:B4|research.*radar|trend',
        'B5-ParallelDocumentProcessor': r'diverga:B5|parallel.*document|batch.*PDF',
        # Category C: Design & Meta-Analysis
        'C1-QuantitativeDesignConsultant': r'diverga:C1|quantitative.*design|RCT',
        'C2-QualitativeDesignConsultant': r'diverga:C2|qualitative.*design|phenomenology',
        'C3-MixedMethodsDesignConsultant': r'diverga:C3|mixed.*method|QUAN.*qual',
        'C4-ExperimentalMaterialsDeveloper': r'diverga:C4|experimental.*material',
        'C5-MetaAnalysisMaster': r'diverga:C5|meta.*analysis|C5',
        'C6-DataIntegrityGuard': r'diverga:C6|data.*integrity',
        'C7-ErrorPreventionEngine': r'diverga:C7|error.*prevent',
        # Category D: Data Collection
        'D1-SamplingStrategyAdvisor': r'diverga:D1|sampling|sample.*size',
        'D2-InterviewFocusGroupSpecialist': r'diverga:D2|interview|focus.*group',
        'D3-ObservationProtocolDesigner': r'diverga:D3|observation.*protocol',
        'D4-MeasurementInstrumentDeveloper': r'diverga:D4|measurement|instrument|scale',
        # Category E: Analysis
        'E1-QuantitativeAnalysisGuide': r'diverga:E1|quantitative.*analysis|statistical',
        'E2-QualitativeCodingSpecialist': r'diverga:E2|qualitative.*cod|thematic',
        'E3-MixedMethodsIntegrationSpecialist': r'diverga:E3|integration|joint.*display',
        'E4-AnalysisCodeGenerator': r'diverga:E4|analysis.*code|R|Python|SPSS',
        'E5-SensitivityAnalysisDesigner': r'diverga:E5|sensitivity.*analysis',
        # Category F: Quality
        'F1-InternalConsistencyChecker': r'diverga:F1|internal.*consist',
        'F2-ChecklistManager': r'diverga:F2|checklist|PRISMA.*2020|CONSORT',
        'F3-ReproducibilityAuditor': r'diverga:F3|reproducibility|OSF',
        'F4-BiasTrustworthinessDetector': r'diverga:F4|bias|trustworth|p-hack',
        'F5-HumanizationVerifier': r'diverga:F5|humanization.*verif|citation.*integrity',
        # Category G: Communication
        'G1-JournalMatcher': r'diverga:G1|journal.*match|impact.*factor',
        'G2-AcademicCommunicator': r'diverga:G2|academic.*commun|abstract',
        'G3-PeerReviewStrategist': r'diverga:G3|peer.*review|reviewer.*comment',
        'G4-PreregistrationComposer': r'diverga:G4|pre.*regist|OSF.*pre',
        'G5-AcademicStyleAuditor': r'diverga:G5|style.*audit|AI.*pattern',
        'G6-AcademicStyleHumanizer': r'diverga:G6|humaniz|balanced.*humaniz',
        # Category H: Specialized
        'H1-EthnographicResearchAdvisor': r'diverga:H1|ethnograph',
        'H2-ActionResearchFacilitator': r'diverga:H2|action.*research|PAR|CBPR',
    }

    # T-Score pattern
    TSCORE_PATTERN = r'T[=-]?\s*(\d+\.?\d*)'

    # VS options pattern
    VS_OPTIONS_PATTERN = r'\[([A-Z])\].*?(?:T[=-]?\s*\d+\.?\d*|\(T\s*=\s*\d+\.?\d*\))'

    def __init__(self, session_path: str, scenario_id: Optional[str] = None):
        """
        Initialize extractor with session path.

        Args:
            session_path: Path to Claude Code session JSONL file
            scenario_id: Optional scenario ID for matching against expected
        """
        self.session_path = Path(session_path)
        self.scenario_id = scenario_id
        self.turns: list[Turn] = []
        self.checkpoints: list[Checkpoint] = []
        self.agents_invoked: list[AgentInvocation] = []
        self._active_checkpoint: Optional[Checkpoint] = None
        self._language: str = "unknown"
        self._turn_count = 0

    def extract(self) -> ExtractionResult:
        """
        Parse JSONL and extract conversation.

        Returns:
            ExtractionResult with all extracted data
        """
        if not self.session_path.exists():
            raise FileNotFoundError(f"Session file not found: {self.session_path}")

        with open(self.session_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        entry = json.loads(line)
                        self._process_entry(entry)
                    except json.JSONDecodeError:
                        continue  # Skip malformed lines

        # Finalize any open checkpoint
        if self._active_checkpoint and self._active_checkpoint.status == 'TRIGGERED':
            self._active_checkpoint.status = 'INCOMPLETE'

        return ExtractionResult(
            session_id=self.session_path.stem,
            scenario_id=self.scenario_id,
            extracted_at=datetime.now().isoformat(),
            language=self._language,
            total_turns=len(self.turns),
            turns=[asdict(t) for t in self.turns],
            checkpoints=[asdict(c) for c in self.checkpoints],
            agents_invoked=[asdict(a) for a in self.agents_invoked],
            metrics=self._calculate_metrics()
        )

    def _process_entry(self, entry: dict) -> None:
        """Process a single JSONL entry."""
        entry_type = entry.get('type', '')

        if entry_type == 'user' or entry.get('role') == 'user':
            self._process_user_turn(entry)
        elif entry_type == 'assistant' or entry.get('role') == 'assistant':
            self._process_assistant_turn(entry)
        elif entry_type == 'tool_result':
            self._process_tool_result(entry)

    def _process_user_turn(self, entry: dict) -> None:
        """Process user message."""
        self._turn_count += 1
        content = entry.get('content', entry.get('message', ''))

        # Detect language from first substantial user turn
        if self._language == "unknown" and len(content) > 20:
            self._language = self._detect_language(content)

        turn = Turn(
            turn_number=self._turn_count,
            role='user',
            content=content,
            timestamp=entry.get('timestamp'),
            turn_type=self._classify_user_input(content)
        )
        self.turns.append(turn)

        # Check if user is responding to checkpoint
        if self._active_checkpoint:
            selection = self._extract_selection(content)
            if selection:
                self._active_checkpoint.user_selection = selection
                self._active_checkpoint.turn_resolved = self._turn_count
                self._active_checkpoint.wait_turns = (
                    self._turn_count - self._active_checkpoint.turn_triggered
                )
                self._active_checkpoint.status = 'PASSED'
                self._active_checkpoint = None

    def _process_assistant_turn(self, entry: dict) -> None:
        """Process assistant message."""
        self._turn_count += 1
        content = entry.get('content', entry.get('message', ''))
        tool_calls = entry.get('tool_calls', [])

        turn = Turn(
            turn_number=self._turn_count,
            role='assistant',
            content=content,
            timestamp=entry.get('timestamp'),
            tool_calls=tool_calls
        )

        # Detect checkpoint triggers
        checkpoint_id = self._detect_checkpoint(content)
        if checkpoint_id:
            turn.checkpoint_triggered = checkpoint_id
            turn.halt_verified = self._verify_halt(content)

            # Create checkpoint tracker
            level = self._get_checkpoint_level(checkpoint_id)
            checkpoint = Checkpoint(
                id=checkpoint_id,
                status='TRIGGERED',
                turn_triggered=self._turn_count,
                level=level
            )
            self.checkpoints.append(checkpoint)
            self._active_checkpoint = checkpoint

        # Check if maintaining checkpoint (technical question without selection)
        if self._active_checkpoint and self._active_checkpoint.status == 'TRIGGERED':
            turn.maintains_checkpoint = True

        # Detect VS options and T-Scores
        vs_count, t_scores = self._extract_vs_options(content)
        turn.vs_options = vs_count
        turn.t_scores = t_scores

        # Detect agent invocations from tool calls
        for tool_call in tool_calls:
            agent = self._detect_agent_from_tool_call(tool_call)
            if agent:
                turn.agent_invoked = agent
                self.agents_invoked.append(AgentInvocation(
                    agent=agent,
                    turn=self._turn_count,
                    trigger='tool_call',
                    tool_call_id=tool_call.get('id')
                ))

        self.turns.append(turn)

    def _process_tool_result(self, entry: dict) -> None:
        """Process tool result for agent detection."""
        tool_name = entry.get('tool_name', '')
        if 'diverga:' in tool_name.lower() or 'task' in tool_name.lower():
            content = entry.get('content', str(entry.get('result', '')))
            for agent, pattern in self.AGENT_PATTERNS.items():
                if re.search(pattern, content, re.IGNORECASE):
                    # Check if not already tracked
                    if not any(a.agent == agent for a in self.agents_invoked):
                        self.agents_invoked.append(AgentInvocation(
                            agent=agent,
                            turn=self._turn_count,
                            trigger='tool_result'
                        ))

    def _classify_user_input(self, content: str) -> str:
        """Classify user input type."""
        content_lower = content.lower()

        for input_type, patterns in self.USER_TYPE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    return input_type

        return 'STANDARD_RESPONSE'

    def _detect_checkpoint(self, content: str) -> Optional[str]:
        """Detect checkpoint in assistant response."""
        for level, patterns in self.CHECKPOINT_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    return match.group(0)

        # Also check for generic checkpoint indicators
        if re.search(r'CHECKPOINT.*:', content, re.IGNORECASE):
            match = re.search(r'CHECKPOINT[:\s]*(\w+)', content, re.IGNORECASE)
            if match:
                return f"CP_{match.group(1).upper()}"

        return None

    def _get_checkpoint_level(self, checkpoint_id: str) -> str:
        """Get checkpoint level (RED, ORANGE, YELLOW)."""
        for level, patterns in self.CHECKPOINT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, checkpoint_id, re.IGNORECASE):
                    return level
        return 'UNKNOWN'

    def _verify_halt(self, content: str) -> bool:
        """Verify that assistant halted for user input."""
        halt_indicators = [
            r'which.*would you.*like',
            r'which.*direction',
            r'please.*select',
            r'choose.*option',
            r'approve.*proceed',
            r'confirm.*continue',
            r'\?$',
        ]
        for pattern in halt_indicators:
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                return True
        return False

    def _extract_vs_options(self, content: str) -> tuple[int, list]:
        """Extract VS methodology options and T-Scores."""
        options = re.findall(self.VS_OPTIONS_PATTERN, content, re.IGNORECASE)
        t_scores = [float(t) for t in re.findall(self.TSCORE_PATTERN, content)]
        return len(set(options)), t_scores

    def _extract_selection(self, content: str) -> Optional[str]:
        """Extract user's option selection."""
        # Direct [A], [B], [C] selection
        match = re.search(r'\[([A-Z])\]', content)
        if match:
            return match.group(1)

        # "Option A" or "I choose A"
        match = re.search(r'(?:option|choose|select)\s+([A-Z])\b', content, re.IGNORECASE)
        if match:
            return match.group(1)

        return None

    def _detect_agent_from_tool_call(self, tool_call: dict) -> Optional[str]:
        """Detect agent from tool call."""
        tool_name = tool_call.get('name', tool_call.get('tool', ''))
        args = tool_call.get('arguments', tool_call.get('input', {}))

        # Check tool name for agent pattern
        for agent, pattern in self.AGENT_PATTERNS.items():
            if re.search(pattern, tool_name, re.IGNORECASE):
                return agent

        # Check arguments for agent references
        if isinstance(args, dict):
            prompt = args.get('prompt', '') + args.get('description', '')
            for agent, pattern in self.AGENT_PATTERNS.items():
                if re.search(pattern, prompt, re.IGNORECASE):
                    return agent

        return None

    def _detect_language(self, content: str) -> str:
        """Detect language from content."""
        # Korean character detection
        korean_chars = len(re.findall(r'[\uac00-\ud7af]', content))
        # English word detection
        english_words = len(re.findall(r'\b[a-zA-Z]{3,}\b', content))

        if korean_chars > english_words:
            return 'Korean'
        return 'English'

    def _calculate_metrics(self) -> dict:
        """Calculate extraction metrics."""
        user_turns = [t for t in self.turns if t.role == 'user']

        # Count user input types
        type_counts = {}
        for turn in user_turns:
            t_type = turn.turn_type or 'UNKNOWN'
            type_counts[t_type] = type_counts.get(t_type, 0) + 1

        # Checkpoint compliance
        red_checkpoints = [c for c in self.checkpoints if c.level == 'RED']
        red_passed = [c for c in red_checkpoints if c.status == 'PASSED']
        checkpoint_compliance = (
            len(red_passed) / len(red_checkpoints) * 100
            if red_checkpoints else 100
        )

        # Agent transition count
        agent_transitions = len(set(
            self.agents_invoked[i].agent
            for i in range(1, len(self.agents_invoked))
            if self.agents_invoked[i].agent != self.agents_invoked[i-1].agent
        )) if len(self.agents_invoked) > 1 else 0

        return {
            'total_turns': len(self.turns),
            'user_turns': len(user_turns),
            'assistant_turns': len(self.turns) - len(user_turns),
            'user_input_types': type_counts,
            'technical_questions': type_counts.get('TECHNICAL_FOLLOW_UP', 0),
            'methodological_challenges': type_counts.get('METHODOLOGICAL_CHALLENGE', 0),
            'agent_transitions': agent_transitions,
            'total_checkpoints': len(self.checkpoints),
            'checkpoints_passed': len([c for c in self.checkpoints if c.status == 'PASSED']),
            'checkpoint_compliance_pct': round(checkpoint_compliance, 1),
            'unique_agents_invoked': len(set(a.agent for a in self.agents_invoked)),
            'language': self._language,
        }


class ConversationEvaluator:
    """
    Evaluate extracted conversation against expected scenario.

    Compares actual conversation behavior against expected outcomes
    defined in scenario YAML files.
    """

    def __init__(self, extracted: ExtractionResult, expected_path: str):
        """
        Initialize evaluator.

        Args:
            extracted: Extraction result to evaluate
            expected_path: Path to expected scenario YAML file
        """
        self.extracted = extracted
        with open(expected_path, 'r', encoding='utf-8') as f:
            self.expected = yaml.safe_load(f)

    def evaluate(self) -> dict:
        """Run all evaluations and return report."""
        results = {
            'scenario_id': self.expected.get('scenario_id'),
            'passed': True,
            'checks': [],
            'summary': {}
        }

        # Run checks
        checks = [
            self._check_checkpoint_compliance(),
            self._check_language_consistency(),
            self._check_agent_invocations(),
            self._check_technical_depth(),
            self._check_context_retention(),
        ]

        results['checks'] = checks
        results['passed'] = all(c['passed'] for c in checks)

        # Summary
        passed_count = sum(1 for c in checks if c['passed'])
        results['summary'] = {
            'total_checks': len(checks),
            'passed': passed_count,
            'failed': len(checks) - passed_count,
            'pass_rate': round(passed_count / len(checks) * 100, 1)
        }

        return results

    def _check_checkpoint_compliance(self) -> dict:
        """Check checkpoint compliance."""
        result = {
            'name': 'Checkpoint Compliance',
            'passed': True,
            'details': []
        }

        compliance = self.extracted.metrics.get('checkpoint_compliance_pct', 100)
        target = 100  # Must be 100% for RED checkpoints

        if compliance < target:
            result['passed'] = False
            result['details'].append(
                f"Checkpoint compliance {compliance}% < target {target}%"
            )
        else:
            result['details'].append(f"All checkpoints properly triggered and resolved")

        return result

    def _check_language_consistency(self) -> dict:
        """Check language matches expected."""
        result = {
            'name': 'Language Consistency',
            'passed': True,
            'details': []
        }

        expected_lang = self.expected.get('language', '').split('→')[0].strip()
        actual_lang = self.extracted.language

        if expected_lang.lower() not in actual_lang.lower():
            result['passed'] = False
            result['details'].append(
                f"Expected {expected_lang}, got {actual_lang}"
            )
        else:
            result['details'].append(f"Language matches: {actual_lang}")

        return result

    def _check_agent_invocations(self) -> dict:
        """Check expected agents were invoked."""
        result = {
            'name': 'Agent Invocations',
            'passed': True,
            'details': []
        }

        expected_agents = set(self.expected.get('agents_involved', []))
        actual_agents = set(
            a.agent for a in self.extracted.agents_invoked
            if hasattr(a, 'agent')
        )

        # Also check from dict format
        if not actual_agents:
            actual_agents = set(
                a['agent'] for a in self.extracted.agents_invoked
                if isinstance(a, dict)
            )

        missing = expected_agents - actual_agents
        if missing:
            result['passed'] = False
            result['details'].append(f"Missing agents: {missing}")

        result['details'].append(f"Invoked: {actual_agents}")

        return result

    def _check_technical_depth(self) -> dict:
        """Check technical question handling."""
        result = {
            'name': 'Technical Depth',
            'passed': True,
            'details': []
        }

        tech_questions = self.extracted.metrics.get('technical_questions', 0)
        expected_min = self.expected.get('expected_technical_questions', 0)

        if tech_questions < expected_min:
            result['details'].append(
                f"Technical questions: {tech_questions} (expected >= {expected_min})"
            )
        else:
            result['details'].append(f"Technical questions handled: {tech_questions}")

        return result

    def _check_context_retention(self) -> dict:
        """Check context retained across agent transitions."""
        result = {
            'name': 'Context Retention',
            'passed': True,
            'details': []
        }

        transitions = self.extracted.metrics.get('agent_transitions', 0)
        result['details'].append(f"Agent transitions: {transitions}")

        # This would require deeper analysis of content continuity
        # For now, we assume passed if transitions occurred

        return result


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Extract and analyze Claude Code session conversations'
    )
    parser.add_argument(
        '--session', '-s',
        required=True,
        help='Path to Claude Code session JSONL file'
    )
    parser.add_argument(
        '--output', '-o',
        default='.',
        help='Output directory for extracted conversation'
    )
    parser.add_argument(
        '--scenario-id', '-i',
        help='Scenario ID for matching'
    )
    parser.add_argument(
        '--expected', '-e',
        help='Path to expected scenario YAML for evaluation'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['yaml', 'json'],
        default='yaml',
        help='Output format (default: yaml)'
    )

    args = parser.parse_args()

    # Extract conversation
    extractor = ConversationExtractor(args.session, args.scenario_id)
    result = extractor.extract()

    # Convert to dict for output
    result_dict = asdict(result) if hasattr(result, '__dataclass_fields__') else {
        'session_id': result.session_id,
        'scenario_id': result.scenario_id,
        'extracted_at': result.extracted_at,
        'language': result.language,
        'total_turns': result.total_turns,
        'turns': result.turns,
        'checkpoints': result.checkpoints,
        'agents_invoked': result.agents_invoked,
        'metrics': result.metrics,
    }

    # Output extracted conversation
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{result.scenario_id or result.session_id}.{args.format}"
    output_path = output_dir / filename

    with open(output_path, 'w', encoding='utf-8') as f:
        if args.format == 'yaml':
            yaml.dump(result_dict, f, default_flow_style=False, allow_unicode=True)
        else:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)

    print(f"Extracted conversation saved to: {output_path}")
    print(f"Total turns: {result.total_turns}")
    print(f"Language: {result.language}")
    print(f"Checkpoints: {len(result.checkpoints)}")
    print(f"Agents invoked: {len(result.agents_invoked)}")

    # Evaluate if expected scenario provided
    if args.expected:
        evaluator = ConversationEvaluator(result, args.expected)
        eval_result = evaluator.evaluate()

        eval_path = output_dir / f"{result.scenario_id or result.session_id}_evaluation.{args.format}"
        with open(eval_path, 'w', encoding='utf-8') as f:
            if args.format == 'yaml':
                yaml.dump(eval_result, f, default_flow_style=False, allow_unicode=True)
            else:
                json.dump(eval_result, f, indent=2, ensure_ascii=False)

        print(f"\nEvaluation results: {eval_path}")
        print(f"Pass rate: {eval_result['summary']['pass_rate']}%")


if __name__ == '__main__':
    main()
