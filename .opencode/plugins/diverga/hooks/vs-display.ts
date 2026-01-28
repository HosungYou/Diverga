/**
 * VS Display Hook
 * Renders VS methodology alternatives with T-Scores
 */

import type { PluginContext, ToolParams, TScoreEntry } from '../types';

/**
 * T-Score visual indicators
 */
const T_SCORE_ICONS: Record<string, string> = {
  low: '🟢',
  medium: '🟡',
  high: '🟠',
  experimental: '🔴',
};

/**
 * Get T-Score label and icon
 */
function getTScoreDisplay(score: number): { label: string; icon: string; risk: string } {
  if (score >= 0.7) {
    return { label: 'Common', icon: '🟢', risk: 'low' };
  } else if (score >= 0.5) {
    return { label: 'Established', icon: '🟢', risk: 'low' };
  } else if (score >= 0.4) {
    return { label: 'Moderate', icon: '🟡', risk: 'medium' };
  } else if (score >= 0.3) {
    return { label: 'Emerging', icon: '🟡', risk: 'medium' };
  } else if (score >= 0.2) {
    return { label: 'Innovative', icon: '🟠', risk: 'high' };
  } else {
    return { label: 'Experimental', icon: '🔴', risk: 'experimental' };
  }
}

/**
 * Format T-Score for display
 */
function formatTScore(score: number): string {
  const display = getTScoreDisplay(score);
  return `T=${score.toFixed(2)} ${display.icon} (${display.label})`;
}

/**
 * Generate VS direction display
 */
export function formatVSDirections(
  directions: Array<{
    id: string;
    label: string;
    description: string;
    tScore: number;
    recommended?: boolean;
  }>
): string {
  const output: string[] = [
    '',
    '### VS Alternative Directions',
    '',
  ];

  for (const dir of directions) {
    const display = getTScoreDisplay(dir.tScore);
    const recommended = dir.recommended ? ' ⭐' : '';

    output.push(`**Direction ${dir.id}** (${formatTScore(dir.tScore)})${recommended}`);
    output.push(`  - ${dir.label}`);
    output.push(`  - ${dir.description}`);
    output.push('');
  }

  output.push('---');
  output.push('**Please select a direction (A/B/C/...):**');
  output.push('');

  return output.join('\n');
}

/**
 * Generate modal warning display
 */
export function formatModalWarning(
  modalOptions: Array<{
    option: string;
    tScore: number;
    issue: string;
  }>
): string {
  const output: string[] = [
    '',
    '⚠️ **Modal Warning**: The following are the most predictable approaches:',
    '',
    '| Approach | T-Score | Issue |',
    '|----------|---------|-------|',
  ];

  for (const modal of modalOptions) {
    output.push(`| ${modal.option} | ${modal.tScore.toFixed(2)} | ${modal.issue} |`);
  }

  output.push('');
  output.push('➡️ This is the baseline. We will explore more differentiated options.');
  output.push('');

  return output.join('\n');
}

/**
 * Main VS display hook
 */
export async function vsDisplay(
  params: ToolParams,
  result: unknown,
  context: PluginContext
): Promise<unknown> {
  // Check if result contains VS methodology data
  const vsData = extractVSData(result);

  if (!vsData) {
    return result;
  }

  // Format modal warning if present
  let output = '';

  if (vsData.modalOptions && vsData.modalOptions.length > 0) {
    output += formatModalWarning(vsData.modalOptions);
  }

  // Format directions
  if (vsData.directions && vsData.directions.length > 0) {
    output += formatVSDirections(vsData.directions);
  }

  // Add VS output to result
  if (typeof result === 'object' && result !== null) {
    return {
      ...result,
      vsDisplay: output,
    };
  }

  return result;
}

/**
 * Extract VS data from result
 */
function extractVSData(result: unknown): {
  modalOptions?: Array<{ option: string; tScore: number; issue: string }>;
  directions?: Array<{
    id: string;
    label: string;
    description: string;
    tScore: number;
    recommended?: boolean;
  }>;
} | null {
  if (!result || typeof result !== 'object') {
    return null;
  }

  const r = result as Record<string, unknown>;

  // Check for VS data markers
  if (r.vsMethodology || r.alternatives || r.directions) {
    return {
      modalOptions: r.modalOptions as any,
      directions: r.directions as any || r.alternatives as any,
    };
  }

  return null;
}

/**
 * Generate T-Score visualization bar
 */
export function visualizeTScore(score: number, width: number = 20): string {
  const filled = Math.round(score * width);
  const empty = width - filled;
  const bar = '█'.repeat(filled) + '░'.repeat(empty);

  const display = getTScoreDisplay(score);

  return `[${bar}] ${score.toFixed(2)} ${display.label}`;
}

/**
 * Get creativity level recommendation based on T-Score
 */
export function getCreativityRecommendation(tScore: number): string {
  if (tScore >= 0.5) {
    return 'Conservative - Safe, validated approaches';
  } else if (tScore >= 0.3) {
    return 'Balanced - Differentiated + defensible';
  } else if (tScore >= 0.2) {
    return 'Innovative - High contribution potential';
  } else {
    return 'Extreme - Maximum creativity, paradigm-challenging';
  }
}
