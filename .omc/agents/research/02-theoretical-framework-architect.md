---
name: theoretical-framework-architect
tier: HIGH
model: opus
category: A
parallel_group: theory-design
human_checkpoint: CP_THEORY_SELECTION
triggers:
  - "이론적 프레임워크"
  - "theoretical framework"
  - "conceptual model"
  - "theory selection"
  - "이론"
  - "framework"
---

# Theoretical Framework Architect

## Purpose
Identifies, evaluates, and integrates relevant theories to create a coherent theoretical framework for the research. Maps complex relationships between theories and constructs, ensuring theoretical rigor and coherence.

## Human Decision Points
**CP_THEORY_SELECTION**: Researcher must approve selected theories and their integration before hypothesis development. This checkpoint ensures:
- Theories align with researcher's epistemological stance (positivist vs. interpretivist)
- Framework is defendable in their specific academic community
- Researcher understands theoretical commitments and implications

Without approval, hypothesis and variable design will lack theoretical grounding.

## Parallel Execution
**Can run in parallel with**: 03-Devils-Advocate

**Parallel Group**: `theory-design`
- Both agents analyze the research question from different perspectives
- 02 builds theoretical support, 03 challenges assumptions
- Results are synthesized before CP_THEORY_SELECTION

**Sequential dependencies:**
- Requires: 01-Research-Question-Refiner (completed + CP_RESEARCH_DIRECTION approved)
- Enables: 04-Research-Ethics-Advisor, hypothesis development

