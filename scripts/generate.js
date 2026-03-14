#!/usr/bin/env node

// @ts-check
/**
 * Diverga Code Generator
 *
 * Reads config/agents.json (SSoT) and generates derived files:
 *   1. src/agents/definitions.generated.ts  (TypeScript agent registry)
 *   2. mcp/agent-prerequisite-map.json      (prerequisite graph)
 *   3. AGENTS.md                            (agent table between markers)
 *
 * Usage:
 *   node scripts/generate.js           # default: --write
 *   node scripts/generate.js --write   # write generated files
 *   node scripts/generate.js --check   # compare only, exit 1 on drift
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = resolve(__dirname, '..');

const AGENTS_JSON = resolve(ROOT, 'config/agents.json');
const DEFINITIONS_TS = resolve(ROOT, 'src/agents/definitions.generated.ts');
const PREREQUISITE_MAP = resolve(ROOT, 'mcp/agent-prerequisite-map.json');
const AGENTS_MD = resolve(ROOT, 'AGENTS.md');

const MARKER_START = '<!-- GENERATED:START -->';
const MARKER_END = '<!-- GENERATED:END -->';

// ---------------------------------------------------------------------------
// CLI flag parsing
// ---------------------------------------------------------------------------

const args = process.argv.slice(2);
const checkMode = args.includes('--check');

// ---------------------------------------------------------------------------
// Load & validate agents.json
// ---------------------------------------------------------------------------

if (!existsSync(AGENTS_JSON)) {
  console.error(`ERROR: ${AGENTS_JSON} not found`);
  process.exit(1);
}

/** @type {{ version: string; agents: Array<Record<string, any>> }} */
const config = JSON.parse(readFileSync(AGENTS_JSON, 'utf-8'));

if (!config.agents || !Array.isArray(config.agents)) {
  console.error('ERROR: agents.json missing "agents" array');
  process.exit(1);
}

if (config.agents.length === 0) {
  console.error('ERROR: agents.json has zero agents');
  process.exit(1);
}

const agents = config.agents;
console.log(`Loaded ${agents.length} agents from config/agents.json (v${config.version})`);

// ---------------------------------------------------------------------------
// Helper: flatten triggers object to string array
// ---------------------------------------------------------------------------

/**
 * Flatten { en: [...], ko: [...] } into a single string[]
 * @param {Record<string, string[]> | string[]} triggers
 * @returns {string[]}
 */
function flattenTriggers(triggers) {
  if (Array.isArray(triggers)) return triggers;
  const result = [];
  for (const lang of Object.keys(triggers)) {
    result.push(...triggers[lang]);
  }
  return result;
}

// ---------------------------------------------------------------------------
// Generator 1: definitions.generated.ts
// ---------------------------------------------------------------------------

