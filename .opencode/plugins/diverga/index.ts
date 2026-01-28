/**
 * Diverga OpenCode Plugin
 * Multi-agent research coordinator for OpenCode
 *
 * Based on oh-my-opencode plugin architecture
 * https://github.com/code-yeongyu/oh-my-opencode
 */

import type { Plugin, PluginContext, HookResult } from './types';
import { checkpointEnforcer } from './hooks/checkpoint-enforcer';
import { autoTrigger } from './hooks/auto-trigger';
import { vsDisplay } from './hooks/vs-display';
import { modelRouter } from './hooks/model-router';
import { loadContext, saveContext } from './hooks/context-manager';
import { AGENT_REGISTRY, getAgent, listAgents as getAgentList } from './agents';
import { CHECKPOINTS, formatCheckpoint } from './checkpoints';
import { T_SCORE_REFERENCE, formatTScoreTable } from './tscore';

/**
 * Diverga Plugin Configuration
 */
export const PLUGIN_CONFIG = {
  name: 'diverga',
  version: '6.0.0',
  description: 'Research Coordinator - Multi-agent system for social science research',
};

/**
 * Plugin initialization
 */
export function initialize(context: PluginContext): Plugin {
  console.log(`[Diverga] Initializing v${PLUGIN_CONFIG.version}`);

  // Load research context if exists
  const researchContext = loadContext();
  if (researchContext) {
    console.log(`[Diverga] Loaded research context: ${researchContext.projectName}`);
  }

  return {
    name: PLUGIN_CONFIG.name,
    version: PLUGIN_CONFIG.version,

    // Hook registrations
    hooks: {
      'tool.execute.before': async (params) => {
        // Check for checkpoints
        const checkpointResult = await checkpointEnforcer(params, context);
        if (!checkpointResult.proceed) {
          return checkpointResult;
        }

        // Route to correct model
        const routedParams = modelRouter(params);
        return { proceed: true, params: routedParams };
      },

      'tool.execute.after': async (params, result) => {
        // Display VS alternatives if applicable
        await vsDisplay(params, result, context);

        // Update context state
        await saveContext(context);

        return result;
      },

      'tui.prompt.append': (prompt: string) => {
        // Auto-trigger agent detection
        const detectedAgent = autoTrigger(prompt);
        if (detectedAgent) {
          return {
            append: `\n\n[Diverga: Agent ${detectedAgent.id} (${detectedAgent.name}) activated]`,
            agent: detectedAgent,
          };
        }
        return { append: '' };
      },

      'session.created': () => {
        // Inject system prompt additions
        return {
          systemPrompt: getSystemPromptAdditions(),
        };
      },
    },

    // Command handlers
    commands: {
      'diverga:list': () => listAgents(),
      'diverga:agent': (args) => showAgent(args.agentId),
      'diverga:checkpoint': () => showCheckpoints(),
      'diverga:tscore': () => showTScore(),
      'diverga:context': () => showContext(),
      'diverga:vs': () => showVSMethodology(),
    },
  };
}

/**
 * List all agents
 */
function listAgents(): string {
  const agents = getAgentList();
  const output: string[] = [
    '╔═══════════════════════════════════════════════════════════════╗',
    '║                  Diverga Agent Catalog                        ║',
    '╚═══════════════════════════════════════════════════════════════╝',
    '',
  ];

  // Group by category
  const categories = new Map<string, typeof agents>();
  for (const agent of agents) {
    const existing = categories.get(agent.category) || [];
    existing.push(agent);
    categories.set(agent.category, existing);
  }

  for (const [category, categoryAgents] of categories) {
    output.push(`\n## ${category}\n`);
    for (const agent of categoryAgents) {
      output.push(`  ${agent.icon} ${agent.id}: ${agent.name} (${agent.tier})`);
    }
  }

  output.push(`\n\nTotal: ${agents.length} agents`);
  return output.join('\n');
}

/**
 * Show agent details
 */
function showAgent(agentId: string): string {
  const agent = getAgent(agentId);
  if (!agent) {
    return `Agent "${agentId}" not found. Use "diverga:list" to see all agents.`;
  }

  return `
╔═══════════════════════════════════════════════════════════════╗
║  ${agent.icon} ${agent.id}: ${agent.name.padEnd(45)}║
╚═══════════════════════════════════════════════════════════════╝

Category:     ${agent.category}
Tier:         ${agent.tier}
Model:        ${agent.claudeModel}
VS Level:     ${agent.vsLevel}

Description:
${agent.description}

Triggers:
${agent.triggers.keywords.map(k => `  - ${k}`).join('\n')}

Checkpoints:
${(agent.checkpoints || []).map(c => `  - ${c}`).join('\n') || '  (none)'}
`;
}

/**
 * Show checkpoints
 */
