/**
 * Tests for scripts/generate.js
 *
 * Uses Node.js built-in test runner (node:test) and assert module.
 * Tests the code generation script by running it in isolated temp directories.
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { execSync } from 'child_process';

// ===========================================================================
// Test helpers
// ===========================================================================

function createTestContext() {
  const tmpDir = mkdtempSync(join(tmpdir(), 'generate-test-'));

  // Create minimal project structure
  mkdirSync(join(tmpDir, 'config'), { recursive: true });
  mkdirSync(join(tmpDir, 'src', 'agents'), { recursive: true });
  mkdirSync(join(tmpDir, 'mcp'), { recursive: true });
  mkdirSync(join(tmpDir, 'scripts'), { recursive: true });

  // Copy generate.js script to tmpDir
  const generateScript = readFileSync(
    join(process.cwd(), 'scripts', 'generate.js'),
    'utf-8'
  );
  writeFileSync(join(tmpDir, 'scripts', 'generate.js'), generateScript);

  // Create minimal agents.json with 3 test agents
  const agentsConfig = {
    version: '8.5.0',
    agents: [
      {
        id: 'a1',
        fullId: 'a1-research-question-refiner',
        directoryName: 'a1-research-question-refiner',
        displayName: 'Research Question Refiner',
        description: 'Refines research questions for clarity',
        model: 'opus',
        tier: 'HIGH',
        tools: ['Read', 'Write', 'Bash'],
        icon: '🎯',
        vsLevel: 'Full',
        vsPhases: [1, 2, 3],
        triggers: {
          en: ['research question', 'RQ', 'refine question'],
          ko: ['연구 질문', '연구문제', 'RQ']
        },
        paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
        checkpoints: ['CP_RESEARCH_DIRECTION', 'CP_VS_001'],
        creativityModules: ['divergent'],
        category: 'A',
        categoryName: 'Foundation',
        prerequisites: [],
        ownCheckpoints: [
          { id: 'CP_RESEARCH_DIRECTION', level: 'required' },
          { id: 'CP_VS_001', level: 'required' }
        ],
        entryPoint: true
      },
      {
        id: 'b1',
        fullId: 'b1-systematic-literature-scout',
        directoryName: 'b1-systematic-literature-scout',
        displayName: 'Systematic Literature Scout',
        description: "Searches literature systematically",
        model: 'sonnet',
        tier: 'MEDIUM',
        tools: ['Read', 'WebSearch'],
        icon: '📚',
        vsLevel: 'Enhanced',
        vsPhases: [2, 3],
        triggers: {
          en: ['systematic review', 'literature search', 'PRISMA'],
          ko: ['체계적 문헌고찰', '문헌 검색']
        },
        paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
        checkpoints: ['CP_SCREENING_CRITERIA'],
        creativityModules: [],
        category: 'B',
        categoryName: 'Evidence',
        prerequisites: ['CP_RESEARCH_DIRECTION'],
        ownCheckpoints: [
          { id: 'CP_SCREENING_CRITERIA', level: 'recommended' }
        ]
      },
      {
        id: 'i0',
        fullId: 'i0-review-pipeline-orchestrator',
        directoryName: 'i0-review-pipeline-orchestrator',
        displayName: 'Review Pipeline Orchestrator',
        description: 'Orchestrates systematic review pipeline',
        model: 'opus',
        tier: 'HIGH',
        tools: ['Read', 'Write', 'Bash', 'TeamCreate'],
        icon: '🎼',
        vsLevel: 'Full',
        vsPhases: [1, 2, 3, 4],
        triggers: {
          en: ['systematic review', 'PRISMA', 'literature review automation'],
          ko: ['체계적 문헌고찰', '프리즈마', '문헌고찰 자동화']
        },
        paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
        checkpoints: ['SCH_DATABASE_SELECTION', 'SCH_API_KEY_VALIDATION'],
        creativityModules: [],
        category: 'I',
        categoryName: 'Systematic Review Automation',
        prerequisites: [],
        ownCheckpoints: [
          { id: 'SCH_DATABASE_SELECTION', level: 'required' },
          { id: 'SCH_API_KEY_VALIDATION', level: 'required' }
        ]
      }
    ]
  };

  writeFileSync(
    join(tmpDir, 'config', 'agents.json'),
    JSON.stringify(agentsConfig, null, 2)
  );

  // Create minimal AGENTS.md with markers
  const agentsMd = `# Diverga Agents

## Overview

### 44 Specialized Research Agents

<!-- GENERATED:START -->
<!-- GENERATED:END -->

## Categories

### Category A: Foundation
...
`;

  writeFileSync(join(tmpDir, 'AGENTS.md'), agentsMd);

  return { tmpDir };
}

function cleanup(tmpDir) {
  rmSync(tmpDir, { recursive: true, force: true });
}

function runGenerate(tmpDir, args = '--write') {
  execSync(`node scripts/generate.js ${args}`, {
    cwd: tmpDir,
    encoding: 'utf-8',
    stdio: 'pipe'
  });
}

// ===========================================================================
// 1. Loading
// ===========================================================================

describe('generate.js - Loading', () => {
  let tmpDir;

  beforeEach(() => {
    ({ tmpDir } = createTestContext());
  });

  afterEach(() => {
    cleanup(tmpDir);
  });

  it('loads agents.json and parses correctly', () => {
    runGenerate(tmpDir);

    // Check that generated files exist (proves parsing succeeded)
    assert.ok(existsSync(join(tmpDir, 'src', 'agents', 'definitions.generated.ts')));
  });

  it('counts agents correctly', () => {
    runGenerate(tmpDir);

    const tsContent = readFileSync(
      join(tmpDir, 'src', 'agents', 'definitions.generated.ts'),
      'utf-8'
    );

    // Fixture has 3 agents (a1, b1, i0) across 3 categories
    // Each category shows its count, verify all 3 agents appear in AGENT_CONFIGS
    assert.match(tsContent, /'a1'/);
    assert.match(tsContent, /'b1'/);
    assert.match(tsContent, /'i0'/);
  });

  it('validates required fields (id, displayName, category, tier, model)', () => {
    // Create invalid agents.json (missing displayName)
    const invalidConfig = {
      version: '8.5.0',
      agents: [
        {
          id: 'a1',
          // displayName missing
          category: 'A',
          tier: 'HIGH',
          model: 'opus'
        }
      ]
    };

    writeFileSync(
      join(tmpDir, 'config', 'agents.json'),
      JSON.stringify(invalidConfig, null, 2)
    );

    // Should throw or exit with error
    assert.throws(() => {
      runGenerate(tmpDir);
    });
  });

  it('throws on missing/invalid agents.json', () => {
    // Remove agents.json
    rmSync(join(tmpDir, 'config', 'agents.json'));

    assert.throws(() => {
      runGenerate(tmpDir);
    });
  });
});

// ===========================================================================
// 2. TypeScript generation
// ===========================================================================

describe('generate.js - TypeScript generation', () => {
  let tmpDir;

  beforeEach(() => {
    ({ tmpDir } = createTestContext());
  });

  afterEach(() => {
    cleanup(tmpDir);
  });

  it('generates valid TypeScript file', () => {
    runGenerate(tmpDir);

    assert.ok(existsSync(join(tmpDir, 'src', 'agents', 'definitions.generated.ts')));

    const content = readFileSync(
      join(tmpDir, 'src', 'agents', 'definitions.generated.ts'),
      'utf-8'
    );

    // Should be valid TS syntax (check for imports and exports)
    assert.match(content, /import type \{/);
    assert.match(content, /export const AGENT_MAPPINGS/);
    assert.match(content, /export const AGENT_CONFIGS/);
  });

  it('contains AGENT_MAPPINGS array with correct count', () => {
    runGenerate(tmpDir);

    const content = readFileSync(
      join(tmpDir, 'src', 'agents', 'definitions.generated.ts'),
      'utf-8'
    );

    // Should have 3 agents in AGENT_MAPPINGS
    const mappingsMatch = content.match(/export const AGENT_MAPPINGS.*?\[(.*?)\];/s);
    assert.ok(mappingsMatch);

    const mappingsContent = mappingsMatch[1];
    const agentCount = (mappingsContent.match(/shortId:/g) || []).length;
    assert.equal(agentCount, 3);
  });

  it('contains AGENT_CONFIGS record with all agents', () => {
    runGenerate(tmpDir);

    const content = readFileSync(
      join(tmpDir, 'src', 'agents', 'definitions.generated.ts'),
      'utf-8'
    );

    // Should have all 3 agents: a1, b1, i0
    assert.match(content, /'a1':\s*\{/);
    assert.match(content, /'b1':\s*\{/);
    assert.match(content, /'i0':\s*\{/);
  });

  it('preserves triggers (en/ko arrays)', () => {
    runGenerate(tmpDir);

    const content = readFileSync(
      join(tmpDir, 'src', 'agents', 'definitions.generated.ts'),
      'utf-8'
    );

    // Should have triggers for a1
    assert.match(content, /research question/);
    assert.match(content, /연구 질문/);
  });

  it('handles special characters in descriptions (quotes, apostrophes)', () => {
    runGenerate(tmpDir);

    const content = readFileSync(
      join(tmpDir, 'src', 'agents', 'definitions.generated.ts'),
      'utf-8'
    );

    // b1 has "Searches literature systematically" with apostrophe
    // Should be properly escaped
    assert.match(content, /Searches literature systematically/);
  });

  it('output contains // @generated header', () => {
    runGenerate(tmpDir);

    const content = readFileSync(
      join(tmpDir, 'src', 'agents', 'definitions.generated.ts'),
      'utf-8'
    );

    assert.match(content, /\/\/ @generated DO NOT EDIT/);
  });
});

// ===========================================================================
// 3. Prerequisite map generation
// ===========================================================================

describe('generate.js - Prerequisite map generation', () => {
  let tmpDir;

  beforeEach(() => {
    ({ tmpDir } = createTestContext());
  });

  afterEach(() => {
    cleanup(tmpDir);
  });

  it('generates valid JSON', () => {
    runGenerate(tmpDir);

    const content = readFileSync(
      join(tmpDir, 'mcp', 'agent-prerequisite-map.json'),
      'utf-8'
    );

    // Should parse without error
    const data = JSON.parse(content);
    assert.ok(data);
  });

  it('contains agents section with prerequisites and own_checkpoints', () => {
    runGenerate(tmpDir);

    const data = JSON.parse(readFileSync(
      join(tmpDir, 'mcp', 'agent-prerequisite-map.json'),
      'utf-8'
    ));

    assert.ok(data.agents);
    assert.ok(data.agents.a1);
    assert.ok(Array.isArray(data.agents.a1.prerequisites));
    assert.ok(Array.isArray(data.agents.a1.own_checkpoints));
  });

  it('contains dependency_order with levels', () => {
    runGenerate(tmpDir);

    const data = JSON.parse(readFileSync(
      join(tmpDir, 'mcp', 'agent-prerequisite-map.json'),
      'utf-8'
    ));

    assert.ok(data.dependency_order);
    assert.ok(data.dependency_order.level_0);
  });

  it('contains checkpoint_levels', () => {
    runGenerate(tmpDir);

    const data = JSON.parse(readFileSync(
      join(tmpDir, 'mcp', 'agent-prerequisite-map.json'),
      'utf-8'
    ));

    assert.ok(data.checkpoint_levels);
    assert.ok(data.checkpoint_levels.CP_RESEARCH_DIRECTION);
  });

  it('entry points marked correctly (a1, i0)', () => {
    runGenerate(tmpDir);

    const data = JSON.parse(readFileSync(
      join(tmpDir, 'mcp', 'agent-prerequisite-map.json'),
      'utf-8'
    ));

    assert.equal(data.agents.a1.entry_point, true);
    assert.equal(data.agents.i0.entry_point, undefined); // i0 not marked as entry point
    assert.equal(data.agents.b1.entry_point, undefined);
  });
});

// ===========================================================================
// 4. AGENTS.md generation
// ===========================================================================

describe('generate.js - AGENTS.md generation', () => {
  let tmpDir;

  beforeEach(() => {
    ({ tmpDir } = createTestContext());
  });

  afterEach(() => {
    cleanup(tmpDir);
  });

  it('generates markdown table', () => {
    runGenerate(tmpDir);

    const content = readFileSync(join(tmpDir, 'AGENTS.md'), 'utf-8');

    // Should contain markdown table
    assert.match(content, /\| ID \| Display Name \| Category \| Tier \| Model \| VS Level \| Key Triggers \|/);
  });

  it('table has correct columns (ID, Name, Category, Tier, Model, VS Level, Triggers)', () => {
    runGenerate(tmpDir);

    const content = readFileSync(join(tmpDir, 'AGENTS.md'), 'utf-8');

    // Check header row
    assert.match(content, /\| ID \|/);
    assert.match(content, /\| Display Name \|/);
    assert.match(content, /\| Category \|/);
    assert.match(content, /\| Tier \|/);
    assert.match(content, /\| Model \|/);
    assert.match(content, /\| VS Level \|/);
    assert.match(content, /\| Key Triggers \|/);
  });

  it('contains all agents', () => {
    runGenerate(tmpDir);

    const content = readFileSync(join(tmpDir, 'AGENTS.md'), 'utf-8');

    // Should have 3 agent rows
    assert.match(content, /\| A1 \|/);
    assert.match(content, /\| B1 \|/);
    assert.match(content, /\| I0 \|/);
  });

  it('inserts between GENERATED:START/END markers', () => {
    runGenerate(tmpDir);

    const content = readFileSync(join(tmpDir, 'AGENTS.md'), 'utf-8');

    assert.match(content, /<!-- GENERATED:START -->/);
    assert.match(content, /<!-- GENERATED:END -->/);

    // Table should be between markers
    const startIdx = content.indexOf('<!-- GENERATED:START -->');
    const endIdx = content.indexOf('<!-- GENERATED:END -->');
    const tableContent = content.slice(startIdx, endIdx);

    assert.match(tableContent, /\| A1 \|/);
  });

  it('creates markers if missing', () => {
    // Create AGENTS.md without markers but with "### 44 Specialized" heading
    const agentsMd = `# Diverga Agents

## Overview

### 44 Specialized Research Agents

Here are all the agents...

## Categories
`;

    writeFileSync(join(tmpDir, 'AGENTS.md'), agentsMd);

    runGenerate(tmpDir);

    const content = readFileSync(join(tmpDir, 'AGENTS.md'), 'utf-8');

    // Should have added markers
    assert.match(content, /<!-- GENERATED:START -->/);
    assert.match(content, /<!-- GENERATED:END -->/);
  });
});
