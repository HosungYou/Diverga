/**
 * Diverga T-Score Reference
 * Typicality scores for VS methodology
 */

import type { TScoreEntry } from './types';

/**
 * T-Score ranges and their meanings
 */
export const T_SCORE_REFERENCE: TScoreEntry[] = [
  {
    range: [0.7, 1.0],
    label: 'Common/Modal',
    meaning: 'Highly typical, safe but limited novelty contribution',
    suitableFor: 'Replication studies, confirmatory research',
    riskLevel: 'low',
    icon: '🟢',
  },
  {
    range: [0.5, 0.7],
    label: 'Established',
    meaning: 'Well-established approach, needs specificity for contribution',
    suitableFor: 'Standard research, mid-tier journals',
    riskLevel: 'low',
    icon: '🟢',
  },
  {
    range: [0.4, 0.5],
    label: 'Moderate',
    meaning: 'Balanced risk-novelty, clear differentiation possible',
    suitableFor: 'Most academic research, good contribution potential',
    riskLevel: 'medium',
    icon: '🟡',
  },
  {
    range: [0.3, 0.4],
    label: 'Emerging',
    meaning: 'Novel approach, emerging in literature',
    suitableFor: 'Innovative journals, strong theoretical support needed',
    riskLevel: 'medium',
    icon: '🟡',
  },
  {
    range: [0.2, 0.3],
    label: 'Innovative',
    meaning: 'Novel, requires strong justification and defense',
    suitableFor: 'Top-tier journals seeking contribution',
    riskLevel: 'high',
    icon: '🟠',
  },
  {
    range: [0.0, 0.2],
    label: 'Experimental',
    meaning: 'Highly novel, high risk/reward, paradigm-challenging',
    suitableFor: 'Groundbreaking research, experienced researchers',
    riskLevel: 'experimental',
    icon: '🔴',
  },
];

/**
 * Creativity levels
 */
export const CREATIVITY_LEVELS = {
  Conservative: { minT: 0.5, description: 'Safe, validated approaches' },
  Balanced: { minT: 0.3, description: 'Differentiated + defensible' },
  Innovative: { minT: 0.2, description: 'High contribution potential' },
  Extreme: { minT: 0.0, description: 'Maximum creativity, paradigm-challenging' },
};

/**
 * Look up T-Score entry for a given score
 */
export function lookupTScore(score: number): TScoreEntry | undefined {
  return T_SCORE_REFERENCE.find(
    entry => score >= entry.range[0] && score <= entry.range[1]
  );
}

/**
 * Format T-Score for display
 */
export function formatTScore(score: number): string {
  const entry = lookupTScore(score);
  if (!entry) return `T=${score.toFixed(2)}`;
  return `T=${score.toFixed(2)} ${entry.icon} (${entry.label})`;
}

/**
 * Format T-Score table for display
 */
export function formatTScoreTable(): string {
  return `
╔═══════════════════════════════════════════════════════════════╗
║                  T-Score Reference Table                      ║
╚═══════════════════════════════════════════════════════════════╝

T-Score measures "typicality" - how common a research approach is.

┌────────────┬─────────────┬────────────────────────────────────┐
│ T-Score    │ Label       │ Meaning                            │
├────────────┼─────────────┼────────────────────────────────────┤
│ ≥ 0.7      │ 🟢 Common   │ Highly typical, limited novelty    │
│ 0.5-0.7    │ 🟢 Estab.   │ Standard, needs specificity        │
│ 0.4-0.5    │ 🟡 Moderate │ Balanced risk-novelty              │
│ 0.3-0.4    │ 🟡 Emerging │ Novel, needs justification         │
│ 0.2-0.3    │ 🟠 Innovate │ High contribution potential        │
│ < 0.2      │ 🔴 Experim. │ Paradigm-challenging               │
└────────────┴─────────────┴────────────────────────────────────┘

Creativity Levels:
  Conservative (T ≥ 0.5) - Safe, validated approaches
  Balanced (T ≥ 0.3)     - Differentiated + defensible
  Innovative (T ≥ 0.2)   - High contribution potential
  Extreme (T < 0.2)      - Maximum creativity
`;
}

export default T_SCORE_REFERENCE;
