/**
 * Diverga HUD - State Management
 *
 * Manages HUD state persistence and loading.
 * State is stored in .research/hud-state.json
 *
 * @module lib/hud/state
 * @version 8.0.0
 */

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

/**
 * HUD state structure
 */
export interface HUDState {
  version: string;
  enabled: boolean;
  preset: 'research' | 'checkpoint' | 'memory' | 'minimal';
  last_updated: string;
  cache: HUDCache;
}

/**
 * Cached HUD data for quick rendering
 */
export interface HUDCache {
  project_name: string;
  current_stage: string;
  checkpoints_completed: number;
  checkpoints_total: number;
  memory_health: number;
}

/**
 * Default HUD state
 */
export const DEFAULT_HUD_STATE: HUDState = {
  version: '1.0.0',
  enabled: true,
  preset: 'research',
  last_updated: new Date().toISOString(),
  cache: {
    project_name: '',
    current_stage: 'foundation',
    checkpoints_completed: 0,
    checkpoints_total: 11,
    memory_health: 100
  }
};

/**
 * Stage definitions with checkpoint mapping
 */
export const STAGES = {
  foundation: { order: 1, name: 'Foundation', checkpoints: ['CP_RESEARCH_DIRECTION', 'CP_PARADIGM_SELECTION', 'CP_SCOPE_DEFINITION'] },
  theory: { order: 2, name: 'Theory', checkpoints: ['CP_THEORY_SELECTION', 'CP_VARIABLE_DEFINITION'] },
  methodology: { order: 3, name: 'Methodology', checkpoints: ['CP_METHODOLOGY_APPROVAL'] },
  design: { order: 4, name: 'Design', checkpoints: ['CP_DATABASE_SELECTION', 'CP_SEARCH_STRATEGY', 'CP_SAMPLE_PLANNING'] },
  execution: { order: 5, name: 'Execution', checkpoints: ['CP_SCREENING_CRITERIA', 'CP_RAG_READINESS', 'CP_DATA_EXTRACTION'] },
  analysis: { order: 6, name: 'Analysis', checkpoints: ['CP_ANALYSIS_PLAN'] },
  validation: { order: 7, name: 'Validation', checkpoints: ['CP_QUALITY_GATES', 'CP_PEER_REVIEW', 'CP_PUBLICATION_READY'] }
} as const;

/**
 * Get total number of checkpoints
 */
export function getTotalCheckpoints(): number {
  return Object.values(STAGES).reduce((sum, stage) => sum + stage.checkpoints.length, 0);
}

/**
 * Find project root by looking for .research directory
 */
export function findProjectRoot(startDir: string = process.cwd()): string | null {
  let current = startDir;

  while (current !== path.parse(current).root) {
    if (fs.existsSync(path.join(current, '.research'))) {
      return current;
    }
    current = path.dirname(current);
  }

  return null;
}

/**
 * Load HUD state from .research/hud-state.json
 */
export function loadHUDState(projectRoot?: string): HUDState | null {
  const root = projectRoot || findProjectRoot();
  if (!root) return null;

  const statePath = path.join(root, '.research', 'hud-state.json');

  try {
    if (fs.existsSync(statePath)) {
      const content = fs.readFileSync(statePath, 'utf-8');
      return JSON.parse(content) as HUDState;
    }
  } catch (e) {
    // Return null if file doesn't exist or is invalid
  }

  return null;
}

/**
 * Save HUD state to .research/hud-state.json
 */
