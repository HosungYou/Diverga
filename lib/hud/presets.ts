/**
 * Diverga HUD - Preset Definitions
 *
 * Defines different HUD display modes for various use cases.
 *
 * @module lib/hud/presets
 * @version 8.0.0
 */

import { HUDCache } from './state';
import {
  color, bold, dim, styled,
  HUD_COLORS, memoryHealthColor,
  BRIGHT_MAGENTA, BRIGHT_CYAN, GREEN, YELLOW, RED, DIM, RESET
} from './colors';

/**
 * HUD preset type
 */
export type PresetName = 'research' | 'checkpoint' | 'memory' | 'minimal';

/**
 * Preset configuration
 */
export interface PresetConfig {
  name: PresetName;
  description: string;
  render: (cache: HUDCache) => string;
}

/**
 * Generate progress bar string
 */
function progressBar(completed: number, total: number, width: number = 11): string {
  const filled = total > 0 ? Math.min(Math.round((completed / total) * width), width) : 0;
  const filledStr = color('●'.repeat(filled), GREEN);
  const emptyStr = color('○'.repeat(width - filled), DIM);
  return filledStr + emptyStr;
}

/**
 * Format memory health with color
 */
function formatMemoryHealth(percent: number): string {
  const healthColor = memoryHealthColor(percent);
  return `${color('🧠', BRIGHT_MAGENTA)} ${color(`${percent}%`, healthColor)}`;
}

/**
 * Truncate project name if too long
 */
function truncateName(name: string, maxLen: number = 20): string {
  if (name.length <= maxLen) return name;
  return name.substring(0, maxLen - 3) + '...';
}

/**
 * Research preset (default)
 * Shows: Stage, Checkpoints, Memory
 *
 * Example: 🔬 AI-Ethics-HR │ Stage: foundation │ ●●○○○○○○○○○ (2/11) │ 🧠 95%
 */
const researchPreset: PresetConfig = {
  name: 'research',
  description: 'Standard research view with stage, checkpoints, and memory health',
  render: (cache: HUDCache): string => {
    const projectName = truncateName(cache.project_name || 'No Project', 20);
    const stage = cache.current_stage || 'foundation';
    const completed = cache.checkpoints_completed || 0;
    const total = cache.checkpoints_total || 11;
    const memory = cache.memory_health || 100;

    const icon = color('🔬', BRIGHT_MAGENTA);
    const nameStr = bold(projectName);
    const sep = color('│', DIM);
    const stageStr = `Stage: ${color(stage, BRIGHT_CYAN)}`;
    const progress = `${progressBar(completed, total)} (${completed}/${total})`;
    const memoryStr = formatMemoryHealth(memory);

    return `${icon} ${nameStr} ${sep} ${stageStr} ${sep} ${progress} ${sep} ${memoryStr}`;
  }
};

/**
 * Checkpoint preset
 * Shows detailed checkpoint information
 *
 * Example:
 * 🔬 AI-Ethics-HR │ Stage: foundation
 * Checkpoints: ●●○○○○○○○○○ (2/11)
 *  ✅ CP_RESEARCH_DIRECTION │ ✅ CP_PARADIGM_SELECTION
 *  🔴 CP_SCOPE_DEFINITION (pending)
 */
const checkpointPreset: PresetConfig = {
  name: 'checkpoint',
  description: 'Detailed checkpoint view for decision sessions',
  render: (cache: HUDCache): string => {
    const projectName = truncateName(cache.project_name || 'No Project', 20);
    const stage = cache.current_stage || 'foundation';
    const completed = cache.checkpoints_completed || 0;
    const total = cache.checkpoints_total || 11;

    const icon = color('🔬', BRIGHT_MAGENTA);
    const nameStr = bold(projectName);
    const sep = color('│', DIM);
    const stageStr = `Stage: ${color(stage, BRIGHT_CYAN)}`;

    const line1 = `${icon} ${nameStr} ${sep} ${stageStr}`;
    const line2 = `Checkpoints: ${progressBar(completed, total)} (${completed}/${total})`;

    // In a real implementation, we'd show specific checkpoint statuses
    // For now, show a simplified view
    const completedIcon = color('✅', GREEN);
    const pendingIcon = color('🔴', RED);
    const line3 = ` ${completed > 0 ? completedIcon : ''} ${completed} completed ${sep} ${pendingIcon} ${total - completed} pending`;

    return `${line1}\n${line2}\n${line3}`;
  }
};

/**
 * Memory preset
 * Shows memory health and context details
 *
 * Example: 🔬 AI-Ethics-HR │ 🧠 Memory: 95% │ Context: loaded │ Sessions: 5
 */
const memoryPreset: PresetConfig = {
  name: 'memory',
  description: 'Memory health and context debugging view',
  render: (cache: HUDCache): string => {
    const projectName = truncateName(cache.project_name || 'No Project', 20);
    const memory = cache.memory_health || 100;

    const icon = color('🔬', BRIGHT_MAGENTA);
    const nameStr = bold(projectName);
    const sep = color('│', DIM);

    const memoryStr = `${color('🧠', BRIGHT_MAGENTA)} Memory: ${color(`${memory}%`, memoryHealthColor(memory))}`;

    // Additional context info would be loaded from state in real implementation
    const contextStatus = memory > 50 ? color('loaded', GREEN) : color('sparse', YELLOW);
    const contextStr = `Context: ${contextStatus}`;

    return `${icon} ${nameStr} ${sep} ${memoryStr} ${sep} ${contextStr}`;
  }
};

/**
 * Minimal preset
 * Shows only stage
 *
 * Example: 🔬 foundation
 */
const minimalPreset: PresetConfig = {
  name: 'minimal',
  description: 'Minimal view showing only current stage',
  render: (cache: HUDCache): string => {
    const stage = cache.current_stage || 'foundation';

    const icon = color('🔬', BRIGHT_MAGENTA);
    const stageStr = color(stage, BRIGHT_CYAN);

    return `${icon} ${stageStr}`;
  }
};

/**
 * All available presets
 */
export const PRESETS: Record<PresetName, PresetConfig> = {
  research: researchPreset,
  checkpoint: checkpointPreset,
  memory: memoryPreset,
  minimal: minimalPreset
};

/**
 * Get preset by name
 */
export function getPreset(name: PresetName): PresetConfig {
  return PRESETS[name] || PRESETS.research;
}

/**
 * List all available presets
 */
export function listPresets(): PresetConfig[] {
  return Object.values(PRESETS);
}

/**
 * Validate preset name
 */
export function isValidPreset(name: string): name is PresetName {
  return name in PRESETS;
}

export default {
  PRESETS,
  getPreset,
  listPresets,
  isValidPreset
};
