#!/usr/bin/env node

/**
 * prereq-enforcer.mjs — Claude Code PreToolUse hook
 *
 * Unified interceptor for both Task and Skill tool calls targeting diverga:* agents.
 * Handles subagent_type (Task) and skill (Skill) fields.
 * Checks prerequisites via prereq-checker.mjs and injects
 * soft-block warnings as additionalContext.
 */

import { checkAgentPrereqs, formatWarningMessage } from '../mcp/lib/prereq-checker.mjs';
import { existsSync, readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

// Load agent alias map for human-readable name resolution
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
let aliasMap = {};
try {
  const aliasPath = join(__dirname, '..', 'config', 'agent-aliases.json');
  const aliasData = JSON.parse(readFileSync(aliasPath, 'utf8'));
  aliasMap = aliasData.aliases || {};
} catch {
  // Alias file missing or malformed — continue without aliases
}

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', () => {
  try {
    const hookData = JSON.parse(input);
    const result = processHook(hookData);
    process.stdout.write(JSON.stringify(result));
  } catch (e) {
    // On error, allow the tool call to proceed
    process.stdout.write(JSON.stringify({ continue: true }));
  }
});

function findResearchDir() {
  let dir = process.cwd();
  for (let i = 0; i < 10; i++) {
    if (existsSync(join(dir, 'research')) || existsSync(join(dir, '.research'))) {
      return dir;
    }
    const parent = dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return process.cwd();
}

function processHook(hookData) {
  const toolInput = hookData.tool_input || {};

  // Handle both Task (subagent_type) and Skill (skill) tool calls
  let source = toolInput.subagent_type || toolInput.skill || '';

  // Resolve alias if source uses a human-readable name (e.g., "diverga:meta-analysis" → "diverga:c5")
  const aliasKey = source.replace(/^diverga:/i, '');
  if (aliasMap[aliasKey]) {
    source = `diverga:${aliasMap[aliasKey]}`;
  }

  const match = source.match(/^diverga:([a-ix]\d+)/i);

  if (!match) {
    // Not a Diverga agent call — pass through
    return { continue: true };
  }

  const agentId = match[1].toLowerCase();
  const researchDir = findResearchDir();
  const prereqResult = checkAgentPrereqs(agentId, researchDir);

  if (prereqResult.approved) {
    return { continue: true };
  }

  const message = formatWarningMessage(prereqResult);

  // Soft block: always continue, inject warning as additionalContext
  return {
    continue: true,
    additionalContext: message
  };
}
