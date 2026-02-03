#!/usr/bin/env python3
"""
Diverga QA Protocol v3.2.2 - True Automated Testing via CLI

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
from typing import Any, Dict, List, Optional, Tuple


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
    CLI-based automated test runner for Diverga QA Protocol v3.2.2.

    Executes actual CLI commands to get real AI responses, unlike the
    v2.x simulator which uses hardcoded response templates.
    """

    SUPPORTED_CLIS = ['claude', 'opencode', 'codex']
    PROTOCOL_DIR = Path(__file__).parent.parent / "protocol"
    DEFAULT_TIMEOUT = 300  # 5 minutes per turn

    # Checkpoint alias mapping: descriptive names → formal CP_ identifiers
    # This enables hybrid detection that works with both formal and natural language checkpoints
    CHECKPOINT_ALIASES = {
        # Research Direction & Paradigm
        'Research Direction': 'CP_RESEARCH_DIRECTION',
        'Paradigm Selection': 'CP_PARADIGM_SELECTION',
        'Paradigm Confirmation': 'CP_PARADIGM_CONFIRMATION',
        'Research Question': 'CP_RESEARCH_DIRECTION',
        '연구 방향': 'CP_RESEARCH_DIRECTION',
        '패러다임 선택': 'CP_PARADIGM_SELECTION',
        '패러다임 확인': 'CP_PARADIGM_CONFIRMATION',

        # Theory & Framework
        'Theory Selection': 'CP_THEORY_SELECTION',
        'Theoretical Framework': 'CP_THEORY_SELECTION',
        '이론 선택': 'CP_THEORY_SELECTION',
        '이론적 프레임워크': 'CP_THEORY_SELECTION',

        # Methodology
        'Methodology Approval': 'CP_METHODOLOGY_APPROVAL',
        'Method Approval': 'CP_METHODOLOGY_APPROVAL',
        '방법론 승인': 'CP_METHODOLOGY_APPROVAL',

        # Meta-Analysis Specific
        'Effect Size Selection': 'CP_EFFECT_SIZE_SELECTION',
        'Effect Size Target Selection': 'CP_EFFECT_SIZE_SELECTION',
        'Effect Size': 'CP_EFFECT_SIZE_SELECTION',
        '효과크기 선택': 'CP_EFFECT_SIZE_SELECTION',

        'Heterogeneity Analysis': 'CP_HETEROGENEITY_ANALYSIS',
        'Heterogeneity Strategy': 'CP_HETEROGENEITY_ANALYSIS',
        '이질성 분석': 'CP_HETEROGENEITY_ANALYSIS',

        'Moderator Analysis': 'CP_MODERATOR_ANALYSIS',
        'Moderator Analysis Strategy': 'CP_MODERATOR_ANALYSIS',
        'Moderator Strategy': 'CP_MODERATOR_ANALYSIS',
        '조절변수 분석': 'CP_MODERATOR_ANALYSIS',

        'Multiple Testing': 'CP_MULTIPLE_TESTING',
        'Multiple Testing Strategy': 'CP_MULTIPLE_TESTING',
        '다중검정': 'CP_MULTIPLE_TESTING',

        'Single-Group Study Decision': 'CP_SINGLE_GROUP_DECISION',
        'Single Group Decision': 'CP_SINGLE_GROUP_DECISION',
        '단일그룹 연구 결정': 'CP_SINGLE_GROUP_DECISION',

        'F-Statistic Details': 'CP_FSTAT_DETAILS',
        'F-Statistic': 'CP_FSTAT_DETAILS',
        'F통계량': 'CP_FSTAT_DETAILS',

        # Analysis
        'Analysis Plan': 'CP_ANALYSIS_PLAN',
        '분석 계획': 'CP_ANALYSIS_PLAN',

        # Quality & Integration
        'Quality Review': 'CP_QUALITY_REVIEW',
        '품질 검토': 'CP_QUALITY_REVIEW',

        'Integration Strategy': 'CP_INTEGRATION_STRATEGY',
        '통합 전략': 'CP_INTEGRATION_STRATEGY',

        # Humanization
        'Humanization Review': 'CP_HUMANIZATION_REVIEW',
        'Humanization Verify': 'CP_HUMANIZATION_VERIFY',
        '휴먼화 검토': 'CP_HUMANIZATION_REVIEW',

        # Sampling & Data Collection
        'Sampling Strategy': 'CP_SAMPLING_STRATEGY',
        '표집 전략': 'CP_SAMPLING_STRATEGY',

        'Protocol Design': 'CP_PROTOCOL_DESIGN',
        '프로토콜 설계': 'CP_PROTOCOL_DESIGN',

        # Qualitative
        'Coding Approach': 'CP_CODING_APPROACH',
        '코딩 접근': 'CP_CODING_APPROACH',

        'Theme Validation': 'CP_THEME_VALIDATION',
        '주제 검증': 'CP_THEME_VALIDATION',

        'Trustworthiness': 'CP_TRUSTWORTHINESS',
        '신뢰성': 'CP_TRUSTWORTHINESS',

        'Member Check': 'CP_MEMBER_CHECK',
        '멤버 체크': 'CP_MEMBER_CHECK',

        # Writing & Review
        'Writing Style': 'CP_WRITING_STYLE',
        '작성 스타일': 'CP_WRITING_STYLE',

        'Final Review': 'CP_FINAL_REVIEW',
        '최종 검토': 'CP_FINAL_REVIEW',

        # Additional mappings for AI-generated variants
        'Analysis Plan Approval': 'CP_METHODOLOGY_APPROVAL',
        'Moderator Selection': 'CP_MODERATOR_ANALYSIS',
        'Analysis Model': 'CP_HETEROGENEITY_ANALYSIS',
        'Data Extraction': 'CP_DATA_EXTRACTION',

        # Search & Screening
        'Search Strategy': 'CP_SEARCH_STRATEGY',
        '검색 전략': 'CP_SEARCH_STRATEGY',

        'Screening Criteria': 'CP_SCREENING_CRITERIA',
        '선별 기준': 'CP_SCREENING_CRITERIA',

        'Extraction Template': 'CP_EXTRACTION_TEMPLATE',
        '추출 템플릿': 'CP_EXTRACTION_TEMPLATE',
    }

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

    def _check_skill_loaded(self, response: str) -> Dict[str, Any]:
        """
        Verify if Diverga skill was actually loaded and active.

        Looks for definitive markers that indicate the skill is loaded:
        1. Skill activation confirmation message
        2. Research Coordinator specific terminology
        3. VS methodology markers (T-Score, options with typicality)
        4. Checkpoint system markers with proper formatting
        5. Agent invocation patterns via Task tool

        Returns dict with 'loaded', 'confidence', 'evidence' keys.
        """
        evidence = []
        confidence_score = 0

        # Check 1: Skill activation markers (weight: 30)
        activation_patterns = [
            r'Research\s*Coordinator\s*v[\d.]+',  # Version mention
            r'diverga[:\-]research[:\-]coordinator',  # Skill name
            r'Human[:\-]Centered\s*Edition',  # v6.0 marker
            r'(27|33|40)\s*specialized\s*agents',  # Agent system mention (v5.0=27, v6.0.1=33, v6.3+=40)
            r'패러다임\s*(탐지|감지)',  # Korean paradigm detection
            r'[A-H][1-7][-\s]?[A-Za-z-]+',  # Agent name pattern like A1-ResearchQuestionRefiner
        ]
        for pattern in activation_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                evidence.append(f"Skill marker: {pattern[:30]}...")
                confidence_score += 30
                break

        # Check 2: VS Methodology markers (weight: 25)
        vs_patterns = [
            r'\(T\s*=\s*\d+\.?\d*\)',  # T-Score notation
            r'T[:\-]Score',  # T-Score label
            r'Typicality\s*Score',  # Full name
            r'\[A\].*\[B\].*\[C\]',  # Option format
            r'modal\s*(recommendation|option)',  # Modal awareness
        ]
        for pattern in vs_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                evidence.append(f"VS marker: {pattern[:30]}...")
                confidence_score += 25
                break

        # Check 3: Checkpoint system markers (weight: 25)
        checkpoint_patterns = [
            r'🔴\s*CHECKPOINT',  # Red checkpoint emoji
            r'🟠\s*CHECKPOINT',  # Orange checkpoint emoji
            r'체크포인트.*CP_',  # Korean checkpoint
            r'Human\s*Checkpoint\s*System',  # System mention
            r'MANDATORY\s*HALT',  # Halt terminology
        ]
        for pattern in checkpoint_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                evidence.append(f"Checkpoint marker: {pattern[:30]}...")
                confidence_score += 25
                break

        # Check 4: Agent invocation evidence (weight: 20)
        agent_patterns = [
            r'Task\(subagent_type\s*=\s*["\']diverga:',  # Task tool call
            r'diverga:[a-h][1-7]',  # Agent ID pattern
            r'([A-H][1-7])\s*에이전트\s*실행',  # Korean agent execution
        ]
        for pattern in agent_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                evidence.append(f"Agent marker: {pattern[:30]}...")
                confidence_score += 20
                break

        # Determine overall confidence
        if confidence_score >= 50:
            loaded = True
            confidence = 'HIGH' if confidence_score >= 75 else 'MEDIUM'
        elif confidence_score >= 25:
            loaded = True
            confidence = 'LOW'
        else:
            loaded = False
            confidence = 'NONE'

        return {
            'loaded': loaded,
            'confidence': confidence,
            'score': confidence_score,
            'evidence': evidence
        }

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

    def _normalize_checkpoint_name(self, name: str) -> Optional[str]:
        """
        Normalize a checkpoint name to formal CP_ format using alias mapping.

        Args:
            name: Raw checkpoint name (could be formal CP_XXX or descriptive)

        Returns:
            Normalized CP_ identifier or None if not recognized
        """
        name = name.strip()

        # Already in formal format
        if name.upper().startswith('CP_'):
            return name.upper()

        # Check alias mapping (case-insensitive)
        name_lower = name.lower()
        for alias, formal_id in self.CHECKPOINT_ALIASES.items():
            if alias.lower() == name_lower:
                return formal_id

        # Try partial matching for common patterns
        for alias, formal_id in self.CHECKPOINT_ALIASES.items():
            # If the name contains the core keywords from the alias
            alias_words = set(alias.lower().split())
            name_words = set(name_lower.split())
            if len(alias_words) >= 2 and alias_words <= name_words:
                return formal_id

        return None

    def _detect_checkpoints(self, response: str) -> List[Dict[str, Any]]:
        """
        Detect checkpoint markers in response with confidence scoring.

        HYBRID DETECTION (v3.2.0):
        1. Primary: Look for formal CP_XXX identifiers
        2. Fallback: Detect descriptive names and map via CHECKPOINT_ALIASES

        Returns list of dicts with 'id', 'confidence', 'level', 'context', and 'original' keys.

        Checkpoint naming convention (from research-coordinator):
        - CP_RESEARCH_DIRECTION, CP_PARADIGM_SELECTION, CP_THEORY_SELECTION
        - CP_METHODOLOGY_APPROVAL, CP_ANALYSIS_PLAN, CP_INTEGRATION_STRATEGY
        - CP_QUALITY_REVIEW, CP_EFFECT_SIZE_SELECTION, CP_HETEROGENEITY_ANALYSIS
        - CP_HUMANIZATION_REVIEW, CP_HUMANIZATION_VERIFY, etc.

        Confidence levels:
        - HIGH: Emoji marker + formal CP_XXX with options OR emoji + descriptive with options
        - MEDIUM: Text "CHECKPOINT" + CP_XXX format OR emoji + descriptive without options
        - LOW: Partial match or text mention without action
        """
        detected = []
        seen_ids = set()

        # Valid checkpoint ID pattern: CP_ followed by uppercase words/digits
        # Examples: CP_RESEARCH_DIRECTION, CP_META_TIER3_REVIEW, CP_GATE_2
        VALID_CP_PATTERN = r'^CP_[A-Z0-9]+(?:_[A-Z0-9]+)*$'

        # ============================================
        # PHASE 1: Detect formal CP_XXX identifiers
        # ============================================

        # HIGH confidence: Emoji + full checkpoint format + options presented
        # Supports multiple formats:
        # - 🔴 CHECKPOINT: CP_XXX
        # - 🔴 CP_XXX (확인)
        # - 🔴 CP_XXX
        # - ## 🔴 CP_XXX
        high_patterns_formal = [
            # Format: 🔴 CHECKPOINT: CP_XXX
            (r'🔴\s*(?:CHECKPOINT|체크포인트)[:\s]+\*?\*?(CP_[A-Z0-9]+(?:_[A-Z0-9]+)*)\*?\*?', 'RED'),
            (r'🟠\s*(?:CHECKPOINT|체크포인트)[:\s]+\*?\*?(CP_[A-Z0-9]+(?:_[A-Z0-9]+)*)\*?\*?', 'ORANGE'),
            (r'🟡\s*(?:CHECKPOINT|체크포인트)[:\s]+\*?\*?(CP_[A-Z0-9]+(?:_[A-Z0-9]+)*)\*?\*?', 'YELLOW'),
            # Format: 🔴 CP_XXX (with optional markdown headers and annotations)
            (r'(?:#+\s*)?🔴\s*(CP_[A-Z0-9]+(?:_[A-Z0-9]+)*)\s*(?:\([^)]*\))?', 'RED'),
            (r'(?:#+\s*)?🟠\s*(CP_[A-Z0-9]+(?:_[A-Z0-9]+)*)\s*(?:\([^)]*\))?', 'ORANGE'),
            (r'(?:#+\s*)?🟡\s*(CP_[A-Z0-9]+(?:_[A-Z0-9]+)*)\s*(?:\([^)]*\))?', 'YELLOW'),
        ]

        for pattern, level in high_patterns_formal:
            for match in re.finditer(pattern, response, re.IGNORECASE):
                cp_id = match.group(1).upper()
                after_match = response[match.end():match.end() + 500]
                has_options = bool(re.search(r'\[(?:Y|N|A|B|C|[1-3])\]|옵션\s*[A-C]|Option\s*[A-C]', after_match, re.IGNORECASE))

                if re.match(VALID_CP_PATTERN, cp_id) and cp_id not in seen_ids:
                    detected.append({
                        'id': cp_id,
                        'confidence': 'HIGH' if has_options else 'MEDIUM',
                        'level': level,
                        'context': 'formal CP_ with emoji' + (' + options' if has_options else ''),
                        'original': cp_id
                    })
                    seen_ids.add(cp_id)

        # MEDIUM confidence: Plain text checkpoint format with CP_
        medium_patterns_formal = [
            r'(?:\*\*)?CHECKPOINT(?:\*\*)?[:\s]+\*?\*?(CP_[A-Z0-9]+(?:_[A-Z0-9]+)*)\*?\*?',
            r'(?:checkpoint|체크포인트)\s*[:]\s*(CP_[A-Z0-9]+(?:_[A-Z0-9]+)*)',
            r'(?:\*\*)?CHECKPOINT(?:\*\*)?[:\s]+\*?\*?(META_[A-Z0-9]+(?:_[A-Z0-9]+)*)\*?\*?',
            # Format: ## CP_XXX or ### CP_XXX (without emoji)
            r'^#+\s*(CP_[A-Z0-9]+(?:_[A-Z0-9]+)*)\s*(?:\([^)]*\))?',
            # Format: **CP_XXX** in bold
            r'\*\*(CP_[A-Z0-9]+(?:_[A-Z0-9]+)*)\*\*',
        ]

        for pattern in medium_patterns_formal:
            for match in re.finditer(pattern, response, re.IGNORECASE):
                cp_id = match.group(1).upper()
                if re.match(VALID_CP_PATTERN, cp_id) and cp_id not in seen_ids:
                    detected.append({
                        'id': cp_id,
                        'confidence': 'MEDIUM',
                        'level': 'UNKNOWN',
                        'context': 'formal CP_ text mention',
                        'original': cp_id
                    })
                    seen_ids.add(cp_id)

        # ============================================
        # PHASE 2: Detect descriptive checkpoint names (HYBRID)
        # ============================================

        # HIGH/MEDIUM confidence: Emoji + descriptive name (no CP_ prefix)
        # Pattern: 🔴 CHECKPOINT: Effect Size Target Selection
        descriptive_patterns = [
            (r'🔴\s*(?:CHECKPOINT|체크포인트)[:\s]+([A-Za-z가-힣][A-Za-z0-9가-힣\s\-]+?)(?:\n|\*\*|$)', 'RED'),
            (r'🟠\s*(?:CHECKPOINT|체크포인트)[:\s]+([A-Za-z가-힣][A-Za-z0-9가-힣\s\-]+?)(?:\n|\*\*|$)', 'ORANGE'),
            (r'🟡\s*(?:CHECKPOINT|체크포인트)[:\s]+([A-Za-z가-힣][A-Za-z0-9가-힣\s\-]+?)(?:\n|\*\*|$)', 'YELLOW'),
        ]

        for pattern, level in descriptive_patterns:
            for match in re.finditer(pattern, response, re.IGNORECASE):
                raw_name = match.group(1).strip()

                # Skip if it's already a formal CP_ identifier (handled in Phase 1)
                if raw_name.upper().startswith('CP_'):
                    continue

                # Try to map to formal identifier
                formal_id = self._normalize_checkpoint_name(raw_name)

                if formal_id and formal_id not in seen_ids:
                    after_match = response[match.end():match.end() + 500]
                    has_options = bool(re.search(r'\[(?:Y|N|A|B|C|[1-3])\]|옵션\s*[A-C]|Option\s*[A-C]', after_match, re.IGNORECASE))

                    detected.append({
                        'id': formal_id,
                        'confidence': 'HIGH' if has_options else 'MEDIUM',
                        'level': level,
                        'context': f'descriptive → {formal_id}' + (' + options' if has_options else ''),
                        'original': raw_name
                    })
                    seen_ids.add(formal_id)
                elif not formal_id:
                    # Unknown descriptive name - still record it with LOW confidence
                    # Generate a pseudo-ID from the name
                    pseudo_id = 'CP_' + re.sub(r'[^A-Z0-9]', '_', raw_name.upper()).strip('_')
                    pseudo_id = re.sub(r'_+', '_', pseudo_id)  # Remove duplicate underscores

                    if pseudo_id not in seen_ids and len(pseudo_id) > 4:
                        detected.append({
                            'id': pseudo_id,
                            'confidence': 'LOW',
                            'level': level,
                            'context': f'unmapped descriptive: {raw_name[:30]}',
                            'original': raw_name
                        })
                        seen_ids.add(pseudo_id)

        # ============================================
        # PHASE 3: LOW confidence - partial mentions
        # ============================================

        low_patterns = [
            r'(?:checkpoint|체크포인트)\s+(?:for\s+)?([A-Z][A-Z_]+)',
        ]

        for pattern in low_patterns:
            for match in re.finditer(pattern, response, re.IGNORECASE):
                raw_id = match.group(1).upper()
                cp_id = f"CP_{raw_id}" if not raw_id.startswith('CP_') else raw_id
                if re.match(VALID_CP_PATTERN, cp_id) and cp_id not in seen_ids:
                    detected.append({
                        'id': cp_id,
                        'confidence': 'LOW',
                        'level': 'UNKNOWN',
                        'context': 'inferred from text',
                        'original': raw_id
                    })
                    seen_ids.add(cp_id)

        return detected

    def _get_checkpoint_ids(self, detected_checkpoints: List[Dict[str, Any]], min_confidence: str = 'MEDIUM') -> List[str]:
        """Extract checkpoint IDs from detected checkpoints, filtered by minimum confidence."""
        confidence_order = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        min_level = confidence_order.get(min_confidence, 2)

        return [
            cp['id'] for cp in detected_checkpoints
            if confidence_order.get(cp['confidence'], 0) >= min_level
        ]

    def _detect_agents(self, response: str) -> List[Dict[str, Any]]:
        """
        Detect agent invocations in response with confidence scoring.

        Returns list of dicts with 'id', 'confidence', and 'context' keys.

        Confidence levels:
        - HIGH: Task tool invocation (e.g., Task(subagent_type="diverga:a1"))
        - MEDIUM: Explicit agent reference with action verb (e.g., "A1 에이전트 실행")
        - LOW: Text mention only (e.g., "A1-ResearchQuestionRefiner를 사용할 수 있습니다")

        Note: Valid Diverga agents per category (33 agents total, v6.0.1):
        - A1-A6: Foundation (6)
        - B1-B4: Evidence (4) - Note: B5 does not exist
        - C1-C7: Design & Meta-Analysis (7)
        - D1-D4: Data Collection (4)
        - E1-E5: Analysis (5)
        - F1-F4: Quality (4) - Note: F5 does not exist
        - G1-G4: Communication (4) - Note: G5-G7 do not exist
        - H1-H2: Specialized (2)
        """
        # Valid agent IDs per category (strict validation)
        VALID_AGENTS = {
            'A': [1, 2, 3, 4, 5, 6],      # Foundation
            'B': [1, 2, 3, 4],             # Evidence (no B5)
            'C': [1, 2, 3, 4, 5, 6, 7],    # Design & Meta-Analysis
            'D': [1, 2, 3, 4],             # Data Collection
            'E': [1, 2, 3, 4, 5],          # Analysis
            'F': [1, 2, 3, 4],             # Quality (no F5)
            'G': [1, 2, 3, 4],             # Communication (no G5-G7)
            'H': [1, 2],                   # Specialized
        }

        def is_valid_agent(agent_id: str) -> bool:
            """Check if agent ID is in the valid registry."""
            if len(agent_id) < 2:
                return False
            letter = agent_id[0].upper()
            try:
                number = int(agent_id[1:])
                return letter in VALID_AGENTS and number in VALID_AGENTS[letter]
            except ValueError:
                return False

        detected = []
        seen_ids = set()

        # HIGH confidence: Task tool invocation
        task_patterns = [
            r'Task\s*\(\s*subagent_type\s*=\s*["\']diverga:([a-h][1-7])["\']',
            r'subagent_type\s*=\s*["\']diverga:([a-h][1-7])["\']',
            r'Task.*diverga:([a-h][1-7])',
            # Also detect general-purpose with agent ID in prompt
            r'Task\s*\(.*model.*["\']([A-H][1-7])["\']',
            r'description\s*=\s*["\'][^"\']*([A-H][1-7])[^"\']*["\']',
        ]
        for pattern in task_patterns:
            for match in re.finditer(pattern, response, re.IGNORECASE):
                agent_id = match.group(1).upper()
                if is_valid_agent(agent_id) and agent_id not in seen_ids:
                    detected.append({
                        'id': agent_id,
                        'confidence': 'HIGH',
                        'context': 'Task tool invocation'
                    })
                    seen_ids.add(agent_id)

        # MEDIUM confidence: Explicit execution with action verbs
        action_patterns = [
            # Korean action verbs
            (r'([A-H][1-7])[-\s]?[A-Za-z-]*\s*(에이전트|agent)?\s*(실행|호출|사용|활성화)', '실행/호출'),
            (r'(실행|호출).*([A-H][1-7])', '실행/호출'),
            # English action verbs
            (r'([A-H][1-7])[-\s]?[A-Za-z-]*\s*(agent)?\s*(invoke|invok|execut|running|activat)', 'invocation'),
            (r'(invoking|executing|running)\s+([A-H][1-7])', 'invocation'),
        ]
        for pattern, context in action_patterns:
            for match in re.finditer(pattern, response, re.IGNORECASE):
                # Extract agent ID from match groups
                for group in match.groups():
                    if group and len(group) >= 2:
                        potential_id = group[:2].upper() if group[0].isalpha() and group[1].isdigit() else None
                        if potential_id and is_valid_agent(potential_id) and potential_id not in seen_ids:
                            detected.append({
                                'id': potential_id,
                                'confidence': 'MEDIUM',
                                'context': context
                            })
                            seen_ids.add(potential_id)

        # LOW confidence: Text mentions only (for reference, not counted as invocations)
        mention_patterns = [
            r'diverga:([a-h][1-7])',  # diverga:a1
            r'([A-H][1-7])-[A-Za-z-]+',  # A1-ResearchQuestionRefiner or A1-research-question-refiner
            r'\*?\*?([A-H][1-7])\*?\*?\s*[-:]\s*[A-Za-z-]+',  # A1: ResearchQuestionRefiner or **A1**-...
        ]
        for pattern in mention_patterns:
            for match in re.finditer(pattern, response, re.IGNORECASE):
                agent_id = match.group(1).upper()
                if is_valid_agent(agent_id) and agent_id not in seen_ids:
                    detected.append({
                        'id': agent_id,
                        'confidence': 'LOW',
                        'context': 'text mention'
                    })
                    seen_ids.add(agent_id)

        return detected

    def _get_agent_ids(self, detected_agents: List[Dict[str, Any]], min_confidence: str = 'LOW') -> List[str]:
        """Extract agent IDs from detected agents, filtered by minimum confidence."""
        confidence_order = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        min_level = confidence_order.get(min_confidence, 1)

        return [
            agent['id'] for agent in detected_agents
            if confidence_order.get(agent['confidence'], 0) >= min_level
        ]

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
        print(f"Diverga QA Protocol v3.2.2 - True Automated Testing")
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
                detected_checkpoints = self._detect_checkpoints(response)
                detected_agents = self._detect_agents(response)
                vs_options = self._extract_vs_options(response)

                # Check if skill is loaded (for first turn)
                skill_check = {}
                if self._turn_count == 1:
                    skill_check = self._check_skill_loaded(response)

                # Extract IDs for backward compatibility
                checkpoint_ids = self._get_checkpoint_ids(detected_checkpoints, min_confidence='MEDIUM')
                agent_ids = self._get_agent_ids(detected_agents, min_confidence='MEDIUM')

                # Record assistant turn
                assistant_turn = Turn(
                    number=turn_num,
                    role='assistant',
                    content=response,
                    timestamp=datetime.now().isoformat(),
                    checkpoints_detected=checkpoint_ids,
                    agents_detected=agent_ids,
                    vs_options=vs_options,
                    metadata={
                        'expected': expected,
                        'detected_checkpoints_full': detected_checkpoints,
                        'detected_agents_full': detected_agents,
                        'skill_check': skill_check
                    }
                )
                self.session.turns.append(assistant_turn)

                # Update session-level aggregates
                for cp in detected_checkpoints:
                    if cp['confidence'] in ['HIGH', 'MEDIUM']:
                        self.session.checkpoints.append({
                            'checkpoint': cp['id'],
                            'turn': turn_num,
                            'confidence': cp['confidence'],
                            'level': cp.get('level', 'UNKNOWN'),
                            'timestamp': datetime.now().isoformat()
                        })

                # Only count agents with HIGH/MEDIUM confidence as actually invoked
                for agent in detected_agents:
                    if agent['confidence'] in ['HIGH', 'MEDIUM']:
                        if agent['id'] not in self.session.agents_invoked:
                            self.session.agents_invoked.append(agent['id'])

                high_cp = len([c for c in detected_checkpoints if c['confidence'] == 'HIGH'])
                high_agents = len([a for a in detected_agents if a['confidence'] in ['HIGH', 'MEDIUM']])
                print(f"  ✓ Completed (CP: {high_cp} high/{len(detected_checkpoints)} total, Agents: {high_agents})")

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

    # Checkpoint equivalence groups: IDs that should be treated as equivalent
    CHECKPOINT_EQUIVALENCES = {
        # Paradigm checkpoints (selection vs confirmation are equivalent)
        'CP_PARADIGM_SELECTION': 'CP_PARADIGM_CONFIRMATION',
        'CP_PARADIGM_CONFIRMATION': 'CP_PARADIGM_SELECTION',

        # Moderator checkpoints (selection vs analysis are equivalent)
        'CP_MODERATOR_SELECTION': 'CP_MODERATOR_ANALYSIS',
        'CP_MODERATOR_ANALYSIS': 'CP_MODERATOR_SELECTION',

        # Approval checkpoints (analysis plan vs methodology are equivalent)
        'CP_ANALYSIS_PLAN_APPROVAL': 'CP_METHODOLOGY_APPROVAL',
        'CP_METHODOLOGY_APPROVAL': 'CP_ANALYSIS_PLAN_APPROVAL',

        # Analysis model vs heterogeneity (both relate to model selection)
        'CP_ANALYSIS_MODEL': 'CP_HETEROGENEITY_ANALYSIS',
        'CP_HETEROGENEITY_ANALYSIS': 'CP_ANALYSIS_MODEL',
    }

    def _fuzzy_checkpoint_match(self, found: str, expected: str) -> bool:
        """
        Check if found checkpoint matches expected checkpoint using fuzzy matching.

        Handles cases like:
        - CP_RESEARCH vs CP_RESEARCH_DIRECTION (partial match)
        - CP_EFFECT_SIZE vs CP_EFFECT_SIZE_SELECTION (partial match)
        - Case insensitivity
        - Equivalent checkpoint IDs (v3.2.0)

        Stricter matching (v3.1.1):
        - Requires 75% keyword overlap instead of 50%
        - All expected keywords must appear in found (for short expected names)
        """
        found_upper = found.upper()
        expected_upper = expected.upper()

        # Exact match (highest priority)
        if found_upper == expected_upper:
            return True

        # Equivalence match (v3.2.0): Check if IDs are equivalent
        if found_upper in self.CHECKPOINT_EQUIVALENCES:
            if self.CHECKPOINT_EQUIVALENCES[found_upper] == expected_upper:
                return True

        # Prefix match: found is a prefix of expected
        # Example: CP_RESEARCH matches CP_RESEARCH_DIRECTION
        if expected_upper.startswith(found_upper) and len(found_upper) >= 6:  # At least "CP_XX"
            return True

        # Prefix match: expected is a prefix of found
        if found_upper.startswith(expected_upper) and len(expected_upper) >= 6:
            return True

        # Strict keyword match: extract key words and compare
        found_words = set(found_upper.replace('CP_', '').replace('META_', '').split('_'))
        expected_words = set(expected_upper.replace('CP_', '').replace('META_', '').split('_'))

        # Remove empty strings
        found_words.discard('')
        expected_words.discard('')

        if not expected_words:
            return False

        overlap = found_words & expected_words

        # For short expected names (1-2 words), require ALL expected words in found
        if len(expected_words) <= 2:
            return expected_words <= found_words

        # For longer names, require 75% overlap
        if len(overlap) >= len(expected_words) * 0.75:
            return True

        return False

    def _validate_session(self) -> Dict[str, Any]:
        """Validate session against protocol expectations."""
        expected_checkpoints = [
            cp['id'] for cp in self.protocol.get('checkpoints_expected', [])
        ]
        found_checkpoints = [cp['checkpoint'] for cp in self.session.checkpoints]

        expected_agents = self.protocol.get('agents_involved', [])

        # Run verification huddle if enabled in protocol
        verification_huddle = self._run_verification_huddle()

        # Skill loading verification
        skill_verification = self._verify_skill_loading()

        # Fuzzy checkpoint matching
        matched_checkpoints = []
        for expected_cp in expected_checkpoints:
            for found_cp in found_checkpoints:
                if self._fuzzy_checkpoint_match(found_cp, expected_cp):
                    matched_checkpoints.append({
                        'expected': expected_cp,
                        'found': found_cp,
                        'exact': found_cp.upper() == expected_cp.upper()
                    })
                    break

        # Calculate compliance with fuzzy matching
        fuzzy_compliance = len(matched_checkpoints) / max(len(expected_checkpoints), 1) * 100
        exact_compliance = len([m for m in matched_checkpoints if m['exact']]) / max(len(expected_checkpoints), 1) * 100

        # Agent matching - extract agent IDs from expected (e.g., "A1-ResearchQuestionRefiner" -> "A1")
        expected_agent_ids = []
        for agent in expected_agents:
            if '-' in agent:
                agent_id = agent.split('-')[0].upper()
            else:
                agent_id = agent.upper()
            if re.match(r'^[A-H][1-7]$', agent_id):
                expected_agent_ids.append(agent_id)

        return {
            'checkpoints': {
                'expected': expected_checkpoints,
                'found': found_checkpoints,
                'matched': matched_checkpoints,
                'missing': [cp for cp in expected_checkpoints
                           if not any(self._fuzzy_checkpoint_match(f, cp) for f in found_checkpoints)],
                'compliance': fuzzy_compliance,
                'exact_compliance': exact_compliance
            },
            'agents': {
                'expected': expected_agents,
                'expected_ids': expected_agent_ids,
                'found': self.session.agents_invoked,
                'match_rate': len(set(expected_agent_ids) & set(self.session.agents_invoked)) / max(len(expected_agent_ids), 1) * 100 if expected_agent_ids else 0
            },
            'turns': {
                'expected_min': int(self.protocol.get('expected_turns', '1').split('-')[0]) if isinstance(self.protocol.get('expected_turns'), str) else self.protocol.get('expected_turns', 1),
                'actual': len([t for t in self.session.turns if t.role == 'user']),
            },
            'skill_loading': skill_verification,
            'verification_huddle': verification_huddle
        }

    def _verify_skill_loading(self) -> Dict[str, Any]:
        """Aggregate skill loading verification from all turns."""
        assistant_turns = [t for t in self.session.turns if t.role == 'assistant']

        if not assistant_turns:
            return {'verified': False, 'reason': 'No assistant responses'}

        # Check first turn for skill loading
        first_turn = assistant_turns[0]
        skill_check = first_turn.metadata.get('skill_check', {})

        if skill_check:
            return {
                'verified': skill_check.get('loaded', False),
                'confidence': skill_check.get('confidence', 'NONE'),
                'score': skill_check.get('score', 0),
                'evidence': skill_check.get('evidence', [])
            }

        # Fallback: Run skill check on first response if not done during execution
        first_response = first_turn.content
        skill_check = self._check_skill_loaded(first_response)

        return {
            'verified': skill_check.get('loaded', False),
            'confidence': skill_check.get('confidence', 'NONE'),
            'score': skill_check.get('score', 0),
            'evidence': skill_check.get('evidence', [])
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
        """Save human-readable conversation transcript with CLI tool suffix."""
        # v3.2.2: Include CLI tool in filename to support dual transcripts
        cli_suffix = f"_{self.session.cli_tool}" if self.session.cli_tool else ""
        transcript_file = output_path / f'conversation_transcript{cli_suffix}.md'

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
                    f.write(f"**Checkpoints Detected**: {', '.join(turn.checkpoints_detected)}\n")
                    # Show confidence from metadata if available
                    full_cps = turn.metadata.get('detected_checkpoints_full', [])
                    if full_cps:
                        f.write("  - Details: ")
                        cp_details = [f"{cp['id']}({cp['confidence']})" for cp in full_cps]
                        f.write(", ".join(cp_details) + "\n")
                    f.write("\n")

                if turn.agents_detected:
                    f.write(f"**Agents Detected**: {', '.join(turn.agents_detected)}\n")
                    # Show confidence from metadata if available
                    full_agents = turn.metadata.get('detected_agents_full', [])
                    if full_agents:
                        f.write("  - Details: ")
                        agent_details = [f"{a['id']}({a['confidence']})" for a in full_agents]
                        f.write(", ".join(agent_details) + "\n")
                    f.write("\n")

                # Show skill check for first turn
                skill_check = turn.metadata.get('skill_check', {})
                if skill_check and turn.number == 1:
                    verified = "✅" if skill_check.get('loaded') else "❌"
                    f.write(f"**Skill Loaded**: {verified} (Confidence: {skill_check.get('confidence', 'NONE')})\n\n")
                if turn.vs_options:
                    f.write("**VS Options**:\n")
                    for opt in turn.vs_options:
                        f.write(f"- [{opt['option']}] {opt['label']} (T={opt['t_score']})\n")
                    f.write("\n")

                f.write("---\n\n")

    def _save_raw_json(self, output_path: Path):
        """Save raw session data as JSON with CLI tool suffix."""
        # v3.2.2: Include CLI tool in filename to support dual transcripts
        cli_suffix = f"_{self.session.cli_tool}" if self.session.cli_tool else ""
        raw_file = output_path / f'conversation_raw{cli_suffix}.json'

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
        """Save test result summary as YAML with CLI tool suffix."""
        # v3.2.2: Include CLI tool in filename to support dual results
        cli_suffix = f"_{self.session.cli_tool}" if self.session.cli_tool else ""
        result_file = output_path / f'{self.session.scenario_id}_test_result{cli_suffix}.yaml'

        validation = self.session.validation_results
        skill_loading = validation.get('skill_loading', {})

        # Status based on both checkpoint compliance and skill loading
        checkpoint_compliance = validation.get('checkpoints', {}).get('compliance', 0)
        skill_verified = skill_loading.get('verified', False)

        if checkpoint_compliance >= 80 and skill_verified:
            status = "PASSED"
        elif checkpoint_compliance >= 80:
            status = "PARTIAL"  # Checkpoints OK but skill not verified
        else:
            status = "FAILED"

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
                'checkpoint_compliance': f"{checkpoint_compliance:.1f}%",
                'agents_invoked': len(self.session.agents_invoked),
                'skill_loaded': skill_verified,
                'skill_confidence': skill_loading.get('confidence', 'NONE'),
            },
            'validation': validation,
            'checkpoints': [
                {
                    'id': cp['checkpoint'],
                    'turn': cp['turn'],
                    'status': 'TRIGGERED',
                    'confidence': cp.get('confidence', 'UNKNOWN')
                }
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
            f.write(f"| Agents Invoked | {len(self.session.agents_invoked)} |\n")

            # Skill loading verification
            skill_loading = validation.get('skill_loading', {})
            skill_status = "✅ Yes" if skill_loading.get('verified') else "❌ No"
            f.write(f"| Skill Loaded | {skill_status} ({skill_loading.get('confidence', 'NONE')}) |\n\n")

            # Skill loading details
            if skill_loading:
                f.write("## 🔧 SKILL LOADING VERIFICATION\n\n")
                f.write(f"**Verified**: {skill_loading.get('verified', False)}\n")
                f.write(f"**Confidence**: {skill_loading.get('confidence', 'NONE')}\n")
                f.write(f"**Score**: {skill_loading.get('score', 0)}/100\n\n")

                if skill_loading.get('evidence'):
                    f.write("**Evidence**:\n")
                    for ev in skill_loading['evidence']:
                        f.write(f"- {ev}\n")
                    f.write("\n")

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
        description='Diverga QA v3.2.2 - True Automated Testing via CLI',
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
