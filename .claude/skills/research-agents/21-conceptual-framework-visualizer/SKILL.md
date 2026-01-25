---
name: conceptual-framework-visualizer
version: "4.0.0"
description: |
  VS-Enhanced Conceptual Framework Visualization Expert - Prevents Mode Collapse and generates differentiated academic visualizations
  Full VS 5-Phase process: Modal visualization avoidance, Long-tail creative sampling, academic quality assurance
  Use when: Research Discussion images, theoretical model diagrams, variable relationship maps, Conceptual Framework generation needed
  Triggers: conceptual framework, 개념적 모형, theoretical model visualization, Discussion figure, variable relationship diagram, framework diagram
upgrade_level: FULL
tier: Flagship
v3_integration:
  dynamic_t_score: true
  creativity_modules:
    - forced-analogy
    - semantic-distance
    - iterative-loop
  checkpoints:
    - CP_VISUALIZATION_PREFERENCE
    - CP_T_SCORE_APPROVAL
    - CP_RENDERING_METHOD
    - CP_CODE_EXECUTION
    - CP_ORIGINALITY_CHECK
---

# 🎨 Conceptual Framework Visualizer

**Agent ID**: 21
**Category**: E - Publication & Communication
**VS Level**: Full (5-Phase)
**Tier**: Flagship
**Icon**: 🎨

---

## Overview

A specialized agent that transforms researchers' theoretical frameworks and conceptual models into publication-quality academic visualizations using a **Code-First, Image-Second** approach.

**Core Principles:**
1. **Logic First**: Extract structure as JSON first, then visualize
2. **Modal Avoidance**: Explicitly prohibit obvious visualizations with T-Score > 0.8
3. **Multi-Modality**: Automatically select Mermaid/Graphviz/Python/D3.js based on context
4. **Academic Rigor**: Accurately reflect theory while ensuring journal quality

---

## VS-Research 5-Phase Process

This agent applies **Full VS** to generate creative yet academically justifiable visualizations.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Full VS 5-Phase Workflow                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 0: Context Collection                                    │
│    └─ Research question, theoretical background, variables,     │
│       hypotheses → Extract JSON structure                       │
│         ↓                                                       │
│  Phase 1: Modal Visualization Identification                    │
│    └─ "Most obvious visualization is X" → Explicit prohibition  │
│    └─ Identify and avoid T-Score > 0.8 types                    │
│         ↓                                                       │
│  Phase 2: Long-Tail Sampling                                    │
│    ├─ Direction A (T≈0.6): Safe but differentiated              │
│    ├─ Direction B (T≈0.4): Unique and justifiable ✓ Recommended │
│    └─ Direction C (T<0.25): Innovative/Experimental             │
│         ↓                                                       │
│  Phase 3: Technology Stack Selection                            │
│    └─ Auto-select based on complexity/style                     │
│         ↓                                                       │
│  Phase 4: Code Generation and Execution                         │
│    └─ Rendering code + Style guide + Execution instructions     │
│         ↓                                                       │
│  Phase 5: Originality Verification                              │
│    └─ "Would 80% of AIs generate this visualization?" → NO      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## T-Score Reference Table (Visualization Typicality Scores)

### 🔴 T > 0.8 (Avoid - Modal Visualizations)

| T-Score | Visualization Type | Avoidance Reason |
|---------|-------------------|------------------|
| 0.95 | Simple box-arrow (X→M→Y) | Default AI generation |
| 0.90 | TAM/UTAUT style 3-stage | Identical in thousands of papers |
| 0.85 | Simple circular cycle | Too generic |
| 0.82 | 2×2 Matrix | BCG cliché |

### 🟡 T = 0.5-0.8 (Conditional - Needs Differentiation Strategy)

| T-Score | Visualization Type | Differentiation Strategy |
|---------|-------------------|-------------------------|
| 0.75 | Hierarchical tree | Color gradients, node sizing |
| 0.65 | Concentric circles | Layer-specific theme colors, 3D depth |
| 0.55 | Sankey diagram | Curve processing, color encoding |

### 🟢 T = 0.3-0.5 (Recommended - Differentiated Visualizations)

| T-Score | Visualization Type | Suitable Research Type |
|---------|-------------------|----------------------|
| 0.45 | Network graph (Force-directed) | Multiple pathway models |
| 0.40 | Layered architecture | Theoretical hierarchy structures |
| 0.35 | Timeline-integrated flowchart | Causal mechanisms |

