/**
 * TDD RED Tests for Diverga v9.0 SQLite State Management
 *
 * Tests the SQLite state layer that replaces YAML files as source of truth.
 * YAML files become export format only for researcher visibility.
 *
 * Module under test: mcp/lib/sqlite-state.js (doesn't exist yet → RED)
 *
 * Uses Node.js built-in test runner (node:test) and assert module.
 * Each test suite creates an isolated temporary directory for state files.
 */

import { describe, it, before, after, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import yaml from 'js-yaml';
import { createStateStore } from '../lib/sqlite-state.js';

/**
 * Helper: create a fresh temp dir and state store for each suite.
 */
function createTestContext() {
  const tmpDir = mkdtempSync(join(tmpdir(), 'sqlite-state-test-'));
  const dbPath = join(tmpDir, 'diverga-state.db');
  const store = createStateStore(dbPath);
  return { tmpDir, dbPath, store };
}

function cleanup(tmpDir) {
  rmSync(tmpDir, { recursive: true, force: true });
}

/** Write a YAML file for migration tests */
function writeTestYaml(tmpDir, filename, data) {
  const filepath = join(tmpDir, filename);
  const dir = join(tmpDir, 'research');
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, filename), yaml.dump(data, { lineWidth: 120, noRefs: true }), 'utf8');
}

/** Read exported YAML file */
function readTestYaml(tmpDir, filename) {
  const filepath = join(tmpDir, 'research', filename);
  if (!existsSync(filepath)) return null;
  return yaml.load(readFileSync(filepath, 'utf8'));
}

// ===========================================================================
// 1. Database Initialization (~5 tests)
// ===========================================================================

