#!/usr/bin/env node
/**
 * Diverga HUD - Statusline Script
 *
 * Standalone Node.js script for Claude Code statusLine integration.
 * Displays research project status in the terminal statusline.
 *
 * Usage in ~/.claude/settings.json:
 * {
 *   "statusLine": {
 *     "type": "command",
 *     "command": "node ~/.claude/hud/diverga-hud.mjs"
 *   }
 * }
 *
 * @version 8.0.0
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// ANSI escape codes
const ESC = '\x1b[';
const RESET = `${ESC}0m`;
const BOLD = `${ESC}1m`;
const DIM = `${ESC}2m`;
const GREEN = `${ESC}32m`;
const YELLOW = `${ESC}33m`;
const RED = `${ESC}31m`;
const CYAN = `${ESC}36m`;
const MAGENTA = `${ESC}35m`;
const BRIGHT_CYAN = `${ESC}96m`;
const BRIGHT_MAGENTA = `${ESC}95m`;

/**
 * Color helper functions
 */
function color(text, colorCode) {
  return `${colorCode}${text}${RESET}`;
}

function bold(text) {
  return `${BOLD}${text}${RESET}`;
}

function dim(text) {
  return `${DIM}${text}${RESET}`;
}

/**
 * Get memory health color based on percentage
 */
function memoryHealthColor(percent) {
  if (percent >= 70) return GREEN;
  if (percent >= 40) return YELLOW;
  return RED;
}

/**
 * Generate progress bar string
 */
function progressBar(completed, total, width = 11) {
  const filled = total > 0 ? Math.min(Math.round((completed / total) * width), width) : 0;
  const filledStr = color('●'.repeat(filled), GREEN);
  const emptyStr = color('○'.repeat(width - filled), DIM);
  return filledStr + emptyStr;
}

/**
 * Truncate project name if too long
 */
function truncateName(name, maxLen = 20) {
  if (name.length <= maxLen) return name;
  return name.substring(0, maxLen - 3) + '...';
}

/**
 * Find project root by looking for .research directory
 */
