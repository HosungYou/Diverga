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
 * ANSI Color codes for terminal output
 */
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  cyan: '\x1b[36m',
  yellow: '\x1b[33m',
  green: '\x1b[32m',
  magenta: '\x1b[35m',
  blue: '\x1b[34m',
  red: '\x1b[31m',
  white: '\x1b[37m',
};

/**
 * ASCII Art Banner
 */
const BANNER = `${colors.cyan}
    ██████╗ ██╗██╗   ██╗███████╗██████╗  ██████╗  █████╗
    ██╔══██╗██║██║   ██║██╔════╝██╔══██╗██╔════╝ ██╔══██╗
    ██║  ██║██║██║   ██║█████╗  ██████╔╝██║  ███╗███████║
    ██║  ██║██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██║   ██║██╔══██║
    ██████╔╝██║ ╚████╔╝ ███████╗██║  ██║╚██████╔╝██║  ██║
    ╚═════╝ ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
${colors.reset}
${colors.yellow}    🎯 Diverge from the Modal · Discover the Exceptional${colors.reset}
${colors.dim}    ─────────────────────────────────────────────────────${colors.reset}
`;

/**
 * Diverga Plugin Configuration
 */
export const PLUGIN_CONFIG = {
  name: 'diverga',
  version: '6.6.1',
  description: 'Research Coordinator - Multi-agent system for social science research',
};

/**
 * Plugin initialization
 */
