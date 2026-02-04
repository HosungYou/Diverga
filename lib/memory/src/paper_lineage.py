"""
Diverga Memory System v8.0 - Paper Lineage Tracking

Tracks each paper's journey through the PRISMA 2020 systematic review pipeline.

Stages:
- identified: Paper discovered from database search
- screened: Title/abstract screening completed
- eligible: Full-text screening completed
- included: Final inclusion decision
- extracted: Data extraction completed
- rag_indexed: Added to RAG vector database

Each stage transition records:
- Decision (include/exclude)
- Rationale
- Source text (for transparency)
- AI confidence (if AI-assisted)
- Human verification status

Author: Diverga Project
Version: 8.0.0
"""

from __future__ import annotations

import yaml
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Literal
from enum import Enum


class LineageStage(str, Enum):
    """PRISMA 2020 pipeline stages."""
    IDENTIFIED = "identified"
    SCREENED = "screened"
    ELIGIBLE = "eligible"
    INCLUDED = "included"
    EXTRACTED = "extracted"
    RAG_INDEXED = "rag_indexed"


class Decision(str, Enum):
    """Stage transition decisions."""
    INCLUDE = "include"
    EXCLUDE = "exclude"
    UNCERTAIN = "uncertain"


@dataclass
class StageTransition:
    """
    Record of a paper moving from one stage to the next.

    Attributes:
        stage: PRISMA stage reached
        decision: Include/exclude/uncertain
        rationale: Human-readable explanation
        timestamp: When transition occurred
        source_text: Original text that led to decision (transparency)
        ai_confidence: AI confidence score (0-1), if AI-assisted
        human_verified: Whether a human has verified this decision
        reviewer_id: ID of human reviewer (if verified)
        exclusion_reason: Standardized reason if excluded
    """
    stage: str
    decision: str
    rationale: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    source_text: Optional[str] = None
    ai_confidence: Optional[float] = None
    human_verified: bool = False
    reviewer_id: Optional[str] = None
    exclusion_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class PaperRecord:
    """
    Complete lineage record for a single paper.

    Attributes:
        paper_id: Unique identifier (DOI, arXiv ID, or internal ID)
        title: Paper title
        authors: List of authors
        source_database: Where paper was found (semantic_scholar, openalex, arxiv)
        current_stage: Most recent stage reached
        transitions: List of stage transitions
        metadata: Additional metadata
    """
    paper_id: str
    title: str
    authors: List[str] = field(default_factory=list)
    source_database: str = ""
    current_stage: str = LineageStage.IDENTIFIED.value
    transitions: List[StageTransition] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "authors": self.authors,
            "source_database": self.source_database,
            "current_stage": self.current_stage,
            "transitions": [t.to_dict() for t in self.transitions],
            "metadata": self.metadata
        }


