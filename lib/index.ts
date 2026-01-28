/**
 * Diverga Cross-Platform Research Agent Library
 *
 * Shared core module for agent discovery, parsing, and VS methodology
 * across Claude Code, OpenAI Codex CLI, and OpenCode platforms.
 */

// Agent system
export {
  discoverAgents,
  loadAgent,
  getAgentById,
  getAgentsByCategory,
  getAgentsByTier,
  getAgentsByParadigm,
  findAgentsByKeyword,
  getAgentSummary,
  exportRegistryToJson,
  importRegistryFromJson,
  DEFAULT_PATHS,
} from './agents/discovery';

export {
  parseSkillMd,
  extractFrontMatter,
  extractAgentId,
  validateAgentDefinition,
} from './agents/parser';

export type {
  AgentDefinition,
  AgentId,
  AgentRegistry,
  ModelTier,
  ClaudeModel,
  CodexModel,
  VSLevel,
  Paradigm,
  PlatformConfig,
  CategoryCode,
} from './agents/types';

export {
  CATEGORIES,
  MODEL_MAPPING,
  TOOL_MAPPING_CODEX,
} from './agents/types';

// Checkpoint system
export {
  CHECKPOINTS,
  getCheckpoint,
  getCheckpointsByLevel,
  getCheckpointsForAgent,
  getCheckpointsByCategory,
  validateCheckpoint,
  formatCheckpointPrompt,
  getRequiredCheckpoints,
  exportCheckpointsAsYaml,
} from './checkpoints/definitions';

export type { CheckpointDefinition, CheckpointLevel } from './agents/types';

// T-Score system
export {
  T_SCORE_RANGES,
  CREATIVITY_LEVELS,
  RQ_TYPICALITY_PATTERNS,
  lookupTScore,
  getTScoreLabel,
  getTScoreRiskLevel,
  isAppropriateForCreativityLevel,
  getRecommendedCreativityLevel,
  formatTScore,
  visualizeTScore,
  getTScoreReferenceTable,
  getVSDirectionTemplate,
  calculateDynamicTScore,
} from './tscore/reference';

export type { TScoreEntry } from './agents/types';
export type { CreativityLevel } from './tscore/reference';

/**
 * Initialize Diverga library with default paths
 */
export function initializeDiverga() {
  const { discoverAgents, DEFAULT_PATHS } = require('./agents/discovery');
  const registry = discoverAgents(DEFAULT_PATHS.userSkills);

  console.log(`Diverga initialized with ${registry.totalAgents} agents`);
  return registry;
}

/**
 * Get library version
 */
export const VERSION = '6.0.0';

/**
 * Platform adapters configuration
 */
export const PLATFORM_CONFIGS = {
  'claude-code': {
    platform: 'claude-code',
    modelMapping: {
      HIGH: 'opus',
      MEDIUM: 'sonnet',
      LOW: 'haiku',
    },
    toolMapping: {
      TodoWrite: 'TodoWrite',
      Task: 'Task',
      Read: 'Read',
      Edit: 'Edit',
      Grep: 'Grep',
      Bash: 'Bash',
      Write: 'Write',
      Glob: 'Glob',
    },
  },
  codex: {
    platform: 'codex',
    modelMapping: {
      HIGH: 'o1',
      MEDIUM: 'gpt-4',
      LOW: 'gpt-3.5-turbo',
    },
    toolMapping: {
      TodoWrite: 'update_plan',
      Task: 'direct_execution',
      Read: 'read_file',
      Edit: 'apply_diff',
      Grep: 'grep',
      Bash: 'shell',
      Write: 'write_file',
      Glob: 'glob',
    },
  },
  opencode: {
    platform: 'opencode',
    modelMapping: {
      HIGH: 'opus',
      MEDIUM: 'sonnet',
      LOW: 'haiku',
    },
    toolMapping: {
      // OpenCode uses same tools as Claude Code
      TodoWrite: 'TodoWrite',
      Task: 'Task',
      Read: 'Read',
      Edit: 'Edit',
      Grep: 'Grep',
      Bash: 'Bash',
      Write: 'Write',
      Glob: 'Glob',
    },
  },
} as const;
