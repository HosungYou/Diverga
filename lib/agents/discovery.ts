/**
 * Diverga Agent Discovery
 * Scans .claude/skills/research-agents/ and parses SKILL.md files
 */

import * as fs from 'fs';
import * as path from 'path';
import type { AgentDefinition, AgentId, AgentRegistry, CategoryCode } from './types';
import { parseSkillMd, extractAgentId, validateAgentDefinition } from './parser';
import { CATEGORIES } from './types';

/**
 * Default paths for agent discovery
 */
export const DEFAULT_PATHS = {
  // User's global Claude skills
  userSkills: path.join(process.env.HOME || '~', '.claude', 'skills', 'research-agents'),
  // Project-local skills
  projectSkills: path.join(process.cwd(), '.claude', 'skills', 'research-agents'),
  // Research coordinator
  coordinator: path.join(process.env.HOME || '~', '.claude', 'skills', 'research-coordinator'),
};

/**
 * Discover all agent SKILL.md files in a directory
 */
export function discoverAgentPaths(basePath: string): string[] {
  const paths: string[] = [];

  if (!fs.existsSync(basePath)) {
    return paths;
  }

  const entries = fs.readdirSync(basePath, { withFileTypes: true });

  for (const entry of entries) {
    if (entry.isDirectory()) {
      const skillPath = path.join(basePath, entry.name, 'SKILL.md');
      if (fs.existsSync(skillPath)) {
        paths.push(skillPath);
      }
    }
  }

  return paths.sort();
}

/**
 * Load a single agent from its SKILL.md path
 */
export function loadAgent(skillPath: string): AgentDefinition | null {
  try {
    const content = fs.readFileSync(skillPath, 'utf-8');
    const dirName = path.basename(path.dirname(skillPath));
    return parseSkillMd(content, dirName, skillPath);
  } catch (error) {
    console.error(`Failed to load agent from ${skillPath}:`, error);
    return null;
  }
}

/**
 * Discover and load all agents from default paths
 */
export function discoverAgents(customPath?: string): AgentRegistry {
  const searchPath = customPath || DEFAULT_PATHS.userSkills;
  const skillPaths = discoverAgentPaths(searchPath);

  const agents = new Map<AgentId, AgentDefinition>();
  const categories = new Map<string, AgentId[]>();

  // Initialize category arrays
  for (const code of Object.keys(CATEGORIES)) {
    categories.set(CATEGORIES[code as CategoryCode], []);
  }

  for (const skillPath of skillPaths) {
    const agent = loadAgent(skillPath);
    if (agent) {
      // Validate
      const errors = validateAgentDefinition(agent);
      if (errors.length > 0) {
        console.warn(`Agent ${agent.id} has validation errors:`, errors);
      }

      agents.set(agent.id, agent);

      // Add to category
      const categoryAgents = categories.get(agent.category) || [];
      categoryAgents.push(agent.id);
      categories.set(agent.category, categoryAgents);
    }
  }

  return {
    version: '6.0.0',
    lastUpdated: new Date().toISOString().split('T')[0],
    totalAgents: agents.size,
    agents,
    categories,
  };
}

/**
 * Get an agent by ID
 */
export function getAgentById(registry: AgentRegistry, id: AgentId): AgentDefinition | undefined {
  // Try exact match
  if (registry.agents.has(id)) {
    return registry.agents.get(id);
  }

  // Try case-insensitive
  const upperId = id.toUpperCase();
  for (const [agentId, agent] of registry.agents) {
    if (agentId.toUpperCase() === upperId) {
      return agent;
    }
  }

  return undefined;
}

/**
 * Get agents by category
 */
export function getAgentsByCategory(registry: AgentRegistry, category: string): AgentDefinition[] {
  const agentIds = registry.categories.get(category) || [];
  return agentIds.map(id => registry.agents.get(id)).filter((a): a is AgentDefinition => a !== undefined);
}

/**
 * Get agents by tier
 */
export function getAgentsByTier(registry: AgentRegistry, tier: 'HIGH' | 'MEDIUM' | 'LOW'): AgentDefinition[] {
  const result: AgentDefinition[] = [];
  for (const agent of registry.agents.values()) {
    if (agent.tier === tier) {
      result.push(agent);
    }
  }
  return result;
}

/**
 * Get agents by paradigm affinity
 */
export function getAgentsByParadigm(
  registry: AgentRegistry,
  paradigm: 'quantitative' | 'qualitative' | 'mixed'
): AgentDefinition[] {
  const result: AgentDefinition[] = [];
  for (const agent of registry.agents.values()) {
    if (agent.paradigmAffinity.includes(paradigm)) {
      result.push(agent);
    }
  }
  return result;
}

/**
 * Find agents by trigger keyword
 */
export function findAgentsByKeyword(registry: AgentRegistry, keyword: string): AgentDefinition[] {
  const lowerKeyword = keyword.toLowerCase();
  const result: AgentDefinition[] = [];

  for (const agent of registry.agents.values()) {
    const triggers = agent.triggers.keywords.map(k => k.toLowerCase());
    if (triggers.some(t => t.includes(lowerKeyword) || lowerKeyword.includes(t))) {
      result.push(agent);
    }
  }

  return result;
}

/**
 * Get agent summary for display
 */
export function getAgentSummary(agent: AgentDefinition): string {
  return `${agent.icon || '🔬'} ${agent.id}: ${agent.name} (${agent.tier})
  ${agent.description}
  Triggers: ${agent.triggers.keywords.slice(0, 5).join(', ')}`;
}

/**
 * Export registry to JSON (for Codex)
 */
export function exportRegistryToJson(registry: AgentRegistry): string {
  const exportData = {
    version: registry.version,
    lastUpdated: registry.lastUpdated,
    totalAgents: registry.totalAgents,
    agents: Object.fromEntries(registry.agents),
    categories: Object.fromEntries(registry.categories),
  };

  return JSON.stringify(exportData, null, 2);
}

/**
 * Import registry from JSON
 */
export function importRegistryFromJson(json: string): AgentRegistry {
  const data = JSON.parse(json);
  return {
    version: data.version,
    lastUpdated: data.lastUpdated,
    totalAgents: data.totalAgents,
    agents: new Map(Object.entries(data.agents)),
    categories: new Map(Object.entries(data.categories)),
  };
}
