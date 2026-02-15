/**
 * Tests for scripts/sync-version.js
 *
 * Uses Node.js built-in test runner (node:test) and assert module.
 * Tests version synchronization across all project files.
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, readFileSync, writeFileSync, mkdirSync, chmodSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { execSync } from 'child_process';

// ===========================================================================
// Test helpers
// ===========================================================================

function createTestContext() {
  const tmpDir = mkdtempSync(join(tmpdir(), 'sync-version-test-'));

  // Create minimal project structure
  mkdirSync(join(tmpDir, 'src'), { recursive: true });
  mkdirSync(join(tmpDir, 'config'), { recursive: true });
  mkdirSync(join(tmpDir, 'skills', 'test-skill'), { recursive: true });
  mkdirSync(join(tmpDir, 'skills', 'another-skill'), { recursive: true });
  mkdirSync(join(tmpDir, '.codex', 'skills', 'diverga-test-skill'), { recursive: true });
  mkdirSync(join(tmpDir, '.codex', 'skills', 'diverga-another-skill'), { recursive: true });
  mkdirSync(join(tmpDir, 'scripts'), { recursive: true });

  // Copy sync-version.js script
  const syncScript = readFileSync(
    join(process.cwd(), 'scripts', 'sync-version.js'),
    'utf-8'
  );
  writeFileSync(join(tmpDir, 'scripts', 'sync-version.js'), syncScript);

  // Create package.json with version
  const packageJson = {
    name: 'test-project',
    version: '1.2.3',
    scripts: {}
  };
  writeFileSync(
    join(tmpDir, 'package.json'),
    JSON.stringify(packageJson, null, 2)
  );

  // Create pyproject.toml
  const pyproject = `[project]
name = "test-project"
version = "1.2.3"
description = "Test project"
`;
  writeFileSync(join(tmpDir, 'pyproject.toml'), pyproject);

  // Create src/index.ts
  const indexTs = `/**
 * Test Project Index
 *
 * Diverga Agent Runtime v1.2.3
 */

export const VERSION = '1.2.3';

export function main() {
  console.log('Test');
}
`;
  writeFileSync(join(tmpDir, 'src', 'index.ts'), indexTs);

  // Create config/diverga-config.json
  const config = {
    version: '1.2.3',
    checkpointLevel: 'required'
  };
  writeFileSync(
    join(tmpDir, 'config', 'diverga-config.json'),
    JSON.stringify(config, null, 2) + '\n'
  );

  // Create skills/test-skill/SKILL.md
  const skillMd = `---
name: test-skill
description: Test skill
version: "1.2.3"
---

# Test Skill

This is a test skill.
`;
  writeFileSync(join(tmpDir, 'skills', 'test-skill', 'SKILL.md'), skillMd);

  // Create skills/another-skill/SKILL.md
  writeFileSync(join(tmpDir, 'skills', 'another-skill', 'SKILL.md'), skillMd);

  // Create .codex/skills/diverga-test-skill/SKILL.md
  const codexSkillMd = `metadata:
  name: diverga-test-skill
  version: 1.2.3
  description: Test skill for Codex

# Test Skill