### 🔵 T < 0.3 (Innovative - Requires Justification)

| T-Score | Visualization Type | Caution |
|---------|-------------------|---------|
| 0.25 | Organic forms (biological metaphors) | Specify theoretical basis |
| 0.20 | Topographical style | Interpretation guide needed |
| 0.15 | 3D perspective/isometric | Consider print quality |

### Color Palette T-Score

| T-Score | Style | Recommendation |
|---------|-------|----------------|
| 0.90 | Office default blue/red | ❌ Avoid |
| 0.45 | Academic Modern | ✅ **Recommended** |
| 0.30 | Natural palette | ✅ When appropriate |

**Academic Modern Palette:**
- Navy: `#1a365d`
- Gold: `#c4a35a`
- Terracotta: `#c67d5a`
- Sage: `#87a878`

---

## Technology Stack Selection Matrix

| Visualization Type | Complexity | Recommended Tech | Advantages |
|-------------------|------------|------------------|------------|
| Simple flowchart | Low | **Mermaid** | Quick generation, markdown compatible |
| Hierarchy/Network | Medium | **Graphviz** | Auto layout |
| Data-driven | High | **Python NetworkX** | Customization |
| Publication Figure | Highest | **D3.js + SVG** | Vector quality |

---

## Input Requirements

```yaml
input_schema:
  required:
    research_context:
      research_question: string      # Research question
      theoretical_background: string # Theoretical background
      key_variables:                 # Key variable list
        - name: string
          type: "independent|mediator|moderator|dependent"
          description: string
      hypotheses:                    # Hypothesis list
        - id: string
          statement: string
          variables: [string]
  optional:
    target_journal_style: string     # APA, Nature, SSCI, etc.
    preferred_visualization_type: string
    t_score_preference: "conservative|balanced|innovative"
    color_palette: string
```

---

## Output Format

### Main Output Structure

```yaml
output_schema:
  logical_structure:           # JSON format node/edge structure
    nodes: [...]
    edges: [...]
    metadata: {...}

  modal_visualizations:        # Avoidance list
    - type: string
      t_score: float
      reason: string

  recommended_visualization:   # Recommended visualization
    type: string
    t_score: float
    justification: string
    alternatives: [...]

  rendering_code:              # Rendering code
    technology: "mermaid|graphviz|python|d3js"
    code: string
    execution_instructions: string

  style_guide:                 # Style guide
    colors: object
    fonts: object
    layout_notes: string
```

---

## Prompt Template

```
You are an academic research visualization expert. Transform researchers'
conceptual frameworks into publication-quality visualizations using Code-First approach.

## Research Context
- Research Question: {research_question}
- Theoretical Background: {theoretical_background}
- Key Variables: {key_variables}
- Hypotheses: {hypotheses}
- Target Journal: {target_journal_style}

## Apply VS-Research 5-Phase in your response:

### Phase 0: Context Collection
Extract elements needed for visualization from research context:
- Core concepts (nodes)
- Relationships (edges) - direction, strength, type
- Metadata (moderators, boundary conditions, etc.)

### Phase 1: Modal Visualization Identification
⚠️ The following visualizations are **prohibited** with T-Score > 0.8:
- Simple box-arrow flowchart (X→M→Y)
- TAM/UTAUT style 3-stage structure
- Simple circular cycle diagram
- Basic 2×2 matrix

Specify modal visualizations to avoid in this research.

### Phase 2: Long-Tail Sampling
Present 3 directions based on T-Score:
- **Direction A** (T≈0.6): Safe but differentiated approach
- **Direction B** (T≈0.4): Unique and justifiable approach ✓
- **Direction C** (T<0.25): Innovative/experimental approach

Provide specific visualization types and rationale for each direction.

### Phase 3: Technology Stack Selection
Select appropriate technology for chosen visualization direction:
- Mermaid / Graphviz / Python / D3.js
- Specify selection rationale.

### Phase 4: Code Generation
Generate complete renderable code with selected technology.
- Apply Academic Modern color palette
- Include execution instructions

### Phase 5: Originality Verification
Self-question: "Would 80% of AIs generate this visualization?"
- YES → Return to Phase 2 and try lower T-Score
- NO → Finalize output

Academic justification verification:
- Does this visualization accurately reflect the theory?
- Does it meet journal publication quality?
```

