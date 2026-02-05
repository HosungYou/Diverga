/**
 * Diverga HUD - Core Rendering Logic
 *
 * Main HUD rendering engine that combines state and presets.
 *
 * @module lib/hud/core
 * @version 8.0.0
 */

import {
  HUDState,
  HUDCache,
  findProjectRoot,
  loadHUDState,
  initializeHUDState,
  refreshCache
} from './state';
import { PresetName, getPreset, isValidPreset } from './presets';

/**
 * Render options
 */
export interface RenderOptions {
  /** Force refresh cache from disk */
  refresh?: boolean;
  /** Override preset for this render */
  preset?: PresetName;
  /** Project root directory (auto-detected if not provided) */
  projectRoot?: string;
}

/**
 * Render result
 */
export interface RenderResult {
  /** Rendered HUD string */
  output: string;
  /** Whether HUD is enabled */
  enabled: boolean;
  /** Whether a project was found */
  hasProject: boolean;
  /** Error message if any */
  error?: string;
}

/**
 * Main HUD renderer class
 */
export class HUDRenderer {
  private projectRoot: string | null;
  private state: HUDState | null;

  constructor(projectRoot?: string) {
    this.projectRoot = projectRoot || findProjectRoot();
    this.state = null;

    if (this.projectRoot) {
      this.state = loadHUDState(this.projectRoot) || initializeHUDState(this.projectRoot);
    }
  }

  /**
   * Check if project exists
   */
  hasProject(): boolean {
    return this.projectRoot !== null && this.state !== null;
  }

  /**
   * Check if HUD is enabled
   */
  isEnabled(): boolean {
    return this.state?.enabled ?? true;
  }

  /**
   * Get current preset name
   */
  getPreset(): PresetName {
    return this.state?.preset ?? 'research';
  }

  /**
   * Get current cache
   */
  getCache(): HUDCache | null {
    return this.state?.cache ?? null;
  }

  /**
   * Refresh cache from disk
   */
  refresh(): void {
    if (this.projectRoot) {
      const cache = refreshCache(this.projectRoot);
      if (this.state) {
        this.state.cache = cache;
      }
    }
  }

  /**
   * Render HUD string
   */
  render(options: RenderOptions = {}): RenderResult {
    // Refresh if requested
    if (options.refresh) {
      this.refresh();
    }

    // No project found
    if (!this.projectRoot || !this.state) {
      return {
        output: '',
        enabled: false,
        hasProject: false,
        error: 'No Diverga project found'
      };
    }

    // HUD disabled
    if (!this.state.enabled) {
      return {
        output: '',
        enabled: false,
        hasProject: true
      };
    }

    // Get preset
    const presetName = options.preset || this.state.preset || 'research';
    if (!isValidPreset(presetName)) {
      return {
        output: '',
        enabled: true,
        hasProject: true,
        error: `Invalid preset: ${presetName}`
      };
    }

    const preset = getPreset(presetName);

    // Render
    try {
      const output = preset.render(this.state.cache);
      return {
        output,
        enabled: true,
        hasProject: true
      };
    } catch (e) {
      return {
        output: '',
        enabled: true,
        hasProject: true,
        error: `Render error: ${e instanceof Error ? e.message : String(e)}`
      };
    }
  }
}

/**
 * Render HUD for current directory
 *
 * This is the main entry point for the statusline command.
 * Returns empty string if no project or HUD disabled.
 */
export function renderHUD(options: RenderOptions = {}): string {
  const renderer = new HUDRenderer(options.projectRoot);
  const result = renderer.render(options);

  if (!result.enabled || !result.hasProject) {
    return '';
  }

  return result.output;
}

/**
 * Render HUD with full result info
 */
export function renderHUDWithInfo(options: RenderOptions = {}): RenderResult {
  const renderer = new HUDRenderer(options.projectRoot);
  return renderer.render(options);
}

/**
 * Quick check if HUD should render
 */
export function shouldRenderHUD(projectRoot?: string): boolean {
  const root = projectRoot || findProjectRoot();
  if (!root) return false;

  const state = loadHUDState(root);
  return state?.enabled ?? true;
}

/**
 * Get HUD status info (for diagnostics)
 */
export function getHUDStatus(projectRoot?: string): {
  hasProject: boolean;
  enabled: boolean;
  preset: PresetName;
  projectName: string;
  stage: string;
  checkpoints: { completed: number; total: number };
  memoryHealth: number;
} {
  const root = projectRoot || findProjectRoot();

  if (!root) {
    return {
      hasProject: false,
      enabled: false,
      preset: 'research',
      projectName: '',
      stage: 'foundation',
      checkpoints: { completed: 0, total: 11 },
      memoryHealth: 100
    };
  }

  const state = loadHUDState(root) || initializeHUDState(root);

  return {
    hasProject: true,
    enabled: state.enabled,
    preset: state.preset,
    projectName: state.cache.project_name,
    stage: state.cache.current_stage,
    checkpoints: {
      completed: state.cache.checkpoints_completed,
      total: state.cache.checkpoints_total
    },
    memoryHealth: state.cache.memory_health
  };
}

export default {
  HUDRenderer,
  renderHUD,
  renderHUDWithInfo,
  shouldRenderHUD,
  getHUDStatus
};
