# Void Cartography Design System

A comprehensive design guide for the Diverga documentation site's deep space aesthetic and component system.

**T-Score: 0.42** (Creative Range) — Balancing dark elegance with purposeful innovation.

---

## Table of Contents

1. [Philosophy & Concept](#philosophy--concept)
2. [Color System](#color-system)
3. [Typography](#typography)
4. [Spacing & Layout](#spacing--layout)
5. [Components Reference](#components-reference)
6. [Animation Patterns](#animation-patterns)
7. [Code Examples](#code-examples)
8. [Bilingual Support](#bilingual-support)
9. [Accessibility](#accessibility)

---

## Philosophy & Concept

### Void Cartography: Mapping the Unexplored

The Void Cartography theme represents Diverga's mission to escape mode collapse and explore the long tail of intellectual possibility. It's not merely a dark theme—it's a philosophical stance rendered in interface design.

**Core Principles:**

- **Deep Space Aesthetic**: Uses a dark, infinite palette reminiscent of astronomical observation—appropriate for research that maps unknown territories
- **Luminescent Accents**: Stellar-colored text and glowing effects against void backgrounds create visual hierarchy without harshness
- **T-Score Visual Language**: Color spectrum from divergent (cyan) through creative (green) to modal (red) communicates research typicality directly in the UI
- **Punctuation Over Decoration**: Sharp corners, minimal rounded edges, and precise geometric elements reflect scientific precision
- **Motion with Purpose**: Animations emphasize content progression and human-system interaction, never distract

### Connection to Diverga Philosophy

The 27-agent orchestration system finds visual expression through:

- **Agent Category Colors (A-H)**: Each research domain gets a distinct vibrant color, making agent identification instant
- **Checkpoint System**: Colored badges communicate research stage and approval requirements
- **T-Score Spectrum**: Central to the interface, reminding researchers that diversity of approach is the system's strength

The T-Score of 0.42 itself is intentional—creative without being radical, predictable enough to understand, surprising enough to inspire.

---

## Color System

### Void Core Palette (Backgrounds)

The foundation of the design system—deep space neutrals providing infinite contrast for content.

```css
--color-void-absolute: #000000    /* Pure black, rarely used directly */
--color-void-deep: #050508        /* Primary background, near-black with purple tint */
--color-void-surface: #0a0a0f     /* Secondary surfaces, slightly elevated */
--color-void-elevated: #12121a    /* Cards and containers */
--color-void-hover: #1a1a24       /* Interactive hover state */
```

**Usage:**
- `.bg-void-deep` - Page background
- `.bg-void-surface` - Dividers, secondary sections
- `.bg-void-elevated` - Cards, modals, dropdowns
- `.bg-void-hover` - Hover states for interactive elements

**Example:**
```tsx
<div className="bg-void-deep min-h-screen">
  <div className="bg-void-elevated border border-stellar-faint/20 p-6">
    Content here
  </div>
</div>
```

### Stellar Accents (Text & Light)

Luminous colors for text, icons, and emphasis against void backgrounds.

```css
--color-stellar-core: #ffffff       /* Primary text, highest contrast */
--color-stellar-bright: #f0f0f5     /* Slightly warm white, reduced glare */
--color-stellar-dim: #8888aa        /* Secondary text, medium emphasis */
--color-stellar-faint: #44445a      /* Tertiary text, low emphasis */
--color-stellar-muted: #2a2a3a      /* Borders, dividers */
```

**Hierarchy:**
```
stellar-core      → Headlines, primary actions
stellar-bright    → Body text, primary focus
stellar-dim       → Secondary text, labels
stellar-faint     → Tertiary text, borders
stellar-muted     → Very subtle borders, dividers
```

**Example:**
```tsx
<div>
  <h1 className="text-stellar-core">Primary Heading</h1>
  <p className="text-stellar-bright">Body text goes here</p>
  <span className="text-stellar-dim">Secondary metadata</span>
  <div className="border-stellar-faint">Border element</div>
</div>
```

### T-Score Spectrum (Modal → Divergent)

The color spectrum visualizing research typicality, directly inspired by Diverga's core mission.

```css
--color-tscore-modal:      #ff3366    /* T ≥ 0.8 - Most typical/conventional */
--color-tscore-typical:    #ff8844    /* T 0.6-0.8 - Common approaches */
--color-tscore-balanced:   #ffcc22    /* T 0.4-0.6 - Balanced approaches */
--color-tscore-creative:   #44ffaa    /* T 0.2-0.4 - Creative/novel approaches */
--color-tscore-divergent:  #22ccff    /* T < 0.2 - Most divergent/rare */
```

**Visual Progression:**
```
Red (Modal)          Yellow          Green (Creative)          Cyan (Divergent)
Predictable    →    Typical    →    Creative         →       Novel/Rare
Mode Collapse  →    Common     →    Off-beaten Path  →       Long Tail
```

**CSS Classes:**
```css
.tscore-text-modal      { color: var(--color-tscore-modal); }
.tscore-text-typical    { color: var(--color-tscore-typical); }
.tscore-text-balanced   { color: var(--color-tscore-balanced); }
.tscore-text-creative   { color: var(--color-tscore-creative); }
.tscore-text-divergent  { color: var(--color-tscore-divergent); }

.tscore-bg-modal        { background-color: var(--color-tscore-modal); }
.tscore-bg-typical      { background-color: var(--color-tscore-typical); }
.tscore-bg-balanced     { background-color: var(--color-tscore-balanced); }
.tscore-bg-creative     { background-color: var(--color-tscore-creative); }
.tscore-bg-divergent    { background-color: var(--color-tscore-divergent); }
```

**T-Score Gradient:**
```css
.tscore-gradient {
  background: linear-gradient(90deg,
    var(--color-tscore-divergent) 0%,     /* Cyan */
    var(--color-tscore-creative) 25%,      /* Green */
    var(--color-tscore-balanced) 50%,      /* Yellow */
    var(--color-tscore-typical) 75%,       /* Orange */
    var(--color-tscore-modal) 100%         /* Red */
  );
}
```

**Example - T-Score Indicator Component:**
```tsx
function TScoreDisplay({ score }: { score: number }) {
  const getColor = (s: number) => {
    if (s >= 0.8) return '#ff3366';  // modal
    if (s >= 0.6) return '#ff8844';  // typical
    if (s >= 0.4) return '#ffcc22';  // balanced
    if (s >= 0.2) return '#44ffaa';  // creative
    return '#22ccff';                // divergent
  };

  return (
    <div className="flex items-center gap-2 px-4 py-2 bg-void-surface border border-stellar-faint/20">
      <div
        className="w-2 h-2 rounded-full"
        style={{ backgroundColor: getColor(score) }}
      />
      <span className="text-stellar-dim font-mono uppercase text-micro">
        T-{score.toFixed(2)}
      </span>
    </div>
  );
}
```

### Category Colors (Agents A-H)

Each research agent category gets a vibrant color for quick visual identification.

```css
--color-category-a: #ff6b6b    /* Research Design (A1-A4) - Coral Red */
--color-category-b: #ffd93d    /* Literature Review (B1-B4) - Gold */
--color-category-c: #6bcb77    /* Methodology (C1-C4) - Emerald Green */
--color-category-d: #4d96ff    /* Analysis (D1-D4) - Sapphire Blue */
--color-category-e: #9b59b6    /* Quality Control (E1-E4) - Amethyst Purple */
--color-category-f: #e17055    /* Writing & Communication (F1-F4) - Copper */
--color-category-g: #00cec9    /* Publication (G1-G4) - Teal */
--color-category-h: #fd79a8    /* Meta-Research (H1-H4) - Rose */
```

**CSS Classes:**
```css
.category-text-a { color: var(--color-category-a); }
.category-text-b { color: var(--color-category-b); }
.category-text-c { color: var(--color-category-c); }
.category-text-d { color: var(--color-category-d); }
.category-text-e { color: var(--color-category-e); }
.category-text-f { color: var(--color-category-f); }
.category-text-g { color: var(--color-category-g); }
.category-text-h { color: var(--color-category-h); }

/* Backgrounds with 15% opacity for subtle backgrounds */
.category-bg-a { background-color: rgba(255, 107, 107, 0.15); }
.category-bg-b { background-color: rgba(255, 217, 61, 0.15); }
.category-bg-c { background-color: rgba(107, 203, 119, 0.15); }
.category-bg-d { background-color: rgba(77, 150, 255, 0.15); }
.category-bg-e { background-color: rgba(155, 89, 182, 0.15); }
.category-bg-f { background-color: rgba(225, 112, 85, 0.15); }
.category-bg-g { background-color: rgba(0, 206, 201, 0.15); }
.category-bg-h { background-color: rgba(253, 121, 168, 0.15); }
```

**Example - Agent Category Badge:**
```tsx
function AgentCategoryBadge({ category, agentName }: { category: string; agentName: string }) {
  const categoryColors: Record<string, string> = {
    a: 'category-text-a', b: 'category-text-b', c: 'category-text-c',
    d: 'category-text-d', e: 'category-text-e', f: 'category-text-f',
    g: 'category-text-g', h: 'category-text-h',
  };

  return (
    <div className={`category-bg-${category} border border-stellar-faint/20 px-3 py-1`}>
      <span className={`font-mono text-micro uppercase tracking-widest ${categoryColors[category]}`}>
        {category.toUpperCase()} — {agentName}
      </span>
    </div>
  );
}
```

### Checkpoint Status Colors

Status indicators for research workflow checkpoints.

```css
--color-checkpoint-required:    #ff3366    /* Must approve before proceeding */
--color-checkpoint-recommended: #ff8844    /* Good to review */
--color-checkpoint-optional:    #ffcc22    /* Nice to have */
--color-checkpoint-complete:    #44ffaa    /* Finished successfully */
```

**Usage Pattern:**
```tsx
<div className="flex items-center gap-2">
  <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#ff3366' }} />
  <span className="text-stellar-core font-mono uppercase text-micro">
    REQUIRED CHECKPOINT
  </span>
</div>
```

### Tier Badge Colors

Model tier identification for agent configurations.

```css
--color-tier-opus:   #9b59b6    /* Advanced reasoning - Purple */
--color-tier-sonnet: #4d96ff    /* Standard processing - Blue */
--color-tier-haiku:  #8888aa    /* Efficient operation - Slate */
```

**Example:**
```tsx
<span className="px-2 py-1 bg-void-surface border border-tier-sonnet/30 text-tier-sonnet font-mono text-micro">
  SONNET
</span>
```

---

## Typography

### Font Families

```css
font-family: 'IBM Plex Sans', 'Pretendard', system-ui, sans-serif
font-display: 'Space Mono', 'JetBrains Mono', monospace
font-mono: 'JetBrains Mono', 'Fira Code', monospace
```

**Purpose:**
- **IBM Plex Sans / Pretendard**: Primary body text, multilingual support (English & Korean)
- **Space Mono**: Headlines, display text, labels—monospace gives technical authority
- **JetBrains Mono**: Code, terminal, technical content—excellent ligatures and readability

### Font Size Scale

Responsive font sizes using `clamp()` for fluid scaling.

```css
.display-xl     clamp(3rem, 8vw, 7rem)     /* Extra large display */
.display        clamp(2.5rem, 6vw, 5rem)   /* Large display */
.heading-1      clamp(2rem, 4vw, 3.5rem)   /* Main heading */
.heading-2      clamp(1.5rem, 3vw, 2.5rem) /* Secondary heading */
.heading-3      clamp(1.25rem, 2vw, 1.75rem) /* Tertiary heading */
.body-lg        1.125rem                    /* Large body */
.body           1rem                        /* Primary body */
.caption        0.875rem                    /* Captions */
.micro          0.75rem                     /* Small labels */
```

**Practical Classes:**

```tsx
{/* Display Sizes */}
<h1 className="text-display-xl">Extra Large Title</h1>
<h1 className="text-display">Page Title</h1>

{/* Heading Sizes */}
<h2 className="text-heading-1">Section Heading</h2>
<h3 className="text-heading-2">Subsection</h3>
<h4 className="text-heading-3">Sub-subsection</h4>

{/* Body Text */}
<p className="text-body-lg">Introductory paragraph with more emphasis</p>
<p className="text-body">Standard paragraph text</p>
<span className="text-caption">Caption or footnote</span>
<label className="text-micro">Label or badge</label>
```

### Heading Styles

Custom heading classes for consistent typography:

```css
.void-display {
  font-size: clamp(3rem, 8vw, 7rem);
  line-height: 0.95;
  letter-spacing: -0.03em;
  font-weight: 700;
  font-family: 'Space Mono', monospace;
}

.void-heading-1 {
  font-size: clamp(2rem, 5vw, 3.5rem);
  line-height: 1.1;
  letter-spacing: -0.02em;
  font-family: 'Space Mono', monospace;
  font-weight: 700;
}

.void-heading-2 {
  font-size: clamp(1.5rem, 3vw, 2.5rem);
  line-height: 1.2;
  letter-spacing: -0.02em;
  font-family: 'Space Mono', monospace;
  font-weight: 700;
}

.void-heading-3 {
  font-size: clamp(1.25rem, 2vw, 1.75rem);
  line-height: 1.3;
  font-family: 'Space Mono', monospace;
  font-weight: 700;
}

.void-body {
  font-family: 'IBM Plex Sans', system-ui, sans-serif;
  line-height: 1.7;
  letter-spacing: 0;
}

.void-label {
  font-family: 'Space Mono', monospace;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--foreground-muted);
}

.void-mono {
  font-family: 'JetBrains Mono', monospace;
}
```

### Example - Complete Typography Section

```tsx
export function TypographyExample() {
  return (
    <div className="space-y-8 bg-void-deep p-8 text-stellar-core">
      {/* Display */}
      <h1 className="void-display">Display Title</h1>

      {/* Heading 1 */}
      <section>
        <h2 className="void-heading-1 mb-4">Section Heading</h2>
        <p className="void-body text-stellar-bright max-w-2xl">
          This is body text using IBM Plex Sans for readability. It maintains
          excellent line-height for comfortable reading across all screen sizes.
        </p>
      </section>

      {/* Heading 2 */}
      <section>
        <h3 className="void-heading-2 mb-3">Subsection</h3>
        <p className="void-body text-stellar-dim">
          This paragraph uses stellar-dim for secondary emphasis.
        </p>
      </section>

      {/* Heading 3 with Label */}
      <section>
        <div className="flex items-center gap-3 mb-2">
          <h4 className="void-heading-3">Details</h4>
          <span className="void-label">Important</span>
        </div>
        <p className="void-body text-stellar-faint">
          Tertiary text for supporting information.
        </p>
      </section>

      {/* Monospace */}
      <code className="void-mono bg-void-elevated p-4 block text-caption">
        const example = "code block with monospace font";
      </code>
    </div>
  );
}
```

---

## Spacing & Layout

### Spacing Scale

Tailwind default spacing (0.25rem increments) is used throughout. Key values:

```css
p-2     0.5rem     (8px)   - Tight spacing
p-4     1rem       (16px)  - Default padding
p-6     1.5rem     (24px)  - Comfortable spacing
p-8     2rem       (32px)  - Section padding
p-12    3rem       (48px)  - Large section spacing
```

### Section Padding Patterns

**Standard page sections:**
```tsx
<section className="px-6 py-12 max-w-7xl mx-auto">
  {/* Content */}
</section>
```

**Card spacing:**
```tsx
<div className="void-card p-6">
  {/* Card content with consistent padding */}
</div>
```

**Hero sections:**
```tsx
<div className="min-h-screen px-6 py-20 flex items-center justify-center">
  {/* Hero content */}
</div>
```

### Container Max-Widths

```css
max-w-2xl    28rem       /* Optimal reading width */
max-w-4xl    56rem       /* Two-column layout */
max-w-6xl    64rem       /* Standard page width */
max-w-7xl    80rem       /* Wide page width */
```

**Usage:**
```tsx
{/* Narrow, readable content */}
<article className="max-w-2xl mx-auto px-6 py-12">
  {/* Article content */}
</article>

{/* Component grid */}
<div className="max-w-6xl mx-auto px-6 py-12">
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {/* Cards */}
  </div>
</div>
```

### Grid Patterns

**Two-column responsive:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-6 px-6">
  <div>{/* Left column */}</div>
  <div>{/* Right column */}</div>
</div>
```

**Three-column responsive:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 px-6">
  <div>{/* Column 1 */}</div>
  <div>{/* Column 2 */}</div>
  <div>{/* Column 3 */}</div>
</div>
```

**Agent category grid (4 columns on desktop):**
```tsx
<div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
  {/* 8 agent category cards (A-H) */}
</div>
```

---

## Components Reference

### Buttons

#### void-btn (Base Button Style)

```css
.void-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: 'Space Mono', monospace;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0.75rem 1.5rem;
  border: 1px solid;
  transition: all 0.2s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
```

#### void-btn-primary

```css
.void-btn-primary {
  background: transparent;
  border-color: rgba(240, 240, 245, 0.2);
  color: var(--color-stellar-core);
}

.void-btn-primary::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--color-stellar-core);
  opacity: 0;
  transform: translateX(-100%);
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.void-btn-primary:hover::before {
  transform: translateX(0);
  opacity: 0.1;
}

.void-btn-primary:hover {
  border-color: rgba(240, 240, 245, 0.5);
}
```

**Usage:**
```tsx
<button className="void-btn void-btn-primary">
  Primary Button
</button>

<a href="/docs" className="void-btn void-btn-primary inline-flex">
  <span>Learn More</span>
  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
  </svg>
</a>
```

#### void-btn-accent

```css
.void-btn-accent {
  background: var(--color-tscore-creative);  /* Green #44ffaa */
  border-color: var(--color-tscore-creative);
  color: var(--color-void-deep);
}

.void-btn-accent:hover {
  box-shadow: 0 0 20px rgba(68, 255, 170, 0.4);
}
```

**Usage:**
```tsx
<button className="void-btn void-btn-accent">
  Start Diverging
</button>
```

#### void-btn-ghost

```css
.void-btn-ghost {
  background: transparent;
  border-color: var(--color-stellar-faint);
  color: var(--color-stellar-faint);
}

.void-btn-ghost:hover {
  border-color: var(--color-stellar-dim);
  color: var(--color-stellar-dim);
}
```

**Usage:**
```tsx
<button className="void-btn void-btn-ghost">
  Explore Agents
</button>
```

### Cards

#### void-card

```css
.void-card {
  background: var(--card);  /* void-elevated */
  border: 1px solid var(--card-border);  /* stellar-faint/10 */
  transition: all 0.3s ease;
}

.void-card:hover {
  border-color: rgba(136, 136, 170, 0.25);
  box-shadow: var(--shadow-glow-sm);
}
```

**Usage:**
```tsx
<div className="void-card p-6">
  <h3 className="void-heading-3 text-stellar-core mb-2">Card Title</h3>
  <p className="text-stellar-dim mb-4">Card description goes here.</p>
  <button className="void-btn void-btn-primary">Action</button>
</div>
```

#### void-card-interactive

```css
.void-card-interactive {
  background: var(--card);
  border: 1px solid var(--card-border);
  cursor: pointer;
  transition: all 0.3s ease;
}

.void-card-interactive:hover {
  border-color: var(--color-tscore-creative);
  box-shadow: var(--shadow-glow);
  transform: translateY(-2px);
}
```

**Usage:**
```tsx
<div
  className="void-card-interactive p-6 cursor-pointer"
  onClick={() => navigateToAgent(agentId)}
>
  <div className="flex items-start justify-between mb-3">
    <h3 className="void-heading-3">A2 — Hypothesis Architect</h3>
    <span className="category-text-a font-mono text-micro">A</span>
  </div>
  <p className="text-stellar-dim text-body">Designs testable hypotheses...</p>
</div>
```

### Navigation

#### void-nav

```css
.void-nav {
  background: rgba(5, 5, 8, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}
```

#### void-nav-link

```css
.void-nav-link {
  font-family: 'Space Mono', monospace;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-stellar-dim);
  transition: color 0.2s ease;
  position: relative;
}

.void-nav-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: var(--color-stellar-core);
  transition: width 0.2s ease;
}

.void-nav-link:hover {
  color: var(--color-stellar-core);
}

.void-nav-link:hover::after {
  width: 100%;
}
```

**Example Navigation:**
```tsx
<nav className="void-nav sticky top-0 z-40">
  <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
    <h1 className="text-stellar-core font-display font-bold text-lg">DIVERGA</h1>
    <div className="flex items-center gap-8">
      <a href="/docs" className="void-nav-link">Documentation</a>
      <a href="/agents" className="void-nav-link">Agents</a>
      <a href="/playground" className="void-nav-link">Playground</a>
    </div>
  </div>
</nav>
```

### Terminal / CLI Component

#### void-terminal

```css
.void-terminal {
  background: var(--color-void-absolute);
  border: 1px solid var(--border);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  overflow: hidden;
}

.void-terminal-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border);
  background: var(--color-void-surface);
}

.void-terminal-dot {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
}

.void-terminal-dot-red    { background: #ff5f56; }
.void-terminal-dot-yellow { background: #ffbd2e; }
.void-terminal-dot-green  { background: #27c93f; }

.void-terminal-content {
  padding: 1rem;
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
}

.void-terminal-prompt {
  color: var(--color-tscore-creative);  /* Green $ */
}

.void-terminal-cursor {
  display: inline-block;
  width: 0.5rem;
  height: 1.25rem;
  background: var(--color-stellar-core);
  animation: cursorBlink 1s step-end infinite;
}
```

**Example Usage:**
```tsx
<InteractiveCLI
  height={400}
  initialCommands={['help', 'diverga init']}
/>
```

See `InteractiveCLI.tsx` for full implementation with command handling and history.

### Badges

#### void-badge

```css
.void-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.75rem;
  font-family: 'Space Mono', monospace;
  font-size: 0.6875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid;
  backdrop-filter: blur(4px);
}

.void-badge-tscore {
  border-color: rgba(136, 136, 170, 0.2);
  background: rgba(10, 10, 15, 0.8);
}
```

**Example:**
```tsx
<span className="void-badge void-badge-tscore">
  <span className="inline-block w-1.5 h-1.5 rounded-full" style={{ backgroundColor: '#44ffaa' }} />
  T-Score Creative
</span>
```

### Dividers

#### void-divider (Simple)

```css
.void-divider {
  height: 1px;
  background: var(--border);
}
```

#### void-divider-glow (With Gradient)

```css
.void-divider-glow {
  height: 1px;
  background: linear-gradient(90deg,
    transparent,
    var(--color-stellar-faint),
    transparent
  );
}
```

**Usage:**
```tsx
<div className="py-8">
  <div className="void-divider-glow" />
</div>
```

### Visualization Containers

#### T-Score Spectrum

Used for displaying research approach distribution:

```tsx
<div className="void-card p-6">
  <h3 className="void-heading-3 mb-6">Theoretical Framework Distribution</h3>
  <TScoreSpectrum
    data={frameworkData}
    locale="en"
    showLabels={true}
    height="lg"
  />
</div>
```

See `TScoreSpectrum.tsx` for implementation details.

#### Particle Canvas (Hero Section)

Used for hero sections with interactive particle animations:

```tsx
<VoidHero />
```

See `VoidHero.tsx` for full particle system implementation.

---

## Animation Patterns

### Tailwind Animations

```css
animation-fade-in       /* 0.5s, ease-out */
animation-slide-up      /* 0.6s, cubic-bezier */
animation-glow-pulse    /* 3s, infinite, ease-in-out */
animation-cursor-blink  /* 1s, step-end, infinite */
```

### Framer Motion Patterns

#### Fade In + Slide Up (Standard Entry)

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
>
  Content enters with fade and slide
</motion.div>
```

#### Staggered Children (List Items)

```tsx
<motion.div
  initial="hidden"
  animate="visible"
  variants={{
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  }}
>
  {items.map((item, i) => (
    <motion.div
      key={i}
      variants={{
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 },
      }}
    >
      {item}
    </motion.div>
  ))}
</motion.div>
```

#### Scroll-Triggered Animations

```tsx
import { useScroll, useTransform } from 'framer-motion';

export function ScrollExample() {
  const { scrollYProgress } = useScroll();

  const opacity = useTransform(scrollYProgress, [0, 0.25], [1, 0]);
  const y = useTransform(scrollYProgress, [0, 0.25], [0, -80]);

  return (
    <motion.div style={{ opacity, y }}>
      Fades and slides as you scroll
    </motion.div>
  );
}
```

#### Hover Scale + Glow

```tsx
<motion.div
  whileHover={{ scale: 1.05 }}
  className="void-card cursor-pointer"
  onHoverStart={() => /* glow effect */}
>
  Interactive card
</motion.div>
```

#### Tap Animation (Mobile-Friendly)

```tsx
<motion.button
  className="void-btn void-btn-accent"
  whileTap={{ scale: 0.95 }}
>
  Press me
</motion.button>
```

### Box Shadows & Glow Effects

```css
--shadow-glow-sm  0 0 10px rgba(68, 255, 170, 0.1)
--shadow-glow     0 0 20px rgba(68, 255, 170, 0.15)
--shadow-glow-lg  0 0 40px rgba(68, 255, 170, 0.2)
--shadow-glow-xl  0 0 60px rgba(68, 255, 170, 0.25)
```

**Usage:**
```tsx
<div className="void-glow">Subtle glow effect</div>
<div className="void-glow-lg">Stronger glow</div>
```

**Text Glow:**
```tsx
<span className="void-text-glow text-tscore-divergent">
  Glowing text effect
</span>
```

---

## Code Examples

### Example 1: Hero Section with T-Score Indicator

```tsx
import { motion } from 'framer-motion';
import { useLocale } from 'next-intl';
import { VoidHero } from '@/components/home/VoidHero';

export default function HeroPage() {
  const locale = useLocale();

  return (
    <div className="relative">
      {/* Particle background */}
      <VoidHero />

      {/* T-Score indicator overlay */}
      <div className="absolute bottom-16 left-1/2 -translate-x-1/2 z-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="flex items-center gap-3 border border-stellar-faint/20 bg-void-surface/50 px-4 py-2 backdrop-blur-sm"
        >
          <div className="h-2 w-2 rounded-full bg-tscore-creative" />
          <span className="font-mono text-micro uppercase tracking-widest text-stellar-faint">
            {locale === 'ko' ? 'Void Cartography' : 'Void Cartography'}
          </span>
          <span className="font-mono text-sm text-stellar-dim">T-0.42</span>
        </motion.div>
      </div>
    </div>
  );
}
```

### Example 2: Agent Card with Category Color

```tsx
import Link from 'next/link';
import { motion } from 'framer-motion';

interface Agent {
  id: string;
  category: string;
  name: string;
  description: string;
  tScore: number;
}

export function AgentCard({ agent, locale }: { agent: Agent; locale: string }) {
  const categoryClasses: Record<string, string> = {
    a: 'category-bg-a category-text-a',
    b: 'category-bg-b category-text-b',
    c: 'category-bg-c category-text-c',
    d: 'category-bg-d category-text-d',
    e: 'category-bg-e category-text-e',
    f: 'category-bg-f category-text-f',
    g: 'category-bg-g category-text-g',
    h: 'category-bg-h category-text-h',
  };

  const getTScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-tscore-modal';
    if (score >= 0.6) return 'text-tscore-typical';
    if (score >= 0.4) return 'text-tscore-balanced';
    if (score >= 0.2) return 'text-tscore-creative';
    return 'text-tscore-divergent';
  };

  return (
    <Link href={`/${locale}/agents/${agent.id}`}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        whileHover={{ y: -4 }}
        className="void-card-interactive group p-6"
      >
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <div>
            <h3 className="void-heading-3 text-stellar-core group-hover:text-stellar-bright transition-colors">
              {agent.name}
            </h3>
            <p className="text-caption text-stellar-faint mt-1">
              Agent {agent.id}
            </p>
          </div>

          {/* Category Badge */}
          <div
            className={`void-badge ${categoryClasses[agent.category]} flex-shrink-0`}
          >
            {agent.category.toUpperCase()}
          </div>
        </div>

        {/* Description */}
        <p className="text-body text-stellar-dim mb-4 line-clamp-2">
          {agent.description}
        </p>

        {/* Footer with T-Score */}
        <div className="flex items-center justify-between pt-4 border-t border-stellar-faint/10">
          <span className="text-micro text-stellar-faint">Research Design</span>
          <span className={`font-mono text-micro ${getTScoreColor(agent.tScore)}`}>
            T-{agent.tScore.toFixed(2)}
          </span>
        </div>
      </motion.div>
    </Link>
  );
}
```

### Example 3: Information Card Section

```tsx
import { motion } from 'framer-motion';
import { useLocale } from 'next-intl';

const features = [
  {
    label: '27 Agents',
    labelKo: '27개 에이전트',
    description: 'Specialized research orchestration',
    descriptionKo: '전문화된 연구 오케스트레이션',
    icon: '◆',
  },
  {
    label: 'VS Methodology',
    labelKo: 'VS 방법론',
    description: 'Escape mode collapse through diversity',
    descriptionKo: '다양성을 통한 모드 붕괴 탈출',
    icon: '◇',
  },
  {
    label: 'T-Score Awareness',
    labelKo: 'T-Score 인식',
    description: 'Typicality-aware research design',
    descriptionKo: '전형성 인식 연구 설계',
    icon: '◈',
  },
];

export function FeaturesSection() {
  const locale = useLocale();

  return (
    <section className="px-6 py-16 bg-void-deep">
      <div className="max-w-6xl mx-auto">
        {/* Section Title */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mb-12"
        >
          <h2 className="void-heading-1 text-stellar-core mb-4">
            {locale === 'ko' ? 'Diverga의 핵심' : 'Core of Diverga'}
          </h2>
          <p className="text-body-lg text-stellar-dim max-w-2xl">
            {locale === 'ko'
              ? 'AI 기반 체계적 문헌 고찰 자동화'
              : 'AI-powered systematic literature review automation'
            }
          </p>
        </motion.div>

        {/* Feature Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="void-card group p-6 hover:border-tscore-creative/50 transition-colors"
            >
              {/* Icon */}
              <div className="text-3xl text-tscore-creative mb-4 group-hover:animate-glow-pulse">
                {feature.icon}
              </div>

              {/* Content */}
              <h3 className="void-heading-3 text-stellar-core mb-2">
                {locale === 'ko' ? feature.labelKo : feature.label}
              </h3>
              <p className="text-body text-stellar-dim">
                {locale === 'ko' ? feature.descriptionKo : feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

### Example 4: Visualization Container with T-Score Spectrum

```tsx
import { TScoreSpectrum } from '@/components/visualization/TScoreSpectrum';
import { motion } from 'framer-motion';
import { useLocale } from 'next-intl';

interface Framework {
  label: string;
  labelKo: string;
  score: number;
  description: string;
  descriptionKo: string;
}

const frameworks: Framework[] = [
  {
    label: 'TAM',
    labelKo: 'TAM',
    score: 0.92,
    description: 'Most commonly recommended theoretical framework',
    descriptionKo: '가장 일반적으로 추천되는 이론적 프레임워크',
  },
  {
    label: 'Hybrid',
    labelKo: '하이브리드',
    score: 0.55,
    description: 'Custom combinations of established theories',
    descriptionKo: '확립된 이론의 맞춤형 조합',
  },
  {
    label: 'Novel',
    labelKo: '새로운 이론',
    score: 0.18,
    description: 'Innovative theoretical combinations',
    descriptionKo: '혁신적인 이론적 조합',
  },
];

export function TheoreticalFrameworkSection() {
  const locale = useLocale();

  return (
    <section className="px-6 py-16 bg-void-surface/30">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mb-8"
        >
          <h2 className="void-heading-2 text-stellar-core mb-2">
            {locale === 'ko'
              ? '이론적 프레임워크 분포'
              : 'Theoretical Framework Distribution'
            }
          </h2>
          <p className="text-body text-stellar-dim">
            {locale === 'ko'
              ? 'T-Score 스펙트럼에 따른 접근법의 다양성'
              : 'Diversity of approaches across the T-Score spectrum'
            }
          </p>
        </motion.div>

        {/* T-Score Visualization */}
        <div className="void-card p-8">
          <TScoreSpectrum
            data={frameworks}
            locale={locale}
            showLabels={true}
            height="lg"
          />
        </div>

        {/* Interpretation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          {[
            {
              title: locale === 'ko' ? '모달' : 'Modal',
              description:
                locale === 'ko'
                  ? '가장 전형적인 선택지'
                  : 'Most typical choices',
              color: 'text-tscore-modal',
            },
            {
              title: locale === 'ko' ? '균형' : 'Balanced',
              description:
                locale === 'ko'
                  ? '창의성과 신뢰성의 균형'
                  : 'Balance creativity and reliability',
              color: 'text-tscore-balanced',
            },
            {
              title: locale === 'ko' ? '발산적' : 'Divergent',
              description:
                locale === 'ko'
                  ? '혁신적인 새로운 접근'
                  : 'Innovative novel approaches',
              color: 'text-tscore-divergent',
            },
          ].map((item, i) => (
            <div key={i} className="void-card p-4">
              <h4 className={`void-heading-3 ${item.color} mb-2`}>
                {item.title}
              </h4>
              <p className="text-caption text-stellar-dim">{item.description}</p>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
```

### Example 5: Interactive CLI Component

```tsx
import { InteractiveCLI } from '@/components/cli/InteractiveCLI';

export function CLIPlayground() {
  return (
    <section className="px-6 py-12 bg-void-deep">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h2 className="void-heading-2 text-stellar-core mb-2">
            Interactive CLI Demo
          </h2>
          <p className="text-body text-stellar-dim">
            Try Diverga commands in the terminal below
          </p>
        </div>

        <InteractiveCLI
          height={400}
          initialCommands={['help']}
        />

        <p className="mt-4 text-caption text-stellar-faint">
          Type commands like: help, diverga init, diverga agents, diverga run a2
        </p>
      </div>
    </section>
  );
}
```

---

## Bilingual Support

### Content Structure Pattern

All components support English and Korean using `next-intl`:

```tsx
import { useLocale } from 'next-intl';

export function BilingualComponent() {
  const locale = useLocale();  // 'en' or 'ko'

  return (
    <div>
      <h1 className="void-heading-1 text-stellar-core">
        {locale === 'ko' ? '한국어 제목' : 'English Heading'}
      </h1>
      <p className="text-body text-stellar-bright">
        {locale === 'ko'
          ? '한국어 본문 텍스트가 여기 옵니다.'
          : 'English body text goes here.'
        }
      </p>
    </div>
  );
}
```

### Data Structure Pattern

For data-driven content, use parallel structures:

```tsx
const agentData = {
  a1: {
    name: 'Research Question Designer',
    nameKo: '연구 질문 설계자',
    description: 'Designs clear, answerable research questions',
    descriptionKo: '명확하고 답할 수 있는 연구 질문 설계',
    category: 'a',
    tScore: 0.35,
  },
};

export function AgentProfile() {
  const locale = useLocale();
  const agent = agentData.a1;

  return (
    <div>
      <h1 className="void-heading-1">
        {locale === 'ko' ? agent.nameKo : agent.name}
      </h1>
      <p className="text-body">
        {locale === 'ko' ? agent.descriptionKo : agent.description}
      </p>
    </div>
  );
}
```

### Language Toggle Pattern

Standard language toggle button:

```tsx
import Link from 'next/link';
import { useLocale } from 'next-intl';

export function LanguageToggle() {
  const locale = useLocale();
  const otherLocale = locale === 'en' ? 'ko' : 'en';

  return (
    <Link
      href={`/${otherLocale}${usePathname().replace(/^\/[a-z]{2}/, '')}`}
      className="void-btn void-btn-ghost text-xs"
    >
      {otherLocale.toUpperCase()}
    </Link>
  );
}
```

---

## Accessibility

### Semantic HTML

Always use proper semantic elements:

```tsx
{/* Good */}
<header className="void-nav">Navigation</header>
<main className="px-6 py-12">Primary content</main>
<aside className="void-card">Secondary content</aside>
<footer className="bg-void-surface">Footer</footer>

{/* Avoid */}
<div className="void-nav">Navigation</div>  {/* ❌ Not semantic */}
<div>Primary content</div>  {/* ❌ Should be <main> */}
```

### Color Contrast

All text meets WCAG AA standards (minimum 4.5:1 for normal text):

- `stellar-core` (#ffffff) on `void-deep` (#050508): 21:1 ✓
- `stellar-dim` (#8888aa) on `void-deep` (#050508): 4.7:1 ✓
- `tscore-creative` (#44ffaa) on `void-deep` (#050508): 6.1:1 ✓

### Focus States

Always include visible focus indicators:

```css
.void-btn:focus-visible {
  outline: 2px solid var(--color-stellar-core);
  outline-offset: 2px;
}

.void-nav-link:focus-visible {
  outline: 2px solid var(--color-stellar-core);
  outline-offset: 2px;
}
```

### Motion & Animation

Respect user preferences for reduced motion:

```tsx
import { useReducedMotion } from 'framer-motion';

export function AnimatedComponent() {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      animate={{ y: 0 }}
      transition={shouldReduceMotion ? { duration: 0 } : { duration: 0.6 }}
    >
      Respects prefers-reduced-motion
    </motion.div>
  );
}
```

### Alt Text for Icons

Always provide context for visual elements:

```tsx
<svg
  className="w-4 h-4"
  aria-label="Arrow pointing right"
  fill="none"
  viewBox="0 0 24 24"
  stroke="currentColor"
>
  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
</svg>
```

---

## Implementation Checklist

When building new pages/components:

- [ ] Use semantic HTML (`<header>`, `<main>`, `<section>`, `<article>`, `<footer>`)
- [ ] Apply color from void core, stellar, or tscore palettes only
- [ ] Use void-card or void-card-interactive for containers
- [ ] Use void-btn-primary, void-btn-accent, or void-btn-ghost for buttons
- [ ] Include proper typography hierarchy (heading-1, heading-2, heading-3)
- [ ] Add bilingual support with `useLocale()` for all text
- [ ] Implement animations with Framer Motion (not CSS alone)
- [ ] Test focus states with keyboard navigation
- [ ] Check color contrast with WCAG tools
- [ ] Add proper spacing with px-6, py-12, gap-6 etc.
- [ ] Use max-w-6xl for page width and center with mx-auto

---

## Resources

- **Tailwind Config**: `/tailwind.config.ts`
- **Global Styles**: `/src/styles/globals.css`
- **Component Examples**:
  - Hero with Particles: `/src/components/home/VoidHero.tsx`
  - T-Score Spectrum: `/src/components/visualization/TScoreSpectrum.tsx`
  - Interactive CLI: `/src/components/cli/InteractiveCLI.tsx`
  - Agent Cards: `/src/components/agents/AgentCard.tsx`
- **Localization**: Uses `next-intl` via `/src/app/[locale]/layout.tsx`