Codex version.
`;
  writeFileSync(
    join(tmpDir, '.codex', 'skills', 'diverga-test-skill', 'SKILL.md'),
    codexSkillMd
  );

  // Create .codex/skills/diverga-another-skill/SKILL.md
  writeFileSync(
    join(tmpDir, '.codex', 'skills', 'diverga-another-skill', 'SKILL.md'),
    codexSkillMd
  );

  return { tmpDir };
}

function cleanup(tmpDir) {
  rmSync(tmpDir, { recursive: true, force: true });
}

function runSync(tmpDir, args = '--fix') {
  const result = execSync(`node scripts/sync-version.js ${args}`, {
    cwd: tmpDir,
    encoding: 'utf-8',
    stdio: 'pipe'
  });
  return result;
}

function runSyncExpectFail(tmpDir, args = '--check') {
  try {
    execSync(`node scripts/sync-version.js ${args}`, {
      cwd: tmpDir,
      encoding: 'utf-8',
      stdio: 'pipe'
    });
    return { exitCode: 0 };
  } catch (error) {
    return { exitCode: error.status };
  }
}

// ===========================================================================
// 1. Version reading
// ===========================================================================

describe('sync-version.js - Version reading', () => {
  let tmpDir;

  beforeEach(() => {
    ({ tmpDir } = createTestContext());
  });

  afterEach(() => {
    cleanup(tmpDir);
  });

  it('reads version from package.json correctly', () => {
    const output = runSync(tmpDir, '--check');

    // Should mention v1.2.3
    assert.match(output, /1\.2\.3/);
  });

  it('handles missing package.json gracefully', () => {
    rmSync(join(tmpDir, 'package.json'));

    assert.throws(() => {
      runSync(tmpDir, '--check');
    });
  });

  it('handles malformed package.json', () => {
    writeFileSync(join(tmpDir, 'package.json'), '{ invalid json }');

    assert.throws(() => {
      runSync(tmpDir, '--check');
    });
  });
});

// ===========================================================================
// 2. Version sync
// ===========================================================================

describe('sync-version.js - Version sync', () => {
  let tmpDir;

  beforeEach(() => {
    ({ tmpDir } = createTestContext());
  });

  afterEach(() => {
    cleanup(tmpDir);
  });

  it('updates pyproject.toml version field', () => {
    // Change package.json version
    const pkg = JSON.parse(readFileSync(join(tmpDir, 'package.json'), 'utf-8'));
    pkg.version = '2.0.0';
    writeFileSync(join(tmpDir, 'package.json'), JSON.stringify(pkg, null, 2));

    runSync(tmpDir, '--fix');

    const pyproject = readFileSync(join(tmpDir, 'pyproject.toml'), 'utf-8');
    assert.match(pyproject, /version = "2\.0\.0"/);
  });

  it('updates src/index.ts VERSION constant and JSDoc', () => {
    const pkg = JSON.parse(readFileSync(join(tmpDir, 'package.json'), 'utf-8'));
    pkg.version = '2.0.0';
    writeFileSync(join(tmpDir, 'package.json'), JSON.stringify(pkg, null, 2));

    runSync(tmpDir, '--fix');

    const indexTs = readFileSync(join(tmpDir, 'src', 'index.ts'), 'utf-8');
    assert.match(indexTs, /export const VERSION = '2\.0\.0'/);
    assert.match(indexTs, /Diverga Agent Runtime v2\.0\.0/);
  });

  it('updates SKILL.md version in frontmatter', () => {
    const pkg = JSON.parse(readFileSync(join(tmpDir, 'package.json'), 'utf-8'));
    pkg.version = '2.0.0';
    writeFileSync(join(tmpDir, 'package.json'), JSON.stringify(pkg, null, 2));

    runSync(tmpDir, '--fix');

    const skillMd = readFileSync(
      join(tmpDir, 'skills', 'test-skill', 'SKILL.md'),
      'utf-8'
    );
    assert.match(skillMd, /version: "2\.0\.0"/);
  });

  it('updates .codex/skills SKILL.md version in metadata', () => {
    const pkg = JSON.parse(readFileSync(join(tmpDir, 'package.json'), 'utf-8'));
    pkg.version = '2.0.0';
    writeFileSync(join(tmpDir, 'package.json'), JSON.stringify(pkg, null, 2));

    runSync(tmpDir, '--fix');

    const codexSkillMd = readFileSync(
      join(tmpDir, '.codex', 'skills', 'diverga-test-skill', 'SKILL.md'),
      'utf-8'
    );
    assert.match(codexSkillMd, /version: 2\.0\.0/);
  });

  it('updates config/diverga-config.json version', () => {
    const pkg = JSON.parse(readFileSync(join(tmpDir, 'package.json'), 'utf-8'));
    pkg.version = '2.0.0';
    writeFileSync(join(tmpDir, 'package.json'), JSON.stringify(pkg, null, 2));

    runSync(tmpDir, '--fix');

    const config = JSON.parse(readFileSync(
      join(tmpDir, 'config', 'diverga-config.json'),
      'utf-8'
    ));
    assert.equal(config.version, '2.0.0');
  });

  it('--check mode reports drift without fixing', () => {
    // Create drift
    const pkg = JSON.parse(readFileSync(join(tmpDir, 'package.json'), 'utf-8'));
    pkg.version = '2.0.0';
    writeFileSync(join(tmpDir, 'package.json'), JSON.stringify(pkg, null, 2));

    const result = runSyncExpectFail(tmpDir, '--check');

    // Should fail
    assert.equal(result.exitCode, 1);

    // Files should NOT be updated
    const pyproject = readFileSync(join(tmpDir, 'pyproject.toml'), 'utf-8');
    assert.match(pyproject, /version = "1\.2\.3"/); // Still old version
  });

  it('--check exits 1 when drift found, 0 when clean', () => {
    // Clean state
    let result = runSyncExpectFail(tmpDir, '--check');
    assert.equal(result.exitCode, 0);

    // Create drift
    const pkg = JSON.parse(readFileSync(join(tmpDir, 'package.json'), 'utf-8'));
    pkg.version = '2.0.0';
    writeFileSync(join(tmpDir, 'package.json'), JSON.stringify(pkg, null, 2));

    result = runSyncExpectFail(tmpDir, '--check');
    assert.equal(result.exitCode, 1);
  });

  it('--fix updates all files', () => {
    // Create drift
    const pkg = JSON.parse(readFileSync(join(tmpDir, 'package.json'), 'utf-8'));
    pkg.version = '3.0.0';
    writeFileSync(join(tmpDir, 'package.json'), JSON.stringify(pkg, null, 2));

    runSync(tmpDir, '--fix');

    // All files should be updated
    const pyproject = readFileSync(join(tmpDir, 'pyproject.toml'), 'utf-8');
    assert.match(pyproject, /version = "3\.0\.0"/);

    const indexTs = readFileSync(join(tmpDir, 'src', 'index.ts'), 'utf-8');
    assert.match(indexTs, /VERSION = '3\.0\.0'/);

    const skillMd = readFileSync(
      join(tmpDir, 'skills', 'test-skill', 'SKILL.md'),
      'utf-8'
    );
    assert.match(skillMd, /version: "3\.0\.0"/);
  });
});

// ===========================================================================
// 3. Edge cases
// ===========================================================================

describe('sync-version.js - Edge cases', () => {
  let tmpDir;

  beforeEach(() => {
    ({ tmpDir } = createTestContext());
  });

  afterEach(() => {
    cleanup(tmpDir);
  });

  it('handles files without version field', () => {
    // Create config without version
    writeFileSync(
      join(tmpDir, 'config', 'diverga-config.json'),
      JSON.stringify({ checkpointLevel: 'required' }, null, 2)
    );

    runSync(tmpDir, '--fix');

    const config = JSON.parse(readFileSync(
      join(tmpDir, 'config', 'diverga-config.json'),
      'utf-8'
    ));

    // Should add version
    assert.equal(config.version, '1.2.3');
  });

  it('handles read-only files (reports error)', () => {
    // Make pyproject.toml read-only
    chmodSync(join(tmpDir, 'pyproject.toml'), 0o444);

    // Change version
    const pkg = JSON.parse(readFileSync(join(tmpDir, 'package.json'), 'utf-8'));
    pkg.version = '2.0.0';
    writeFileSync(join(tmpDir, 'package.json'), JSON.stringify(pkg, null, 2));

    // Should throw error when trying to write
    assert.throws(() => {
      runSync(tmpDir, '--fix');
    });

    // Restore permissions for cleanup
    chmodSync(join(tmpDir, 'pyproject.toml'), 0o644);
  });

  it('no changes when already in sync', () => {
    const output = runSync(tmpDir, '--fix');

    // Should report 0 updated files
    assert.match(output, /0|already/i);
  });

  it('reports correct count of updated files', () => {
    // Create drift in 2 files
    const pkg = JSON.parse(readFileSync(join(tmpDir, 'package.json'), 'utf-8'));
    pkg.version = '2.0.0';
    writeFileSync(join(tmpDir, 'package.json'), JSON.stringify(pkg, null, 2));

    const output = runSync(tmpDir, '--fix');

    // Should report number of updated files (pyproject, src/index.ts, config, 2 skills, 2 codex skills = 7)
    assert.match(output, /7|Updated/);
  });
});
