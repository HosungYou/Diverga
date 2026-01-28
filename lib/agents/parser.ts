/**
 * Diverga SKILL.md Parser
 * Extracts agent definitions from SKILL.md files with YAML frontmatter
 */

import type {
  AgentDefinition,
  AgentId,
  ModelTier,
  ClaudeModel,
  CodexModel,
  VSLevel,
  Paradigm,
  MODEL_MAPPING,
} from './types';

// Simple YAML frontmatter parser (no external dependencies)
interface FrontMatter {
  name: string;
  version?: string;
  description?: string;
  tier?: string;
  model?: string;
  upgrade_level?: string;
  v3_integration?: {
    dynamic_t_score?: boolean;
    creativity_modules?: string[];
    checkpoints?: string[];
  };
  [key: string]: unknown;
}

/**
 * Extract YAML frontmatter from markdown content
 */
export function extractFrontMatter(content: string): FrontMatter | null {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const yamlContent = match[1];
  return parseSimpleYaml(yamlContent);
}

/**
 * Simple YAML parser for frontmatter (handles basic key-value and lists)
 */
function parseSimpleYaml(yaml: string): FrontMatter {
  const result: FrontMatter = { name: '' };
  const lines = yaml.split('\n');
  let currentKey: string | null = null;
  let currentList: string[] | null = null;
  let inMultiline = false;
  let multilineValue = '';

  for (const line of lines) {
    // Handle list items
    if (line.match(/^\s+-\s+/)) {
      const value = line.replace(/^\s+-\s+/, '').trim();
      if (currentList && currentKey) {
        currentList.push(value.replace(/^["']|["']$/g, ''));
      }
      continue;
    }

    // Handle multiline string continuation
    if (inMultiline) {
      if (line.match(/^\s{2,}/)) {
        multilineValue += ' ' + line.trim();
        continue;
      } else {
        if (currentKey) {
          result[currentKey] = multilineValue.trim();
        }
        inMultiline = false;
        multilineValue = '';
      }
    }

    // Handle key-value pairs
    const kvMatch = line.match(/^(\w+):\s*(.*)$/);
    if (kvMatch) {
      const [, key, value] = kvMatch;
      currentKey = key;

      if (value === '' || value === '|') {
        // Start of list or multiline
        currentList = [];
        result[key] = currentList;
        if (value === '|') {
          inMultiline = true;
          currentList = null;
        }
      } else if (value.startsWith('"') || value.startsWith("'")) {
        result[key] = value.replace(/^["']|["']$/g, '');
        currentList = null;
      } else if (value === 'true') {
        result[key] = true;
        currentList = null;
      } else if (value === 'false') {
        result[key] = false;
        currentList = null;
      } else if (!isNaN(Number(value))) {
        result[key] = Number(value);
        currentList = null;
      } else {
        result[key] = value;
        currentList = null;
      }
    }
  }

  return result;
}

/**
 * Extract agent ID from directory name or content
 * e.g., "A1-research-question-refiner" -> "A1"
 */
export function extractAgentId(dirName: string): AgentId {
  const match = dirName.match(/^([A-H]\d+)/i);
  return match ? match[1].toUpperCase() : dirName;
}

/**
 * Map tier string to ModelTier
 */
function mapTier(tier?: string): ModelTier {
  const t = (tier || 'MEDIUM').toUpperCase();
  if (t === 'HIGH' || t === 'CORE') return 'HIGH';
  if (t === 'LOW') return 'LOW';
  return 'MEDIUM';
}

/**
 * Map VS level string
 */
function mapVSLevel(level?: string): VSLevel {
  const l = (level || 'Enhanced').toLowerCase();
  if (l.includes('full')) return 'Full';
  if (l.includes('light')) return 'Light';
  return 'Enhanced';
}

/**
 * Get Claude model from tier
 */
function getClaudeModel(tier: ModelTier): ClaudeModel {
  switch (tier) {
    case 'HIGH': return 'opus';
    case 'LOW': return 'haiku';
    default: return 'sonnet';
  }
}

/**
 * Get Codex model from tier
 */
function getCodexModel(tier: ModelTier): CodexModel {
  switch (tier) {
    case 'HIGH': return 'o1';
    case 'LOW': return 'gpt-3.5-turbo';
    default: return 'gpt-4';
  }
}

/**
 * Parse triggers from SKILL.md content
 */
function extractTriggers(content: string, frontMatter: FrontMatter): { keywords: string[]; context?: string[] } {
  // First check frontmatter description for triggers
  const desc = frontMatter.description || '';
  const triggerMatch = desc.match(/Triggers?:\s*([^\n]+)/i);

  let keywords: string[] = [];
  if (triggerMatch) {
    keywords = triggerMatch[1].split(',').map(k => k.trim());
  }

  // Also look in content for "When to Use" or "Triggers" section
  const whenToUse = content.match(/## When to Use\n([\s\S]*?)(?=\n##|$)/);
  if (whenToUse) {
    const bulletPoints = whenToUse[1].match(/- ([^\n]+)/g);
    if (bulletPoints) {
      keywords = [...keywords, ...bulletPoints.map(b => b.replace(/^- /, '').trim())];
    }
  }

  return {
    keywords: [...new Set(keywords)].filter(k => k.length > 0),
    context: [],
  };
}

/**
 * Extract capabilities from content
 */
function extractCapabilities(content: string): string[] {
  const capabilities: string[] = [];

  // Look for capabilities section or bullet points after "Core Features"
  const capSection = content.match(/## (?:Core Features|Capabilities|Overview)\n([\s\S]*?)(?=\n##|$)/);
  if (capSection) {
    const bullets = capSection[1].match(/- ([^\n]+)/g);
    if (bullets) {
      capabilities.push(...bullets.map(b => b.replace(/^- /, '').replace(/\*\*/g, '').trim()));
    }
  }

  // Also check numbered items
  const numbered = content.match(/\d+\.\s+\*\*([^*]+)\*\*/g);
  if (numbered) {
    capabilities.push(...numbered.map(n => n.replace(/^\d+\.\s+\*\*|\*\*$/g, '').trim()));
  }

  return capabilities.slice(0, 8); // Limit to 8 capabilities
}

/**
 * Extract category from agent ID
 */
function extractCategory(agentId: AgentId): string {
  const categoryMap: Record<string, string> = {
    'A': 'A - Research Foundation',
    'B': 'B - Literature & Evidence',
    'C': 'C - Study Design',
    'D': 'D - Data Collection',
    'E': 'E - Analysis',
    'F': 'F - Quality & Validation',
    'G': 'G - Publication & Communication',
    'H': 'H - Specialized Approaches',
  };

  const prefix = agentId.charAt(0).toUpperCase();
  return categoryMap[prefix] || 'Unknown';
}

/**
 * Parse a SKILL.md file into an AgentDefinition
 */
export function parseSkillMd(
  content: string,
  dirName: string,
  skillPath: string
): AgentDefinition | null {
  const frontMatter = extractFrontMatter(content);
  if (!frontMatter || !frontMatter.name) {
    return null;
  }

  const agentId = extractAgentId(dirName);
  const tier = mapTier(frontMatter.tier as string);

  // Extract icon from content
  const iconMatch = content.match(/\*\*Icon\*\*:\s*(\S+)/);
  const icon = iconMatch ? iconMatch[1] : '🔬';

  // Extract VS level
  const vsLevelMatch = content.match(/\*\*VS Level\*\*:\s*(\w+)/);
  const vsLevel = mapVSLevel(vsLevelMatch?.[1] || frontMatter.upgrade_level as string);

  // Build agent definition
  const agent: AgentDefinition = {
    id: agentId,
    name: frontMatter.name,
    description: typeof frontMatter.description === 'string'
      ? frontMatter.description.split('\n')[0].trim()
      : `Agent ${agentId}`,
    version: frontMatter.version?.toString() || '1.0.0',
    icon,

    category: extractCategory(agentId),
    tier,
    vsLevel,

    claudeModel: getClaudeModel(tier),
    codexModel: getCodexModel(tier),

    capabilities: extractCapabilities(content),
    triggers: extractTriggers(content, frontMatter),

    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],

    skillPath,
  };

  // Add VS integration data if present
  if (frontMatter.v3_integration) {
    const v3 = frontMatter.v3_integration;
    agent.creativityModules = v3.creativity_modules;
    agent.checkpoints = v3.checkpoints;
  }

  // Extract VS phases from content
  const vsPhaseMatch = content.match(/vs_phases:\s*\[([^\]]+)\]/);
  if (vsPhaseMatch) {
    agent.vsPhases = vsPhaseMatch[1].split(',').map(p => parseInt(p.trim()));
  }

  // Extract T-Score domains
  const tScoreSection = content.match(/## Research Question Typicality Score Reference\n([\s\S]*?)(?=\n##|$)/);
  if (tScoreSection) {
    agent.tScoreDomains = ['Research methodology', 'Academic contribution'];
  }

  return agent;
}

/**
 * Validate agent definition
 */
export function validateAgentDefinition(agent: AgentDefinition): string[] {
  const errors: string[] = [];

  if (!agent.id) errors.push('Missing agent ID');
  if (!agent.name) errors.push('Missing agent name');
  if (!agent.description) errors.push('Missing description');
  if (!['HIGH', 'MEDIUM', 'LOW'].includes(agent.tier)) errors.push('Invalid tier');
  if (!['Full', 'Enhanced', 'Light'].includes(agent.vsLevel)) errors.push('Invalid VS level');

  return errors;
}
