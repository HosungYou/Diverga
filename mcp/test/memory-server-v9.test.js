/**
 * TDD RED Tests for Diverga v9.0 Memory Server (New)
 *
 * Tests the new memory server that handles project state, decisions, and priority context.
 * Split from checkpoint-server.js in v9.0.
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
import { createMemoryServer } from '../servers/memory-server.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

/**
 * Helper: create a fresh temp dir and server instance for each suite.
 */
function createTestContext() {
  const tmpDir = mkdtempSync(join(tmpdir(), 'memory-server-v9-test-'));
  const server = createMemoryServer(tmpDir);
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

describe('createMemoryServer factory', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('creates server instance with all memory tools', () => {
    assert.ok(server);
    assert.equal(typeof server.readProjectState, 'function');
    assert.equal(typeof server.updateProjectState, 'function');
    assert.equal(typeof server.addDecision, 'function');
    assert.equal(typeof server.listDecisions, 'function');
    assert.equal(typeof server.readPriorityContext, 'function');
    assert.equal(typeof server.writePriorityContext, 'function');
    assert.equal(typeof server.exportToYaml, 'function');
    cleanup(tmpDir);
  });

  it('does NOT include checkpoint tools (in checkpoint-server)', () => {
    assert.equal(server.checkPrerequisites, undefined);
    assert.equal(server.markCheckpoint, undefined);
    assert.equal(server.checkpointStatus, undefined);
    cleanup(tmpDir);
  });

  it('does NOT include comm tools (in comm-server)', () => {
    assert.equal(server.send, undefined);
    assert.equal(server.broadcast, undefined);
    assert.equal(server.mailbox, undefined);
    cleanup(tmpDir);
  });

  it('accepts research directory parameter', () => {
    const customDir = mkdtempSync(join(tmpdir(), 'custom-memory-'));
    const customServer = createMemoryServer(customDir);
    assert.ok(customServer);
    cleanup(customDir);
    cleanup(tmpDir);
  });

  it('throws error when research directory is missing', () => {
    assert.throws(() => {
      createMemoryServer(null);
    }, /research directory/i);
    cleanup(tmpDir);
  });

  it('creates research/ directory if it does not exist', () => {
    const newDir = mkdtempSync(join(tmpdir(), 'new-memory-'));
    const newServer = createMemoryServer(newDir);

    // Trigger a write operation
    newServer.updateProjectState({ project: { name: 'Test' } });

    const researchPath = join(newDir, 'research');
    assert.equal(existsSync(researchPath), true);
    cleanup(newDir);
    cleanup(tmpDir);
  });

  it('creates .research/ directory for system files', () => {
    const newDir = mkdtempSync(join(tmpdir(), 'new-system-'));
    const newServer = createMemoryServer(newDir);

    // Trigger priority context write
    newServer.writePriorityContext('Test context');

    const systemPath = join(newDir, '.research');
    assert.equal(existsSync(systemPath), true);
    cleanup(newDir);
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 2. readProjectState
// ===========================================================================

describe('readProjectState', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('returns empty state when project-state.yaml does not exist', () => {
    const result = server.readProjectState();
    assert.deepEqual(result, {});
    cleanup(tmpDir);
  });

  it('returns project state from research/project-state.yaml', () => {
    writeTestYaml(join(tmpDir, 'research'), 'project-state.yaml', {
      project: { name: 'AI Study', created: '2025-01-01' },
      research: { paradigm: 'quantitative', question: 'How does AI affect learning?' }
    });

    const result = server.readProjectState();
    assert.equal(result.project.name, 'AI Study');
    assert.equal(result.research.paradigm, 'quantitative');
    cleanup(tmpDir);
  });

  it('reads from .research/ if research/ does not exist (legacy)', () => {
    writeTestYaml(join(tmpDir, '.research'), 'project-state.yaml', {
      project: { name: 'Legacy Project' }
    });

    const result = server.readProjectState();
    assert.equal(result.project.name, 'Legacy Project');
    cleanup(tmpDir);
  });

  it('prefers research/ over .research/ when both exist', () => {
    writeTestYaml(join(tmpDir, 'research'), 'project-state.yaml', {
      project: { name: 'New Project' }
    });
    writeTestYaml(join(tmpDir, '.research'), 'project-state.yaml', {
      project: { name: 'Old Project' }
    });

    const result = server.readProjectState();
    assert.equal(result.project.name, 'New Project');
    cleanup(tmpDir);
  });

  it('handles malformed YAML gracefully', () => {
    writeFileSync(join(tmpDir, 'research', 'project-state.yaml'), 'invalid: yaml: [', 'utf8');

    const result = server.readProjectState();
    assert.deepEqual(result, {}); // Returns empty on parse error
    cleanup(tmpDir);
  });

  it('returns nested objects correctly', () => {
    writeTestYaml(join(tmpDir, 'research'), 'project-state.yaml', {
      project: { name: 'Test' },
      research: {
        paradigm: 'mixed',
        methods: {
          quantitative: { design: 'RCT', n: 100 },
          qualitative: { approach: 'phenomenology' }
        }
      }
    });

    const result = server.readProjectState();
    assert.equal(result.research.methods.quantitative.design, 'RCT');
    assert.equal(result.research.methods.qualitative.approach, 'phenomenology');
    cleanup(tmpDir);
  });

  it('preserves arrays in state', () => {
    writeTestYaml(join(tmpDir, 'research'), 'project-state.yaml', {
      research: {
        databases: ['semantic_scholar', 'openalex', 'arxiv'],
        keywords: ['AI', 'education', 'learning']
      }
    });

    const result = server.readProjectState();
    assert.deepEqual(result.research.databases, ['semantic_scholar', 'openalex', 'arxiv']);
    assert.deepEqual(result.research.keywords, ['AI', 'education', 'learning']);
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 3. updateProjectState
// ===========================================================================

describe('updateProjectState', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('creates project-state.yaml in research/ if it does not exist', () => {
    server.updateProjectState({ project: { name: 'New Project' } });

    const filepath = join(tmpDir, 'research', 'project-state.yaml');
    assert.equal(existsSync(filepath), true);
    cleanup(tmpDir);
  });

  it('writes initial state correctly', () => {
    const result = server.updateProjectState({
      project: { name: 'AI Study', created: '2025-01-01' },
      research: { paradigm: 'quantitative' }
    });

    assert.equal(result.updated, true);

    const data = readTestYaml(join(tmpDir, 'research'), 'project-state.yaml');
    assert.equal(data.project.name, 'AI Study');
    assert.equal(data.research.paradigm, 'quantitative');
    cleanup(tmpDir);
  });

  it('merges updates with existing state', () => {
    writeTestYaml(join(tmpDir, 'research'), 'project-state.yaml', {
      project: { name: 'Original', created: '2025-01-01' },
      research: { paradigm: 'quantitative' }
    });

    server.updateProjectState({
      project: { updated: '2025-01-15' },
      research: { methodology: 'meta-analysis' }
    });

    const data = readTestYaml(join(tmpDir, 'research'), 'project-state.yaml');
    assert.equal(data.project.name, 'Original'); // Preserved
    assert.equal(data.project.created, '2025-01-01'); // Preserved
    assert.equal(data.project.updated, '2025-01-15'); // Added
    assert.equal(data.research.paradigm, 'quantitative'); // Preserved
    assert.equal(data.research.methodology, 'meta-analysis'); // Added
    cleanup(tmpDir);
  });

  it('deep merges nested objects', () => {
    writeTestYaml(join(tmpDir, 'research'), 'project-state.yaml', {
      research: {
        methods: {
          quantitative: { design: 'RCT', n: 100 }
        }
      }
    });

    server.updateProjectState({
      research: {
        methods: {
          quantitative: { power: 0.8 },
          qualitative: { approach: 'phenomenology' }
        }
      }
    });

    const data = readTestYaml(join(tmpDir, 'research'), 'project-state.yaml');
    assert.equal(data.research.methods.quantitative.design, 'RCT'); // Preserved
    assert.equal(data.research.methods.quantitative.n, 100); // Preserved
    assert.equal(data.research.methods.quantitative.power, 0.8); // Added
    assert.equal(data.research.methods.qualitative.approach, 'phenomenology'); // Added
    cleanup(tmpDir);
  });

  it('overwrites primitive values', () => {
    writeTestYaml(join(tmpDir, 'research'), 'project-state.yaml', {
      research: { paradigm: 'quantitative' }
    });

    server.updateProjectState({
      research: { paradigm: 'mixed' }
    });

    const data = readTestYaml(join(tmpDir, 'research'), 'project-state.yaml');
    assert.equal(data.research.paradigm, 'mixed');
    cleanup(tmpDir);
  });

  it('returns updated: true and updated state', () => {
    const result = server.updateProjectState({
      project: { name: 'Test' }
    });

    assert.equal(result.updated, true);
    assert.equal(result.state.project.name, 'Test');
    cleanup(tmpDir);
  });

  it('handles arrays in updates', () => {
    server.updateProjectState({
      research: { databases: ['semantic_scholar', 'openalex'] }
    });

    const data = readTestYaml(join(tmpDir, 'research'), 'project-state.yaml');
    assert.deepEqual(data.research.databases, ['semantic_scholar', 'openalex']);
    cleanup(tmpDir);
  });

  it('migrates from .research/ to research/ on update', () => {
    writeTestYaml(join(tmpDir, '.research'), 'project-state.yaml', {
      project: { name: 'Legacy' }
    });

    server.updateProjectState({
      project: { updated: '2025-01-15' }
    });

    // Should write to research/
    const newPath = join(tmpDir, 'research', 'project-state.yaml');
    assert.equal(existsSync(newPath), true);

    const data = readTestYaml(join(tmpDir, 'research'), 'project-state.yaml');
    assert.equal(data.project.name, 'Legacy');
    assert.equal(data.project.updated, '2025-01-15');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 4. addDecision
// ===========================================================================

describe('addDecision', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('creates decision-log.yaml in research/ if it does not exist', () => {
    server.addDecision('CP_RESEARCH_DIRECTION', 'AI in education', 'Core focus');

    const filepath = join(tmpDir, 'research', 'decision-log.yaml');
    assert.equal(existsSync(filepath), true);
    cleanup(tmpDir);
  });

  it('adds decision with correct structure', () => {
    const result = server.addDecision('CP_RESEARCH_DIRECTION', 'AI in education', 'Core focus');

    assert.equal(result.recorded, true);
    assert.equal(result.decision_id, 'DEV_001');

    const data = readTestYaml(join(tmpDir, 'research'), 'decision-log.yaml');
    const d = data.decisions[0];
    assert.equal(d.decision_id, 'DEV_001');
    assert.equal(d.checkpoint_id, 'CP_RESEARCH_DIRECTION');
    assert.equal(d.selected, 'AI in education');
    assert.equal(d.rationale, 'Core focus');
    assert.equal(d.version, 1);
    assert.ok(d.timestamp);
    cleanup(tmpDir);
  });

  it('generates sequential decision IDs', () => {
    const r1 = server.addDecision('CP_A', 'sel1', 'rat1');
    const r2 = server.addDecision('CP_B', 'sel2', 'rat2');
    const r3 = server.addDecision('CP_C', 'sel3', 'rat3');

    assert.equal(r1.decision_id, 'DEV_001');
    assert.equal(r2.decision_id, 'DEV_002');
    assert.equal(r3.decision_id, 'DEV_003');
    cleanup(tmpDir);
  });

  it('appends to existing decision log', () => {
    writeTestYaml(join(tmpDir, 'research'), 'decision-log.yaml', {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_A', selected: 'x', rationale: 'r', timestamp: '2025-01-01T00:00:00Z', version: 1 }
      ]
    });

    server.addDecision('CP_B', 'y', 'r2');

    const data = readTestYaml(join(tmpDir, 'research'), 'decision-log.yaml');
    assert.equal(data.decisions.length, 2);
    assert.equal(data.decisions[1].decision_id, 'DEV_002');
    cleanup(tmpDir);
  });

  it('includes alternatives_considered when provided', () => {
    server.addDecision(
      'CP_PARADIGM_SELECTION',
      'Quantitative',
      'Best fit for RCT',
      ['Qualitative', 'Mixed Methods']
    );

    const data = readTestYaml(join(tmpDir, 'research'), 'decision-log.yaml');
    const d = data.decisions[0];
    assert.deepEqual(d.alternatives_considered, ['Qualitative', 'Mixed Methods']);
    cleanup(tmpDir);
  });

  it('omits alternatives_considered when not provided', () => {
    server.addDecision('CP_RESEARCH_DIRECTION', 'AI', 'Core');

    const data = readTestYaml(join(tmpDir, 'research'), 'decision-log.yaml');
    const d = data.decisions[0];
    assert.equal(d.alternatives_considered, undefined);
    cleanup(tmpDir);
  });

  it('updates priority context after adding decision', () => {
    server.addDecision('CP_RESEARCH_DIRECTION', 'AI in education', 'Core');

    const contextPath = join(tmpDir, '.research', 'priority-context.md');
    assert.equal(existsSync(contextPath), true);
    cleanup(tmpDir);
  });

  it('includes metadata fields (T-score, agent, etc.) when provided', () => {
    server.addDecision(
      'CP_THEORY_SELECTION',
      'TAM',
      'Well-established framework',
      ['TPB', 'UTAUT'],
      { t_score: 0.65, agent: 'a2', session_id: 'sess_123' }
    );

    const data = readTestYaml(join(tmpDir, 'research'), 'decision-log.yaml');
    const d = data.decisions[0];
    assert.equal(d.metadata.t_score, 0.65);
    assert.equal(d.metadata.agent, 'a2');
    assert.equal(d.metadata.session_id, 'sess_123');
    cleanup(tmpDir);
  });

  it('returns decision_id and recorded: true', () => {
    const result = server.addDecision('CP_TEST', 'test', 'test');
    assert.equal(result.recorded, true);
    assert.ok(result.decision_id.startsWith('DEV_'));
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 5. listDecisions
// ===========================================================================

describe('listDecisions', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('returns empty array when no decisions exist', () => {
    const result = server.listDecisions();
    assert.deepEqual(result, []);
    cleanup(tmpDir);
  });

  it('returns all decisions by default', () => {
    writeTestYaml(join(tmpDir, 'research'), 'decision-log.yaml', {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_A', selected: 'x' },
        { decision_id: 'DEV_002', checkpoint_id: 'CP_B', selected: 'y' },
        { decision_id: 'DEV_003', checkpoint_id: 'CP_C', selected: 'z' }
      ]
    });

    const result = server.listDecisions();
    assert.equal(result.length, 3);
    cleanup(tmpDir);
  });

  it('filters by checkpoint_id', () => {
    writeTestYaml(join(tmpDir, 'research'), 'decision-log.yaml', {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_RESEARCH_DIRECTION', selected: 'AI' },
        { decision_id: 'DEV_002', checkpoint_id: 'CP_PARADIGM_SELECTION', selected: 'Quant' },
        { decision_id: 'DEV_003', checkpoint_id: 'CP_RESEARCH_DIRECTION', selected: 'Updated AI' }
      ]
    });

    const result = server.listDecisions({ checkpoint_id: 'CP_RESEARCH_DIRECTION' });
    assert.equal(result.length, 2);
    assert.equal(result[0].checkpoint_id, 'CP_RESEARCH_DIRECTION');
    assert.equal(result[1].checkpoint_id, 'CP_RESEARCH_DIRECTION');
    cleanup(tmpDir);
  });

  it('filters by agent', () => {
    writeTestYaml(join(tmpDir, 'research'), 'decision-log.yaml', {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_A', selected: 'x', metadata: { agent: 'a1' } },
        { decision_id: 'DEV_002', checkpoint_id: 'CP_B', selected: 'y', metadata: { agent: 'a2' } },
        { decision_id: 'DEV_003', checkpoint_id: 'CP_C', selected: 'z', metadata: { agent: 'a1' } }
      ]
    });

    const result = server.listDecisions({ agent: 'a1' });
    assert.equal(result.length, 2);
    cleanup(tmpDir);
  });

  it('filters by date range (after)', () => {
    writeTestYaml(join(tmpDir, 'research'), 'decision-log.yaml', {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_A', selected: 'x', timestamp: '2025-01-01T00:00:00Z' },
        { decision_id: 'DEV_002', checkpoint_id: 'CP_B', selected: 'y', timestamp: '2025-01-10T00:00:00Z' },
        { decision_id: 'DEV_003', checkpoint_id: 'CP_C', selected: 'z', timestamp: '2025-01-20T00:00:00Z' }
      ]
    });

    const result = server.listDecisions({ after: '2025-01-09T00:00:00Z' });
    assert.equal(result.length, 2);
    assert.equal(result[0].decision_id, 'DEV_002');
    assert.equal(result[1].decision_id, 'DEV_003');
    cleanup(tmpDir);
  });

  it('filters by date range (before)', () => {
    writeTestYaml(join(tmpDir, 'research'), 'decision-log.yaml', {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_A', selected: 'x', timestamp: '2025-01-01T00:00:00Z' },
        { decision_id: 'DEV_002', checkpoint_id: 'CP_B', selected: 'y', timestamp: '2025-01-10T00:00:00Z' },
        { decision_id: 'DEV_003', checkpoint_id: 'CP_C', selected: 'z', timestamp: '2025-01-20T00:00:00Z' }
      ]
    });

    const result = server.listDecisions({ before: '2025-01-11T00:00:00Z' });
    assert.equal(result.length, 2);
    assert.equal(result[0].decision_id, 'DEV_001');
    assert.equal(result[1].decision_id, 'DEV_002');
    cleanup(tmpDir);
  });

  it('combines multiple filters', () => {
    writeTestYaml(join(tmpDir, 'research'), 'decision-log.yaml', {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_A', selected: 'x', timestamp: '2025-01-01T00:00:00Z', metadata: { agent: 'a1' } },
        { decision_id: 'DEV_002', checkpoint_id: 'CP_A', selected: 'y', timestamp: '2025-01-10T00:00:00Z', metadata: { agent: 'a2' } },
        { decision_id: 'DEV_003', checkpoint_id: 'CP_A', selected: 'z', timestamp: '2025-01-20T00:00:00Z', metadata: { agent: 'a1' } }
      ]
    });

    const result = server.listDecisions({
      checkpoint_id: 'CP_A',
      agent: 'a1',
      after: '2025-01-05T00:00:00Z'
    });

    assert.equal(result.length, 1);
    assert.equal(result[0].decision_id, 'DEV_003');
    cleanup(tmpDir);
  });

  it('returns empty array when no matches', () => {
    writeTestYaml(join(tmpDir, 'research'), 'decision-log.yaml', {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_A', selected: 'x' }
      ]
    });

    const result = server.listDecisions({ checkpoint_id: 'CP_NONEXISTENT' });
    assert.deepEqual(result, []);
    cleanup(tmpDir);
  });

  it('reads from .research/ if research/ does not exist', () => {
    writeTestYaml(join(tmpDir, '.research'), 'decision-log.yaml', {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_A', selected: 'x' }
      ]
    });

    const result = server.listDecisions();
    assert.equal(result.length, 1);
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 6. readPriorityContext
// ===========================================================================

describe('readPriorityContext', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('returns empty string when file does not exist', () => {
    const result = server.readPriorityContext();
    assert.equal(result, '');
    cleanup(tmpDir);
  });

  it('reads from .research/priority-context.md', () => {
    const content = 'Project: AI Study | Paradigm: Quantitative';
    writeFileSync(join(tmpDir, '.research', 'priority-context.md'), content, 'utf8');

    const result = server.readPriorityContext();
    assert.equal(result, content);
    cleanup(tmpDir);
  });

  it('preserves exact content without modification', () => {
    const content = 'Special chars: @#$% & newlines\nline2\nline3';
    const dir = join(tmpDir, '.research');
    mkdirSync(dir, { recursive: true });
    writeFileSync(join(dir, 'priority-context.md'), content, 'utf8');

    const result = server.readPriorityContext();
    assert.equal(result, content);
    cleanup(tmpDir);
  });

  it('handles Unicode characters', () => {
    const content = '연구 질문: AI가 학습에 미치는 영향은? 🎓';
    const dir = join(tmpDir, '.research');
    mkdirSync(dir, { recursive: true });
    writeFileSync(join(dir, 'priority-context.md'), content, 'utf8');

    const result = server.readPriorityContext();
    assert.equal(result, content);
    cleanup(tmpDir);
  });

  it('handles empty file', () => {
    const dir = join(tmpDir, '.research');
    mkdirSync(dir, { recursive: true });
    writeFileSync(join(dir, 'priority-context.md'), '', 'utf8');

    const result = server.readPriorityContext();
    assert.equal(result, '');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 7. writePriorityContext
// ===========================================================================

describe('writePriorityContext', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('writes context to .research/priority-context.md', () => {
    const result = server.writePriorityContext('Hello priority context');

    assert.equal(result.written, true);
    assert.equal(result.length, 'Hello priority context'.length);

    const content = readFileSync(join(tmpDir, '.research', 'priority-context.md'), 'utf8');
    assert.equal(content, 'Hello priority context');
    cleanup(tmpDir);
  });

  it('truncates to 500 chars by default', () => {
    const longText = 'A'.repeat(600);
    const result = server.writePriorityContext(longText);

    assert.equal(result.written, true);
    assert.equal(result.length, 500);

    const content = readFileSync(join(tmpDir, '.research', 'priority-context.md'), 'utf8');
    assert.equal(content.length, 500);
    cleanup(tmpDir);
  });

  it('accepts custom maxChars parameter', () => {
    const longText = 'B'.repeat(1000);
    const result = server.writePriorityContext(longText, 800);

    assert.equal(result.length, 800);

    const content = readFileSync(join(tmpDir, '.research', 'priority-context.md'), 'utf8');
    assert.equal(content.length, 800);
    cleanup(tmpDir);
  });

  it('does not truncate text under limit', () => {
    const shortText = 'C'.repeat(300);
    const result = server.writePriorityContext(shortText);

    assert.equal(result.length, 300);
    cleanup(tmpDir);
  });

  it('overwrites existing content', () => {
    server.writePriorityContext('first');
    server.writePriorityContext('second');

    const content = readFileSync(join(tmpDir, '.research', 'priority-context.md'), 'utf8');
    assert.equal(content, 'second');
    cleanup(tmpDir);
  });

  it('creates .research/ directory if it does not exist', () => {
    server.writePriorityContext('test');

    const dir = join(tmpDir, '.research');
    assert.equal(existsSync(dir), true);
    cleanup(tmpDir);
  });

  it('handles Unicode content', () => {
    const content = '연구 질문: AI의 효과 🎓';
    server.writePriorityContext(content);

    const read = readFileSync(join(tmpDir, '.research', 'priority-context.md'), 'utf8');
    assert.equal(read, content);
    cleanup(tmpDir);
  });

  it('returns written: true and final length', () => {
    const result = server.writePriorityContext('test content');
    assert.equal(result.written, true);
    assert.equal(typeof result.length, 'number');
    assert.equal(result.length, 12);
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 8. exportToYaml
// ===========================================================================

describe('exportToYaml', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('exports complete state as YAML string', () => {
    writeTestYaml(join(tmpDir, 'research'), 'project-state.yaml', {
      project: { name: 'Test Project' }
    });
    writeTestYaml(join(tmpDir, 'research'), 'decision-log.yaml', {
      decisions: [{ decision_id: 'DEV_001', checkpoint_id: 'CP_A', selected: 'x' }]
    });

    const result = server.exportToYaml();

    assert.ok(result.includes('project:'));
    assert.ok(result.includes('name: Test Project'));
    assert.ok(result.includes('decisions:'));
    assert.ok(result.includes('DEV_001'));
    cleanup(tmpDir);
  });

  it('includes project state section', () => {
    writeTestYaml(join(tmpDir, 'research'), 'project-state.yaml', {
      project: { name: 'Export Test', created: '2025-01-01' },
      research: { paradigm: 'quantitative' }
    });

    const result = server.exportToYaml();
    const parsed = yaml.load(result);

    assert.equal(parsed.project_state.project.name, 'Export Test');
    assert.equal(parsed.project_state.research.paradigm, 'quantitative');
    cleanup(tmpDir);
  });

  it('includes decisions section', () => {
    writeTestYaml(join(tmpDir, 'research'), 'decision-log.yaml', {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_A', selected: 'x' },
        { decision_id: 'DEV_002', checkpoint_id: 'CP_B', selected: 'y' }
      ]
    });

    const result = server.exportToYaml();
    const parsed = yaml.load(result);

    assert.equal(parsed.decisions.length, 2);
    assert.equal(parsed.decisions[0].decision_id, 'DEV_001');
    cleanup(tmpDir);
  });

  it('includes priority context section', () => {
    const dir = join(tmpDir, '.research');
    mkdirSync(dir, { recursive: true });
    writeFileSync(join(dir, 'priority-context.md'), 'Test priority context', 'utf8');

    const result = server.exportToYaml();
    const parsed = yaml.load(result);

    assert.equal(parsed.priority_context, 'Test priority context');
    cleanup(tmpDir);
  });

  it('handles empty state gracefully', () => {
    const result = server.exportToYaml();
    const parsed = yaml.load(result);

    assert.deepEqual(parsed.project_state, {});
    assert.deepEqual(parsed.decisions, []);
    assert.equal(parsed.priority_context, '');
    cleanup(tmpDir);
  });

  it('includes metadata in export', () => {
    const result = server.exportToYaml();
    const parsed = yaml.load(result);

    assert.ok(parsed.exported_at);
    assert.ok(parsed.version);
    cleanup(tmpDir);
  });

  it('exports valid YAML that can be re-imported', () => {
    writeTestYaml(join(tmpDir, 'research'), 'project-state.yaml', {
      project: { name: 'Round Trip Test' }
    });

    const exported = server.exportToYaml();
    const parsed = yaml.load(exported);

    assert.equal(parsed.project_state.project.name, 'Round Trip Test');
    cleanup(tmpDir);
  });

  it('handles complex nested structures', () => {
    writeTestYaml(join(tmpDir, 'research'), 'project-state.yaml', {
      research: {
        methods: {
          quantitative: { design: 'RCT', variables: ['IV1', 'IV2'] },
          qualitative: { approach: 'phenomenology', participants: 15 }
        }
      }
    });

    const result = server.exportToYaml();
    const parsed = yaml.load(result);

    assert.equal(parsed.project_state.research.methods.quantitative.design, 'RCT');
    assert.deepEqual(parsed.project_state.research.methods.quantitative.variables, ['IV1', 'IV2']);
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 9. Integration: memory workflows
// ===========================================================================

describe('integration: memory workflows', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('complete project lifecycle workflow', () => {
    // Step 1: Initialize project
    server.updateProjectState({
      project: { name: 'AI Study', created: '2025-01-01' }
    });

    // Step 2: Add research question decision
    server.addDecision('CP_RESEARCH_DIRECTION', 'AI in education', 'Core focus');

    // Step 3: Update paradigm
    server.updateProjectState({
      research: { paradigm: 'quantitative' }
    });

    // Step 4: Add paradigm decision
    server.addDecision('CP_PARADIGM_SELECTION', 'Quantitative', 'RCT design');

    // Step 5: Update priority context
    server.writePriorityContext('Project: AI Study | Paradigm: Quantitative | Stage: Design');

    // Verify final state
    const state = server.readProjectState();
    assert.equal(state.project.name, 'AI Study');
    assert.equal(state.research.paradigm, 'quantitative');

    const decisions = server.listDecisions();
    assert.equal(decisions.length, 2);

    const context = server.readPriorityContext();
    assert.ok(context.includes('AI Study'));

    cleanup(tmpDir);
  });

  it('export captures complete state', () => {
    server.updateProjectState({ project: { name: 'Export Test' } });
    server.addDecision('CP_A', 'Decision A', 'Rationale A');
    server.writePriorityContext('Priority context test');

    const exported = server.exportToYaml();
    const parsed = yaml.load(exported);

    assert.equal(parsed.project_state.project.name, 'Export Test');
    assert.equal(parsed.decisions.length, 1);
    assert.equal(parsed.priority_context, 'Priority context test');

    cleanup(tmpDir);
  });

  it('handles legacy .research/ to research/ migration', () => {
    // Start with legacy location
    writeTestYaml(join(tmpDir, '.research'), 'project-state.yaml', {
      project: { name: 'Legacy Project' }
    });

    // Read from legacy
    const state1 = server.readProjectState();
    assert.equal(state1.project.name, 'Legacy Project');

    // Update triggers migration
    server.updateProjectState({ project: { updated: '2025-01-15' } });

    // Should now be in research/
    const newPath = join(tmpDir, 'research', 'project-state.yaml');
    assert.equal(existsSync(newPath), true);

    cleanup(tmpDir);
  });

  it('priority context updates reflect latest decisions', () => {
    server.addDecision('CP_RESEARCH_DIRECTION', 'AI in education', 'Core');

    const context1 = server.readPriorityContext();
    assert.ok(context1.includes('CP_RESEARCH_DIRECTION'));

    server.addDecision('CP_PARADIGM_SELECTION', 'Quantitative', 'RCT');

    const context2 = server.readPriorityContext();
    assert.ok(context2.includes('CP_PARADIGM_SELECTION'));

    cleanup(tmpDir);
  });

  it('filtered decision queries work across updates', () => {
    server.addDecision('CP_A', 'x', 'r1', [], { agent: 'a1' });
    server.addDecision('CP_B', 'y', 'r2', [], { agent: 'a2' });
    server.addDecision('CP_A', 'z', 'r3', [], { agent: 'a1' });

    const cpA = server.listDecisions({ checkpoint_id: 'CP_A' });
    assert.equal(cpA.length, 2);

    const agentA1 = server.listDecisions({ agent: 'a1' });
    assert.equal(agentA1.length, 2);

    cleanup(tmpDir);
  });
});
