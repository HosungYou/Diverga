/**
 * Diverga Cross-Platform Agent Types
 * TypeScript definitions for agent system
 */

// Agent ID pattern: A1, A2, B1, etc.
export type AgentId = string;

// Model tiers
export type ModelTier = 'HIGH' | 'MEDIUM' | 'LOW';

// Model mapping for different platforms
export type ClaudeModel = 'opus' | 'sonnet' | 'haiku';
export type CodexModel = 'o1' | 'gpt-4' | 'gpt-3.5-turbo';

// VS methodology levels
export type VSLevel = 'Full' | 'Enhanced' | 'Light';

// Research paradigms
export type Paradigm = 'quantitative' | 'qualitative' | 'mixed';

// Checkpoint levels
export type CheckpointLevel = 'REQUIRED' | 'RECOMMENDED' | 'OPTIONAL';

/**
 * Agent definition parsed from SKILL.md
 */
export interface AgentDefinition {
  // Core identity
  id: AgentId;
  name: string;
  description: string;
  version: string;
  icon?: string;

  // Classification
  category: string;
  tier: ModelTier;
  vsLevel: VSLevel;

  // Model routing
  claudeModel: ClaudeModel;
  codexModel: CodexModel;

  // Capabilities
  capabilities: string[];
  triggers: {
    keywords: string[];
    context?: string[];
  };

  // Paradigm support
  paradigmAffinity: Paradigm[];

  // VS methodology
  vsPhases?: number[];
  creativityModules?: string[];
  checkpoints?: string[];

  // Dependencies
  dependencies?: {
    requires?: AgentId[];
    sequentialNext?: AgentId[];
    parallelCompatible?: AgentId[];
  };

  // Input/Output schemas
  inputSchema?: {
    required: Record<string, string>;
    optional?: Record<string, string>;
  };
  outputSchema?: {
    mainOutput: Record<string, string>;
  };

  // T-Score domains
  tScoreDomains?: string[];

  // Original path to SKILL.md
  skillPath: string;
}

/**
 * Checkpoint definition
 */
export interface CheckpointDefinition {
  id: string;
  name: string;
  level: CheckpointLevel;
  when: string;
  whatToAsk: string;
  icon: string;
  category: string;
  agentsUsing: AgentId[];
}

/**
 * T-Score reference entry
 */
export interface TScoreEntry {
  range: [number, number];
  label: string;
  meaning: string;
  suitableFor: string;
  riskLevel: 'low' | 'medium' | 'high' | 'experimental';
}

/**
 * Agent registry containing all agents
 */
export interface AgentRegistry {
  version: string;
  lastUpdated: string;
  totalAgents: number;
  agents: Map<AgentId, AgentDefinition>;
  categories: Map<string, AgentId[]>;
}

/**
 * Platform-specific configuration
 */
export interface PlatformConfig {
  platform: 'claude-code' | 'codex' | 'opencode';
  modelMapping: Record<ModelTier, string>;
  toolMapping: Record<string, string>;
}

/**
 * Model tier to model name mapping
 */
export const MODEL_MAPPING = {
  claude: {
    HIGH: 'opus',
    MEDIUM: 'sonnet',
    LOW: 'haiku',
  } as Record<ModelTier, ClaudeModel>,

  codex: {
    HIGH: 'o1',
    MEDIUM: 'gpt-4',
    LOW: 'gpt-3.5-turbo',
  } as Record<ModelTier, CodexModel>,
} as const;

/**
 * Tool mapping from Claude Code to Codex
 */
export const TOOL_MAPPING_CODEX: Record<string, string> = {
  'TodoWrite': 'update_plan',
  'Task': 'direct_execution',
  'Read': 'read_file',
  'Edit': 'apply_diff',
  'Grep': 'grep',
  'Bash': 'shell',
  'Write': 'write_file',
  'Glob': 'glob',
};

/**
 * Category definitions
 */
export const CATEGORIES = {
  A: 'Research Foundation',
  B: 'Literature & Evidence',
  C: 'Study Design',
  D: 'Data Collection',
  E: 'Analysis',
  F: 'Quality & Validation',
  G: 'Publication & Communication',
  H: 'Specialized Approaches',
} as const;

export type CategoryCode = keyof typeof CATEGORIES;
