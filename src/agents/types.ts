/**
 * Diverga Agent Runtime - Type Definitions
 *
 * Shared types for the Diverga research agent system.
 * These types enable the Task tool to spawn agents via subagent_type="diverga:a1" etc.
 */

export type ModelType = 'opus' | 'sonnet' | 'haiku';
export type VSLevel = 'Full' | 'Enhanced' | 'Light';
export type TierLevel = 'HIGH' | 'MEDIUM' | 'LOW';

/**
 * Category identifiers for the 9 agent categories
 */
export type CategoryId = 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I';

/**
 * Category metadata
 */
export interface CategoryInfo {
  id: CategoryId;
  name: string;
  description: string;
}

/**
 * Checkpoint configuration for human-in-the-loop workflow
 */
export interface CheckpointConfig {
  id: string;
  level: 'REQUIRED' | 'RECOMMENDED' | 'OPTIONAL';
  description?: string;
}

/**
 * VS Methodology configuration
 */
export interface VSConfig {
  level: VSLevel;
  phases: number[];  // e.g., [0, 1, 2, 4] for Enhanced, [0, 1, 2, 3, 4, 5] for Full
  dynamicTScore: boolean;
  creativityModules: string[];
}

/**
 * Main agent configuration interface
 */
export interface AgentConfig {
  /** Agent name for Task tool (e.g., "diverga:a1") */
  name: string;

  /** Human-readable display name */
  displayName: string;

  /** Agent description for Task tool */
  description: string;

  /** Full system prompt (loaded from SKILL.md) */
  prompt: string;

  /** Allowed tools for this agent */
  tools: string[];

  /** Default model for this agent */
  model: ModelType;

  /** Default model (alias for compatibility) */
  defaultModel: ModelType;

  /** Agent metadata */
  metadata: AgentMetadata;
}

/**
 * Extended metadata for research agents
 */
export interface AgentMetadata {
  /** Category (A-I) */
  category: CategoryId;

  /** Category name */
  categoryName: string;

  /** Agent tier (HIGH/MEDIUM/LOW) */
  tier: TierLevel;

  /** VS methodology level */
  vsLevel: VSLevel;

  /** VS phases */
  vsPhases: number[];

  /** Human checkpoints */
  checkpoints: string[];

  /** Creativity modules enabled */
  creativityModules: string[];

  /** Trigger keywords (EN + KR) */
  triggers: string[];

  /** Icon */
  icon: string;

  /** Legacy numeric ID (if applicable) */
  legacyId?: string;

  /** Paradigm affinity */
  paradigmAffinity: string[];
}

/**
 * SKILL.md frontmatter structure
 */
export interface SkillFrontmatter {
  name: string;
  version?: string;
  description?: string;
  upgrade_level?: VSLevel;
  tier?: string;
  v3_integration?: {
    dynamic_t_score?: boolean;
    creativity_modules?: string[];
    checkpoints?: string[];
  };
}

/**
 * Parsed SKILL.md content
 */
export interface ParsedSkillFile {
  frontmatter: SkillFrontmatter;
  content: string;
}

/**
 * Agent ID mapping (shorthand to full path)
 */
export interface AgentIdMapping {
  shortId: string;      // e.g., "a1"
  fullId: string;       // e.g., "diverga:a1"
  directoryName: string; // e.g., "A1-research-question-refiner"
}

/**
 * Registry return type
 */
export type AgentRegistry = Record<string, AgentConfig>;

/**
 * Category definitions
 */
export const CATEGORIES: Record<CategoryId, CategoryInfo> = {
  A: { id: 'A', name: 'Research Foundation', description: 'Theory & Design' },
  B: { id: 'B', name: 'Literature & Evidence', description: 'Evidence gathering and synthesis' },
  C: { id: 'C', name: 'Study Design', description: 'Research methodology design' },
  D: { id: 'D', name: 'Data Collection', description: 'Data gathering methods' },
  E: { id: 'E', name: 'Analysis', description: 'Data analysis methods' },
  F: { id: 'F', name: 'Quality & Validation', description: 'Quality assurance' },
  G: { id: 'G', name: 'Publication & Communication', description: 'Research dissemination' },
  H: { id: 'H', name: 'Specialized Approaches', description: 'Specialized methodologies' },
  I: { id: 'I', name: 'Systematic Review Automation', description: 'Automated systematic literature review pipeline' },
};

/**
 * Model tier mapping
 */
export const MODEL_TIERS: Record<TierLevel, ModelType> = {
  HIGH: 'opus',
  MEDIUM: 'sonnet',
  LOW: 'haiku',
};

/**
 * Default tool sets by category
 */
export const CATEGORY_TOOLS: Record<CategoryId, string[]> = {
  A: ['Read', 'Glob', 'Grep', 'WebSearch'],
  B: ['Read', 'Glob', 'Grep', 'WebSearch', 'Bash'],
  C: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
  D: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
  E: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash'],
  F: ['Read', 'Glob', 'Grep'],
  G: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'WebSearch'],
  H: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'WebSearch'],
  I: ['Read', 'Glob', 'Grep', 'Bash', 'Task'],
};
