/**
 * Diverga HUD - Main Entry Point
 *
 * Exports all HUD-related functionality for the Diverga research assistant.
 *
 * The HUD (Heads-Up Display) provides a statusline showing:
 * - Current research project name
 * - Research stage progress
 * - Checkpoint completion status
 * - Memory/context health
 *
 * ## Usage
 *
 * For statusline integration (Claude Code settings.json):
 * ```json
 * {
 *   "statusLine": {
 *     "type": "command",
 *     "command": "node ~/.claude/hud/diverga-hud.mjs"
 *   }
 * }
 * ```
 *
 * ## Presets
 *
 * - `research` (default): Full view with stage, checkpoints, memory
 * - `checkpoint`: Detailed checkpoint information
 * - `memory`: Memory health debugging view
 * - `minimal`: Just the stage name
 *
 * @module lib/hud
 * @version 8.0.0
 */

// Re-export from submodules
export * from './colors';
export * from './state';
export * from './presets';
export * from './core';

// Import for convenient access
import {
  HUDState,
  HUDCache,
  DEFAULT_HUD_STATE,
  STAGES,
  findProjectRoot,
  loadHUDState,
  saveHUDState,
  loadProjectState,
  loadCheckpoints,
  refreshCache,
  initializeHUDState,
  setPreset,
  setEnabled
} from './state';

import {
  PresetName,
  PresetConfig,
  PRESETS,
  getPreset,
  listPresets,
  isValidPreset
} from './presets';

import {
  RenderOptions,
  RenderResult,
  HUDRenderer,
  renderHUD,
  renderHUDWithInfo,
  shouldRenderHUD,
  getHUDStatus
} from './core';

import colors from './colors';

/**
 * Main HUD facade
 *
 * Provides a simple API for common HUD operations.
 */
export const DivergaHUD = {
  // State management
  findProjectRoot,
  loadState: loadHUDState,
  saveState: saveHUDState,
  initState: initializeHUDState,
  refreshCache,

  // Preset management
  setPreset,
  getPreset,
  listPresets,
  isValidPreset,

  // Enable/disable
  enable: (projectRoot?: string) => setEnabled(true, projectRoot),
  disable: (projectRoot?: string) => setEnabled(false, projectRoot),

  // Rendering
  render: renderHUD,
  renderWithInfo: renderHUDWithInfo,
  shouldRender: shouldRenderHUD,
  getStatus: getHUDStatus,

  // Renderer class
  Renderer: HUDRenderer,

  // Constants
  STAGES,
  PRESETS,
  DEFAULT_STATE: DEFAULT_HUD_STATE,

  // Colors
  colors
};

// Default export
export default DivergaHUD;

// Type exports
export type {
  HUDState,
  HUDCache,
  PresetName,
  PresetConfig,
  RenderOptions,
  RenderResult
};