describe('Database initialization', () => {
  let tmpDir, dbPath, store;

  beforeEach(() => {
    ({ tmpDir, dbPath, store } = createTestContext());
  });

  it('creates SQLite file at given path', () => {
    assert.equal(existsSync(dbPath), true, 'Database file should be created');
    cleanup(tmpDir);
  });

  it('creates tables: checkpoints, decisions, project_state, messages, agents', () => {
    // This test verifies table existence by attempting to query each table
    // Since the module doesn't exist yet, this will fail (RED)
    const tables = ['checkpoints', 'decisions', 'project_state', 'messages', 'agents'];

    tables.forEach(tableName => {
      assert.doesNotThrow(() => {
        // Query should not throw if table exists
        store.db.prepare(`SELECT * FROM ${tableName} LIMIT 0`).all();
      }, `Table ${tableName} should exist`);
    });
    cleanup(tmpDir);
  });

  it('idempotent: calling twice does not error', () => {
    // Create another store instance on the same database
    assert.doesNotThrow(() => {
      const store2 = createStateStore(dbPath);
    }, 'Second initialization should not error');
    cleanup(tmpDir);
  });

  it('returns store object with all methods', () => {
    const expectedMethods = [
      'markCheckpoint',
      'getCheckpoint',
      'listCheckpoints',
      'isCheckpointApproved',
      'getCheckpointsByLevel',
      'addDecision',
      'listDecisions',
      'getDecision',
      'amendDecision',
      'getProjectState',
      'updateProjectState',
      'setStage',
      'getStage',
      'exportCheckpointsYaml',
      'exportDecisionLogYaml',
      'exportProjectStateYaml',
      'exportAll',
      'migrateFromYaml'
    ];

    expectedMethods.forEach(method => {
      assert.equal(typeof store[method], 'function', `store.${method} should be a function`);
    });
    cleanup(tmpDir);
  });

  it('database version tracking (schema migrations)', () => {
    // Query schema version metadata table
    assert.doesNotThrow(() => {
      const version = store.db.prepare('SELECT version FROM schema_version ORDER BY applied_at DESC LIMIT 1').get();
      assert.ok(version, 'Schema version should be tracked');
      assert.equal(typeof version.version, 'number', 'Version should be a number');
    }, 'Schema version tracking should exist');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 2. Checkpoint CRUD (~10 tests)
// ===========================================================================

describe('Checkpoint CRUD', () => {
  let tmpDir, dbPath, store;

  beforeEach(() => {
    ({ tmpDir, dbPath, store } = createTestContext());
  });

  it('store.markCheckpoint(cpId, decision, rationale) → creates record', () => {
    const result = store.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core focus area');

    assert.equal(result.recorded, true);
    assert.equal(result.checkpoint_id, 'CP_RESEARCH_DIRECTION');

    const checkpoint = store.getCheckpoint('CP_RESEARCH_DIRECTION');
    assert.equal(checkpoint.checkpoint_id, 'CP_RESEARCH_DIRECTION');
    assert.equal(checkpoint.decision, 'AI in education');
    assert.equal(checkpoint.rationale, 'Core focus area');
    cleanup(tmpDir);
  });

  it('store.getCheckpoint(cpId) → returns checkpoint or null', () => {
    store.markCheckpoint('CP_PARADIGM_SELECTION', 'Quantitative', 'Best fit');

    const exists = store.getCheckpoint('CP_PARADIGM_SELECTION');
    assert.ok(exists, 'Should return checkpoint that exists');
    assert.equal(exists.checkpoint_id, 'CP_PARADIGM_SELECTION');

    const notExists = store.getCheckpoint('CP_NONEXISTENT');
    assert.equal(notExists, null, 'Should return null for non-existent checkpoint');
    cleanup(tmpDir);
  });

  it('store.listCheckpoints() → returns all checkpoints sorted by time', () => {
    store.markCheckpoint('CP_A', 'Decision A', 'Rationale A');
    store.markCheckpoint('CP_B', 'Decision B', 'Rationale B');
    store.markCheckpoint('CP_C', 'Decision C', 'Rationale C');

    const checkpoints = store.listCheckpoints();
    assert.equal(checkpoints.length, 3);

    // Should be sorted by completed_at descending (most recent first)
    assert.equal(checkpoints[0].checkpoint_id, 'CP_C');
    assert.equal(checkpoints[1].checkpoint_id, 'CP_B');
    assert.equal(checkpoints[2].checkpoint_id, 'CP_A');
    cleanup(tmpDir);
  });

  it('store.isCheckpointApproved(cpId) → true/false', () => {
    assert.equal(store.isCheckpointApproved('CP_RESEARCH_DIRECTION'), false, 'Should be false before marking');

    store.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI', 'test');

    assert.equal(store.isCheckpointApproved('CP_RESEARCH_DIRECTION'), true, 'Should be true after marking');
    cleanup(tmpDir);
  });

  it('store.getCheckpointsByLevel("required") → filters by level', () => {
    store.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI', 'test'); // REQUIRED
    store.markCheckpoint('CP_SCREENING_CRITERIA', 'RCT only', 'test'); // RECOMMENDED
    store.markCheckpoint('CP_VISUALIZATION_PREFERENCE', 'Mermaid', 'test'); // OPTIONAL

    const required = store.getCheckpointsByLevel('required');
    assert.ok(required.length > 0, 'Should return required checkpoints');
    assert.ok(required.every(cp => cp.level === 'REQUIRED'), 'All should have REQUIRED level');

    const recommended = store.getCheckpointsByLevel('recommended');
    assert.ok(recommended.length > 0, 'Should return recommended checkpoints');

    const optional = store.getCheckpointsByLevel('optional');
    assert.ok(optional.length > 0, 'Should return optional checkpoints');
    cleanup(tmpDir);
  });

  it('duplicate markCheckpoint updates, does not duplicate', () => {
    store.markCheckpoint('CP_RESEARCH_DIRECTION', 'First decision', 'First rationale');
    store.markCheckpoint('CP_RESEARCH_DIRECTION', 'Updated decision', 'Updated rationale');

    const checkpoints = store.listCheckpoints();
    const matching = checkpoints.filter(cp => cp.checkpoint_id === 'CP_RESEARCH_DIRECTION');

    assert.equal(matching.length, 1, 'Should have exactly one record');
    assert.equal(matching[0].decision, 'Updated decision', 'Should have updated decision');
    assert.equal(matching[0].rationale, 'Updated rationale', 'Should have updated rationale');
    cleanup(tmpDir);
  });

  it('timestamps are auto-set (ISO 8601)', () => {
    store.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI', 'test');

    const checkpoint = store.getCheckpoint('CP_RESEARCH_DIRECTION');
    assert.ok(checkpoint.completed_at, 'Timestamp should exist');

    // Verify ISO 8601 format
    const isoRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/;
    assert.match(checkpoint.completed_at, isoRegex, 'Should be ISO 8601 format');
    cleanup(tmpDir);
  });

  it('rationale is optional', () => {
    const result = store.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education');

    assert.equal(result.recorded, true);

    const checkpoint = store.getCheckpoint('CP_RESEARCH_DIRECTION');
    assert.equal(checkpoint.decision, 'AI in education');
    // rationale should be null or empty string
    assert.ok(!checkpoint.rationale || checkpoint.rationale === '', 'Rationale should be optional');
    cleanup(tmpDir);
  });

  it('checkpoint level is determined from checkpoint_id', () => {
    store.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI', 'test'); // REQUIRED
    store.markCheckpoint('CP_SCREENING_CRITERIA', 'RCT', 'test'); // RECOMMENDED
    store.markCheckpoint('CP_VISUALIZATION_PREFERENCE', 'Mermaid', 'test'); // OPTIONAL

    const cp1 = store.getCheckpoint('CP_RESEARCH_DIRECTION');
    assert.equal(cp1.level, 'REQUIRED');

    const cp2 = store.getCheckpoint('CP_SCREENING_CRITERIA');
    assert.equal(cp2.level, 'RECOMMENDED');

    const cp3 = store.getCheckpoint('CP_VISUALIZATION_PREFERENCE');
    assert.equal(cp3.level, 'OPTIONAL');
    cleanup(tmpDir);
  });

  it('status is always "completed" after markCheckpoint', () => {
    store.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI', 'test');

    const checkpoint = store.getCheckpoint('CP_RESEARCH_DIRECTION');
    assert.equal(checkpoint.status, 'completed');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 3. Decision Log (~8 tests)
// ===========================================================================

describe('Decision log', () => {
  let tmpDir, dbPath, store;

  beforeEach(() => {
    ({ tmpDir, dbPath, store } = createTestContext());
  });

  it('store.addDecision(cpId, selected, rationale, context?) → creates decision', () => {
    const result = store.addDecision('CP_RESEARCH_DIRECTION', 'AI in education', 'Core focus', { agent: 'a1' });

    assert.equal(result.recorded, true);
    assert.ok(result.decision_id, 'Should return decision_id');

    const decision = store.getDecision(result.decision_id);
    assert.equal(decision.checkpoint_id, 'CP_RESEARCH_DIRECTION');
    assert.equal(decision.selected, 'AI in education');
    assert.equal(decision.rationale, 'Core focus');
    cleanup(tmpDir);
  });

  it('store.listDecisions() → all decisions sorted by time', () => {
    store.addDecision('CP_A', 'Decision A', 'Rationale A');
    store.addDecision('CP_B', 'Decision B', 'Rationale B');
    store.addDecision('CP_C', 'Decision C', 'Rationale C');

    const decisions = store.listDecisions();
    assert.equal(decisions.length, 3);

    // Should be sorted by timestamp descending (most recent first)
    assert.equal(decisions[0].checkpoint_id, 'CP_C');
    assert.equal(decisions[1].checkpoint_id, 'CP_B');
    assert.equal(decisions[2].checkpoint_id, 'CP_A');
    cleanup(tmpDir);
  });

  it('store.getDecision(decisionId) → single decision', () => {
    const result = store.addDecision('CP_RESEARCH_DIRECTION', 'AI', 'test');

    const decision = store.getDecision(result.decision_id);
    assert.ok(decision, 'Should return decision');
    assert.equal(decision.decision_id, result.decision_id);
    assert.equal(decision.selected, 'AI');

    const notExists = store.getDecision('DEV_999');
    assert.equal(notExists, null, 'Should return null for non-existent decision');
    cleanup(tmpDir);
  });

  it('store.amendDecision(decisionId, newSelected, newRationale) → updates + keeps history', () => {
    const original = store.addDecision('CP_RESEARCH_DIRECTION', 'Original decision', 'Original rationale');

    const amended = store.amendDecision(original.decision_id, 'Amended decision', 'Amended rationale');

    assert.equal(amended.recorded, true);
    assert.ok(amended.decision_id, 'Should return new decision_id');
    assert.notEqual(amended.decision_id, original.decision_id, 'Should be a new decision_id');

    // Original decision should still exist
    const originalDecision = store.getDecision(original.decision_id);
    assert.ok(originalDecision, 'Original decision should be preserved');
    assert.equal(originalDecision.selected, 'Original decision');

    // New decision should exist
    const amendedDecision = store.getDecision(amended.decision_id);
    assert.equal(amendedDecision.selected, 'Amended decision');
    assert.equal(amendedDecision.version, 2, 'Version should increment');
    cleanup(tmpDir);
  });

  it('decisions are append-only (amend creates new version, old preserved)', () => {
    const v1 = store.addDecision('CP_RESEARCH_DIRECTION', 'v1', 'rationale1');
    const v2 = store.amendDecision(v1.decision_id, 'v2', 'rationale2');
    const v3 = store.amendDecision(v2.decision_id, 'v3', 'rationale3');

    const allDecisions = store.listDecisions();
    const rdDecisions = allDecisions.filter(d => d.checkpoint_id === 'CP_RESEARCH_DIRECTION');

    assert.equal(rdDecisions.length, 3, 'Should have 3 versions');
    assert.equal(rdDecisions[0].version, 3);
    assert.equal(rdDecisions[1].version, 2);
    assert.equal(rdDecisions[2].version, 1);
    cleanup(tmpDir);
  });

  it('decision IDs are auto-generated (DEV_001, DEV_002...)', () => {
    const d1 = store.addDecision('CP_A', 'A', 'r');
    const d2 = store.addDecision('CP_B', 'B', 'r');
    const d3 = store.addDecision('CP_C', 'C', 'r');

    assert.equal(d1.decision_id, 'DEV_001');
    assert.equal(d2.decision_id, 'DEV_002');
    assert.equal(d3.decision_id, 'DEV_003');
    cleanup(tmpDir);
  });

  it('context parameter is optional', () => {
    const withContext = store.addDecision('CP_A', 'A', 'r', { agent: 'a1', t_score: 0.6 });
    const withoutContext = store.addDecision('CP_B', 'B', 'r');

    const d1 = store.getDecision(withContext.decision_id);
    assert.ok(d1.context, 'Context should be stored');

    const d2 = store.getDecision(withoutContext.decision_id);
    assert.ok(!d2.context || d2.context === null, 'Context should be optional');
    cleanup(tmpDir);
  });

  it('timestamp is auto-set for all decisions', () => {
    const result = store.addDecision('CP_RESEARCH_DIRECTION', 'AI', 'test');
    const decision = store.getDecision(result.decision_id);

    assert.ok(decision.timestamp, 'Timestamp should exist');

    const isoRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/;
    assert.match(decision.timestamp, isoRegex, 'Should be ISO 8601 format');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 4. Project State (~6 tests)
// ===========================================================================

describe('Project state', () => {
  let tmpDir, dbPath, store;

  beforeEach(() => {
    ({ tmpDir, dbPath, store } = createTestContext());
  });

  it('store.getProjectState() → returns full state object', () => {
    const state = store.getProjectState();

    assert.ok(state, 'Should return state object');
    assert.equal(typeof state, 'object', 'Should be an object');
    cleanup(tmpDir);
  });

  it('store.updateProjectState(updates) → merges updates', () => {
    store.updateProjectState({ project: { name: 'Test Project' } });
    store.updateProjectState({ research: { paradigm: 'quantitative' } });

    const state = store.getProjectState();
    assert.equal(state.project.name, 'Test Project');
    assert.equal(state.research.paradigm, 'quantitative');
    cleanup(tmpDir);
  });

  it('store.setStage(stageName) → updates current stage', () => {
    store.setStage('design');

    const stage = store.getStage();
    assert.equal(stage, 'design');
    cleanup(tmpDir);
  });

  it('store.getStage() → returns current stage name', () => {
    assert.equal(store.getStage(), null, 'Should be null initially');

    store.setStage('literature_review');
    assert.equal(store.getStage(), 'literature_review');
    cleanup(tmpDir);
  });

  it('initial state is empty object', () => {
    const state = store.getProjectState();

    // Should be an empty object or have minimal default structure
    const keys = Object.keys(state);
    assert.ok(keys.length === 0 || JSON.stringify(state) === '{}', 'Initial state should be empty');
    cleanup(tmpDir);
  });

  it('nested object merging works correctly', () => {
    store.updateProjectState({
      research: {
        paradigm: 'quantitative',
        methodology: 'experimental'
      }
    });

    // Update nested field without overwriting sibling
    store.updateProjectState({
      research: {
        question: 'How does X affect Y?'
      }
    });

    const state = store.getProjectState();
    assert.equal(state.research.paradigm, 'quantitative', 'Original field should be preserved');
    assert.equal(state.research.methodology, 'experimental', 'Original field should be preserved');
    assert.equal(state.research.question, 'How does X affect Y?', 'New field should be added');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 5. YAML Export (~5 tests)
// ===========================================================================

describe('YAML export', () => {
  let tmpDir, dbPath, store;

  beforeEach(() => {
    ({ tmpDir, dbPath, store } = createTestContext());
  });

  it('store.exportCheckpointsYaml() → valid YAML string', () => {
    store.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core focus');
    store.markCheckpoint('CP_PARADIGM_SELECTION', 'Quantitative', 'Best fit');

    const yamlStr = store.exportCheckpointsYaml();

    assert.ok(yamlStr, 'Should return YAML string');
    assert.equal(typeof yamlStr, 'string', 'Should be a string');

    // Verify valid YAML
    const parsed = yaml.load(yamlStr);
    assert.ok(parsed.checkpoints, 'Should have checkpoints key');
    assert.ok(parsed.checkpoints.active, 'Should have active array');
    assert.ok(parsed.checkpoints.active.length >= 2, 'Should have checkpoints');
    cleanup(tmpDir);
  });

  it('store.exportDecisionLogYaml() → valid YAML string', () => {
    store.addDecision('CP_A', 'Decision A', 'Rationale A');
    store.addDecision('CP_B', 'Decision B', 'Rationale B');

    const yamlStr = store.exportDecisionLogYaml();

    assert.ok(yamlStr, 'Should return YAML string');

    const parsed = yaml.load(yamlStr);
    assert.ok(parsed.decisions, 'Should have decisions array');
    assert.equal(parsed.decisions.length, 2, 'Should have 2 decisions');
    cleanup(tmpDir);
  });

  it('store.exportProjectStateYaml() → valid YAML string', () => {
    store.updateProjectState({
      project: { name: 'Test Project' },
      research: { paradigm: 'quantitative' }
    });

    const yamlStr = store.exportProjectStateYaml();

    assert.ok(yamlStr, 'Should return YAML string');

    const parsed = yaml.load(yamlStr);
    assert.equal(parsed.project.name, 'Test Project');
    assert.equal(parsed.research.paradigm, 'quantitative');
    cleanup(tmpDir);
  });

  it('store.exportAll(outputDir) → writes 3 YAML files to directory', () => {
    store.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI', 'test');
    store.addDecision('CP_A', 'A', 'r');
    store.updateProjectState({ project: { name: 'Test' } });

    const outputDir = join(tmpDir, 'research');
    mkdirSync(outputDir, { recursive: true });

    store.exportAll(outputDir);

    assert.ok(existsSync(join(outputDir, 'checkpoints.yaml')), 'checkpoints.yaml should exist');
    assert.ok(existsSync(join(outputDir, 'decision-log.yaml')), 'decision-log.yaml should exist');
    assert.ok(existsSync(join(outputDir, 'project-state.yaml')), 'project-state.yaml should exist');
    cleanup(tmpDir);
  });

  it('exported YAML matches current state exactly', () => {
    store.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core');
    store.addDecision('CP_PARADIGM_SELECTION', 'Quantitative', 'Best fit');
    store.updateProjectState({ project: { name: 'Export Test' } });

    const outputDir = join(tmpDir, 'research');
    mkdirSync(outputDir, { recursive: true });
    store.exportAll(outputDir);

    // Read exported YAML and verify matches SQLite state
    const checkpoints = readTestYaml(tmpDir, 'checkpoints.yaml');
    const cpFromDb = store.getCheckpoint('CP_RESEARCH_DIRECTION');
    assert.equal(checkpoints.checkpoints.active[0].checkpoint_id, cpFromDb.checkpoint_id);
    assert.equal(checkpoints.checkpoints.active[0].decision, cpFromDb.decision);

    const decisionLog = readTestYaml(tmpDir, 'decision-log.yaml');
    const decisionsFromDb = store.listDecisions();
    assert.equal(decisionLog.decisions.length, decisionsFromDb.length);

    const projectState = readTestYaml(tmpDir, 'project-state.yaml');
    const stateFromDb = store.getProjectState();
    assert.equal(projectState.project.name, stateFromDb.project.name);
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 6. Concurrent Access (~4 tests)
// ===========================================================================

describe('Concurrent access', () => {
  let tmpDir, dbPath, store;

  beforeEach(() => {
    ({ tmpDir, dbPath, store } = createTestContext());
  });

  it('two store instances on same DB do not corrupt data', () => {
    const store1 = createStateStore(dbPath);
    const store2 = createStateStore(dbPath);

    store1.markCheckpoint('CP_A', 'Decision A', 'Rationale A');
    store2.markCheckpoint('CP_B', 'Decision B', 'Rationale B');

    const checkpoints1 = store1.listCheckpoints();
    const checkpoints2 = store2.listCheckpoints();

    assert.equal(checkpoints1.length, 2, 'Store 1 should see both checkpoints');
    assert.equal(checkpoints2.length, 2, 'Store 2 should see both checkpoints');
    cleanup(tmpDir);
  });

  it('WAL mode enabled for concurrent reads', () => {
    // Verify WAL mode is enabled
    const walMode = store.db.pragma('journal_mode', { simple: true });
    assert.equal(walMode, 'wal', 'Should use WAL mode for concurrent access');
    cleanup(tmpDir);
  });

  it('write lock prevents data loss', () => {
    const store1 = createStateStore(dbPath);
    const store2 = createStateStore(dbPath);

    // Both stores write to same checkpoint
    store1.markCheckpoint('CP_RESEARCH_DIRECTION', 'First write', 'First');
    store2.markCheckpoint('CP_RESEARCH_DIRECTION', 'Second write', 'Second');

    // One should win (last write wins)
    const checkpoint = store1.getCheckpoint('CP_RESEARCH_DIRECTION');
    assert.ok(checkpoint, 'Checkpoint should exist');
    assert.ok(
      checkpoint.decision === 'First write' || checkpoint.decision === 'Second write',
      'Should have one of the decisions (no corruption)'
    );
    cleanup(tmpDir);
  });

  it('rapid sequential writes all persist', () => {
    const count = 50;

    for (let i = 1; i <= count; i++) {
      store.addDecision(`CP_TEST_${i}`, `Decision ${i}`, `Rationale ${i}`);
    }

    const decisions = store.listDecisions();
    assert.equal(decisions.length, count, 'All rapid writes should persist');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 7. Migration (~5 tests)
// ===========================================================================

describe('Migration', () => {
  let tmpDir, dbPath, store;

  beforeEach(() => {
    ({ tmpDir, dbPath, store } = createTestContext());
  });

  it('store.migrateFromYaml(researchDir) → imports existing YAML files', () => {
    // Create legacy YAML files
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed', decision: 'AI', rationale: 'test' }
        ]
      }
    });

    writeTestYaml(tmpDir, 'decision-log.yaml', {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_RESEARCH_DIRECTION', selected: 'AI', rationale: 'test', version: 1 }
      ]
    });

    writeTestYaml(tmpDir, 'project-state.yaml', {
      project: { name: 'Migration Test' }
    });

    const researchDir = join(tmpDir, 'research');
    const result = store.migrateFromYaml(researchDir);

    assert.equal(result.success, true, 'Migration should succeed');

    // Verify data imported
    const checkpoint = store.getCheckpoint('CP_RESEARCH_DIRECTION');
    assert.ok(checkpoint, 'Checkpoint should be imported');

    const decisions = store.listDecisions();
    assert.equal(decisions.length, 1, 'Decision should be imported');

    const state = store.getProjectState();
    assert.equal(state.project.name, 'Migration Test', 'Project state should be imported');
    cleanup(tmpDir);
  });

  it('handles missing YAML files gracefully', () => {
    const researchDir = join(tmpDir, 'research');
    mkdirSync(researchDir, { recursive: true });

    const result = store.migrateFromYaml(researchDir);

    assert.equal(result.success, true, 'Should succeed even with missing files');
    assert.ok(result.warnings || result.skipped, 'Should report missing files');
    cleanup(tmpDir);
  });

  it('handles empty YAML files', () => {
    writeTestYaml(tmpDir, 'checkpoints.yaml', {});
    writeTestYaml(tmpDir, 'decision-log.yaml', {});
    writeTestYaml(tmpDir, 'project-state.yaml', {});

    const researchDir = join(tmpDir, 'research');
    const result = store.migrateFromYaml(researchDir);

    assert.equal(result.success, true, 'Should handle empty YAML files');
    cleanup(tmpDir);
  });

  it('preserves all data from YAML migration', () => {
    const checkpointsData = {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_A', status: 'completed', decision: 'A', rationale: 'Ra', level: 'REQUIRED' },
          { checkpoint_id: 'CP_B', status: 'completed', decision: 'B', rationale: 'Rb', level: 'RECOMMENDED' }
        ]
      }
    };

    const decisionsData = {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_A', selected: 'A', rationale: 'Ra', version: 1, timestamp: '2025-01-01T00:00:00.000Z' },
        { decision_id: 'DEV_002', checkpoint_id: 'CP_B', selected: 'B', rationale: 'Rb', version: 1, timestamp: '2025-01-02T00:00:00.000Z' }
      ]
    };

    const projectStateData = {
      project: { name: 'Preserve Test', created: '2025-01-01' },
      research: { paradigm: 'quantitative', question: 'How?' }
    };

    writeTestYaml(tmpDir, 'checkpoints.yaml', checkpointsData);
    writeTestYaml(tmpDir, 'decision-log.yaml', decisionsData);
    writeTestYaml(tmpDir, 'project-state.yaml', projectStateData);

    const researchDir = join(tmpDir, 'research');
    store.migrateFromYaml(researchDir);

    // Verify all data preserved
    const checkpoints = store.listCheckpoints();
    assert.equal(checkpoints.length, 2);

    const decisions = store.listDecisions();
    assert.equal(decisions.length, 2);

    const state = store.getProjectState();
    assert.equal(state.project.name, 'Preserve Test');
    assert.equal(state.research.paradigm, 'quantitative');
    cleanup(tmpDir);
  });

  it('migration is idempotent', () => {
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed', decision: 'AI', rationale: 'test' }
        ]
      }
    });

    const researchDir = join(tmpDir, 'research');

    // Run migration twice
    const result1 = store.migrateFromYaml(researchDir);
    const result2 = store.migrateFromYaml(researchDir);

    assert.equal(result1.success, true);
    assert.equal(result2.success, true);

    // Should not duplicate data
    const checkpoints = store.listCheckpoints();
    assert.equal(checkpoints.length, 1, 'Should not duplicate on second migration');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 8. Edge Cases (~5 additional tests)
// ===========================================================================

describe('Edge cases', () => {
  let tmpDir, dbPath, store;

  beforeEach(() => {
    ({ tmpDir, dbPath, store } = createTestContext());
  });

  it('handles null values in rationale', () => {
    const result = store.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI', null);
    assert.equal(result.recorded, true);

    const checkpoint = store.getCheckpoint('CP_RESEARCH_DIRECTION');
    assert.ok(!checkpoint.rationale || checkpoint.rationale === null);
    cleanup(tmpDir);
  });

  it('handles special characters in rationale', () => {
    const specialChars = 'Special chars: @#$%^&*()_+{}[]|\\:";\'<>?,./\n\nMultiline\nWith emojis 🔴🟠🟡';

    store.markCheckpoint('CP_RESEARCH_DIRECTION', 'Test', specialChars);

    const checkpoint = store.getCheckpoint('CP_RESEARCH_DIRECTION');
    assert.equal(checkpoint.rationale, specialChars);
    cleanup(tmpDir);
  });

  it('handles very long rationale (>10KB)', () => {
    const longRationale = 'A'.repeat(15000);

    store.markCheckpoint('CP_RESEARCH_DIRECTION', 'Test', longRationale);

    const checkpoint = store.getCheckpoint('CP_RESEARCH_DIRECTION');
    assert.equal(checkpoint.rationale.length, 15000);
    cleanup(tmpDir);
  });

  it('handles Unicode characters in decisions', () => {
    const unicode = '한글 테스트 中文测试 日本語テスト العربية עברית';

    store.markCheckpoint('CP_RESEARCH_DIRECTION', unicode, 'Unicode test');

    const checkpoint = store.getCheckpoint('CP_RESEARCH_DIRECTION');
    assert.equal(checkpoint.decision, unicode);
    cleanup(tmpDir);
  });

  it('handles empty database queries gracefully', () => {
    assert.equal(store.listCheckpoints().length, 0, 'Empty checkpoint list');
    assert.equal(store.listDecisions().length, 0, 'Empty decision list');
    assert.equal(store.getCheckpoint('NONEXISTENT'), null, 'Null for missing checkpoint');
    assert.equal(store.getDecision('NONEXISTENT'), null, 'Null for missing decision');
    cleanup(tmpDir);
  });
});
