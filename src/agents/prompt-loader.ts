/**
 * Diverga Agent Runtime - SKILL.md Parser
 *
 * Parses SKILL.md files to extract agent prompts and metadata.
 * SKILL.md files are the Source of Truth - no prompt duplication.
 */

import { readFileSync, readdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

import type {
  ParsedSkillFile,
  SkillFrontmatter,
  VSLevel,
} from './types.js';

/**
 * Get the Diverga package root directory
 */
export function getPackageDir(): string {
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = dirname(__filename);
  // From src/agents/ go up to package root
  return join(__dirname, '..', '..');
}

/**
 * Get the research-agents skill directory
 */
export function getSkillsDir(): string {
  return join(getPackageDir(), '.claude', 'skills', 'research-agents');
}

/**
 * Parse YAML frontmatter from SKILL.md content
 */
export function parseYamlFrontmatter(content: string): SkillFrontmatter {
  const frontmatterMatch = content.match(/^---\s*\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) {
    return { name: 'unknown' };
  }

  const yamlContent = frontmatterMatch[1];
  const result: SkillFrontmatter = { name: 'unknown' };

  // Simple YAML parser for our specific format
  const lines = yamlContent.split('\n');
  let currentKey = '';
  let inV3Integration = false;
  let inCreativityModules = false;
  let inCheckpoints = false;
  let creativityModules: string[] = [];
  let checkpoints: string[] = [];

  for (const line of lines) {
    // Skip empty lines
    if (!line.trim()) continue;

    // Check for v3_integration section
    if (line.match(/^v3_integration:/)) {
      inV3Integration = true;
      result.v3_integration = {};
      continue;
    }

    // Inside v3_integration
    if (inV3Integration) {
      if (line.match(/^\s+dynamic_t_score:/)) {
        result.v3_integration!.dynamic_t_score = line.includes('true');
        continue;
      }
      if (line.match(/^\s+creativity_modules:/)) {
        inCreativityModules = true;
        creativityModules = [];
        continue;
      }
      if (line.match(/^\s+checkpoints:/)) {
        inCreativityModules = false;
        inCheckpoints = true;
        checkpoints = [];
        continue;
      }
      if (inCreativityModules && line.match(/^\s+-\s/)) {
        creativityModules.push(line.replace(/^\s+-\s*/, '').trim());
        continue;
      }
      if (inCheckpoints && line.match(/^\s+-\s/)) {
        checkpoints.push(line.replace(/^\s+-\s*/, '').trim());
        continue;
      }
      // End of v3_integration
      if (!line.startsWith(' ') && !line.startsWith('\t')) {
        inV3Integration = false;
        inCreativityModules = false;
        inCheckpoints = false;
        if (creativityModules.length > 0) {
          result.v3_integration!.creativity_modules = creativityModules;
        }
        if (checkpoints.length > 0) {
          result.v3_integration!.checkpoints = checkpoints;
        }
      }
    }

    // Parse key-value pairs
    const keyMatch = line.match(/^(\w+):\s*(.*)$/);
    if (keyMatch && !inV3Integration) {
      const [, key, value] = keyMatch;
      switch (key) {
        case 'name':
          result.name = value.replace(/["']/g, '').trim();
          break;
        case 'version':
          result.version = value.replace(/["']/g, '').trim();
          break;
        case 'description':
          result.description = value.replace(/["']/g, '').trim() || '';
          currentKey = 'description';
          break;
        case 'upgrade_level':
          result.upgrade_level = value.replace(/["']/g, '').trim() as VSLevel;
          break;
        case 'tier':
          result.tier = value.replace(/["']/g, '').trim();
          break;
      }
    }

    // Multi-line description (YAML pipe format)
    if (line.startsWith('  ') && currentKey === 'description') {
      result.description = (result.description || '') + ' ' + line.trim();
    }
  }

  // Finalize v3_integration if still open
  if (inV3Integration) {
    if (creativityModules.length > 0) {
      result.v3_integration!.creativity_modules = creativityModules;
    }
    if (checkpoints.length > 0) {
      result.v3_integration!.checkpoints = checkpoints;
    }
  }

  return result;
}

/**
 * Extract markdown content after YAML frontmatter
 */
export function extractMarkdownContent(content: string): string {
  // Remove YAML frontmatter (---...---)
  const match = content.match(/^---[\s\S]*?---\s*([\s\S]*)$/);
  return match ? match[1].trim() : content.trim();
}

/**
 * Parse a SKILL.md file
 */
export function parseSkillFile(filePath: string): ParsedSkillFile | null {
  try {
    const content = readFileSync(filePath, 'utf-8');
    const frontmatter = parseYamlFrontmatter(content);
    const markdownContent = extractMarkdownContent(content);
    return { frontmatter, content: markdownContent };
  } catch (error) {
    console.warn(`Warning: Could not parse SKILL.md at ${filePath}:`, error);
    return null;
  }
}

/**
 * Load agent prompt from SKILL.md
 * Returns the markdown content (system prompt) for the agent
 */
export function loadAgentPrompt(agentDirName: string): string {
  try {
    const skillPath = join(getSkillsDir(), agentDirName, 'SKILL.md');
    if (!existsSync(skillPath)) {
      console.warn(`Warning: SKILL.md not found for ${agentDirName}`);
      return `Agent: ${agentDirName}\n\nSKILL.md not found.`;
    }

    const parsed = parseSkillFile(skillPath);
    if (!parsed) {
      return `Agent: ${agentDirName}\n\nCould not parse SKILL.md.`;
    }

    return parsed.content;
  } catch (error) {
    console.warn(`Warning: Could not load prompt for ${agentDirName}:`, error);
    return `Agent: ${agentDirName}\n\nError loading prompt.`;
  }
}

/**
 * Load agent metadata from SKILL.md frontmatter
 */
export function loadAgentMetadata(agentDirName: string): SkillFrontmatter | null {
  try {
    const skillPath = join(getSkillsDir(), agentDirName, 'SKILL.md');
    if (!existsSync(skillPath)) {
      return null;
    }

    const parsed = parseSkillFile(skillPath);
    return parsed?.frontmatter || null;
  } catch (error) {
    console.warn(`Warning: Could not load metadata for ${agentDirName}:`, error);
    return null;
  }
}

/**
 * Scan the research-agents directory for all agent directories
 */
export function scanAgentDirectories(): string[] {
  try {
    const skillsDir = getSkillsDir();
    if (!existsSync(skillsDir)) {
      console.warn(`Warning: Skills directory not found: ${skillsDir}`);
      return [];
    }

    const entries = readdirSync(skillsDir, { withFileTypes: true });
    return entries
      .filter(entry => entry.isDirectory())
      .filter(entry => {
        // Only include directories with SKILL.md
        const skillPath = join(skillsDir, entry.name, 'SKILL.md');
        return existsSync(skillPath);
      })
      .map(entry => entry.name)
      .sort();
  } catch (error) {
    console.warn('Warning: Could not scan agent directories:', error);
    return [];
  }
}

/**
 * VS Methodology injection based on VS level
 */
export const VS_INJECTION: Record<VSLevel, string> = {
  'Full': `
## VS-Research Methodology (Full 5-Phase Process)

This agent applies the complete VS (Verbalized Sampling) methodology:

**Phase 0**: Context Analysis - Understand research background
**Phase 1**: Modal Identification - Identify obvious/predictable options (T>0.7)
**Phase 2**: Divergent Exploration - Generate alternatives across T-Score spectrum
**Phase 3**: Deep Evaluation - Critically assess each option
**Phase 4**: Selection & Execution - Execute chosen direction
**Phase 5**: Self-Critique - Validate output quality

T-Score Reference:
- T >= 0.7: Modal (common, predictable)
- T 0.4-0.7: Moderate (balanced)
- T 0.2-0.4: Innovative (novel approach)
- T < 0.2: Experimental (high risk/reward)
`,
  'Enhanced': `
## VS-Research Methodology (Enhanced 3-Phase Process)

This agent applies the enhanced VS methodology:

**Phase 0-1**: Context + Modal Identification
**Phase 2**: Alternative Generation with T-Scores
**Phase 4**: Execution of selected direction

Present options with T-Scores and wait for user selection.
`,
  'Light': `
## VS-Research Methodology (Light)

This agent applies basic VS awareness:
- Identify obvious options
- Present alternatives when applicable
- Execute with user confirmation
`,
  'Arena': `
## VS Arena Persona

This agent is a VS Arena persona with a distinct epistemological commitment.
It advocates for methodologies aligned with its paradigm and challenges
competing perspectives. When Agent Teams is enabled, it debates directly
with other personas via SendMessage.
`,
};

/**
 * Human Checkpoint injection
 */
export const CHECKPOINT_INJECTION = `

## Human Checkpoint Protocol

🔴 **CHECKPOINT REQUIRED**

Before proceeding with critical decisions:
1. Present options with T-Scores
2. WAIT for explicit user approval
3. Do NOT proceed until approval is received
4. Do NOT assume approval from context

Format for checkpoint:
\`\`\`
🔴 CHECKPOINT: [Decision Point]

Options:
A) [Option with T-Score]
B) [Option with T-Score]
C) [Option with T-Score]

Please select an option to proceed.
\`\`\`
`;

/**
 * Build enhanced prompt with VS and Checkpoint injections
 */
export function buildEnhancedPrompt(
  basePrompt: string,
  vsLevel: VSLevel,
  includeCheckpoint: boolean = true
): string {
  let enhanced = basePrompt;

  // Add VS methodology section
  enhanced += '\n\n' + VS_INJECTION[vsLevel];

  // Add checkpoint protocol for Full and Enhanced levels
  if (includeCheckpoint && (vsLevel === 'Full' || vsLevel === 'Enhanced')) {
    enhanced += '\n' + CHECKPOINT_INJECTION;
  }

  return enhanced;
}