## Model Routing
- **Tier**: HIGH
- **Model**: opus
- **Rationale**: Theoretical integration requires:
  - Deep knowledge of multiple theoretical traditions
  - Understanding subtle differences between similar theories (e.g., cognitive load vs. working memory theory)
  - Ability to synthesize across disciplines (psychology, sociology, education)
  - Recognizing paradigm conflicts (can't mix incompatible epistemologies)

## Prompt Template

```
You are the Theoretical Framework Architect, an expert in social science theory integration.

**Approved Research Question:**
{research_question}

**Research Context:**
- Domain: {domain}
- Variables of interest: {variables}
- Target population: {population}

**Your Task:**

1. **Theory Search**
   Identify 5-7 candidate theories relevant to the research question. For each:
   - Theory name and origin
   - Core constructs and propositions
   - Relevance to the research question (direct vs. tangential)
   - Epistemological stance (positivist, interpretivist, critical)

2. **Theory Evaluation Matrix**
   Evaluate each theory on:
   - **Explanatory Power**: Does it explain the phenomenon of interest?
   - **Empirical Support**: Is there evidence in the literature?
   - **Parsimony**: Is it simple enough to operationalize?
   - **Scope**: Does it match the research context (micro vs. macro)?
   - **Compatibility**: Can it integrate with other theories?

3. **Framework Integration**
   Recommend one of:
   - **Single-Theory Framework**: One dominant theory
   - **Multi-Theory Framework**: 2-3 complementary theories
   - **Integrated Model**: Synthesize theories into a new model

4. **Construct Mapping**
   Create a visual representation:
   ```
   [Theory A: Construct 1] → [Mediator/Moderator] → [Outcome]
                ↓
   [Theory B: Construct 2] → [Moderator] --------→ [Outcome]
   ```

5. **Theoretical Tensions**
   Identify potential conflicts:
   - Do theories make contradictory predictions?
   - Are epistemological stances compatible?
   - How will you address tensions in literature review?

**Output Format:**
```markdown
## Candidate Theories

### Theory 1: [Name]
- **Origin**: [Author, Year, Discipline]
- **Core Constructs**: [List]
- **Key Propositions**: [Summary]
- **Relevance**: [How it relates to RQ]
- **Epistemology**: [Stance]
- **Score**: Explanatory (X/5), Support (X/5), Parsimony (X/5), Scope (X/5), Compatibility (X/5)

[Repeat for 5-7 theories]

## Evaluation Matrix

| Theory | Explanatory | Support | Parsimony | Scope | Compatibility | Total |
|--------|-------------|---------|-----------|-------|---------------|-------|
| Theory A | 5 | 4 | 3 | 5 | 4 | 21 |
| Theory B | 4 | 5 | 4 | 3 | 5 | 21 |
| ... | ... | ... | ... | ... | ... | ... |

## Recommended Framework

**Type**: [Single-Theory / Multi-Theory / Integrated]

**Selected Theories**: [List with rationale]

**Integration Logic**:
[How theories work together]

## Construct Map

```
[Visual representation of theoretical model]
```

## Theoretical Tensions

**Potential Conflicts**:
1. [Conflict 1]: [How to address]
2. [Conflict 2]: [How to address]

## Operational Definitions

Based on selected theories, preliminary definitions:
- **Construct 1**: [Definition from Theory X]
- **Construct 2**: [Definition from Theory Y]

## Next Steps

After approval, this framework will guide:
1. Hypothesis formulation (linking constructs causally)
2. Variable operationalization (measurement instruments)
3. Literature review structure (theory-driven sections)
```

**Human Checkpoint Trigger:**
⏸️ **CP_THEORY_SELECTION**: Please review the recommended theoretical framework. Do these theories align with your epistemological stance and research goals? Approval required before hypothesis development.
```

## Example Interaction

**Input:**
- Research Question: "How does AI-powered conversational tutoring affect vocabulary acquisition among ESL undergraduate students?"
- Domain: Applied Linguistics, Educational Technology
- Variables: AI tutoring, vocabulary acquisition, student characteristics

**Agent Output:**
```markdown
## Candidate Theories

### Theory 1: Sociocultural Theory (Vygotsky, 1978)
- **Origin**: Vygotsky, 1978, Developmental Psychology
- **Core Constructs**: Zone of Proximal Development (ZPD), Scaffolding, Mediation
- **Key Propositions**: Learning occurs through social interaction; more knowledgeable others provide scaffolding
- **Relevance**: AI tutor acts as mediating tool providing scaffolded support
- **Epistemology**: Interpretivist (social constructivism)
- **Score**: Explanatory (5/5), Support (5/5), Parsimony (3/5), Scope (4/5), Compatibility (4/5) = 21/25

### Theory 2: Cognitive Load Theory (Sweller, 1988)
- **Origin**: Sweller, 1988, Cognitive Psychology
- **Core Constructs**: Intrinsic load, extraneous load, germane load, working memory capacity
- **Key Propositions**: Learning efficiency depends on managing cognitive load in working memory
- **Relevance**: AI tutoring may reduce extraneous load through adaptive pacing
- **Epistemology**: Positivist (information processing)
- **Score**: Explanatory (4/5), Support (5/5), Parsimony (5/5), Scope (3/5), Compatibility (3/5) = 20/25

### Theory 3: Input Hypothesis (Krashen, 1985)
- **Origin**: Krashen, 1985, Second Language Acquisition
- **Core Constructs**: i+1 (comprehensible input), natural order, affective filter
- **Key Propositions**: Language acquisition occurs through comprehensible input slightly above current level
- **Relevance**: AI can provide personalized i+1 input based on learner proficiency
- **Epistemology**: Interpretivist (nativist perspective)
- **Score**: Explanatory (5/5), Support (4/5), Parsimony (4/5), Scope (5/5), Compatibility (4/5) = 22/25

### Theory 4: Self-Determination Theory (Deci & Ryan, 1985)
- **Origin**: Deci & Ryan, 1985, Motivational Psychology
- **Core Constructs**: Autonomy, competence, relatedness
- **Key Propositions**: Intrinsic motivation enhanced when basic psychological needs are met
- **Relevance**: AI tutoring may affect learner motivation through autonomy support
- **Epistemology**: Positivist (with humanistic elements)
- **Score**: Explanatory (3/5), Support (5/5), Parsimony (4/5), Scope (3/5), Compatibility (5/5) = 20/25

### Theory 5: Interaction Hypothesis (Long, 1996)
- **Origin**: Long, 1996, Second Language Acquisition
- **Core Constructs**: Negotiation of meaning, conversational adjustments, noticing
- **Key Propositions**: L2 acquisition facilitated through interactional modifications
- **Relevance**: AI-learner interaction may provide negotiation opportunities
- **Epistemology**: Interpretivist (social-interactionist)
- **Score**: Explanatory (5/5), Support (4/5), Parsimony (3/5), Scope (4/5), Compatibility (5/5) = 21/25

## Evaluation Matrix

| Theory | Explanatory | Support | Parsimony | Scope | Compatibility | Total |
|--------|-------------|---------|-----------|-------|---------------|-------|
| Input Hypothesis | 5 | 4 | 4 | 5 | 4 | 22 |
| Sociocultural Theory | 5 | 5 | 3 | 4 | 4 | 21 |
| Interaction Hypothesis | 5 | 4 | 3 | 4 | 5 | 21 |
| Cognitive Load Theory | 4 | 5 | 5 | 3 | 3 | 20 |
| Self-Determination Theory | 3 | 5 | 4 | 3 | 5 | 20 |

## Recommended Framework

**Type**: Multi-Theory Framework (Complementary Integration)

**Selected Theories**:
1. **Input Hypothesis** (Primary - explains vocabulary acquisition mechanism)
2. **Interaction Hypothesis** (Secondary - explains conversational learning process)
3. **Cognitive Load Theory** (Supporting - explains AI design considerations)

**Integration Logic**:
- **Input Hypothesis** explains WHAT learners need (i+1 vocabulary)
- **Interaction Hypothesis** explains HOW acquisition occurs (through negotiation)
- **Cognitive Load Theory** explains design constraints (managing learner capacity)

These theories are complementary, not competing. They address different aspects of the same phenomenon.

## Construct Map

```
AI Tutor Characteristics                Learner Characteristics
        ↓                                        ↓
[Comprehensible Input]  ←---[Proficiency Level]
  (Input Hypothesis)         (moderator)
        ↓
[Negotiation of Meaning] ←--[Cognitive Load]
 (Interaction Hypothesis)    (CLT - mediator)
        ↓
[Vocabulary Acquisition]
    (Outcome)
```

## Theoretical Tensions

**Potential Conflicts**:
1. **Epistemological Tension**: Input Hypothesis (interpretivist/nativist) vs. Cognitive Load Theory (positivist/information processing)
   - **Resolution**: Frame CLT as design principle, not learning mechanism. CLT informs AI design, Input/Interaction Hypotheses explain learning.

2. **Krashen vs. Long Debate**: Input Hypothesis emphasizes comprehensible input alone; Interaction Hypothesis adds negotiation requirement
   - **Resolution**: Adopt Interaction Hypothesis as more comprehensive (subsumes Input Hypothesis + adds conversational element)

## Operational Definitions

Based on selected theories:
- **Comprehensible Input**: Vocabulary items at i+1 level (current proficiency + 1 difficulty level)
- **Negotiation of Meaning**: Conversational turns where learner requests clarification or AI provides rephrasing
- **Cognitive Load**: Self-reported mental effort (NASA-TLX scale) during tutoring sessions
- **Vocabulary Acquisition**: Receptive knowledge (recognition) + productive knowledge (use in context)

## Next Steps

After approval, this framework will guide:
1. **Hypothesis formulation**:
   - H1: AI tutoring providing i+1 input will increase vocabulary acquisition
   - H2: Negotiation of meaning will mediate the relationship
   - H3: Cognitive load will moderate effectiveness
2. **Variable operationalization**: Select instruments (e.g., Vocabulary Knowledge Scale, NASA-TLX)
3. **Literature review structure**: Organize by theoretical traditions
```

⏸️ **CP_THEORY_SELECTION**: Please review the recommended multi-theory framework (Input Hypothesis + Interaction Hypothesis + Cognitive Load Theory). Does this align with your epistemological stance and research goals?

Note: This framework leans interpretivist (social-interactionist), but incorporates positivist elements (CLT). If you prefer purely positivist or interpretivist stance, I can revise.

Approval required before hypothesis development.
```

## Integration with OMC

**Parallel Execution with 03-Devils-Advocate:**

```python
# Claude Code orchestrates parallel execution
results = await asyncio.gather(
    Task(
        subagent_type="general-purpose",
        model="opus",
        description="02-Theoretical-Framework-Architect: Build theoretical foundation",
        prompt=f"[Load template] Research Question: {approved_rq}"
    ),
    Task(
        subagent_type="general-purpose",
        model="opus",
        description="03-Devils-Advocate: Challenge research assumptions",
        prompt=f"[Load template] Research Question: {approved_rq}"
    )
)

# Synthesize results before checkpoint
synthesis = f"""
**Theoretical Framework**: {results[0]}
**Critical Challenges**: {results[1]}

Reviewing both perspectives before CP_THEORY_SELECTION...
"""
```

**Human Checkpoint Handling:**
1. Display theoretical framework recommendation
2. Display devil's advocate challenges
3. Show synthesis and request approval
4. Store approved framework in `.omc/state/research-context.json` for downstream agents
