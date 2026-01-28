/**
 * Diverga T-Score Reference
 * Typicality scores for VS methodology
 */

import type { TScoreEntry } from '../agents/types';

/**
 * T-Score ranges and their meanings
 */
export const T_SCORE_RANGES: TScoreEntry[] = [
  {
    range: [0.7, 1.0],
    label: 'Common/Modal',
    meaning: 'Highly typical, safe but limited novelty contribution',
    suitableFor: 'Replication studies, confirmatory research',
    riskLevel: 'low',
  },
  {
    range: [0.5, 0.7],
    label: 'Established',
    meaning: 'Well-established approach, needs specificity for contribution',
    suitableFor: 'Standard research, mid-tier journals',
    riskLevel: 'low',
  },
  {
    range: [0.4, 0.5],
    label: 'Moderate',
    meaning: 'Balanced risk-novelty, clear differentiation possible',
    suitableFor: 'Most academic research, good contribution potential',
    riskLevel: 'medium',
  },
  {
    range: [0.3, 0.4],
    label: 'Emerging',
    meaning: 'Novel approach, emerging in literature',
    suitableFor: 'Innovative journals, strong theoretical support needed',
    riskLevel: 'medium',
  },
  {
    range: [0.2, 0.3],
    label: 'Innovative',
    meaning: 'Novel, requires strong justification and defense',
    suitableFor: 'Top-tier journals seeking contribution',
    riskLevel: 'high',
  },
  {
    range: [0.0, 0.2],
    label: 'Experimental',
    meaning: 'Highly novel, high risk/reward, paradigm-challenging',
    suitableFor: 'Groundbreaking research, experienced researchers',
    riskLevel: 'experimental',
  },
];

/**
 * Creativity levels and their T-Score thresholds
 */
export const CREATIVITY_LEVELS = {
  Conservative: { minT: 0.5, description: 'Safe, validated approaches' },
  Balanced: { minT: 0.3, description: 'Differentiated + defensible' },
  Innovative: { minT: 0.2, description: 'High contribution potential' },
  Extreme: { minT: 0.0, description: 'Maximum creativity, paradigm-challenging' },
} as const;

export type CreativityLevel = keyof typeof CREATIVITY_LEVELS;

/**
 * Research question typicality patterns
 */
export const RQ_TYPICALITY_PATTERNS = {
  modal: [
    { pattern: 'What is the effect of [X] on [Y]?', tScore: 0.90, issue: 'Simple causation, broad scope' },
    { pattern: 'What is the relationship between [X] and [Y]?', tScore: 0.85, issue: 'Simple correlation' },
    { pattern: 'Survey on perceptions of [X]', tScore: 0.88, issue: 'Descriptive only' },
    { pattern: 'Current status and improvement of [X]', tScore: 0.92, issue: 'Practitioner report' },
  ],
  established: [
    { pattern: 'Effect of [X] on [Y] moderated by [Z]', tScore: 0.65, advantage: 'Boundary conditions' },
    { pattern: 'Mediation of [X] → [M] → [Y]', tScore: 0.60, advantage: 'Mechanism explanation' },
    { pattern: 'Effect of [X] on [Y] in [specific context]', tScore: 0.55, advantage: 'Context specificity' },
  ],
  innovative: [
    { pattern: 'Multiple mediation: [X] → [M1,M2] → [Y]', tScore: 0.40, advantage: 'Complex mechanisms' },
    { pattern: 'Moderated mediation with [Z]', tScore: 0.35, advantage: 'Conditional processes' },
    { pattern: 'Temporal dynamics of [X] → [Y]', tScore: 0.30, advantage: 'Longitudinal effects' },
  ],
  experimental: [
    { pattern: 'Paradoxical/non-linear effects of [X]', tScore: 0.22, advantage: 'Challenge assumptions' },
    { pattern: 'Reverse causality: [Y] → [X]', tScore: 0.18, advantage: 'Novel direction' },
    { pattern: 'Naming new phenomenon [Z]', tScore: 0.15, advantage: 'Paradigm contribution' },
  ],
};

/**
 * Look up T-Score entry for a given score
 */
export function lookupTScore(score: number): TScoreEntry | undefined {
  return T_SCORE_RANGES.find(entry =>
    score >= entry.range[0] && score <= entry.range[1]
  );
}