function generateDefinitionsTS() {
  const lines = [];

  lines.push(`// @generated DO NOT EDIT - Generated from config/agents.json by scripts/generate.js`);
  lines.push(`// Version: ${config.version}`);
  lines.push(``);
  lines.push(`import type {`);
  lines.push(`  ModelType,`);
  lines.push(`  TierLevel,`);
  lines.push(`  CategoryId,`);
  lines.push(`  AgentIdMapping,`);
  lines.push(`} from './types.js';`);
  lines.push(``);

  // ---- AGENT_MAPPINGS ----
  lines.push(`// ============================================================`);
  lines.push(`// AGENT ID MAPPINGS`);
  lines.push(`// Maps shorthand IDs (a1, b1, etc.) to directory names`);
  lines.push(`// ============================================================`);
  lines.push(``);
  lines.push(`export const AGENT_MAPPINGS: AgentIdMapping[] = [`);

  // Group by category
  const categories = groupByCategory(agents);
  for (const [catId, catAgents] of Object.entries(categories)) {
    const catName = catAgents[0].categoryName;
    lines.push(`  // Category ${catId}: ${catName} (${catAgents.length} agents)`);
    for (const agent of catAgents) {
      lines.push(`  { shortId: '${agent.id}', fullId: '${agent.fullId}', directoryName: '${agent.directoryName}' },`);
    }
    lines.push(``);
  }

  lines.push(`];`);
  lines.push(``);

  // ---- AgentStaticConfig interface ----
  lines.push(`// ============================================================`);
  lines.push(`// AGENT METADATA DEFINITIONS`);
  lines.push(`// Static metadata for each agent (tools, model, tier, etc.)`);
  lines.push(`// ============================================================`);
  lines.push(``);
  lines.push(`interface AgentStaticConfig {`);
  lines.push(`  displayName: string;`);
  lines.push(`  description: string;`);
  lines.push(`  model: ModelType;`);
  lines.push(`  tier: TierLevel;`);
  lines.push(`  tools: string[];`);
  lines.push(`  icon: string;`);
  lines.push(`  vsLevel: 'Full' | 'Enhanced' | 'Light' | 'Arena';`);
  lines.push(`  vsPhases: number[];`);
  lines.push(`  triggers: string[];`);
  lines.push(`  paradigmAffinity: string[];`);
  lines.push(`  checkpoints: string[];`);
  lines.push(`  creativityModules: string[];`);
  lines.push(`  category: CategoryId;`);
  lines.push(`  categoryName: string;`);
  lines.push(`}`);
  lines.push(``);

  // ---- AGENT_CONFIGS ----
  lines.push(`export const AGENT_CONFIGS: Record<string, AgentStaticConfig> = {`);

  for (const [catId, catAgents] of Object.entries(categories)) {
    const catName = catAgents[0].categoryName;
    lines.push(`  // ============================================================`);
    lines.push(`  // CATEGORY ${catId}: ${catName.toUpperCase()} (${catAgents.length} agents)`);
    lines.push(`  // ============================================================`);
    lines.push(``);

    for (const agent of catAgents) {
      const triggers = flattenTriggers(agent.triggers);
      const displayName = escapeTS(agent.displayName);
      const description = escapeTS(agent.description);

      lines.push(`  '${agent.id}': {`);
      lines.push(`    displayName: ${displayName},`);
      lines.push(`    description: ${description},`);
      lines.push(`    model: '${agent.model}',`);
      lines.push(`    tier: '${agent.tier}',`);
      lines.push(`    tools: ${JSON.stringify(agent.tools)},`);
      lines.push(`    icon: '${agent.icon}',`);
      lines.push(`    vsLevel: '${agent.vsLevel}',`);
      lines.push(`    vsPhases: ${JSON.stringify(agent.vsPhases)},`);
      lines.push(`    triggers: ${formatStringArray(triggers)},`);
      lines.push(`    paradigmAffinity: ${JSON.stringify(agent.paradigmAffinity)},`);
      lines.push(`    checkpoints: ${JSON.stringify(agent.checkpoints)},`);
      lines.push(`    creativityModules: ${JSON.stringify(agent.creativityModules)},`);
      lines.push(`    category: '${agent.category}',`);
      lines.push(`    categoryName: '${agent.categoryName}',`);
      lines.push(`  },`);
      lines.push(``);
    }
  }

  lines.push(`};`);
  lines.push(``);

  return lines.join('\n');
}

/**
 * Escape a string for TypeScript single-quoted string.
 * Returns the properly quoted form.
 * @param {string} str
 * @returns {string}
 */
function escapeTS(str) {
  if (str.includes("'") && !str.includes('"')) {
    // Use double quotes for strings containing single quotes
    return `"${str.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
  }
  return `'${str.replace(/\\/g, '\\\\').replace(/'/g, "\\'")}'`;
}

/**
 * Format a string array for TypeScript, using single quotes.
 * @param {string[]} arr
 * @returns {string}
 */
function formatStringArray(arr) {
  if (arr.length === 0) return '[]';
  const items = arr.map(s => escapeTS(s));
  const joined = items.join(', ');
  if (joined.length < 100) {
    return `[${joined}]`;
  }
  return `[\n      ${items.join(',\n      ')},\n    ]`;
}

// ---------------------------------------------------------------------------
// Generator 2: mcp/agent-prerequisite-map.json
// ---------------------------------------------------------------------------

function generatePrerequisiteMap() {
  const agentMap = {};

  for (const agent of agents) {
    const entry = {
      prerequisites: agent.prerequisites || [],
      own_checkpoints: (agent.ownCheckpoints || []).map(cp => ({
        id: cp.id,
        level: cp.level,
      })),
    };

    if (agent.entryPoint) {
      entry.entry_point = true;
    }

    agentMap[agent.id] = entry;
  }

  // Build dependency order from the data
  const dependencyOrder = buildDependencyOrder(agents);

  // Build checkpoint levels
  const checkpointLevels = buildCheckpointLevels(agents);

  const result = {
    agents: agentMap,
    dependency_order: dependencyOrder,
    checkpoint_levels: checkpointLevels,
  };

  return JSON.stringify(result, null, 2) + '\n';
}

/**
 * Build dependency order from agent prerequisite/checkpoint data.
 * Groups checkpoints by their dependency depth.
 * @param {Array<Record<string, any>>} agents
 * @returns {Record<string, string[]>}
 */
