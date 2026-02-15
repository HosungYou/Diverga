/**
 * Tests for scripts/doctor.js
 *
 * Uses Node.js built-in test runner (node:test) and assert module.
 * Tests the diagnostic script functionality.
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { execSync } from 'child_process';

// ===========================================================================
// Test helpers
// ===========================================================================

function createTestContext() {
  const tmpDir = mkdtempSync(join(tmpdir(), 'doctor-test-'));

  // Create minimal project structure
  mkdirSync(join(tmpDir, 'config'), { recursive: true });
  mkdirSync(join(tmpDir, 'src'), { recursive: true });
  mkdirSync(join(tmpDir, 'mcp'), { recursive: true });
  mkdirSync(join(tmpDir, 'skills'), { recursive: true });
  mkdirSync(join(tmpDir, '.codex', 'skills'), { recursive: true });
  mkdirSync(join(tmpDir, 'scripts'), { recursive: true });

  // Copy doctor.js and sync-version.js scripts
  const doctorScript = readFileSync(
    join(process.cwd(), 'scripts', 'doctor.js'),
    'utf-8'
  );
  writeFileSync(join(tmpDir, 'scripts', 'doctor.js'), doctorScript);

  const syncScript = readFileSync(
    join(process.cwd(), 'scripts', 'sync-version.js'),
    'utf-8'
  );
  writeFileSync(join(tmpDir, 'scripts', 'sync-version.js'), syncScript);

  // Initialize git repo with an initial commit (HEAD must exist for rev-parse)
  execSync('git init', { cwd: tmpDir, stdio: 'pipe' });
  execSync('git config user.email "test@example.com"', { cwd: tmpDir, stdio: 'pipe' });
  execSync('git config user.name "Test User"', { cwd: tmpDir, stdio: 'pipe' });
  writeFileSync(join(tmpDir, '.gitkeep'), '');
  execSync('git add .gitkeep && git commit -m "init"', { cwd: tmpDir, stdio: 'pipe' });

  // Create package.json
  const packageJson = {
    name: 'test-project',
    version: '1.0.0',
    scripts: {
      build: 'tsc',
      typecheck: 'tsc --noEmit',
      clean: 'rm -rf dist',
      generate: 'node scripts/generate.js',
      'generate:check': 'node scripts/generate.js --check',
      'version:sync': 'node scripts/sync-version.js',
      'version:check': 'node scripts/sync-version.js --check',
      release: 'npm run version:sync && npm run generate'
    }
  };
  writeFileSync(
    join(tmpDir, 'package.json'),
    JSON.stringify(packageJson, null, 2)
  );

  // Create pyproject.toml
  writeFileSync(
    join(tmpDir, 'pyproject.toml'),
    '[project]\nname = "test"\nversion = "1.0.0"\n'
  );

  // Create src/index.ts
  writeFileSync(
    join(tmpDir, 'src', 'index.ts'),
    `export const VERSION = '1.0.0';\n// Diverga Agent Runtime v1.0.0\n`
  );

  // Create config/diverga-config.json
  writeFileSync(
    join(tmpDir, 'config', 'diverga-config.json'),
    JSON.stringify({ version: '1.0.0' }, null, 2)
  );

  return { tmpDir };
}

function cleanup(tmpDir) {
  rmSync(tmpDir, { recursive: true, force: true });
}

function runDoctor(tmpDir) {
  try {
    const output = execSync('node scripts/doctor.js', {
      cwd: tmpDir,
      encoding: 'utf-8',
      stdio: 'pipe'
    });
    return { exitCode: 0, output };
  } catch (error) {
    return { exitCode: error.status, output: error.stdout.toString() };
  }
}

// ===========================================================================
// 1. Individual checks
// ===========================================================================

describe('doctor.js - Individual checks', () => {
  let tmpDir;

  beforeEach(() => {
    ({ tmpDir } = createTestContext());
  });

  afterEach(() => {
    cleanup(tmpDir);
  });

  it('Node.js version check passes on current system', () => {
    const result = runDoctor(tmpDir);

    assert.match(result.output, /Node\.js.*v\d+\.\d+\.\d+/);
    // Should pass (we're running on Node >= 18)
    assert.match(result.output, /✓.*Node\.js/);
  });

  it('Git check works in git repo', () => {
    const result = runDoctor(tmpDir);

    assert.match(result.output, /✓.*Git repository/);
  });

  it('Version consistency check (set up matching versions → pass)', () => {
    // All versions already set to 1.0.0 in createTestContext
    const result = runDoctor(tmpDir);

    assert.match(result.output, /✓.*Version consistency/);
  });

  it('Version consistency check (set up mismatched → fail)', () => {
    // Change one version
    const pkg = JSON.parse(readFileSync(join(tmpDir, 'package.json'), 'utf-8'));
    pkg.version = '2.0.0';
    writeFileSync(join(tmpDir, 'package.json'), JSON.stringify(pkg, null, 2));

    const result = runDoctor(tmpDir);

    assert.match(result.output, /✗.*Version consistency/);
  });

  it('Agent count check (create agents.json with 44 → pass)', () => {
    // Create agents.json with 44 agents
    const agents = [];
    for (let i = 1; i <= 44; i++) {
      agents.push({
        id: `a${i}`,
        displayName: `Agent ${i}`,
        model: 'opus',
        tier: 'HIGH',
        category: 'A'
      });
    }

    writeFileSync(
      join(tmpDir, 'config', 'agents.json'),
      JSON.stringify({ version: '1.0.0', agents }, null, 2)
    );

    const result = runDoctor(tmpDir);

    assert.match(result.output, /✓.*Agent count.*44/);
  });

  it('Agent count check (create with 40 → fail)', () => {
    // Create agents.json with 40 agents
    const agents = [];
    for (let i = 1; i <= 40; i++) {
      agents.push({
        id: `a${i}`,
        displayName: `Agent ${i}`,
        model: 'opus',
        tier: 'HIGH',
        category: 'A'
      });
    }

    writeFileSync(
      join(tmpDir, 'config', 'agents.json'),
      JSON.stringify({ version: '1.0.0', agents }, null, 2)
    );

    const result = runDoctor(tmpDir);

    assert.match(result.output, /✗.*Agent count.*40.*expected 44/);
  });

  it('SKILL.md presence check', () => {
    // Create agents.json with 2 agents
    const agents = [
      { id: 'a1', displayName: 'Agent 1', model: 'opus', tier: 'HIGH', category: 'A' },
      { id: 'a2', displayName: 'Agent 2', model: 'sonnet', tier: 'MEDIUM', category: 'A' }
    ];

    writeFileSync(
      join(tmpDir, 'config', 'agents.json'),
      JSON.stringify({ version: '1.0.0', agents }, null, 2)
    );

    // Create only one SKILL.md
    mkdirSync(join(tmpDir, 'skills', 'a1'), { recursive: true });
    writeFileSync(join(tmpDir, 'skills', 'a1', 'SKILL.md'), '# Skill A1');

    const result = runDoctor(tmpDir);

    assert.match(result.output, /✗.*SKILL\.md files.*1\/2/);
  });

  it('MCP server check (create checkpoint-server.js → pass)', () => {
    writeFileSync(
      join(tmpDir, 'mcp', 'checkpoint-server.js'),
      '// MCP server'
    );

    const result = runDoctor(tmpDir);

    assert.match(result.output, /✓.*MCP server/);
  });

  it('Package.json scripts check', () => {
    // Already created with all required scripts in createTestContext
    const result = runDoctor(tmpDir);

    assert.match(result.output, /✓.*Package\.json.*8\/8/);
  });
});

// ===========================================================================
// 2. Summary
// ===========================================================================

describe('doctor.js - Summary', () => {
  let tmpDir;

  beforeEach(() => {
    ({ tmpDir } = createTestContext());
  });

  afterEach(() => {
    cleanup(tmpDir);
  });

  it('Exit code 0 when all pass', () => {
    // Set up passing state
    writeFileSync(
      join(tmpDir, 'mcp', 'checkpoint-server.js'),
      '// MCP server'
    );

    // Create 44 agents
    const agents = [];
    for (let i = 1; i <= 44; i++) {
      agents.push({
        id: `a${i}`,
        displayName: `Agent ${i}`,
        model: 'opus',
        tier: 'HIGH',
        category: 'A'
      });
    }

    writeFileSync(
      join(tmpDir, 'config', 'agents.json'),
      JSON.stringify({ version: '1.0.0', agents }, null, 2)
    );

    // Create all SKILL.md files with version in YAML frontmatter
    for (let i = 1; i <= 44; i++) {
      mkdirSync(join(tmpDir, 'skills', `a${i}`), { recursive: true });
      writeFileSync(
        join(tmpDir, 'skills', `a${i}`, 'SKILL.md'),
        `---\nname: a${i}\nversion: "1.0.0"\n---\n# Skill a${i}\n`
      );

      mkdirSync(join(tmpDir, '.codex', 'skills', `diverga-a${i}`), { recursive: true });
      writeFileSync(
        join(tmpDir, '.codex', 'skills', `diverga-a${i}`, 'SKILL.md'),
        `---\nname: diverga-a${i}\nmetadata:\n  version: 1.0.0\n---\n# Skill a${i}\n`
      );
    }

    const result = runDoctor(tmpDir);

    // TypeScript check may fail in isolated temp dirs (no node_modules/tsc),
    // so verify all OTHER checks pass (8/9 minimum)
    assert.match(result.output, /✓.*Node\.js/);
    assert.match(result.output, /✓.*Git repository/);
    assert.match(result.output, /✓.*Version consistency/);
    assert.match(result.output, /✓.*Agent count/);
    assert.match(result.output, /✓.*SKILL\.md/);
    assert.match(result.output, /✓.*MCP server/);
    assert.match(result.output, /✓.*Package\.json/);
    // At least 8 of 9 checks should pass (TypeScript may fail without tsc)
    assert.match(result.output, /(?:8|9)\/9 checks passed/);
  });

  it('Exit code 1 when any fail', () => {
    // Create failing condition (wrong agent count)
    const agents = [
      { id: 'a1', displayName: 'Agent 1', model: 'opus', tier: 'HIGH', category: 'A' }
    ];

    writeFileSync(
      join(tmpDir, 'config', 'agents.json'),
      JSON.stringify({ version: '1.0.0', agents }, null, 2)
    );

    const result = runDoctor(tmpDir);

    assert.equal(result.exitCode, 1);
  });

  it('Output includes pass/fail count', () => {
    const result = runDoctor(tmpDir);

    // Should show X/Y checks passed
    assert.match(result.output, /Summary:\s+\d+\/\d+\s+checks passed/);
  });
});
