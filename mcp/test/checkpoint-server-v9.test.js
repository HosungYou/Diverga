/**
 * TDD RED Tests for Diverga v9.0 Checkpoint Server (Split)
 *
 * Tests the split checkpoint server that handles ONLY checkpoint and prerequisite tools.
 * Memory/decision tools are moved to memory-server.js.
 * Comm tools are moved to comm-server.js.
 *
 * Uses Node.js built-in test runner (node:test) and assert module.
 */

import { describe, it, before, after, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import yaml from 'js-yaml';
import { createCheckpointServer } from '../servers/checkpoint-server.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PREREQ_MAP = JSON.parse(readFileSync(join(__dirname, '..', 'agent-prerequisite-map.json'), 'utf8'));

/**
 * Helper: create a fresh temp dir and server instance for each suite.
 */
function createTestContext() {
  const tmpDir = mkdtempSync(join(tmpdir(), 'checkpoint-server-v9-test-'));
  const server = createCheckpointServer(PREREQ_MAP, tmpDir);
  return { tmpDir, server };
}

function cleanup(tmpDir) {
  rmSync(tmpDir, { recursive: true, force: true });
}

/** Write a YAML file into the temp research dir */
function writeTestYaml(tmpDir, filename, data) {
  const filepath = join(tmpDir, filename);
  const dir = dirname(filepath);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(filepath, yaml.dump(data, { lineWidth: 120, noRefs: true }), 'utf8');
}

/** Read a YAML file from the temp research dir */
function readTestYaml(tmpDir, filename) {
  const filepath = join(tmpDir, filename);
  if (!existsSync(filepath)) return null;
  return yaml.load(readFileSync(filepath, 'utf8'));
}

// ===========================================================================
// 1. Server Factory
// ===========================================================================

describe('createCheckpointServer factory', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('creates server instance with all checkpoint tools', () => {
    assert.ok(server);
    assert.equal(typeof server.checkPrerequisites, 'function');
    assert.equal(typeof server.markCheckpoint, 'function');
    assert.equal(typeof server.checkpointStatus, 'function');
    cleanup(tmpDir);
  });

  it('does NOT include memory tools (moved to memory-server)', () => {
    assert.equal(server.readProjectState, undefined);
    assert.equal(server.updateProjectState, undefined);
    assert.equal(server.addDecision, undefined);
    assert.equal(server.listDecisions, undefined);
    assert.equal(server.exportToYaml, undefined);
    cleanup(tmpDir);
  });

  it('does NOT include comm tools (moved to comm-server)', () => {
    assert.equal(server.send, undefined);
    assert.equal(server.broadcast, undefined);
    assert.equal(server.mailbox, undefined);
    assert.equal(server.acknowledge, undefined);
    assert.equal(server.registerAgent, undefined);
    cleanup(tmpDir);
  });

  it('accepts prerequisite map and research directory', () => {
    const customMap = { agents: { a1: { prerequisites: [] } } };
    const customDir = mkdtempSync(join(tmpdir(), 'custom-'));

    const customServer = createCheckpointServer(customMap, customDir);
    assert.ok(customServer);

    cleanup(customDir);
    cleanup(tmpDir);
  });

  it('throws error when prerequisite map is missing', () => {
    assert.throws(() => {
      createCheckpointServer(null, tmpDir);
    }, /prerequisite map/i);
    cleanup(tmpDir);
  });

  it('throws error when research directory is missing', () => {
    assert.throws(() => {
      createCheckpointServer(PREREQ_MAP, null);
    }, /research directory/i);
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 2. checkPrerequisites (same contract as v8)
// ===========================================================================

describe('checkPrerequisites', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('entry point agent returns approved:true with no prerequisites', () => {
    const result = server.checkPrerequisites('a1');
    assert.equal(result.approved, true);
    assert.deepEqual(result.missing, []);
    assert.match(result.message, /entry point|no prerequisites/i);
    cleanup(tmpDir);
  });

  it('agent with unmet prerequisites returns approved:false and missing list', () => {
    const result = server.checkPrerequisites('c5');
    assert.equal(result.approved, false);
    assert.ok(result.missing.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(result.missing.includes('CP_METHODOLOGY_APPROVAL'));
    cleanup(tmpDir);
  });

  it('agent with all prerequisites met returns approved:true', () => {
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' },
          { checkpoint_id: 'CP_METHODOLOGY_APPROVAL', status: 'completed' },
        ]
      }
    });

    const result = server.checkPrerequisites('c5');
    assert.equal(result.approved, true);
    assert.deepEqual(result.missing, []);
    cleanup(tmpDir);
  });

  it('normalizes agent IDs correctly', () => {
    const r1 = server.checkPrerequisites('C5');
    const r2 = server.checkPrerequisites('c5');
    const r3 = server.checkPrerequisites('c5-meta-analysis');

    assert.deepEqual(r1.missing, r2.missing);
    assert.deepEqual(r2.missing, r3.missing);
    cleanup(tmpDir);
  });

  it('recognizes prerequisites from decision-log.yaml', () => {
    writeTestYaml(tmpDir, 'decision-log.yaml', {
      decisions: [
        { checkpoint_id: 'CP_RESEARCH_DIRECTION', selected: 'AI in education' }
      ]
    });

    const result = server.checkPrerequisites('a2');
    assert.equal(result.approved, true);
    cleanup(tmpDir);
  });

  it('reads from research/ directory (v8.4 dual structure)', () => {
    const researchDir = join(tmpDir, 'research');
    mkdirSync(researchDir, { recursive: true });

    writeFileSync(
      join(researchDir, 'checkpoints.yaml'),
      yaml.dump({
        checkpoints: {
          active: [{ checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' }]
        }
      })
    );

    const result = server.checkPrerequisites('a2');
    assert.equal(result.approved, true);
    cleanup(tmpDir);
  });

  it('falls back to legacy .research/ directory', () => {
    const legacyDir = join(tmpDir, '.research');
    mkdirSync(legacyDir, { recursive: true });

    writeFileSync(
      join(legacyDir, 'checkpoints.yaml'),
      yaml.dump({
        checkpoints: {
          active: [{ checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' }]
        }
      })
    );

    const result = server.checkPrerequisites('a2');
    assert.equal(result.approved, true);
    cleanup(tmpDir);
  });

  it('prefers research/ over .research/ when both exist', () => {
    const researchDir = join(tmpDir, 'research');
    const legacyDir = join(tmpDir, '.research');
    mkdirSync(researchDir, { recursive: true });
    mkdirSync(legacyDir, { recursive: true });

    // research/ has CP_RESEARCH_DIRECTION
    writeFileSync(
      join(researchDir, 'checkpoints.yaml'),
      yaml.dump({
        checkpoints: {
          active: [{ checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' }]
        }
      })
    );

    // .research/ has different checkpoint
    writeFileSync(
      join(legacyDir, 'checkpoints.yaml'),
      yaml.dump({
        checkpoints: {
          active: [{ checkpoint_id: 'CP_PARADIGM_SELECTION', status: 'completed' }]
        }
      })
    );

    const result = server.checkPrerequisites('a2');
    assert.equal(result.approved, true); // Should find CP_RESEARCH_DIRECTION from research/
    cleanup(tmpDir);
  });

  it('returns own_checkpoints field', () => {
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        active: [{ checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' }]
      }
    });

    const result = server.checkPrerequisites('a2');
    assert.ok(Array.isArray(result.own_checkpoints));
    assert.ok(result.own_checkpoints.length > 0);
    cleanup(tmpDir);
  });

  it('handles malformed checkpoints.yaml gracefully', () => {
    writeFileSync(join(tmpDir, 'checkpoints.yaml'), 'invalid: yaml: [', 'utf8');

    const result = server.checkPrerequisites('a2');
    assert.equal(result.approved, false); // Should default to not approved on error
    cleanup(tmpDir);
  });

  it('handles missing agent in prerequisite map', () => {
    const result = server.checkPrerequisites('z99-unknown');
    assert.equal(result.approved, true); // Unknown agents have no restrictions
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 3. markCheckpoint (same contract as v8)
// ===========================================================================

describe('markCheckpoint', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('creates checkpoints.yaml if it does not exist', () => {
    assert.equal(existsSync(join(tmpDir, 'checkpoints.yaml')), false);

    server.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core research area');

    assert.equal(existsSync(join(tmpDir, 'checkpoints.yaml')), true);
    cleanup(tmpDir);
  });

  it('writes to research/ directory by default (v8.4)', () => {
    server.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core');

    const researchPath = join(tmpDir, 'research', 'checkpoints.yaml');
    assert.equal(existsSync(researchPath), true);
    cleanup(tmpDir);
  });

  it('records checkpoint with correct structure', () => {
    server.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core research area');

    const data = readTestYaml(join(tmpDir, 'research'), 'checkpoints.yaml');
    const cp = data.checkpoints.active[0];
    assert.equal(cp.checkpoint_id, 'CP_RESEARCH_DIRECTION');
    assert.equal(cp.status, 'completed');
    assert.equal(cp.decision, 'AI in education');
    assert.equal(cp.rationale, 'Core research area');
    assert.ok(cp.completed_at);
    cleanup(tmpDir);
  });

  it('creates decision-log.yaml in research/ directory', () => {
    server.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core');

    const decisionPath = join(tmpDir, 'research', 'decision-log.yaml');
    assert.equal(existsSync(decisionPath), true);
    cleanup(tmpDir);
  });

  it('records decision with correct structure', () => {
    server.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core');

    const data = readTestYaml(join(tmpDir, 'research'), 'decision-log.yaml');
    const d = data.decisions[0];
    assert.equal(d.decision_id, 'DEV_001');
    assert.equal(d.checkpoint_id, 'CP_RESEARCH_DIRECTION');
    assert.equal(d.selected, 'AI in education');
    assert.equal(d.rationale, 'Core');
    cleanup(tmpDir);
  });

  it('generates sequential decision IDs', () => {
    const r1 = server.markCheckpoint('CP_RESEARCH_DIRECTION', 'D1', 'R1');
    const r2 = server.markCheckpoint('CP_PARADIGM_SELECTION', 'D2', 'R2');
    const r3 = server.markCheckpoint('CP_THEORY_SELECTION', 'D3', 'R3');

    assert.equal(r1.decision_id, 'DEV_001');
    assert.equal(r2.decision_id, 'DEV_002');
    assert.equal(r3.decision_id, 'DEV_003');
    cleanup(tmpDir);
  });

  it('updates priority context in .research/ directory', () => {
    server.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core');

    const contextPath = join(tmpDir, '.research', 'priority-context.md');
    assert.equal(existsSync(contextPath), true);

    const content = readFileSync(contextPath, 'utf8');
    assert.ok(content.includes('CP_RESEARCH_DIRECTION'));
    cleanup(tmpDir);
  });

  it('replaces pending entry if exists for same checkpoint', () => {
    writeTestYaml(join(tmpDir, 'research'), 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'pending', level: 'REQUIRED' }
        ]
      }
    });

    server.markCheckpoint('CP_RESEARCH_DIRECTION', 'Final decision', 'Updated');

    const data = readTestYaml(join(tmpDir, 'research'), 'checkpoints.yaml');
    const matching = data.checkpoints.active.filter(cp => cp.checkpoint_id === 'CP_RESEARCH_DIRECTION');
    assert.equal(matching.length, 1);
    assert.equal(matching[0].status, 'completed');
    cleanup(tmpDir);
  });

  it('returns correct response shape', () => {
    const result = server.markCheckpoint('CP_RESEARCH_DIRECTION', 'test', 'test');
    assert.equal(result.recorded, true);
    assert.equal(result.checkpoint_id, 'CP_RESEARCH_DIRECTION');
    assert.equal(result.decision_id, 'DEV_001');
    cleanup(tmpDir);
  });

  it('handles checkpoint level from definitions', () => {
    const result = server.markCheckpoint('CP_RESEARCH_DIRECTION', 'test', 'test');

    const data = readTestYaml(join(tmpDir, 'research'), 'checkpoints.yaml');
    const cp = data.checkpoints.active[0];
    assert.equal(cp.level, 'REQUIRED'); // CP_RESEARCH_DIRECTION is REQUIRED
    cleanup(tmpDir);
  });

  it('handles unknown checkpoint gracefully', () => {
    const result = server.markCheckpoint('UNKNOWN_CP_999', 'decision', 'rationale');
    assert.equal(result.recorded, true);

    const data = readTestYaml(join(tmpDir, 'research'), 'checkpoints.yaml');
    const cp = data.checkpoints.active[0];
    assert.equal(cp.level, 'UNKNOWN');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 4. checkpointStatus (same contract as v8)
// ===========================================================================

describe('checkpointStatus', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('returns empty arrays when no checkpoints exist', () => {
    const result = server.checkpointStatus();
    assert.deepEqual(result.passed, []);
    assert.deepEqual(result.pending, []);
    assert.equal(result.total_decisions, 0);
    assert.ok(Array.isArray(result.blocked));
    cleanup(tmpDir);
  });

  it('returns passed checkpoints from checkpoints.yaml', () => {
    writeTestYaml(join(tmpDir, 'research'), 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' },
          { checkpoint_id: 'CP_PARADIGM_SELECTION', status: 'completed' },
        ]
      }
    });

    const result = server.checkpointStatus();
    assert.ok(result.passed.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(result.passed.includes('CP_PARADIGM_SELECTION'));
    cleanup(tmpDir);
  });

  it('returns passed checkpoints from decision-log.yaml', () => {
    writeTestYaml(join(tmpDir, 'research'), 'decision-log.yaml', {
      decisions: [
        { checkpoint_id: 'CP_THEORY_SELECTION', selected: 'TAM' }
      ]
    });

    const result = server.checkpointStatus();
    assert.ok(result.passed.includes('CP_THEORY_SELECTION'));
    cleanup(tmpDir);
  });

  it('lists pending checkpoints correctly', () => {
    writeTestYaml(join(tmpDir, 'research'), 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' },
          { checkpoint_id: 'CP_PARADIGM_SELECTION', status: 'pending' },
        ]
      }
    });

    const result = server.checkpointStatus();
    assert.ok(result.passed.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(result.pending.includes('CP_PARADIGM_SELECTION'));
    cleanup(tmpDir);
  });

  it('lists blocked agents with missing prerequisites', () => {
    const result = server.checkpointStatus();

    const c5blocked = result.blocked.find(b => b.agent === 'c5');
    assert.ok(c5blocked);
    assert.ok(c5blocked.missing.includes('CP_RESEARCH_DIRECTION'));
    cleanup(tmpDir);
  });

  it('unblocks agents when prerequisites are met', () => {
    writeTestYaml(join(tmpDir, 'research'), 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' },
        ]
      }
    });

    const result = server.checkpointStatus();
    const a2blocked = result.blocked.find(b => b.agent === 'a2');
    assert.equal(a2blocked, undefined);
    cleanup(tmpDir);
  });

  it('deduplicates checkpoints from both sources', () => {
    writeTestYaml(join(tmpDir, 'research'), 'checkpoints.yaml', {
      checkpoints: {
        active: [{ checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' }]
      }
    });
    writeTestYaml(join(tmpDir, 'research'), 'decision-log.yaml', {
      decisions: [{ checkpoint_id: 'CP_RESEARCH_DIRECTION', selected: 'AI' }]
    });

    const result = server.checkpointStatus();
    const count = result.passed.filter(cp => cp === 'CP_RESEARCH_DIRECTION').length;
    assert.equal(count, 1);
    cleanup(tmpDir);
  });

  it('returns total_decisions count', () => {
    writeTestYaml(join(tmpDir, 'research'), 'decision-log.yaml', {
      decisions: [
        { checkpoint_id: 'CP_A', selected: 'x' },
        { checkpoint_id: 'CP_B', selected: 'y' },
      ]
    });

    const result = server.checkpointStatus();
    assert.equal(result.total_decisions, 2);
    cleanup(tmpDir);
  });

  it('handles multiple stages in checkpoints.yaml', () => {
    writeTestYaml(join(tmpDir, 'research'), 'checkpoints.yaml', {
      checkpoints: {
        stage1: [{ checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' }],
        stage2: [{ checkpoint_id: 'CP_PARADIGM_SELECTION', status: 'completed' }],
        active: [{ checkpoint_id: 'CP_METHODOLOGY_APPROVAL', status: 'pending' }]
      }
    });

    const result = server.checkpointStatus();
    assert.ok(result.passed.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(result.passed.includes('CP_PARADIGM_SELECTION'));
    assert.ok(result.pending.includes('CP_METHODOLOGY_APPROVAL'));
    cleanup(tmpDir);
  });

  it('reads from both research/ and .research/ directories', () => {
    writeTestYaml(join(tmpDir, 'research'), 'checkpoints.yaml', {
      checkpoints: {
        active: [{ checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' }]
      }
    });
    writeTestYaml(join(tmpDir, '.research'), 'decision-log.yaml', {
      decisions: [{ checkpoint_id: 'CP_PARADIGM_SELECTION', selected: 'Quant' }]
    });

    const result = server.checkpointStatus();
    assert.ok(result.passed.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(result.passed.includes('CP_PARADIGM_SELECTION'));
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 5. Integration: checkpoint enforcement workflow
// ===========================================================================

describe('integration: checkpoint enforcement workflow', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('full workflow: check → mark → verify', () => {
    // Step 1: Check prerequisites - c5 blocked
    const check1 = server.checkPrerequisites('c5');
    assert.equal(check1.approved, false);

    // Step 2: Mark first prerequisite
    server.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI Learning', 'Core');

    // Step 3: Still blocked (missing CP_METHODOLOGY_APPROVAL)
    const check2 = server.checkPrerequisites('c5');
    assert.equal(check2.approved, false);

    // Step 4: Mark second prerequisite
    server.markCheckpoint('CP_METHODOLOGY_APPROVAL', 'Meta-analysis', 'Best fit');

    // Step 5: Now approved
    const check3 = server.checkPrerequisites('c5');
    assert.equal(check3.approved, true);

    // Step 6: Verify status
    const status = server.checkpointStatus();
    assert.ok(status.passed.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(status.passed.includes('CP_METHODOLOGY_APPROVAL'));

    cleanup(tmpDir);
  });

  it('multiple agents unblock as checkpoints complete', () => {
    // Initially: a2, c1, c2, c3 all blocked (need CP_RESEARCH_DIRECTION)
    assert.equal(server.checkPrerequisites('a2').approved, false);
    assert.equal(server.checkPrerequisites('c1').approved, false);

    // Mark CP_RESEARCH_DIRECTION
    server.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI', 'Core');

    // a2 unblocked (only needed CP_RESEARCH_DIRECTION)
    assert.equal(server.checkPrerequisites('a2').approved, true);

    // c1 still blocked (needs CP_PARADIGM_SELECTION too)
    assert.equal(server.checkPrerequisites('c1').approved, false);

    // Mark CP_PARADIGM_SELECTION
    server.markCheckpoint('CP_PARADIGM_SELECTION', 'Quantitative', 'RCT design');

    // c1 now unblocked
    assert.equal(server.checkPrerequisites('c1').approved, true);

    cleanup(tmpDir);
  });

  it('checkpoint status reflects real-time changes', () => {
    let status = server.checkpointStatus();
    assert.equal(status.passed.length, 0);

    server.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI', 'test');
    status = server.checkpointStatus();
    assert.equal(status.passed.length, 1);

    server.markCheckpoint('CP_PARADIGM_SELECTION', 'Quant', 'test');
    status = server.checkpointStatus();
    assert.equal(status.passed.length, 2);

    cleanup(tmpDir);
  });

  it('handles legacy .research/ migration to research/', () => {
    // Write to legacy .research/
    writeTestYaml(join(tmpDir, '.research'), 'checkpoints.yaml', {
      checkpoints: {
        active: [{ checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' }]
      }
    });

    // Server should still read it
    const result = server.checkPrerequisites('a2');
    assert.equal(result.approved, true);

    // New writes go to research/
    server.markCheckpoint('CP_PARADIGM_SELECTION', 'Quant', 'test');
    const researchPath = join(tmpDir, 'research', 'checkpoints.yaml');
    assert.equal(existsSync(researchPath), true);

    cleanup(tmpDir);
  });
});