function buildDependencyOrder(agents) {
  // Collect all checkpoints and their dependencies
  const allCheckpoints = new Set();
  const checkpointDeps = new Map(); // cp -> set of prerequisite CPs

  for (const agent of agents) {
    // Own checkpoints are produced by this agent
    for (const cp of (agent.ownCheckpoints || [])) {
      allCheckpoints.add(cp.id);
      if (!checkpointDeps.has(cp.id)) {
        checkpointDeps.set(cp.id, new Set());
      }
      // This agent's prerequisites are dependencies of its own checkpoints
      for (const prereq of (agent.prerequisites || [])) {
        checkpointDeps.get(cp.id).add(prereq);
      }
    }

    // Prerequisites are consumed
    for (const prereq of (agent.prerequisites || [])) {
      allCheckpoints.add(prereq);
      if (!checkpointDeps.has(prereq)) {
        checkpointDeps.set(prereq, new Set());
      }
    }
  }

  // Topological sort into levels
  const levels = {};
  const assigned = new Set();
  let level = 0;

  while (assigned.size < allCheckpoints.size) {
    const thisLevel = [];
    for (const cp of allCheckpoints) {
      if (assigned.has(cp)) continue;
      const deps = checkpointDeps.get(cp) || new Set();
      const unmetDeps = [...deps].filter(d => !assigned.has(d));
      if (unmetDeps.length === 0) {
        thisLevel.push(cp);
      }
    }

    if (thisLevel.length === 0) {
      // Remaining have circular deps - just add them all
      const remaining = [...allCheckpoints].filter(cp => !assigned.has(cp));
      if (remaining.length > 0) {
        levels[`level_${level}`] = remaining.sort();
        remaining.forEach(cp => assigned.add(cp));
      }
      break;
    }

    thisLevel.sort();
    levels[`level_${level}`] = thisLevel;
    thisLevel.forEach(cp => assigned.add(cp));
    level++;
  }

  return levels;
}

/**
 * Build checkpoint levels map from agent data.
 * @param {Array<Record<string, any>>} agents
 * @returns {Record<string, string>}
 */
function buildCheckpointLevels(agents) {
  const levels = {};

  for (const agent of agents) {
    for (const cp of (agent.ownCheckpoints || [])) {
      // Use the most restrictive level if duplicated
      const existing = levels[cp.id];
      if (!existing || levelPriority(cp.level) > levelPriority(existing)) {
        levels[cp.id] = cp.level;
      }
    }
  }

  // Sort by level priority (required first, then recommended, then optional)
  const sorted = {};
  const entries = Object.entries(levels);
  entries.sort((a, b) => levelPriority(b[1]) - levelPriority(a[1]));
  for (const [id, level] of entries) {
    sorted[id] = level;
  }

  return sorted;
}

/**
 * @param {string} level
 * @returns {number}
 */
function levelPriority(level) {
  switch (level) {
    case 'required': return 3;
    case 'recommended': return 2;
    case 'optional': return 1;
    default: return 0;
  }
}

// ---------------------------------------------------------------------------
// Generator 3: AGENTS.md table section
// ---------------------------------------------------------------------------

function generateAgentsMDTable() {
  const lines = [];
  lines.push('');
  lines.push('| ID | Display Name | Category | Tier | Model | VS Level | Key Triggers |');
  lines.push('|----|-------------|----------|------|-------|----------|-------------|');

  for (const agent of agents) {
    const triggers = flattenTriggers(agent.triggers);
    const keyTriggers = triggers.slice(0, 3).join(', ');
    const id = agent.id.toUpperCase();
    lines.push(`| ${id} | ${agent.displayName} | ${agent.category}: ${agent.categoryName} | ${agent.tier} | ${agent.model} | ${agent.vsLevel} | ${keyTriggers} |`);
  }

  lines.push('');
  return lines.join('\n');
}

/**
 * Update AGENTS.md by inserting/replacing content between GENERATED markers.
 * If markers don't exist, insert them around the "Agent Registry" section.
 * @returns {string} The full updated AGENTS.md content
 */
