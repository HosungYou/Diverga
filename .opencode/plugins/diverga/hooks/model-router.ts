/**
 * Model Router Hook
 * Routes requests to appropriate model based on agent tier
 */

import type { ToolParams } from '../types';
import { getAgent } from '../agents';

/**
 * Model tier mapping
 */
const MODEL_TIERS = {
  HIGH: {
    claude: 'opus',
    codex: 'o1',
    opencode: 'opus',
  },
  MEDIUM: {
    claude: 'sonnet',
    codex: 'gpt-4',
    opencode: 'sonnet',
  },
  LOW: {
    claude: 'haiku',
    codex: 'gpt-3.5-turbo',
    opencode: 'haiku',
  },
} as const;

/**
 * Detect current platform
 */
function detectPlatform(): 'claude' | 'codex' | 'opencode' {
  // Check environment variables or process info
  if (process.env.CODEX_CLI) {
    return 'codex';
  }
  if (process.env.OPENCODE) {
    return 'opencode';
  }
  // Default to Claude
  return 'claude';
}

/**
 * Get model for a given tier and platform
 */
export function getModelForTier(
  tier: 'HIGH' | 'MEDIUM' | 'LOW',
  platform?: 'claude' | 'codex' | 'opencode'
): string {
  const p = platform || detectPlatform();
  return MODEL_TIERS[tier][p];
}

/**
 * Get model for a specific agent
 */
export function getModelForAgent(
  agentId: string,
  platform?: 'claude' | 'codex' | 'opencode'
): string {
  const agent = getAgent(agentId);
  if (!agent) {
    // Default to MEDIUM tier
    return getModelForTier('MEDIUM', platform);
  }
  return getModelForTier(agent.tier, platform);
}

/**
 * Model router hook
 * Modifies params to use appropriate model based on agent being invoked
 */
export function modelRouter(params: ToolParams): ToolParams {
  // Check if params contains agent information
  const agentId = extractAgentId(params);

  if (!agentId) {
    // No agent specified, return unchanged
    return params;
  }

  // Get appropriate model
  const model = getModelForAgent(agentId);

  // Add model to params
  return {
    ...params,
    arguments: {
      ...params.arguments,
      model,
      _divergaAgent: agentId,
    },
  };
}

/**
 * Extract agent ID from params
 */
function extractAgentId(params: ToolParams): string | null {
  // Check various places agent might be specified
  const args = params.arguments;

  if (args.agentId) {
    return args.agentId as string;
  }

  if (args.agent) {
    return args.agent as string;
  }

  // Check if subagent_type contains diverga agent
  if (args.subagent_type) {
    const subagent = args.subagent_type as string;
    const match = subagent.match(/diverga:([A-H]\d+)/i);
    if (match) {
      return match[1].toUpperCase();
    }
  }

  // Check description for agent pattern
  if (args.description) {
    const desc = args.description as string;
    const match = desc.match(/\b([A-H]\d+)[-:]/i);
    if (match) {
      return match[1].toUpperCase();
    }
  }

  return null;
}

/**
 * Get tier for complexity of task
 */
export function getTierForComplexity(complexity: 'simple' | 'standard' | 'complex'): 'HIGH' | 'MEDIUM' | 'LOW' {
  switch (complexity) {
    case 'simple': return 'LOW';
    case 'complex': return 'HIGH';
    default: return 'MEDIUM';
  }
}

/**
 * Estimate task complexity from prompt
 */
export function estimateComplexity(prompt: string): 'simple' | 'standard' | 'complex' {
  const lowerPrompt = prompt.toLowerCase();

  // Complex indicators
  const complexIndicators = [
    'design', 'architect', 'strategic', 'paradigm', 'framework',
    'integration', 'synthesis', 'theory', 'complex', 'comprehensive',
    'meta-analysis', 'mixed methods', 'ethnography', 'grounded theory',
  ];

  // Simple indicators
  const simpleIndicators = [
    'calculate', 'convert', 'extract', 'lookup', 'list',
    'check', 'verify', 'generate code', 'format',
  ];

  const complexCount = complexIndicators.filter(i => lowerPrompt.includes(i)).length;
  const simpleCount = simpleIndicators.filter(i => lowerPrompt.includes(i)).length;

  if (complexCount >= 2) {
    return 'complex';
  } else if (simpleCount >= 2 && complexCount === 0) {
    return 'simple';
  }

  return 'standard';
}

/**
 * Get recommended model based on prompt
 */
export function getRecommendedModel(prompt: string, platform?: 'claude' | 'codex' | 'opencode'): string {
  const complexity = estimateComplexity(prompt);
  const tier = getTierForComplexity(complexity);
  return getModelForTier(tier, platform);
}