class PaperLineage:
    """
    Paper lineage tracking for systematic reviews.

    Manages the journey of papers through PRISMA stages with
    full transparency on AI vs. human decisions.

    Attributes:
        project_root: Project root directory
        lineage_file: Path to paper-lineage.yaml
        papers: Dictionary of paper_id -> PaperRecord
    """

    # Standard exclusion reasons (PRISMA 2020)
    EXCLUSION_REASONS = {
        "wrong_population": "Population does not match criteria",
        "wrong_intervention": "Intervention/exposure does not match",
        "wrong_comparator": "Comparator does not match",
        "wrong_outcome": "Outcomes do not match criteria",
        "wrong_study_design": "Study design does not match",
        "duplicate": "Duplicate of another included study",
        "no_full_text": "Full text not available",
        "wrong_language": "Language not in inclusion criteria",
        "wrong_publication_type": "Publication type excluded",
        "other": "Other reason (see rationale)"
    }

    def __init__(self, project_root: Path):
        """
        Initialize paper lineage tracker.

        Args:
            project_root: Project root directory
        """
        self.project_root = Path(project_root)
        self.lineage_file = self.project_root / ".research" / "paper-lineage.yaml"
        self.papers: Dict[str, PaperRecord] = {}
        self._load()

    def track_paper(
        self,
        paper_id: str,
        stage: str,
        decision: str,
        rationale: str,
        title: Optional[str] = None,
        authors: Optional[List[str]] = None,
        source_database: Optional[str] = None,
        source_text: Optional[str] = None,
        ai_confidence: Optional[float] = None,
        human_verified: bool = False,
        reviewer_id: Optional[str] = None,
        exclusion_reason: Optional[str] = None
    ) -> bool:
        """
        Track a paper's stage transition.

        Args:
            paper_id: Paper identifier (DOI, arXiv ID, etc.)
            stage: PRISMA stage reached
            decision: Include/exclude/uncertain
            rationale: Explanation for decision
            title: Paper title (required for new papers)
            authors: List of authors
            source_database: Source database (semantic_scholar, openalex, arxiv)
            source_text: Text that led to decision (for transparency)
            ai_confidence: AI confidence (0-1), if AI-assisted
            human_verified: Whether human verified
            reviewer_id: Human reviewer ID
            exclusion_reason: Standardized exclusion reason code

        Returns:
            True if tracked successfully
        """
        # Create new paper record if not exists
        if paper_id not in self.papers:
            if not title:
                print(f"Warning: Title required for new paper {paper_id}")
                return False

            self.papers[paper_id] = PaperRecord(
                paper_id=paper_id,
                title=title,
                authors=authors or [],
                source_database=source_database or "",
                current_stage=LineageStage.IDENTIFIED.value
            )

        paper = self.papers[paper_id]

        # Create transition record
        transition = StageTransition(
            stage=stage,
            decision=decision,
            rationale=rationale,
            source_text=source_text,
            ai_confidence=ai_confidence,
            human_verified=human_verified,
            reviewer_id=reviewer_id,
            exclusion_reason=exclusion_reason
        )

        # Add transition and update current stage
        paper.transitions.append(transition)
        paper.current_stage = stage

        # Save immediately
        self._save()

        return True

    def get_paper_journey(self, paper_id: str) -> Optional[Dict[str, Any]]:
        """
        Get complete journey for a paper.

        Args:
            paper_id: Paper identifier

        Returns:
            Paper record as dictionary, or None if not found
        """
        if paper_id not in self.papers:
            return None

        return self.papers[paper_id].to_dict()

    def get_papers_at_stage(self, stage: str) -> List[Dict[str, Any]]:
        """
        Get all papers currently at a specific stage.

        Args:
            stage: PRISMA stage

        Returns:
            List of paper records
        """
        return [
            p.to_dict() for p in self.papers.values()
            if p.current_stage == stage
        ]

    def get_papers_needing_verification(self) -> List[Dict[str, Any]]:
        """
        Get papers with AI decisions that need human verification.

        Returns:
            List of papers with unverified AI decisions
        """
        needs_review = []

        for paper in self.papers.values():
            for transition in paper.transitions:
                if transition.ai_confidence is not None and not transition.human_verified:
                    needs_review.append({
                        "paper_id": paper.paper_id,
                        "title": paper.title,
                        "stage": transition.stage,
                        "decision": transition.decision,
                        "ai_confidence": transition.ai_confidence,
                        "rationale": transition.rationale
                    })
                    break

        return needs_review

    def verify_decision(
        self,
        paper_id: str,
        stage: str,
        reviewer_id: str,
        approved: bool,
        new_rationale: Optional[str] = None
    ) -> bool:
        """
        Verify an AI-assisted decision.

        Args:
            paper_id: Paper identifier
            stage: Stage to verify
            reviewer_id: Human reviewer ID
            approved: Whether decision is approved
            new_rationale: Updated rationale if not approved

        Returns:
            True if verified successfully
        """
        if paper_id not in self.papers:
            return False

        paper = self.papers[paper_id]

        for transition in paper.transitions:
            if transition.stage == stage:
                transition.human_verified = True
                transition.reviewer_id = reviewer_id

                if not approved and new_rationale:
                    transition.rationale = new_rationale

                self._save()
                return True

        return False

    def get_prisma_counts(self) -> Dict[str, int]:
        """
        Get paper counts for PRISMA flow diagram.

        Returns:
            Dictionary with counts by stage
        """
        counts = {
            "identified": 0,
            "duplicates_removed": 0,
            "screened": 0,
            "excluded_screening": 0,
            "eligible": 0,
            "excluded_eligibility": 0,
            "included": 0,
            "extracted": 0,
            "rag_indexed": 0
        }

        for paper in self.papers.values():
            stage = paper.current_stage

            # Count by final stage
            if stage == "identified":
                counts["identified"] += 1
            elif stage == "screened":
                # Check if excluded
                last_transition = paper.transitions[-1] if paper.transitions else None
                if last_transition and last_transition.decision == "exclude":
                    counts["excluded_screening"] += 1
                else:
                    counts["screened"] += 1
            elif stage == "eligible":
                last_transition = paper.transitions[-1] if paper.transitions else None
                if last_transition and last_transition.decision == "exclude":
                    counts["excluded_eligibility"] += 1
                else:
                    counts["eligible"] += 1
            elif stage == "included":
                counts["included"] += 1
            elif stage == "extracted":
                counts["extracted"] += 1
            elif stage == "rag_indexed":
                counts["rag_indexed"] += 1

        # Calculate duplicates
        counts["duplicates_removed"] = sum(
            1 for p in self.papers.values()
            for t in p.transitions
            if t.exclusion_reason == "duplicate"
        )

        return counts

    def export_prisma_data(self) -> Dict[str, Any]:
        """
        Export data for PRISMA 2020 flow diagram generation.

        Returns:
            Dictionary with all PRISMA-required data
        """
        counts = self.get_prisma_counts()

        # Get exclusion reasons breakdown
        exclusions_screening = {}
        exclusions_eligibility = {}

        for paper in self.papers.values():
            for transition in paper.transitions:
                if transition.decision == "exclude" and transition.exclusion_reason:
                    reason = transition.exclusion_reason
                    if transition.stage == "screened":
                        exclusions_screening[reason] = exclusions_screening.get(reason, 0) + 1
                    elif transition.stage == "eligible":
                        exclusions_eligibility[reason] = exclusions_eligibility.get(reason, 0) + 1

        return {
            "counts": counts,
            "exclusions_screening": exclusions_screening,
            "exclusions_eligibility": exclusions_eligibility,
            "databases_searched": list(set(
                p.source_database for p in self.papers.values() if p.source_database
            )),
            "ai_assisted_count": sum(
                1 for p in self.papers.values()
                for t in p.transitions
                if t.ai_confidence is not None
            ),
            "human_verified_count": sum(
                1 for p in self.papers.values()
                for t in p.transitions
                if t.human_verified
            )
        }

    def _load(self):
        """Load lineage data from YAML file."""
        if not self.lineage_file.exists():
            return

        try:
            with open(self.lineage_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}

            for paper_data in data.get('papers', []):
                transitions = [
                    StageTransition(**t) for t in paper_data.get('transitions', [])
                ]
                paper = PaperRecord(
                    paper_id=paper_data['paper_id'],
                    title=paper_data.get('title', ''),
                    authors=paper_data.get('authors', []),
                    source_database=paper_data.get('source_database', ''),
                    current_stage=paper_data.get('current_stage', 'identified'),
                    transitions=transitions,
                    metadata=paper_data.get('metadata', {})
                )
                self.papers[paper.paper_id] = paper
        except Exception as e:
            print(f"Warning: Failed to load paper lineage: {e}")

    def _save(self):
        """Save lineage data to YAML file."""
        self.lineage_file.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": "8.0",
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "papers": [p.to_dict() for p in self.papers.values()]
        }

        try:
            with open(self.lineage_file, 'w', encoding='utf-8') as f:
                f.write("# Diverga Paper Lineage v8.0\n")
                f.write("# PRISMA 2020 paper tracking with transparency metadata\n\n")
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        except Exception as e:
            print(f"Warning: Failed to save paper lineage: {e}")