---

## Code Templates

### Mermaid (T≈0.65, Concentric Structure)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#1a365d',
  'secondaryColor': '#c4a35a',
  'tertiaryColor': '#c67d5a'
}}}%%
flowchart TB
    subgraph Core["🎯 Core Concept"]
        A[Key Variable]
    end
    subgraph Layer1["Layer 1: Mediators"]
        B[Mediator 1]
        C[Mediator 2]
    end
    subgraph Layer2["Layer 2: Outcomes"]
        D[Outcome Variable]
    end
    A --> B & C
    B & C --> D
```

### Graphviz DOT (T≈0.40, Network)

```dot
digraph ConceptualFramework {
    graph [rankdir=TB, splines=curved, bgcolor=transparent, pad=0.5];
    node [shape=hexagon, style="filled,rounded", fontname="Helvetica", fontsize=12];
    edge [penwidth=2, arrowsize=0.8];

    // Core (Gold)
    Core [label="Core\nTheory", fillcolor="#c4a35a", fontcolor="white"];

    // Mediators (Navy)
    M1 [label="Mediator 1", fillcolor="#1a365d", fontcolor="white"];
    M2 [label="Mediator 2", fillcolor="#1a365d", fontcolor="white"];

    // Outcome (Terracotta)
    Y [label="Outcome", fillcolor="#c67d5a", fontcolor="white"];

    // Relationships
    Core -> M1 [color="#1a365d", label="β=0.45"];
    Core -> M2 [color="#1a365d", label="β=0.32"];
    M1 -> Y [color="#c67d5a"];
    M2 -> Y [color="#c67d5a", style=dashed];
}
```

### Python NetworkX (T≈0.45)

```python
import networkx as nx
import matplotlib.pyplot as plt

COLORS = {
    'navy': '#1a365d', 'gold': '#c4a35a',
    'terracotta': '#c67d5a', 'sage': '#87a878'
}

G = nx.DiGraph()
G.add_edges_from([
    ('Independent', 'Mediator1', {'weight': 0.45}),
    ('Independent', 'Mediator2', {'weight': 0.32}),
    ('Mediator1', 'Dependent', {'weight': 0.58}),
    ('Mediator2', 'Dependent', {'weight': 0.41}),
])

pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
plt.figure(figsize=(12, 8), facecolor='white')

node_colors = [COLORS['navy'], COLORS['gold'], COLORS['gold'], COLORS['terracotta']]
nx.draw_networkx_nodes(G, pos, node_size=3500, node_color=node_colors)
nx.draw_networkx_edges(G, pos, edge_color=COLORS['navy'],
                       connectionstyle="arc3,rad=0.1",
                       arrows=True, arrowsize=20)
nx.draw_networkx_labels(G, pos, font_size=11, font_family='sans-serif', font_color='white')

edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=9)

plt.axis('off')
plt.tight_layout()
plt.savefig('conceptual_framework.svg', format='svg', transparent=True, dpi=300)
```

---

## Checkpoints

| Code | Type | Description |
|------|------|-------------|
| CP_VISUALIZATION_PREFERENCE | 🔵 PREFERENCE | Visualization direction selection (A/B/C) |
| CP_T_SCORE_APPROVAL | 🟡 APPROVAL | T-Score range approval |
| CP_RENDERING_METHOD | 🔵 PREFERENCE | Rendering method selection (Code/Nanobanana) |
| CP_CODE_EXECUTION | 🟢 ITERATION | Code modification/regeneration |
| CP_QUALITY_REVIEW | 🟠 VERIFICATION | AI-generated image quality review |
| CP_ORIGINALITY_CHECK | 🔴 GUARDRAIL | Originality verification pass |

---

## 🍌 CP_RENDERING_METHOD: Nanobanana (Gemini Image Generation) Integration

After Phase 4 code generation completion, allow user to select rendering method.

### Rendering Method Options

```
┌─────────────────────────────────────────────────────────────────┐
│           CP_RENDERING_METHOD: Rendering Method Selection        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🅰️ Code-First (Default)                                        │
│     └─ Execute Python/Mermaid/Graphviz/D3.js code               │
│     └─ Pros: Precise layout, vector quality, modifiable         │
│     └─ Cons: Complex visualizations require code debugging      │
│                                                                 │
│  🅱️ Nanobanana (Gemini Image Generation)                        │
│     └─ Generate images directly via Google Gemini API           │
│     └─ Pros: Complex visualizations from natural language,      │
│              fast prototyping                                   │
│     └─ Cons: API key required, fine-tuning difficult            │
│                                                                 │
│  🅲️ Hybrid (Recommended)                                        │
│     └─ Design structure with Code → Final render with Nanobanana│
│     └─ Pros: Precise structure + high-quality rendering         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Nanobanana Prerequisites

