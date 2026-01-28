#!/usr/bin/env node

/**
 * Diverga Codex CLI Wrapper
 * Command-line interface for Diverga research agents in OpenAI Codex CLI
 *
 * Usage:
 *   diverga-codex setup      - First-time setup
 *   diverga-codex list       - List all agents
 *   diverga-codex agent <id> - Show agent details
 *   diverga-codex context    - Show current research context
 *   diverga-codex checkpoint - Show checkpoint status
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  version: '6.0.0',
  registryPath: path.join(__dirname, 'agents', 'index.json'),
  contextPath: path.join(process.cwd(), '.research', 'project-state.yaml'),
  skillsPath: path.join(process.env.HOME || '~', '.claude', 'skills', 'research-agents'),
};

// Model mapping
const MODEL_MAP = {
  HIGH: 'o1',
  MEDIUM: 'gpt-4',
  LOW: 'gpt-3.5-turbo',
};

// Agent registry (embedded for standalone use)
const AGENT_REGISTRY = {
  'A1': { name: 'Research Question Refiner', tier: 'MEDIUM', icon: '🔬', category: 'A - Research Foundation' },
  'A2': { name: 'Theoretical Framework Architect', tier: 'HIGH', icon: '🏛️', category: 'A - Research Foundation' },
  'A3': { name: "Devil's Advocate", tier: 'MEDIUM', icon: '😈', category: 'A - Research Foundation' },
  'A4': { name: 'Research Ethics Advisor', tier: 'MEDIUM', icon: '⚖️', category: 'A - Research Foundation' },
  'A5': { name: 'Paradigm & Worldview Advisor', tier: 'HIGH', icon: '🌍', category: 'A - Research Foundation' },
  'A6': { name: 'Conceptual Framework Visualizer', tier: 'HIGH', icon: '🎨', category: 'A - Research Foundation' },
  'B1': { name: 'Literature Review Strategist', tier: 'MEDIUM', icon: '📚', category: 'B - Literature & Evidence' },
  'B2': { name: 'Evidence Quality Appraiser', tier: 'MEDIUM', icon: '🔍', category: 'B - Literature & Evidence' },
  'B3': { name: 'Effect Size Extractor', tier: 'LOW', icon: '📊', category: 'B - Literature & Evidence' },
  'B4': { name: 'Research Radar', tier: 'LOW', icon: '📡', category: 'B - Literature & Evidence' },
  'B5': { name: 'Parallel Document Processor', tier: 'MEDIUM', icon: '📄', category: 'B - Literature & Evidence' },
  'C1': { name: 'Quantitative Design Consultant', tier: 'HIGH', icon: '📈', category: 'C - Study Design' },
  'C2': { name: 'Qualitative Design Consultant', tier: 'HIGH', icon: '🎙️', category: 'C - Study Design' },
  'C3': { name: 'Mixed Methods Design Consultant', tier: 'HIGH', icon: '🔀', category: 'C - Study Design' },
  'C4': { name: 'Experimental Materials Developer', tier: 'MEDIUM', icon: '🧪', category: 'C - Study Design' },
  'C5': { name: 'Meta-Analysis Master', tier: 'HIGH', icon: '📊', category: 'C - Study Design' },
  'C6': { name: 'Data Integrity Guard', tier: 'MEDIUM', icon: '🛡️', category: 'C - Study Design' },
  'C7': { name: 'Error Prevention Engine', tier: 'MEDIUM', icon: '⚠️', category: 'C - Study Design' },
  'D1': { name: 'Sampling Strategy Advisor', tier: 'MEDIUM', icon: '🎯', category: 'D - Data Collection' },
  'D2': { name: 'Interview & Focus Group Specialist', tier: 'MEDIUM', icon: '🎤', category: 'D - Data Collection' },
  'D3': { name: 'Observation Protocol Designer', tier: 'LOW', icon: '👁️', category: 'D - Data Collection' },
  'D4': { name: 'Measurement Instrument Developer', tier: 'HIGH', icon: '📏', category: 'D - Data Collection' },
  'E1': { name: 'Quantitative Analysis Guide', tier: 'HIGH', icon: '🔢', category: 'E - Analysis' },
  'E2': { name: 'Qualitative Coding Specialist', tier: 'MEDIUM', icon: '🏷️', category: 'E - Analysis' },
  'E3': { name: 'Mixed Methods Integration', tier: 'HIGH', icon: '🔗', category: 'E - Analysis' },
  'E4': { name: 'Analysis Code Generator', tier: 'LOW', icon: '💻', category: 'E - Analysis' },
  'E5': { name: 'Sensitivity Analysis Designer', tier: 'MEDIUM', icon: '🎚️', category: 'E - Analysis' },
  'F1': { name: 'Internal Consistency Checker', tier: 'LOW', icon: '✅', category: 'F - Quality & Validation' },
  'F2': { name: 'Checklist Manager', tier: 'LOW', icon: '📋', category: 'F - Quality & Validation' },
  'F3': { name: 'Reproducibility Auditor', tier: 'MEDIUM', icon: '🔄', category: 'F - Quality & Validation' },
  'F4': { name: 'Bias & Trustworthiness Detector', tier: 'MEDIUM', icon: '⚠️', category: 'F - Quality & Validation' },
  'F5': { name: 'Humanization Verifier', tier: 'MEDIUM', icon: '👤', category: 'F - Quality & Validation' },
  'G1': { name: 'Journal Matcher', tier: 'MEDIUM', icon: '📰', category: 'G - Publication' },
  'G2': { name: 'Academic Communicator', tier: 'MEDIUM', icon: '✍️', category: 'G - Publication' },
  'G3': { name: 'Peer Review Strategist', tier: 'HIGH', icon: '👥', category: 'G - Publication' },
  'G4': { name: 'Pre-registration Composer', tier: 'MEDIUM', icon: '📝', category: 'G - Publication' },
  'G5': { name: 'Academic Style Auditor', tier: 'MEDIUM', icon: '📖', category: 'G - Publication' },
  'G6': { name: 'Academic Style Humanizer', tier: 'MEDIUM', icon: '🖊️', category: 'G - Publication' },
  'H1': { name: 'Ethnographic Research Advisor', tier: 'HIGH', icon: '🌐', category: 'H - Specialized' },
  'H2': { name: 'Action Research Facilitator', tier: 'HIGH', icon: '🎬', category: 'H - Specialized' },
};

// Commands
const commands = {
  help() {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║           Diverga Research Coordinator - Codex CLI            ║
║                       Version ${CONFIG.version}                        ║
╚═══════════════════════════════════════════════════════════════╝

Usage: diverga-codex <command> [options]

Commands:
  setup              First-time setup and verification
  list               List all available agents
  agent <id>         Show details for a specific agent (e.g., A1, B2)
  context            Show current research project context
  checkpoint         Show checkpoint status
  tscore             Display T-Score reference table
  vs                 Explain VS methodology

Examples:
  diverga-codex list
  diverga-codex agent A1
  diverga-codex tscore
`);
  },

  setup() {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                    Diverga Setup for Codex                    ║
╚═══════════════════════════════════════════════════════════════╝

Checking configuration...
`);

    // Check for AGENTS.md
    const agentsMdPath = path.join(__dirname, 'AGENTS.md');
    if (fs.existsSync(agentsMdPath)) {
      console.log('✅ AGENTS.md found');
    } else {
      console.log('❌ AGENTS.md not found');
    }

    // Check for skills directory
    if (fs.existsSync(CONFIG.skillsPath)) {
      const skills = fs.readdirSync(CONFIG.skillsPath);
      console.log(`✅ Skills directory found (${skills.length} agents)`);
    } else {
      console.log('⚠️  Skills directory not found at:', CONFIG.skillsPath);
    }

    console.log(`
Setup complete!

To use Diverga with Codex:
1. Copy this directory to ~/.codex/diverga/
2. Codex will automatically read AGENTS.md on startup
3. Use keywords to trigger agents (e.g., "research question", "meta-analysis")

For more information, see AGENTS.md
`);
  },

  list() {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                  Diverga Agent Catalog                        ║
╚═══════════════════════════════════════════════════════════════╝
`);

    const categories = {};
    for (const [id, agent] of Object.entries(AGENT_REGISTRY)) {
      if (!categories[agent.category]) {
        categories[agent.category] = [];
      }
      categories[agent.category].push({ id, ...agent });
    }

    for (const [category, agents] of Object.entries(categories)) {
      console.log(`\n## ${category}\n`);
      for (const agent of agents) {
        const model = MODEL_MAP[agent.tier];
        console.log(`  ${agent.icon} ${agent.id}: ${agent.name} (${model})`);
      }
    }

    console.log(`\n\nTotal: ${Object.keys(AGENT_REGISTRY).length} agents`);
  },

  agent(id) {
    if (!id) {
      console.log('Usage: diverga-codex agent <id>');
      console.log('Example: diverga-codex agent A1');
      return;
    }

    const upperId = id.toUpperCase();
    const agent = AGENT_REGISTRY[upperId];

    if (!agent) {
      console.log(`Agent "${id}" not found.`);
      console.log('Use "diverga-codex list" to see all agents.');
      return;
    }

    const model = MODEL_MAP[agent.tier];

    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║  ${agent.icon} ${upperId}: ${agent.name.padEnd(45)}║
╚═══════════════════════════════════════════════════════════════╝

Category:   ${agent.category}
Tier:       ${agent.tier}
Model:      ${model}

To invoke this agent, use keywords in your prompt related to:
- ${agent.name}
`);
  },

  context() {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                  Research Project Context                     ║
╚═══════════════════════════════════════════════════════════════╝
`);

    if (fs.existsSync(CONFIG.contextPath)) {
      const context = fs.readFileSync(CONFIG.contextPath, 'utf-8');
      console.log(context);
    } else {
      console.log('No active research project found.');
      console.log(`\nTo start a new project, create: ${CONFIG.contextPath}`);
      console.log('\nOr use a research-related prompt to initialize a project.');
    }
  },

  checkpoint() {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                  Checkpoint Reference                         ║
╚═══════════════════════════════════════════════════════════════╝

REQUIRED CHECKPOINTS (🔴 MANDATORY HALT)
─────────────────────────────────────────
  CP_RESEARCH_DIRECTION    Research question finalized
  CP_PARADIGM_SELECTION    Methodology approach
  CP_THEORY_SELECTION      Framework chosen
  CP_METHODOLOGY_APPROVAL  Design complete
  CP_VS_001                After VS alternatives
  CP_VS_003                Before execution

RECOMMENDED CHECKPOINTS (🟠 SUGGESTED HALT)
─────────────────────────────────────────
  CP_ANALYSIS_PLAN         Before analysis
  CP_INTEGRATION_STRATEGY  Mixed methods only
  CP_QUALITY_REVIEW        Assessment done
  CP_SCREENING_CRITERIA    Inclusion/exclusion set
  CP_SAMPLING_STRATEGY     Sample determined

OPTIONAL CHECKPOINTS (🟡 DEFAULTS AVAILABLE)
─────────────────────────────────────────
  CP_VISUALIZATION_PREFERENCE  Before visuals
  CP_SEARCH_STRATEGY           Database selection
  CP_WRITING_STYLE             Before writing
`);
  },

  tscore() {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                  T-Score Reference Table                      ║
╚═══════════════════════════════════════════════════════════════╝

T-Score measures "typicality" - how common a research approach is.

┌────────────┬─────────────┬────────────────────────────────────┐
│ T-Score    │ Label       │ Meaning                            │
├────────────┼─────────────┼────────────────────────────────────┤
│ ≥ 0.7      │ 🟢 Common   │ Highly typical, limited novelty    │
│ 0.5-0.7    │ 🟢 Estab.   │ Standard, needs specificity        │
│ 0.4-0.5    │ 🟡 Moderate │ Balanced risk-novelty              │
│ 0.3-0.4    │ 🟡 Emerging │ Novel, needs justification         │
│ 0.2-0.3    │ 🟠 Innovate │ High contribution potential        │
│ < 0.2      │ 🔴 Experim. │ Paradigm-challenging               │
└────────────┴─────────────┴────────────────────────────────────┘

Creativity Levels:
  Conservative (T ≥ 0.5) - Safe, validated approaches
  Balanced (T ≥ 0.3)     - Differentiated + defensible
  Innovative (T ≥ 0.2)   - High contribution potential
  Extreme (T < 0.2)      - Maximum creativity
`);
  },

  vs() {
    console.log(`
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

EXAMPLE OUTPUT:
─────────────────────────────────────────────────────────────────

  ⚠️ Modal Warning: These are the most predictable approaches:
  │ Approach              │ T-Score │ Issue           │
  │───────────────────────│─────────│─────────────────│
  │ Survey research       │ 0.90    │ Limited novelty │
  │ Simple correlation    │ 0.85    │ No mechanism    │

  VS Alternatives:
  [A] Survey + moderators (T=0.65) 🟢 - Safe differentiation
  [B] Sequential mixed methods (T=0.40) 🟡 - Balanced novelty ⭐
  [C] Design-based research (T=0.22) 🟠 - Innovative

  Which direction? (A/B/C)
`);
  },
};

// Main
function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';

  if (commands[command]) {
    commands[command](args[1]);
  } else {
    console.log(`Unknown command: ${command}`);
    commands.help();
  }
}

main();