function findProjectRoot(startDir = process.cwd()) {
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
function loadHUDState(projectRoot) {
  const statePath = path.join(projectRoot, '.research', 'hud-state.json');

  try {
    if (fs.existsSync(statePath)) {
      const content = fs.readFileSync(statePath, 'utf-8');
      return JSON.parse(content);
    }
  } catch (e) {
    // Ignore errors
  }

  return null;
}

/**
 * Load project state from .research/project-state.yaml (simple YAML parsing)
 */
function loadProjectState(projectRoot) {
  const statePath = path.join(projectRoot, '.research', 'project-state.yaml');

  try {
    if (fs.existsSync(statePath)) {
      const content = fs.readFileSync(statePath, 'utf-8');
      // Simple YAML parsing for key fields
      const result = {};

      const lines = content.split('\n');
      for (const line of lines) {
        const match = line.match(/^(\w+):\s*(.+)$/);
        if (match) {
          const [, key, value] = match;
          // Remove quotes if present
          result[key] = value.replace(/^["']|["']$/g, '').trim();
        }
      }

      return result;
    }
  } catch (e) {
    // Ignore errors
  }

  return null;
}

/**
 * Load checkpoints from .research/checkpoints.yaml (simple YAML parsing)
 */
function loadCheckpoints(projectRoot) {
  const checkpointsPath = path.join(projectRoot, '.research', 'checkpoints.yaml');

  try {
    if (fs.existsSync(checkpointsPath)) {
      const content = fs.readFileSync(checkpointsPath, 'utf-8');

      // Simple parsing: count completed checkpoints
      const completedMatches = content.match(/completed:\s*\n((?:\s*-\s*.+\n?)*)/);
      if (completedMatches) {
        const completedItems = completedMatches[1].match(/^\s*-\s*.+/gm) || [];
        return {
          completed: completedItems.map(item => item.replace(/^\s*-\s*/, '').trim())
        };
      }

      return { completed: [] };
    }
  } catch (e) {
    // Ignore errors
  }

  return { completed: [] };
}

/**
 * Calculate memory health percentage
 */
function calculateMemoryHealth(projectRoot) {
  try {
    const decisionLogPath = path.join(projectRoot, '.research', 'decision-log.yaml');

    let health = 100;

    if (fs.existsSync(decisionLogPath)) {
      const stats = fs.statSync(decisionLogPath);
      const sizeMB = stats.size / (1024 * 1024);
      if (sizeMB > 5) health -= 20;
      else if (sizeMB > 2) health -= 10;
    }

    return Math.max(0, health);
  } catch (e) {
    return 100;
  }
}

/**
 * Build cache from project files
 */
function buildCache(projectRoot) {
  const cache = {
    project_name: '',
    current_stage: 'foundation',
    checkpoints_completed: 0,
    checkpoints_total: 11,
    memory_health: 100
  };

  // Load project state
  const projectState = loadProjectState(projectRoot);
  if (projectState) {
    cache.project_name = projectState.project_name || projectState.name || '';
    cache.current_stage = projectState.current_stage || 'foundation';
  }

  // Load checkpoints
  const checkpoints = loadCheckpoints(projectRoot);
  if (checkpoints && checkpoints.completed) {
    cache.checkpoints_completed = checkpoints.completed.length;
  }

  // Calculate memory health
  cache.memory_health = calculateMemoryHealth(projectRoot);

  return cache;
}

/**
 * Render HUD presets
 */
const PRESETS = {
  /**
   * Research preset (default)
   * Shows: Stage, Checkpoints, Memory
   */
  research: (cache) => {
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
    const memoryStr = `${color('🧠', BRIGHT_MAGENTA)} ${color(`${memory}%`, memoryHealthColor(memory))}`;

    return `${icon} ${nameStr} ${sep} ${stageStr} ${sep} ${progress} ${sep} ${memoryStr}`;
  },

  /**
   * Checkpoint preset
   */
  checkpoint: (cache) => {
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

    return `${line1}\n${line2}`;
  },

  /**
   * Memory preset
   */
  memory: (cache) => {
    const projectName = truncateName(cache.project_name || 'No Project', 20);
    const memory = cache.memory_health || 100;

    const icon = color('🔬', BRIGHT_MAGENTA);
    const nameStr = bold(projectName);
    const sep = color('│', DIM);

    const memoryStr = `${color('🧠', BRIGHT_MAGENTA)} Memory: ${color(`${memory}%`, memoryHealthColor(memory))}`;
    const contextStatus = memory > 50 ? color('loaded', GREEN) : color('sparse', YELLOW);
    const contextStr = `Context: ${contextStatus}`;

    return `${icon} ${nameStr} ${sep} ${memoryStr} ${sep} ${contextStr}`;
  },

  /**
   * Minimal preset
   */
  minimal: (cache) => {
    const stage = cache.current_stage || 'foundation';

    const icon = color('🔬', BRIGHT_MAGENTA);
    const stageStr = color(stage, BRIGHT_CYAN);

    return `${icon} ${stageStr}`;
  }
};

/**
 * Main function
 */
function main() {
  // Find project root
  const projectRoot = findProjectRoot();

  if (!projectRoot) {
    // No project found, output nothing
    return;
  }

  // Load or build state
  let state = loadHUDState(projectRoot);
  let cache;

  if (state && state.cache) {
    cache = state.cache;
  } else {
    cache = buildCache(projectRoot);
  }

  // Check if HUD is disabled
  if (state && state.enabled === false) {
    return;
  }

  // Get preset
  const presetName = (state && state.preset) || 'research';
  const preset = PRESETS[presetName] || PRESETS.research;

  // Render and output
  try {
    const output = preset(cache);
    process.stdout.write(output);
  } catch (e) {
    // Silent failure
  }
}

// Run
main();