export function initialize(context: PluginContext): Plugin {
  console.log(BANNER);
  console.log(`${colors.bright}    Research Coordinator for OpenCode${colors.reset}  │  ${colors.green}v${PLUGIN_CONFIG.version}${colors.reset}  │  ${colors.cyan}40 Agents${colors.reset}`);
  console.log(`${colors.dim}    Powered by VS (Verbalized Sampling) Methodology${colors.reset}\n`);

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
      'tool.execute.before': async (params): Promise<HookResult> => {
        // Check for checkpoints
        const checkpointResult = await checkpointEnforcer(params, context);
        if (!checkpointResult.proceed) {
          return checkpointResult;
        }

        // Route to correct model
        const routedParams = modelRouter(params);
        return { proceed: true, params: routedParams as unknown as Record<string, unknown> };
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
      'diverga:agent': (args) => showAgent(args?.agentId ?? ''),
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
  const tierColors: Record<string, string> = {
    HIGH: colors.red,
    MEDIUM: colors.yellow,
    LOW: colors.green,
  };
  const output: string[] = [
    BANNER,
    `${colors.bright}    Agent Catalog${colors.reset}  │  ${colors.cyan}${agents.length} Agents${colors.reset}`,
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
    output.push(`\n${colors.bright}${category}${colors.reset}\n`);
    for (const agent of categoryAgents) {
      const tierColor = tierColors[agent.tier] || colors.white;
      output.push(`  ${agent.icon} ${colors.cyan}${agent.id}${colors.reset}: ${agent.name} ${tierColor}(${agent.tier})${colors.reset}`);
    }
  }

  output.push(`\n${colors.dim}Total: ${agents.length} agents${colors.reset}`);
  return output.join('\n');
}

/**
 * Show agent details
 */
function showAgent(agentId: string): string {
  const agent = getAgent(agentId);
  if (!agent) {
    return `${colors.red}Agent "${agentId}" not found.${colors.reset} Use ${colors.cyan}diverga:list${colors.reset} to see all agents.`;
  }

  const tierColors: Record<string, string> = {
    HIGH: colors.red,
    MEDIUM: colors.yellow,
    LOW: colors.green,
  };
  const tierColor = tierColors[agent.tier] || colors.white;

  return `${BANNER}
${colors.bright}    ${agent.icon} ${agent.id}: ${agent.name}${colors.reset}

${colors.cyan}Category:${colors.reset}     ${agent.category}
${colors.cyan}Tier:${colors.reset}         ${tierColor}${agent.tier}${colors.reset}
${colors.cyan}Model:${colors.reset}        ${agent.claudeModel}
${colors.cyan}VS Level:${colors.reset}     ${agent.vsLevel}

${colors.bright}Description:${colors.reset}
${agent.description}

${colors.bright}Triggers:${colors.reset}
${agent.triggers.keywords.map(k => `  ${colors.green}•${colors.reset} ${k}`).join('\n')}

${colors.bright}Checkpoints:${colors.reset}
${(agent.checkpoints || []).map(c => `  ${colors.yellow}•${colors.reset} ${c}`).join('\n') || `  ${colors.dim}(none)${colors.reset}`}
`;
}

/**
 * Show checkpoints
 */
function showCheckpoints(): string {
  const output: string[] = [
    BANNER,
    `${colors.bright}    Checkpoint Reference${colors.reset}`,
    '',
    `${colors.red}REQUIRED CHECKPOINTS (🔴 MANDATORY HALT)${colors.reset}`,
    `${colors.dim}─────────────────────────────────────────${colors.reset}`,
  ];

  for (const cp of CHECKPOINTS.filter(c => c.level === 'REQUIRED')) {
    output.push(`  ${colors.red}●${colors.reset} ${colors.cyan}${cp.id.padEnd(28)}${colors.reset} ${cp.when}`);
  }

  output.push('');
  output.push(`${colors.yellow}RECOMMENDED CHECKPOINTS (🟠 SUGGESTED HALT)${colors.reset}`);
  output.push(`${colors.dim}─────────────────────────────────────────${colors.reset}`);

  for (const cp of CHECKPOINTS.filter(c => c.level === 'RECOMMENDED')) {
    output.push(`  ${colors.yellow}●${colors.reset} ${colors.cyan}${cp.id.padEnd(28)}${colors.reset} ${cp.when}`);
  }

  output.push('');
  output.push(`${colors.green}OPTIONAL CHECKPOINTS (🟡 DEFAULTS AVAILABLE)${colors.reset}`);
  output.push(`${colors.dim}─────────────────────────────────────────${colors.reset}`);

  for (const cp of CHECKPOINTS.filter(c => c.level === 'OPTIONAL')) {
    output.push(`  ${colors.green}●${colors.reset} ${colors.cyan}${cp.id.padEnd(28)}${colors.reset} ${cp.when}`);
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
    return `${BANNER}
${colors.bright}    Research Project Context${colors.reset}

${colors.yellow}No active research project found.${colors.reset}

To start a new project, use a research-related prompt such as:
  ${colors.green}•${colors.reset} "I want to conduct a systematic review on AI in education"
  ${colors.green}•${colors.reset} "Help me design a phenomenological study"
  ${colors.green}•${colors.reset} "메타분석 연구를 시작하고 싶어"
`;
  }

  return `${BANNER}
${colors.bright}    Research Project Context${colors.reset}

${colors.cyan}Project:${colors.reset}        ${context.projectName}
${colors.cyan}Type:${colors.reset}           ${context.projectType}
${colors.cyan}Paradigm:${colors.reset}       ${context.paradigm}
${colors.cyan}Current Stage:${colors.reset}  ${context.currentStage}
${colors.cyan}Created:${colors.reset}        ${context.createdAt}

${colors.bright}Research Question:${colors.reset}
${context.researchQuestion || `${colors.dim}(not set)${colors.reset}`}

${colors.bright}Theoretical Framework:${colors.reset}
${context.theoreticalFramework || `${colors.dim}(not set)${colors.reset}`}

${colors.bright}Completed Checkpoints:${colors.reset}
${context.completedCheckpoints.map(c => `  ${colors.green}✅${colors.reset} ${c}`).join('\n') || `  ${colors.dim}(none)${colors.reset}`}

${colors.bright}Pending Checkpoints:${colors.reset}
${context.pendingCheckpoints.map(c => `  ${colors.yellow}⏳${colors.reset} ${c}`).join('\n') || `  ${colors.dim}(none)${colors.reset}`}
`;
}

/**
 * Show VS methodology explanation
 */
function showVSMethodology(): string {
  return `${BANNER}
${colors.bright}    VS Methodology Explained${colors.reset}

${colors.cyan}VS (Verbalized Sampling)${colors.reset} prevents AI "mode collapse" - the tendency
to always recommend the most common approaches.

${colors.bright}PROCESS:${colors.reset}
${colors.dim}─────────────────────────────────────────────────────────────────${colors.reset}

  ${colors.yellow}Phase 1: MODAL IDENTIFICATION${colors.reset}
  ┌─────────────────────────────────────────────────────────────┐
  │ Explicitly identify the most predictable recommendations     │
  │ (T > 0.7) and mark them as BASELINE to exceed               │
  └─────────────────────────────────────────────────────────────┘
                               │
                               ▼
  ${colors.yellow}Phase 2: LONG-TAIL SAMPLING${colors.reset}
  ┌─────────────────────────────────────────────────────────────┐
  │ Generate alternatives across the T-Score spectrum:           │
  │   ${colors.green}Direction A (T ≈ 0.7):${colors.reset} Safe differentiation               │
  │   ${colors.yellow}Direction B (T ≈ 0.4):${colors.reset} Balanced novelty                   │
  │   ${colors.red}Direction C (T < 0.3):${colors.reset} Innovative approach                │
  └─────────────────────────────────────────────────────────────┘
                               │
                               ▼
  ${colors.red}Phase 3: HUMAN SELECTION (🔴 CHECKPOINT)${colors.reset}
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