def generate_prisma_mermaid(lineage: PaperLineage) -> str:
    """
    Generate Mermaid diagram for PRISMA 2020 flow.

    Args:
        lineage: PaperLineage instance

    Returns:
        Mermaid diagram string
    """
    data = lineage.export_prisma_data()
    counts = data['counts']

    mermaid = """flowchart TD
    subgraph Identification
        A1[Records identified from databases<br/>n = {identified}]
        A2[Duplicates removed<br/>n = {duplicates}]
    end

    subgraph Screening
        B1[Records screened<br/>n = {screened}]
        B2[Records excluded<br/>n = {excluded_screening}]
    end

    subgraph Eligibility
        C1[Full-text assessed<br/>n = {eligible}]
        C2[Excluded<br/>n = {excluded_eligibility}]
    end

    subgraph Included
        D1[Studies included<br/>n = {included}]
        D2[Data extracted<br/>n = {extracted}]
        D3[RAG indexed<br/>n = {rag}]
    end

    A1 --> A2
    A2 --> B1
    B1 --> B2
    B1 --> C1
    C1 --> C2
    C1 --> D1
    D1 --> D2
    D2 --> D3
""".format(
        identified=counts['identified'],
        duplicates=counts['duplicates_removed'],
        screened=counts['screened'],
        excluded_screening=counts['excluded_screening'],
        eligible=counts['eligible'],
        excluded_eligibility=counts['excluded_eligibility'],
        included=counts['included'],
        extracted=counts['extracted'],
        rag=counts['rag_indexed']
    )

    return mermaid