function updateAgentsMD() {
  if (!existsSync(AGENTS_MD)) {
    console.error(`WARNING: ${AGENTS_MD} not found, skipping AGENTS.md generation`);
    return null;
  }

  let content = readFileSync(AGENTS_MD, 'utf-8');
  const tableContent = generateAgentsMDTable();

  const startIdx = content.indexOf(MARKER_START);
  const endIdx = content.indexOf(MARKER_END);

  if (startIdx !== -1 && endIdx !== -1) {
    // Replace between markers
    const before = content.slice(0, startIdx + MARKER_START.length);
    const after = content.slice(endIdx);
    return before + tableContent + after;
  }

  // Markers don't exist - insert them around the "Agent Registry" section
  // Find the "## Agent Registry" heading
  const registryMatch = content.match(/^## Agent Registry.*$/m);
  if (!registryMatch) {
    // Try alternative heading
    const altMatch = content.match(/^### 44 Specialized Research Agents.*$/m);
    if (!altMatch) {
      console.error('WARNING: Could not find agent table section in AGENTS.md');
      console.error('Add <!-- GENERATED:START --> and <!-- GENERATED:END --> markers manually');
      return null;
    }
  }

  // Insert markers and table after "### 44 Specialized..." line
  const insertPoint = content.indexOf('### 44 Specialized Research Agents');
  if (insertPoint === -1) {
    console.error('WARNING: Could not find insertion point in AGENTS.md');
    return null;
  }

  // Find end of that line
  const lineEnd = content.indexOf('\n', insertPoint);
  if (lineEnd === -1) {
    console.error('WARNING: Unexpected EOF in AGENTS.md');
    return null;
  }

  // Find the next major section after the agent tables
  // Look for "---" + next "##" heading that is NOT a "### Category" heading
  // We'll find the "## Human Checkpoint System" or similar next top-level section
  // Actually, let's find "### Category A:" through the last category table end
  const categoryPattern = /^### Category [A-I]:/gm;
  let lastCategoryMatch = null;
  let match;
  while ((match = categoryPattern.exec(content)) !== null) {
    // Only count the first set of category headings (lines < 400)
    if (match.index < content.indexOf('## Trigger Keywords') || content.indexOf('## Trigger Keywords') === -1) {
      lastCategoryMatch = match;
    }
  }

  // Insert GENERATED markers + table right after the "### 44 Specialized" line
  const insertContent = `\n\n${MARKER_START}${tableContent}${MARKER_END}\n`;
  const updated = content.slice(0, lineEnd) + insertContent + content.slice(lineEnd);
  return updated;
}

// ---------------------------------------------------------------------------
// Utility: group agents by category
// ---------------------------------------------------------------------------

/**
 * @param {Array<Record<string, any>>} agents
 * @returns {Record<string, Array<Record<string, any>>>}
 */
function groupByCategory(agents) {
  const groups = {};
  for (const agent of agents) {
    const cat = agent.category;
    if (!groups[cat]) groups[cat] = [];
    groups[cat].push(agent);
  }
  return groups;
}

// ---------------------------------------------------------------------------
// Main: generate & write or check
// ---------------------------------------------------------------------------

function main() {
  const generated = {
    [DEFINITIONS_TS]: generateDefinitionsTS(),
    [PREREQUISITE_MAP]: generatePrerequisiteMap(),
  };

  // AGENTS.md
  const agentsMdContent = updateAgentsMD();
  if (agentsMdContent) {
    generated[AGENTS_MD] = agentsMdContent;
  }

  if (checkMode) {
    // --check mode: compare generated vs existing
    let driftFound = false;

    for (const [filePath, content] of Object.entries(generated)) {
      if (!existsSync(filePath)) {
        console.error(`DRIFT: ${relative(filePath)} does not exist (needs generation)`);
        driftFound = true;
        continue;
      }

      const existing = readFileSync(filePath, 'utf-8');
      if (existing !== content) {
        console.error(`DRIFT: ${relative(filePath)} differs from generated output`);
        driftFound = true;
      } else {
        console.log(`  OK: ${relative(filePath)}`);
      }
    }

    if (driftFound) {
      console.error('\nRun "node scripts/generate.js --write" to update');
      process.exit(1);
    }

    console.log(`\nAll ${Object.keys(generated).length} files up to date`);
    process.exit(0);
  }

  // --write mode (default)
  let filesWritten = 0;
  for (const [filePath, content] of Object.entries(generated)) {
    writeFileSync(filePath, content, 'utf-8');
    console.log(`  Wrote: ${relative(filePath)}`);
    filesWritten++;
  }

  console.log(`\nGenerated ${filesWritten} files from ${agents.length} agents`);
}

/**
 * Get path relative to ROOT
 * @param {string} absPath
 * @returns {string}
 */
function relative(absPath) {
  if (absPath.startsWith(ROOT)) {
    return absPath.slice(ROOT.length + 1);
  }
  return absPath;
}

main();