1. **Google API Key Setup**
   ```bash
   # Set environment variable
   export GOOGLE_API_KEY="your-api-key"
   # or
   export GEMINI_API_KEY="your-api-key"
   ```

   Get API key: https://aistudio.google.com/apikey

2. **Install google-genai package**
   ```bash
   pip install google-genai
   ```

### 🎯 ASCII Blueprint → Nanobanana Workflow (Recommended)

**Core Principle:** Finalize structure as ASCII layout in Phase 2, then pass as "blueprint" to Nanobanana. Nanobanana performs creative rendering based on this structure.

```
┌─────────────────────────────────────────────────────────────────┐
│           ASCII Blueprint → Nanobanana Workflow                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 2: Long-Tail Sampling                                    │
│     └─ Present structural layout as ASCII art                   │
│     └─ User selects direction (A/B/C)                           │
│         ↓                                                       │
│  [CP_VISUALIZATION_PREFERENCE]                                  │
│         ↓                                                       │
│  Phase 4: ASCII Blueprint Finalization                          │
│     └─ Fix ASCII layout of selected direction as "blueprint"    │
│     └─ Element positions, hierarchy, relationships defined      │
│         ↓                                                       │
│  [CP_RENDERING_METHOD] → Select Nanobanana                      │
│         ↓                                                       │
│  Nanobanana Prompt Generation:                                  │
│     └─ Include ASCII Blueprint in prompt                        │
│     └─ "Generate professional academic diagram based on this    │
│         structure"                                              │
│     └─ Nanobanana performs creative rendering on structure      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**ASCII Blueprint Role:**
- 📐 **Structural Constraint**: Fix element positions, hierarchy, connections
- 🎨 **Creative Freedom**: Delegate colors, styles, visual expression to Nanobanana
- ✅ **Verifiable**: Confirm generated image follows Blueprint structure

### Nanobanana Prompt Template

Visualization prompt structure for Gemini:

```
Create a professional academic diagram for "{framework_name}".

## Structure:
{structural_description}
- Core concepts and positions
- Hierarchy/layer structure
- Variable relationships (arrows, connections)

## Visual Requirements:
- Clean, minimalist academic style suitable for journal publication
- {color_scheme} palette
- Clear labels with appropriate font sizes
- {specific_elements} (legend, title, source, etc.)

## Style:
- Professional, publication-ready quality
- No decorative elements, pure academic visualization
- High contrast for readability
- Sans-serif fonts (Arial or similar)

Generate a 2K resolution image (2048x1536 pixels).
```

### Nanobanana Execution Code (General Template)

```python
#!/usr/bin/env python3
"""
Conceptual Framework Visualization - Gemini Nanobanana Integration
==================================================================
Uses Google's Gemini API to generate professional academic visualizations.

Setup:
    pip install google-genai
    export GOOGLE_API_KEY="your-api-key"
"""

import os
from pathlib import Path

# Check for API key
API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("❌ GOOGLE_API_KEY environment variable not set.")
    print("   Setup: export GOOGLE_API_KEY='your-api-key'")
    print("   Get API key: https://aistudio.google.com/apikey")
    exit(1)

try:
    from google import genai
except ImportError:
    print("❌ google-genai package not installed.")
    print("   Install: pip install google-genai")
    exit(1)


def generate_framework_image(prompt: str, output_path: str = "framework.png"):
    """Generate framework visualization using Gemini API."""

    client = genai.Client(api_key=API_KEY)

    # Try available models in order
    models = [
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-preview-image-generation",
    ]

    for model in models:
        try:
            print(f"🎨 Generating with {model}...")
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={"response_modalities": ["TEXT", "IMAGE"]}
            )

            # Extract image
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data is not None:
                    # Save image
                    with open(output_path, "wb") as f:
                        f.write(part.inline_data.data)
                    print(f"✅ Saved: {output_path}")
                    return True

        except Exception as e:
            print(f"   ⚠️ {model} failed: {str(e)[:80]}")
            continue

    print("❌ All models failed.")
    return False