export function saveHUDState(state: HUDState, projectRoot?: string): boolean {
  const root = projectRoot || findProjectRoot();
  if (!root) return false;

  const researchDir = path.join(root, '.research');
  const statePath = path.join(researchDir, 'hud-state.json');

  try {
    // Ensure .research directory exists
    if (!fs.existsSync(researchDir)) {
      fs.mkdirSync(researchDir, { recursive: true });
    }

    // Update timestamp
    state.last_updated = new Date().toISOString();

    // Write state
    fs.writeFileSync(statePath, JSON.stringify(state, null, 2), 'utf-8');
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * Load project state from .research/project-state.yaml
 */
export function loadProjectState(projectRoot?: string): Record<string, any> | null {
  const root = projectRoot || findProjectRoot();
  if (!root) return null;

  const statePath = path.join(root, '.research', 'project-state.yaml');

  try {
    if (fs.existsSync(statePath)) {
      const content = fs.readFileSync(statePath, 'utf-8');
      return yaml.load(content) as Record<string, any>;
    }
  } catch (e) {
    // Return null if file doesn't exist or is invalid
  }

  return null;
}

/**
 * Load checkpoints from .research/checkpoints.yaml
 */
export function loadCheckpoints(projectRoot?: string): Record<string, any> | null {
  const root = projectRoot || findProjectRoot();
  if (!root) return null;

  const checkpointsPath = path.join(root, '.research', 'checkpoints.yaml');

  try {
    if (fs.existsSync(checkpointsPath)) {
      const content = fs.readFileSync(checkpointsPath, 'utf-8');
      return yaml.load(content) as Record<string, any>;
    }
  } catch (e) {
    // Return null if file doesn't exist or is invalid
  }

  return null;
}

/**
 * Refresh HUD cache from project state
 */
export function refreshCache(projectRoot?: string): HUDCache {
  const root = projectRoot || findProjectRoot();

  const cache: HUDCache = {
    project_name: '',
    current_stage: 'foundation',
    checkpoints_completed: 0,
    checkpoints_total: getTotalCheckpoints(),
    memory_health: 100
  };

  if (!root) return cache;

  // Load project state
  const projectState = loadProjectState(root);
  if (projectState) {
    cache.project_name = projectState.project_name || projectState.name || '';
    cache.current_stage = projectState.current_stage || 'foundation';
  }

  // Load checkpoints
  const checkpoints = loadCheckpoints(root);
  if (checkpoints) {
    const completed = checkpoints.completed || [];
    cache.checkpoints_completed = Array.isArray(completed) ? completed.length : 0;
  }

  // Calculate memory health (placeholder - could be based on context file size)
  cache.memory_health = calculateMemoryHealth(root);

  return cache;
}

/**
 * Calculate memory health percentage
 * Based on context file sizes and session count
 */
function calculateMemoryHealth(projectRoot: string): number {
  try {
    const sessionsDir = path.join(projectRoot, '.research', 'sessions');
    const decisionLogPath = path.join(projectRoot, '.research', 'decision-log.yaml');

    let health = 100;

    // Check if decision log exists and its size
    if (fs.existsSync(decisionLogPath)) {
      const stats = fs.statSync(decisionLogPath);
      const sizeMB = stats.size / (1024 * 1024);
      // Reduce health if file is very large
      if (sizeMB > 5) health -= 20;
      else if (sizeMB > 2) health -= 10;
    }

    // Check session count
    if (fs.existsSync(sessionsDir)) {
      const sessions = fs.readdirSync(sessionsDir).filter(f => f.endsWith('.yaml') || f.endsWith('.json'));
      if (sessions.length > 50) health -= 15;
      else if (sessions.length > 20) health -= 5;
    }

    return Math.max(0, health);
  } catch (e) {
    return 100; // Default to healthy if can't calculate
  }
}

/**
 * Initialize or update HUD state
 */
export function initializeHUDState(projectRoot?: string): HUDState {
  const root = projectRoot || findProjectRoot();

  // Load existing state or create default
  let state = loadHUDState(root || undefined);
  if (!state) {
    state = { ...DEFAULT_HUD_STATE };
  }

  // Refresh cache
  state.cache = refreshCache(root || undefined);

  // Save updated state
  if (root) {
    saveHUDState(state, root);
  }

  return state;
}

/**
 * Set HUD preset
 */
export function setPreset(preset: HUDState['preset'], projectRoot?: string): boolean {
  const root = projectRoot || findProjectRoot();
  if (!root) return false;

  const state = loadHUDState(root) || { ...DEFAULT_HUD_STATE };
  state.preset = preset;
  state.cache = refreshCache(root);

  return saveHUDState(state, root);
}

/**
 * Enable or disable HUD
 */
export function setEnabled(enabled: boolean, projectRoot?: string): boolean {
  const root = projectRoot || findProjectRoot();
  if (!root) return false;

  const state = loadHUDState(root) || { ...DEFAULT_HUD_STATE };
  state.enabled = enabled;

  return saveHUDState(state, root);
}

export default {
  DEFAULT_HUD_STATE,
  STAGES,
  getTotalCheckpoints,
  findProjectRoot,
  loadHUDState,
  saveHUDState,
  loadProjectState,
  loadCheckpoints,
  refreshCache,
  initializeHUDState,
  setPreset,
  setEnabled
};