/**
 * Get label for a T-Score
 */
export function getTScoreLabel(score: number): string {
  const entry = lookupTScore(score);
  return entry ? entry.label : 'Unknown';
}

/**
 * Get risk level for a T-Score
 */
export function getTScoreRiskLevel(score: number): 'low' | 'medium' | 'high' | 'experimental' {
  const entry = lookupTScore(score);
  return entry ? entry.riskLevel : 'medium';
}

/**
 * Check if T-Score is appropriate for creativity level
 */
export function isAppropriateForCreativityLevel(
  tScore: number,
  level: CreativityLevel
): boolean {
  const threshold = CREATIVITY_LEVELS[level].minT;
  return tScore >= threshold;
}

/**
 * Get recommended creativity level for a T-Score
 */
export function getRecommendedCreativityLevel(tScore: number): CreativityLevel {
  if (tScore >= 0.5) return 'Conservative';
  if (tScore >= 0.3) return 'Balanced';
  if (tScore >= 0.2) return 'Innovative';
  return 'Extreme';
}

/**
 * Format T-Score for display
 */
export function formatTScore(score: number): string {
  const entry = lookupTScore(score);
  if (!entry) return `T=${score.toFixed(2)}`;

  const riskIcon = {
    low: '🟢',
    medium: '🟡',
    high: '🟠',
    experimental: '🔴',
  }[entry.riskLevel];

  return `T=${score.toFixed(2)} ${riskIcon} (${entry.label})`;
}

/**
 * Generate T-Score visualization bar
 */
export function visualizeTScore(score: number, width: number = 20): string {
  const filled = Math.round(score * width);
  const empty = width - filled;
  const bar = '█'.repeat(filled) + '░'.repeat(empty);

  const entry = lookupTScore(score);
  const label = entry ? entry.label : '';

  return `[${bar}] ${score.toFixed(2)} ${label}`;
}

/**
 * Get T-Score reference table as markdown
 */
export function getTScoreReferenceTable(): string {
  const rows = T_SCORE_RANGES.map(entry => {
    const riskIcon = {
      low: '🟢',
      medium: '🟡',
      high: '🟠',
      experimental: '🔴',
    }[entry.riskLevel];

    return `| ${entry.range[0].toFixed(1)}-${entry.range[1].toFixed(1)} | ${riskIcon} ${entry.label} | ${entry.meaning} | ${entry.suitableFor} |`;
  });

  return `
| T-Score Range | Label | Meaning | Suitable For |
|---------------|-------|---------|--------------|
${rows.join('\n')}
`;
}

/**
 * Get VS direction template
 */
export function getVSDirectionTemplate(
  directions: Array<{ label: string; tScore: number; description: string }>
): string {
  const formatted = directions.map((d, i) => {
    const letter = String.fromCharCode(65 + i); // A, B, C, ...
    return `**Direction ${letter}** (${formatTScore(d.tScore)}): ${d.label}
  - ${d.description}`;
  });

  return `
### VS Alternative Directions

${formatted.join('\n\n')}

---
**Please select a direction (A/B/C/...):**
`;
}

/**
 * Calculate dynamic T-Score based on context
 * This is a simplified version - real implementation would use external API
 */
export function calculateDynamicTScore(
  baseScore: number,
  context: {
    journalLevel?: 'top-tier' | 'mid-tier' | 'general';
    researchType?: 'quantitative' | 'qualitative' | 'mixed';
    fieldSaturation?: 'high' | 'medium' | 'low';
  }
): number {
  let adjustedScore = baseScore;

  // Adjust based on journal level
  if (context.journalLevel === 'top-tier') {
    adjustedScore -= 0.1; // More innovation expected
  } else if (context.journalLevel === 'general') {
    adjustedScore += 0.05; // Less innovation expected
  }

  // Adjust based on field saturation
  if (context.fieldSaturation === 'high') {
    adjustedScore -= 0.1; // Need more differentiation
  } else if (context.fieldSaturation === 'low') {
    adjustedScore += 0.1; // Even common approaches are novel
  }

  // Clamp to valid range
  return Math.max(0, Math.min(1, adjustedScore));
}
