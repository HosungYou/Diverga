# Checkpoint Timeline Feature

## Overview

An engaging, interactive timeline visualization that shows where critical checkpoints occur in research workflows.

## Design Aesthetic

**Direction**: Neo-brutalist meets academic sophistication
- **Color Strategy**: Checkpoint-aware color coding (red = REQUIRED, amber = RECOMMENDED, teal = OPTIONAL)
- **Motion**: Staggered reveals with hover interactions and glow effects
- **Typography**: JetBrains Mono for technical IDs, Pretendard for descriptions
- **Composition**: Vertical timeline with expandable checkpoint cards

## Files Created

### 1. `/src/lib/data/workflows.ts`
**Purpose**: Centralized workflow definitions with checkpoint mappings

**Key Features**:
- 4 complete workflows (Quantitative, Qualitative, Mixed Methods, Meta-Analysis)
- Each workflow has:
  - Stage-by-stage agent assignments
  - Bilingual descriptions (EN/KO)
  - Checkpoint IDs for validation gates
  - Estimated completion time
- `checkpointInfo` mapping with human-readable names and descriptions

**Example Workflow Structure**:
```typescript
{
  id: 'quantitative',
  slug: 'quantitative',
  paradigm: 'quantitative',
  estimatedTime: '8-12 weeks',
  stages: [
    {
      agent: 'A1',
      description: { en: '...', ko: '...' },
      checkpoint: 'CP_RESEARCH_DIRECTION' // REQUIRED checkpoint
    },
    // ... more stages
  ]
}
```

### 2. `/src/components/CheckpointTimeline.tsx`
**Purpose**: Reusable timeline component with checkpoint visualization

**Visual Features**:
- **Checkpoint Indicators**:
  - 🔴 REQUIRED: Red border, red glow on hover
  - 🟠 RECOMMENDED: Amber border, amber glow
  - 🟢 OPTIONAL: Teal border, subtle glow
- **Interactive Elements**:
  - Click stage to expand checkpoint details
  - Hover for scale animation and shadow
  - Animated stage number badges
- **Timeline Design**:
  - Vertical gradient line connecting stages
  - Color-coded checkpoint markers
  - Expandable cards with checkpoint metadata

**Component Props**:
```typescript
{
  stages: WorkflowStage[];
  locale: 'en' | 'ko';
}
```

### 3. `/src/app/[locale]/workflows/[slug]/page.tsx`
**Purpose**: Workflow detail page with integrated timeline

**Features**:
- Workflow metadata display (estimated time, checkpoint count)
- Full checkpoint timeline visualization
- Breadcrumb navigation
- 404 handling for invalid workflow slugs

### 4. `/src/app/[locale]/workflows/page.tsx`
**Purpose**: Updated workflows listing with checkpoint counts

**Enhancements**:
- Display checkpoint count per workflow
- Show first 6 agent IDs with "+N" overflow
- Stage count metadata
- Enhanced color coding per workflow type

## Checkpoint Levels

### REQUIRED (Red)
Critical validation gates that **must** be completed before proceeding.

Examples:
- `CP_RESEARCH_DIRECTION`: Research question clarity
- `CP_METHODOLOGY_APPROVAL`: IRB and design approval
- `CP_META_GATE`: Meta-analysis validation

### RECOMMENDED (Amber)
Best practice checkpoints that **should** be completed for rigor.

Examples:
- `CP_ANALYSIS_PLAN`: Preregistration of analysis
- `CP_INTEGRATION_STRATEGY`: Mixed methods integration check

### OPTIONAL (Teal)
Helpful checkpoints for enhanced quality.

Examples:
- `CP_VISUALIZATION_PREFERENCE`: Visual style configuration

## User Interaction Flow

1. **Browse Workflows** (`/workflows`)
   - See all 4 research paradigm workflows
   - View checkpoint counts at a glance
   - Click "View Timeline" to see details

2. **Explore Timeline** (`/workflows/{slug}`)
   - Read workflow overview and metadata
   - View complete stage-by-stage timeline
   - Click any stage to expand checkpoint details

3. **Expand Checkpoint** (Timeline Interaction)
   - Click stage card → See checkpoint type (REQUIRED/RECOMMENDED/OPTIONAL)
   - Read checkpoint name and description
   - View technical checkpoint ID for reference

## Bilingual Support

All content fully localized:
- Workflow names and descriptions
- Stage descriptions
- Checkpoint names and descriptions
- UI labels (e.g., "체크포인트" vs "Checkpoint")

## Animation Details

### Stage Reveal
- Staggered entrance (50ms delay between stages)
- Slide-in from left with fade
- Scale-up on hover (1.01x)

### Checkpoint Expansion
- Smooth height animation (300ms)
- Fade-in content
- Glow effect on active checkpoints

### Timeline Line
- Gradient from diverga → teal → gold
- 30% opacity for subtlety
- Connects all stages vertically

## Color Palette

### Checkpoint Colors
```css
REQUIRED:    Red 500    (#ef4444)
RECOMMENDED: Amber 500  (#f59e0b)
OPTIONAL:    Teal 500   (#14b8a6)
```

### Workflow Type Colors
```css
Quantitative:  Blue (#3b82f6)
Qualitative:   Purple (#a855f7)
Mixed Methods: Teal (#14b8a6)
Meta-Analysis: Emerald (#10b981)
```

## Technical Implementation

### Data Flow
```
workflows.ts (data)
  ↓
WorkflowDetailPage (page)
  ↓
CheckpointTimeline (component)
  ↓
checkpointInfo (metadata lookup)
```

### State Management
- Single state variable: `expandedIndex` (number | null)
- Click handler toggles expansion per stage
- No global state needed

### Responsive Design
- Mobile: Vertical timeline, full-width cards
- Desktop: Same layout (timeline is naturally vertical)
- Touch-friendly: Large click targets (48px min)

## Future Enhancements

Potential additions:
1. **Progress Tracking**: "You are here" indicator for active research projects
2. **Checkpoint History**: Log of completed checkpoints with timestamps
3. **Branching Timelines**: Show alternative paths based on decisions
4. **Collaborative Annotations**: Team notes on specific checkpoints
5. **Export Timeline**: PDF/PNG export of research plan

## Browser Compatibility

- Modern browsers (Chrome 90+, Firefox 88+, Safari 14+)
- Requires JavaScript enabled
- CSS Grid and Flexbox support
- Framer Motion animations (graceful degradation)

## Accessibility

- Semantic HTML (`<button>`, proper heading hierarchy)
- Keyboard navigation (Tab/Enter to expand stages)
- ARIA labels on icons
- Color contrast meets WCAG AA standards
- Focus indicators on interactive elements

## Performance

- Minimal re-renders (memoized stage data)
- Lazy animation initialization
- No external API calls
- Static data (workflows.ts)
- Bundle size: ~15KB (gzipped)

---

**Created**: January 27, 2026
**Designer**: Claude Code (Sonnet 4.5)
**Aesthetic**: Neo-brutalist academic with checkpoint-aware interaction design