function showCheckpoints(): string {
  const output: string[] = [
    '╔═══════════════════════════════════════════════════════════════╗',
    '║                  Checkpoint Reference                         ║',
    '╚═══════════════════════════════════════════════════════════════╝',
    '',
    'REQUIRED CHECKPOINTS (🔴 MANDATORY HALT)',
    '─────────────────────────────────────────',
  ];

  for (const cp of CHECKPOINTS.filter(c => c.level === 'REQUIRED')) {
    output.push(`  ${cp.id.padEnd(28)} ${cp.when}`);
  }

  output.push('');
  output.push('RECOMMENDED CHECKPOINTS (🟠 SUGGESTED HALT)');
  output.push('─────────────────────────────────────────');

  for (const cp of CHECKPOINTS.filter(c => c.level === 'RECOMMENDED')) {
    output.push(`  ${cp.id.padEnd(28)} ${cp.when}`);
  }

  output.push('');
  output.push('OPTIONAL CHECKPOINTS (🟡 DEFAULTS AVAILABLE)');
  output.push('─────────────────────────────────────────');

  for (const cp of CHECKPOINTS.filter(c => c.level === 'OPTIONAL')) {
    output.push(`  ${cp.id.padEnd(28)} ${cp.when}`);
  }

  return output.join('\n');
}

/**
 * Show T-Score reference
 */
function showTScore(): string {
  return formatTScoreTable();
}

/**
 * Show current context
 */
function showContext(): string {
  const context = loadContext();

  if (!context) {
    return `
╔═══════════════════════════════════════════════════════════════╗
║                  Research Project Context                     ║
╚═══════════════════════════════════════════════════════════════╝

No active research project found.

To start a new project, use a research-related prompt such as:
- "I want to conduct a systematic review on AI in education"
- "Help me design a phenomenological study"
- "메타분석 연구를 시작하고 싶어"
`;
  }

  return `
╔═══════════════════════════════════════════════════════════════╗
║                  Research Project Context                     ║
╚═══════════════════════════════════════════════════════════════╝

Project:        ${context.projectName}
Type:           ${context.projectType}
Paradigm:       ${context.paradigm}
Current Stage:  ${context.currentStage}
Created:        ${context.createdAt}

Research Question:
${context.researchQuestion || '(not set)'}

Theoretical Framework:
${context.theoreticalFramework || '(not set)'}

Completed Checkpoints:
${context.completedCheckpoints.map(c => `  ✅ ${c}`).join('\n') || '  (none)'}

Pending Checkpoints:
${context.pendingCheckpoints.map(c => `  ⏳ ${c}`).join('\n') || '  (none)'}
`;
}

/**
 * Show VS methodology explanation
 */
function showVSMethodology(): string {
  return `
╔═══════════════════════════════════════════════════════════════╗
║                  VS Methodology Explained                     ║
╚═══════════════════════════════════════════════════════════════╝

VS (Verbalized Sampling) prevents AI "mode collapse" - the tendency
to always recommend the most common approaches.

PROCESS:
─────────────────────────────────────────────────────────────────

  Phase 1: MODAL IDENTIFICATION
  ┌─────────────────────────────────────────────────────────────┐
  │ Explicitly identify the most predictable recommendations     │
  │ (T > 0.7) and mark them as BASELINE to exceed               │
  └─────────────────────────────────────────────────────────────┘
                               │
                               ▼
  Phase 2: LONG-TAIL SAMPLING
  ┌─────────────────────────────────────────────────────────────┐
  │ Generate alternatives across the T-Score spectrum:           │
  │   Direction A (T ≈ 0.7): Safe differentiation               │
  │   Direction B (T ≈ 0.4): Balanced novelty                   │
  │   Direction C (T < 0.3): Innovative approach                │
  └─────────────────────────────────────────────────────────────┘
                               │
                               ▼
  Phase 3: HUMAN SELECTION (🔴 CHECKPOINT)
  ┌─────────────────────────────────────────────────────────────┐
  │ Present ALL options with T-Scores                           │
  │ WAIT for explicit user selection                            │
  │ Execute selected direction                                   │
  └─────────────────────────────────────────────────────────────┘
`;
}

/**
 * Get system prompt additions for session
 */
function getSystemPromptAdditions(): string {
  return `
# Diverga Research Coordinator v6.0

You are enhanced with Diverga - a multi-agent system for social science research.

## Core Principles

1. **Human decisions remain with humans** - Stop at checkpoints and wait for approval
2. **VS Methodology** - Always present alternatives with T-Scores, never single recommendations
3. **Paradigm support** - Quantitative, qualitative, and mixed methods

## Checkpoint Protocol

At REQUIRED checkpoints (🔴):
1. STOP immediately
2. Present options with VS alternatives
3. WAIT for explicit user approval
4. DO NOT proceed until approval received

❌ NEVER: "Proceeding with..." without asking
✅ ALWAYS: "Which direction would you like? (A/B/C)"

## T-Score Reference

| T-Score | Label | Risk |
|---------|-------|------|
| ≥ 0.7 | Common | 🟢 Low |
| 0.4-0.7 | Moderate | 🟡 Medium |
| 0.2-0.4 | Innovative | 🟠 High |
| < 0.2 | Experimental | 🔴 Experimental |

## Available Agents (40)

Categories: Research Foundation, Literature & Evidence, Study Design,
Data Collection, Analysis, Quality & Validation, Publication, Specialized

Use keyword detection to activate appropriate agents automatically.
`;
}

// Export for external use
export { AGENT_REGISTRY, CHECKPOINTS, T_SCORE_REFERENCE };
export default { initialize, PLUGIN_CONFIG };
