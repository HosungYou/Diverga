/**
 * Context Manager Hook
 * Manages research project state persistence
 */

import * as fs from 'fs';
import * as path from 'path';
import type { PluginContext, ResearchContext, Decision } from '../types';

/**
 * Context file paths
 */
const CONTEXT_PATHS = {
  projectState: '.research/project-state.yaml',
  decisionLog: '.research/decision-log.yaml',
};

/**
 * Default research context
 */
const DEFAULT_CONTEXT: ResearchContext = {
  projectName: '',
  projectType: 'quantitative',
  paradigm: 'post-positivist',
  currentStage: 0,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  researchQuestion: undefined,
  theoreticalFramework: undefined,
  completedCheckpoints: [],
  pendingCheckpoints: [],
  decisions: [],
};

// In-memory context cache
let _contextCache: ResearchContext | null = null;

/**
 * Get context file path
 */
function getContextPath(): string {
  return path.join(process.cwd(), CONTEXT_PATHS.projectState);
}

/**
 * Load context from file
 */
export function loadContext(): ResearchContext | null {
  // Return cached if available
  if (_contextCache) {
    return _contextCache;
  }

  const contextPath = getContextPath();

  if (!fs.existsSync(contextPath)) {
    return null;
  }

  try {
    const content = fs.readFileSync(contextPath, 'utf-8');
    _contextCache = parseYamlContext(content);
    return _contextCache;
  } catch (error) {
    console.error('[Diverga] Failed to load context:', error);
    return null;
  }
}

/**
 * Save context to file
 */
export function saveContext(pluginContext?: PluginContext): void {
  if (!_contextCache) {
    return;
  }

  const contextPath = getContextPath();
  const dirPath = path.dirname(contextPath);

  // Ensure directory exists
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }

  // Update timestamp
  _contextCache.updatedAt = new Date().toISOString();

  try {
    const content = serializeYamlContext(_contextCache);
    fs.writeFileSync(contextPath, content, 'utf-8');
  } catch (error) {
    console.error('[Diverga] Failed to save context:', error);
  }
}

/**
 * Create new research context
 */
export function createContext(
  projectName: string,
  projectType: ResearchContext['projectType'] = 'quantitative'
): ResearchContext {
  _contextCache = {
    ...DEFAULT_CONTEXT,
    projectName,
    projectType,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  saveContext();
  return _contextCache;
}

/**
 * Update context field
 */
export function updateContext(updates: Partial<ResearchContext>): void {
  if (!_contextCache) {
    _contextCache = { ...DEFAULT_CONTEXT };
  }

  _contextCache = {
    ..._contextCache,
    ...updates,
    updatedAt: new Date().toISOString(),
  };

  saveContext();
}

/**
 * Add completed checkpoint
 */
export function addCompletedCheckpoint(checkpointId: string, decision: Decision): void {
  if (!_contextCache) {
    return;
  }

  if (!_contextCache.completedCheckpoints.includes(checkpointId)) {
    _contextCache.completedCheckpoints.push(checkpointId);
  }

  _contextCache.pendingCheckpoints = _contextCache.pendingCheckpoints.filter(
    cp => cp !== checkpointId
  );

  _contextCache.decisions.push(decision);

  saveContext();
}

/**
 * Get current stage checkpoints
 */
export function getStageCheckpoints(stage: number): string[] {
  // Stage to checkpoint mapping
  const stageCheckpoints: Record<number, string[]> = {
    1: ['CP_RESEARCH_DIRECTION', 'CP_VS_001'],
    2: ['CP_PARADIGM_SELECTION'],
    3: ['CP_THEORY_SELECTION', 'CP_VS_001', 'CP_VS_003'],
    4: ['CP_METHODOLOGY_APPROVAL'],
    5: ['CP_SCREENING_CRITERIA', 'CP_SAMPLING_STRATEGY'],
    6: ['CP_ANALYSIS_PLAN', 'CP_CODING_APPROACH'],
    7: ['CP_QUALITY_REVIEW', 'CP_THEME_VALIDATION'],
    8: ['CP_WRITING_STYLE'],
  };

  return stageCheckpoints[stage] || [];
}

/**
 * Clear context (for new project)
 */
export function clearContext(): void {
  _contextCache = null;

  const contextPath = getContextPath();
  if (fs.existsSync(contextPath)) {
    fs.unlinkSync(contextPath);
  }
}

/**
 * Parse YAML-like context (simple parser)
 */
function parseYamlContext(content: string): ResearchContext {
  const context = { ...DEFAULT_CONTEXT };
  const lines = content.split('\n');

  let currentKey: string | null = null;
  let inList = false;
  let listKey: string | null = null;

  for (const line of lines) {
    // Skip comments and empty lines
    if (line.startsWith('#') || line.trim() === '') {
      continue;
    }

    // Handle list items
    if (line.match(/^\s+-\s/)) {
      if (listKey && Array.isArray((context as any)[listKey])) {
        const value = line.replace(/^\s+-\s+/, '').trim();
        (context as any)[listKey].push(value);
      }
      continue;
    }

    // Handle key-value pairs
    const kvMatch = line.match(/^(\w+):\s*(.*)$/);
    if (kvMatch) {
      const [, key, value] = kvMatch;
      currentKey = key;

      if (value === '' || value === '|') {
        // Start of list or multiline
        if (['completedCheckpoints', 'pendingCheckpoints', 'decisions'].includes(key)) {
          listKey = key;
          (context as any)[key] = [];
        }
      } else {
        (context as any)[key] = value.replace(/^["']|["']$/g, '');
        listKey = null;
      }
    }
  }

  return context;
}

/**
 * Serialize context to YAML-like format
 */
function serializeYamlContext(context: ResearchContext): string {
  const lines: string[] = [
    '# Research Project State',
    `# Generated by Diverga v6.0.0`,
    '',
    `projectName: "${context.projectName}"`,
    `projectType: ${context.projectType}`,
    `paradigm: ${context.paradigm}`,
    `currentStage: ${context.currentStage}`,
    `createdAt: "${context.createdAt}"`,
    `updatedAt: "${context.updatedAt}"`,
    '',
  ];

  if (context.researchQuestion) {
    lines.push(`researchQuestion: "${context.researchQuestion}"`);
  }

  if (context.theoreticalFramework) {
    lines.push(`theoreticalFramework: "${context.theoreticalFramework}"`);
  }

  lines.push('');
  lines.push('completedCheckpoints:');
  for (const cp of context.completedCheckpoints) {
    lines.push(`  - ${cp}`);
  }

  lines.push('');
  lines.push('pendingCheckpoints:');
  for (const cp of context.pendingCheckpoints) {
    lines.push(`  - ${cp}`);
  }

  lines.push('');
  lines.push('decisions:');
  for (const decision of context.decisions) {
    lines.push(`  - checkpoint: ${decision.checkpoint}`);
    lines.push(`    timestamp: "${decision.timestamp}"`);
    lines.push(`    selected: "${decision.selected}"`);
  }

  return lines.join('\n');
}

export default {
  loadContext,
  saveContext,
  createContext,
  updateContext,
  clearContext,
};