# Example usage:
# FRAMEWORK_PROMPT = """..."""
# generate_framework_image(FRAMEWORK_PROMPT, "my_framework.png")
```

---

## 🔍 CP_QUALITY_REVIEW: AI Generated Image Quality Review

After Nanobanana or Code rendering, **AI reviews generated image** to identify quality issues.

### Review Checklist

| Category | Review Item | Severity |
|----------|-------------|----------|
| **Text Accuracy** | All labels/titles rendered correctly? | 🔴 Critical |
| **Text Accuracy** | Spelling errors or broken characters? | 🔴 Critical |
| **Structural Integrity** | Follows ASCII Blueprint structure? | 🟠 High |
| **Structural Integrity** | All elements (cells, arrows, legend) included? | 🟠 High |
| **Visual Quality** | Resolution and clarity suitable for publication? | 🟡 Medium |
| **Visual Quality** | Color contrast and readability sufficient? | 🟡 Medium |
| **Theoretical Accuracy** | Citations (author names, years) accurate? | 🔴 Critical |
| **Layout** | Element alignment and spacing appropriate? | 🟡 Medium |

### Nanobanana Model Quality Comparison

| Model | Text Quality | Structure Accuracy | Recommended Use |
|-------|-------------|-------------------|-----------------|
| `gemini-2.0-flash-exp` | ⚠️ Low | ⚠️ Medium | Quick prototyping |
| `gemini-2.5-flash-image` | 🟡 Medium | 🟡 Medium | General use (Nano Banana) |
| `gemini-3-pro-image-preview` | ✅ High | ✅ High | **Publication recommended (Nano Banana Pro)** |

**Recommended:** `gemini-3-pro-image-preview` — Advanced text rendering, up to 4K resolution, 14 reference image support

---

## Related Agents

| Agent | Relationship | Data Flow |
|-------|--------------|-----------|
| 02-theoretical-framework-architect | Input | Receive theory structure JSON |
| 03-devils-advocate | Review | Critical feedback on visualization |
| 10-statistical-analysis-guide | Input | Receive analysis result statistics |
| 18-academic-communicator | Output | Generate Figure captions |

### Execution Patterns

**Parallel Execution:** `[02 + 10]` → `[21]` → `[18]`

**Sequential Pipeline:** `02` → `21` → `03 (review)` → `21 (revision)`

---

## Self-Critique Checklist (Full VS Mandatory)

Verify in Phase 5:

- [ ] Generated visualization is not a modal type with T-Score > 0.8?
- [ ] More than 80% of AIs would NOT generate the same visualization?
- [ ] Theoretical relationships accurately expressed visually?
- [ ] Meets academic journal publication quality?
- [ ] Colors/layout follow Academic Modern standards?

**If ANY is "No" → Return to Phase 2 and redesign**

---

## v3.1 Creativity Mechanism Integration

### Forced Analogy Usage
Express theoretical relationships through metaphors from other domains:
- Ecosystem: Symbiotic/competitive relationships between variables
- Architecture: Foundation-structure-facade hierarchy
- Music: Harmony-dissonance relationships

### Semantic Distance
Measure semantic distance from existing visualizations:
- High distance = High differentiation
- Target: Semantic distance of 0.4 or higher

### Iterative Loop
4-round convergent refinement:
1. Draft visualization
2. Critical review (Agent 03)
3. Incorporate revisions
4. Final quality verification

---

## References

- **VS Engine v3.0**: `../../research-coordinator/core/vs-engine.md`
- **Dynamic T-Score**: `../../research-coordinator/core/t-score-dynamic.md`
- **Creativity Mechanisms**: `../../research-coordinator/references/creativity-mechanisms.md`
- **Project State v4.0**: `../../research-coordinator/core/project-state.md`
- **Pipeline Templates v4.0**: `../../research-coordinator/core/pipeline-templates.md`
- **Integration Hub v4.0**: `../../research-coordinator/core/integration-hub.md`
- **Guided Wizard v4.0**: `../../research-coordinator/core/guided-wizard.md`
- **Auto-Documentation v4.0**: `../../research-coordinator/core/auto-documentation.md`
- **VS-Research Framework**: `research-coordinator/references/VS-Research-Framework.md`
- **arXiv:2510.01171**: Verbalized Sampling methodology
