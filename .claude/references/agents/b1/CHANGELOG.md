# SKILL.md Changelog - Literature Review Strategist

## Version 4.1.0 (2026-01-25)

### Major Changes

**Agent Renamed**: `systematic-literature-scout` → `literature-review-strategist`
**New Title**: B1-Literature Review Strategist

### New Review Types Supported

Added support for **5 additional review methodologies** beyond systematic reviews:

1. **Scoping Review** (JBI Scoping Review, PRISMA-ScR)
   - Purpose: Research area mapping, gap identification
   - Timeline: 4-8 months
   - Standards: JBI Manual, PRISMA-ScR (22 items)

2. **Meta-Synthesis/Meta-Ethnography** (Noblit & Hare, 1988)
   - Purpose: Qualitative research integration
   - Timeline: 8-12 months
   - Standards: ENTREQ (21 items)
   - Approaches: Meta-ethnography, Thematic synthesis, Critical interpretive synthesis

3. **Realist Synthesis** (RAMESES standard)
   - Purpose: Complex intervention context-mechanism-outcome analysis
   - Timeline: 8-14 months
   - Standards: RAMESES (24 items)
   - Framework: C+M→O configurations

4. **Narrative Review** (Traditional, Critical, Integrative)
   - Purpose: Theory development, concept clarification
   - Timeline: 3-6 months
   - Standards: No formal checklist (logical structure required)

5. **Rapid Review** (Accelerated PRISMA)
   - Purpose: Urgent policy decisions
   - Timeline: 2-4 weeks
   - Standards: PRISMA-RR (adapted)

### New Sections Added

#### 1. Review Type Specifications (Lines 188-285)
Detailed methodology for each review type:
- Standard/framework
- Search requirements
- Quality indicators
- Key differences

#### 2. Review Type Selection Guide (Lines 423-463)
Decision tree for users unsure which review type to use:
- Interactive decision flow
- Comparison table (6 dimensions)
- Timeline and rigor comparison

#### 3. Review-Type Specific Modal Warnings (Lines 94-186)
Separate Phase 1 warnings for each review type:
- Systematic Review: Single DB, English-only
- Scoping Review: Too narrow scope, no iteration
- Meta-Synthesis: Quantitative DB focus, exhaustive search
- Realist Synthesis: No CMO framing, linear search
- Narrative Review: Cherry-picking, no scope
- Rapid Review: Too comprehensive, no transparency

#### 4. Review-Type Specific Database Recommendations (Lines 465-491)
Tailored database selections:
- Systematic: PubMed, Scopus, WoS, PsycINFO, ERIC
- Scoping: 2-3 major + Google Scholar
- Meta-Synthesis: PsycINFO, CINAHL, Sociological Abstracts
- Realist: Iterative snowballing + theory papers
- Narrative: 1-2 selective + key journals
- Rapid: PubMed + 1 discipline DB (recent only)

#### 5. Review-Type Specific Reporting Standards (Lines 505-515)
Checklist requirements:
- PRISMA 2020 (27 items) - Systematic
- PRISMA-ScR (22 items) - Scoping
- ENTREQ (21 items) - Meta-Synthesis
- RAMESES (24 items) - Realist
- No standard - Narrative
- PRISMA-RR (adapted) - Rapid

#### 6. Example Workflows (Lines 517-569)
Four detailed workflow examples:
- Systematic Review (PRISMA 2020)
- Scoping Review (JBI) - with Korean example
- Meta-Synthesis (Noblit & Hare)
- Realist Synthesis (RAMESES)

#### 7. Expanded References (Lines 571-608)
Added 20+ new references:
- JBI Manual, Arksey & O'Malley (2005)
- Noblit & Hare (1988), ENTREQ
- RAMESES, Pawson (2006)
- Rapid review methodology papers

### Updated Metadata

```yaml
name: literature-review-strategist  # Changed from systematic-literature-scout
version: 4.1.0  # Bumped from 4.0.0
description: |
  Supports: Systematic Review, Scoping Review, Meta-Synthesis, 
  Realist Synthesis, Narrative Review, Rapid Review
triggers: 
  - Added: scoping review, meta-synthesis, realist synthesis, 
    narrative review, rapid review
```

### Updated Input Requirements (Lines 286-297)

Added required field:
```yaml
Required:
  - review_type: "systematic_review | scoping_review | meta_synthesis | realist_synthesis | narrative_review | rapid_review"
```

### Backward Compatibility

All existing systematic review functionality preserved:
- PRISMA 2020 workflow unchanged
- VS 5-Phase process intact
- Database recommendations for systematic reviews maintained
- Creativity mechanisms still available

### Files Affected

- `/Volumes/External SSD/Projects/research-coordinator/.claude/skills/research-agents/05-systematic-literature-scout/SKILL.md`

### Next Steps

**Recommended Updates for Related Agents**:
1. **Agent #09**: Meta-Synthesis Coordinator (new agent needed)
2. **Agent #10**: Realist Evaluator (new agent needed)
3. **Agent #06**: Evidence Quality Appraiser (update for CASP, JBI critical appraisal tools)

**Integration Updates**:
- Update `pipeline-templates.md` to include scoping/meta-synthesis workflows
- Add review type selection to `guided-wizard.md`
- Update `project-state.yaml` schema to include `review_type` field

---

## Version History

- **4.1.0** (2026-01-25): Added 5 new review types, decision guidance, expanded references
- **4.0.0** (2025-XX-XX): Full VS integration, PRISMA 2020 focus
- **3.0.0** (2025-XX-XX): Initial VS-enhanced version

