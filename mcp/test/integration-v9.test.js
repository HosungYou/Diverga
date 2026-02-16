/**
 * Diverga v9.0 MCP Integration Test
 *
 * Verifies all 16 MCP tools work end-to-end through the full stack:
 * tool-registry → servers → storage (both YAML and SQLite backends)
 */

import { describe, it, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, existsSync, rmSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';

import { createCheckpointServer } from '../servers/checkpoint-server.js';
import { createMemoryServer } from '../servers/memory-server.js';
import { createCommServer } from '../servers/comm-server.js';
import { createSqliteServers } from '../lib/sqlite-servers.js';
import { createToolRegistry } from '../lib/tool-registry.js';

// =============================================================================
// Test Fixtures
// =============================================================================

const prereqMap = {
  agents: {
    a1: { entry_point: true, own_checkpoints: ['CP_RESEARCH_DIRECTION'] },
    i0: { prerequisites: [], own_checkpoints: [] },
    i1: {
      prerequisites: [],
      own_checkpoints: ['SCH_DATABASE_SELECTION', 'SCH_API_KEY_VALIDATION']
    },
    i2: {
      prerequisites: ['SCH_DATABASE_SELECTION'],
      own_checkpoints: ['SCH_SCREENING_CRITERIA']
    },
    i3: {
      prerequisites: ['SCH_SCREENING_CRITERIA'],
      own_checkpoints: ['SCH_RAG_READINESS']
    },
    c5: {
      prerequisites: ['CP_RESEARCH_DIRECTION', 'CP_METHODOLOGY_APPROVAL'],
      own_checkpoints: ['CP_ANALYSIS_PLAN']
    },
  }
};

// =============================================================================
// Section 1: YAML Backend Integration Tests
// =============================================================================

describe('Diverga v9.0 Integration Tests - YAML Backend', () => {
  let tmpDir;
  let registry;
  let dispatch;

  before(() => {
    tmpDir = mkdtempSync(join(tmpdir(), 'diverga-test-yaml-'));
    console.log(`YAML test directory: ${tmpDir}`);

    const checkpointServer = createCheckpointServer(prereqMap, tmpDir);
    const memoryServer = createMemoryServer(tmpDir);
    const commServer = createCommServer(tmpDir);

    const result = createToolRegistry(checkpointServer, memoryServer, commServer);
    registry = result;
    dispatch = result.dispatch;
  });

  after(() => {
    if (tmpDir && existsSync(tmpDir)) {
      rmSync(tmpDir, { recursive: true, force: true });
    }
  });

  it('should verify tools are registered', () => {
    assert.ok(registry.tools, 'Tools array should exist');
    assert.equal(registry.tools.length, 16, 'Should have 16 tools');
    assert.equal(typeof dispatch, 'function', 'Dispatch should be a function');
  });

  it('should check prerequisites for known agent', async () => {
    const result = await dispatch('diverga_check_prerequisites', { agent_id: 'a1' });
    assert.equal(result.approved, true, 'Entry point agent should be approved');
    assert.deepEqual(result.missing, [], 'Should have no missing prerequisites');
    assert.ok(result.message, 'Should have a message');
    assert.ok(Array.isArray(result.own_checkpoints), 'Should have own_checkpoints array');
  });

  it('should mark checkpoint and retrieve status', async () => {
    const markResult = await dispatch('diverga_mark_checkpoint', {
      checkpoint_id: 'SCH_DATABASE_SELECTION',
      decision: 'Semantic Scholar + OpenAlex',
      rationale: 'Best API coverage'
    });

    assert.equal(markResult.recorded, true, 'Checkpoint should be recorded');
    assert.equal(markResult.checkpoint_id, 'SCH_DATABASE_SELECTION');
    assert.ok(markResult.decision_id, 'Should have decision_id');

    const statusResult = await dispatch('diverga_checkpoint_status', {});
    assert.ok(Array.isArray(statusResult.passed), 'Passed should be array');
    assert.ok(
      statusResult.passed.includes('SCH_DATABASE_SELECTION'),
      'Should show checkpoint as passed'
    );
  });

  it('should update and read project state', async () => {
    const updateResult = await dispatch('diverga_project_update', {
      updates: { stage: 'screening', category: 'systematic_review' }
    });

    assert.equal(updateResult.updated, true, 'Should be updated');
    assert.ok(updateResult.state, 'Should return state');

    const readResult = await dispatch('diverga_project_status', {});
    assert.equal(readResult.stage, 'screening');
    assert.equal(readResult.category, 'systematic_review');
  });

  it('should add and list decisions', async () => {
    const addResult = await dispatch('diverga_decision_add', {
      checkpoint_id: 'SCH_SCREENING_CRITERIA',
      selected: 'AI-PRISMA 6-dimension',
      rationale: 'Systematic approach',
      alternatives: ['Manual screening', 'Keyword only'],
      metadata: { agent: 'i2' }
    });

    assert.equal(addResult.recorded, true);
    assert.ok(addResult.decision_id, 'Should have decision_id');

    const listResult = await dispatch('diverga_decision_list', {});
    assert.ok(Array.isArray(listResult), 'Should return array');

    const found = listResult.find(d => d.checkpoint_id === 'SCH_SCREENING_CRITERIA');
    assert.ok(found, 'Should include the decision');
    assert.equal(found.selected, 'AI-PRISMA 6-dimension');
  });

  it('should write and read priority context', async () => {
    const writeResult = await dispatch('diverga_priority_write', {
      context: 'Systematic review on AI in education. Using Semantic Scholar + OpenAlex.',
      max_chars: 500
    });

    assert.equal(writeResult.written, true);
    assert.ok(writeResult.length <= 500, 'Should respect max_chars');

    const readResult = await dispatch('diverga_priority_read', {});
    assert.ok(readResult.includes('AI in education'), 'Should contain written content');
  });

  it('should export to YAML', async () => {
    const yamlResult = await dispatch('diverga_export_yaml', {});
    assert.equal(typeof yamlResult, 'string', 'Should return string');
    assert.ok(yamlResult.includes('version: 9.0.0'), 'Should have version');
    assert.ok(yamlResult.includes('project_state:'), 'Should have project_state');
  });

  it('should register and list agents', async () => {
    const registerResult = await dispatch('diverga_agent_register', {
      agent_id: 'i0',
      metadata: { category: 'I', model: 'opus', status: 'active' }
    });

    assert.equal(registerResult.registered, true);
    assert.equal(registerResult.agent_id, 'i0');

    const listResult = await dispatch('diverga_agent_list', {});
    assert.ok(Array.isArray(listResult), 'Should return array');

    const found = listResult.find(a => a.agent_id === 'i0');
    assert.ok(found, 'Should include registered agent');
    assert.equal(found.category, 'I');
  });

  it('should send message, read mailbox, and acknowledge', async () => {
    // Register agents first
    await dispatch('diverga_agent_register', {
      agent_id: 'i1',
      metadata: { category: 'I' }
    });

    // Send message
    const sendResult = await dispatch('diverga_message_send', {
      from: 'i0',
      to: 'i1',
      content: 'Start database search',
      metadata: { priority: 'high' }
    });

    assert.equal(sendResult.sent, true);
    assert.ok(sendResult.message_id, 'Should have message_id');

    // Read mailbox
    const mailboxResult = await dispatch('diverga_message_mailbox', {
      agent_id: 'i1',
      unread_only: false
    });

    assert.ok(Array.isArray(mailboxResult), 'Should return array');
    const msg = mailboxResult.find(m => m.message_id === sendResult.message_id);
    assert.ok(msg, 'Should find the message');
    assert.equal(msg.from, 'i0');
    assert.equal(msg.content, 'Start database search');

    // Acknowledge
    const ackResult = await dispatch('diverga_message_acknowledge', {
      message_id: sendResult.message_id,
      response: 'Search initiated'
    });

    assert.equal(ackResult.acknowledged, true);
    assert.equal(ackResult.message_id, sendResult.message_id);
  });
});

// =============================================================================
// Section 2: SQLite Backend Integration Tests
// =============================================================================

describe('Diverga v9.0 Integration Tests - SQLite Backend', () => {
  let tmpDir;
  let dbPath;
  let servers;
  let registry;
  let dispatch;

  before(() => {
    tmpDir = mkdtempSync(join(tmpdir(), 'diverga-test-sqlite-'));
    dbPath = join(tmpDir, '.research', 'diverga.db');
    console.log(`SQLite test directory: ${tmpDir}`);

    servers = createSqliteServers(dbPath, prereqMap);
    const result = createToolRegistry(
      servers.checkpointServer,
      servers.memoryServer,
      servers.commServer
    );
    registry = result;
    dispatch = result.dispatch;
  });

  after(() => {
    if (servers) {
      servers.close();
    }
    if (tmpDir && existsSync(tmpDir)) {
      rmSync(tmpDir, { recursive: true, force: true });
    }
  });

  it('should verify tools are registered', () => {
    assert.ok(registry.tools, 'Tools array should exist');
    assert.equal(registry.tools.length, 16, 'Should have 16 tools');
    assert.equal(typeof dispatch, 'function', 'Dispatch should be a function');
  });

  it('should check prerequisites for known agent', async () => {
    const result = await dispatch('diverga_check_prerequisites', { agent_id: 'a1' });
    assert.equal(result.approved, true, 'Entry point agent should be approved');
    assert.deepEqual(result.missing, [], 'Should have no missing prerequisites');
    assert.ok(result.message, 'Should have a message');
    assert.ok(Array.isArray(result.own_checkpoints), 'Should have own_checkpoints array');
  });

  it('should mark checkpoint and retrieve status', async () => {
    const markResult = await dispatch('diverga_mark_checkpoint', {
      checkpoint_id: 'SCH_DATABASE_SELECTION',
      decision: 'Semantic Scholar + OpenAlex',
      rationale: 'Best API coverage'
    });

    assert.equal(markResult.recorded, true, 'Checkpoint should be recorded');
    assert.equal(markResult.checkpoint_id, 'SCH_DATABASE_SELECTION');
    assert.ok(markResult.decision_id, 'Should have decision_id');

    const statusResult = await dispatch('diverga_checkpoint_status', {});
    assert.ok(Array.isArray(statusResult.passed), 'Passed should be array');
    assert.ok(
      statusResult.passed.includes('SCH_DATABASE_SELECTION'),
      'Should show checkpoint as passed'
    );
  });

  it('should update and read project state', async () => {
    const updateResult = await dispatch('diverga_project_update', {
      updates: { stage: 'screening', category: 'systematic_review' }
    });

    assert.equal(updateResult.updated, true, 'Should be updated');
    assert.ok(updateResult.state, 'Should return state');

    const readResult = await dispatch('diverga_project_status', {});
    assert.equal(readResult.stage, 'screening');
    assert.equal(readResult.category, 'systematic_review');
  });

  it('should add and list decisions', async () => {
    const addResult = await dispatch('diverga_decision_add', {
      checkpoint_id: 'SCH_SCREENING_CRITERIA',
      selected: 'AI-PRISMA 6-dimension',
      rationale: 'Systematic approach',
      alternatives: ['Manual screening', 'Keyword only'],
      metadata: { agent: 'i2' }
    });

    assert.equal(addResult.recorded, true);
    assert.ok(addResult.decision_id, 'Should have decision_id');

    const listResult = await dispatch('diverga_decision_list', {});
    assert.ok(Array.isArray(listResult), 'Should return array');

    const found = listResult.find(d => d.checkpoint_id === 'SCH_SCREENING_CRITERIA');
    assert.ok(found, 'Should include the decision');
    assert.equal(found.selected, 'AI-PRISMA 6-dimension');
  });

  it('should write and read priority context', async () => {
    const writeResult = await dispatch('diverga_priority_write', {
      context: 'Systematic review on AI in education. Using Semantic Scholar + OpenAlex.',
      max_chars: 500
    });

    assert.equal(writeResult.written, true);
    assert.ok(writeResult.length <= 500, 'Should respect max_chars');

    const readResult = await dispatch('diverga_priority_read', {});
    assert.ok(readResult.includes('AI in education'), 'Should contain written content');
  });

  it('should export to YAML', async () => {
    const yamlResult = await dispatch('diverga_export_yaml', {});
    assert.equal(typeof yamlResult, 'string', 'Should return string');
    assert.ok(yamlResult.includes('version: 9.0.0'), 'Should have version');
    assert.ok(yamlResult.includes('project_state:'), 'Should have project_state');
  });

  it('should register and list agents', async () => {
    const registerResult = await dispatch('diverga_agent_register', {
      agent_id: 'i0',
      metadata: { category: 'I', model: 'opus', status: 'active' }
    });

    assert.equal(registerResult.registered, true);
    assert.equal(registerResult.agent_id, 'i0');

    const listResult = await dispatch('diverga_agent_list', {});
    assert.ok(Array.isArray(listResult), 'Should return array');

    const found = listResult.find(a => a.agent_id === 'i0');
    assert.ok(found, 'Should include registered agent');
    assert.equal(found.category, 'I');
  });

  it('should send message, read mailbox, and acknowledge', async () => {
    // Register agents first
    await dispatch('diverga_agent_register', {
      agent_id: 'i1',
      metadata: { category: 'I' }
    });

    // Send message
    const sendResult = await dispatch('diverga_message_send', {
      from: 'i0',
      to: 'i1',
      content: 'Start database search',
      metadata: { priority: 'high' }
    });

    assert.equal(sendResult.sent, true);
    assert.ok(sendResult.message_id, 'Should have message_id');

    // Read mailbox (autoMark=true by default, so status will be 'read' after retrieval)
    const mailboxResult = await dispatch('diverga_message_mailbox', {
      agent_id: 'i1',
      unread_only: false,
      includeRead: true
    });

    assert.ok(Array.isArray(mailboxResult), 'Should return array');
    const msg = mailboxResult.find(m => m.message_id === sendResult.message_id);
    assert.ok(msg, 'Should find the message');
    assert.equal(msg.from, 'i0');
    assert.equal(msg.content, 'Start database search');

    // Acknowledge
    const ackResult = await dispatch('diverga_message_acknowledge', {
      message_id: sendResult.message_id,
      response: 'Search initiated'
    });

    assert.equal(ackResult.acknowledged, true);
    assert.equal(ackResult.message_id, sendResult.message_id);
  });
});

// =============================================================================
// Section 3: Cross-Backend Consistency Tests
// =============================================================================

describe('Diverga v9.0 Cross-Backend Consistency', () => {
  let yamlDir;
  let sqliteDir;
  let yamlDispatch;
  let sqliteDispatch;
  let sqliteServers;

  before(() => {
    // Setup YAML backend
    yamlDir = mkdtempSync(join(tmpdir(), 'diverga-test-yaml-cross-'));
    const yamlCheckpoint = createCheckpointServer(prereqMap, yamlDir);
    const yamlMemory = createMemoryServer(yamlDir);
    const yamlComm = createCommServer(yamlDir);
    yamlDispatch = createToolRegistry(yamlCheckpoint, yamlMemory, yamlComm).dispatch;

    // Setup SQLite backend
    sqliteDir = mkdtempSync(join(tmpdir(), 'diverga-test-sqlite-cross-'));
    const dbPath = join(sqliteDir, '.research', 'diverga.db');
    sqliteServers = createSqliteServers(dbPath, prereqMap);
    sqliteDispatch = createToolRegistry(
      sqliteServers.checkpointServer,
      sqliteServers.memoryServer,
      sqliteServers.commServer
    ).dispatch;
  });

  after(() => {
    if (sqliteServers) {
      sqliteServers.close();
    }
    if (yamlDir && existsSync(yamlDir)) {
      rmSync(yamlDir, { recursive: true, force: true });
    }
    if (sqliteDir && existsSync(sqliteDir)) {
      rmSync(sqliteDir, { recursive: true, force: true });
    }
  });

  it('should return same structure from checkpoint_status on empty state', async () => {
    const yamlResult = await yamlDispatch('diverga_checkpoint_status', {});
    const sqliteResult = await sqliteDispatch('diverga_checkpoint_status', {});

    assert.ok(Array.isArray(yamlResult.passed), 'YAML should have passed array');
    assert.ok(Array.isArray(sqliteResult.passed), 'SQLite should have passed array');
    assert.ok(Array.isArray(yamlResult.pending), 'YAML should have pending array');
    assert.ok(Array.isArray(sqliteResult.pending), 'SQLite should have pending array');
    assert.ok(Array.isArray(yamlResult.blocked), 'YAML should have blocked array');
    assert.ok(Array.isArray(sqliteResult.blocked), 'SQLite should have blocked array');
    assert.equal(typeof yamlResult.total_decisions, 'number');
    assert.equal(typeof sqliteResult.total_decisions, 'number');
  });

  it('should return same structure from project_status on empty state', async () => {
    const yamlResult = await yamlDispatch('diverga_project_status', {});
    const sqliteResult = await sqliteDispatch('diverga_project_status', {});

    assert.equal(typeof yamlResult, 'object', 'YAML should return object');
    assert.equal(typeof sqliteResult, 'object', 'SQLite should return object');
  });

  it('should return same keys after marking checkpoint', async () => {
    const yamlResult = await yamlDispatch('diverga_mark_checkpoint', {
      checkpoint_id: 'TEST_CP',
      decision: 'test',
      rationale: 'test'
    });

    const sqliteResult = await sqliteDispatch('diverga_mark_checkpoint', {
      checkpoint_id: 'TEST_CP',
      decision: 'test',
      rationale: 'test'
    });

    assert.deepEqual(
      Object.keys(yamlResult).sort(),
      Object.keys(sqliteResult).sort(),
      'Should have same keys'
    );
    assert.equal(yamlResult.recorded, true);
    assert.equal(sqliteResult.recorded, true);
  });
});

// =============================================================================
// Section 4: Full Pipeline Simulation Tests
// =============================================================================

describe('Diverga v9.0 Full Pipeline Simulation', () => {
  let tmpDir;
  let dispatch;
  let servers;

  before(() => {
    tmpDir = mkdtempSync(join(tmpdir(), 'diverga-test-pipeline-'));
    const dbPath = join(tmpDir, '.research', 'diverga.db');
    servers = createSqliteServers(dbPath, prereqMap);
    dispatch = createToolRegistry(
      servers.checkpointServer,
      servers.memoryServer,
      servers.commServer
    ).dispatch;
  });

  after(() => {
    if (servers) {
      servers.close();
    }
    if (tmpDir && existsSync(tmpDir)) {
      rmSync(tmpDir, { recursive: true, force: true });
    }
  });

  it('should simulate systematic review pipeline', async () => {
    // Register agents
    await dispatch('diverga_agent_register', {
      agent_id: 'i0',
      metadata: { category: 'I', role: 'orchestrator' }
    });
    await dispatch('diverga_agent_register', {
      agent_id: 'i1',
      metadata: { category: 'I', role: 'retrieval' }
    });
    await dispatch('diverga_agent_register', {
      agent_id: 'i2',
      metadata: { category: 'I', role: 'screening' }
    });
    await dispatch('diverga_agent_register', {
      agent_id: 'i3',
      metadata: { category: 'I', role: 'rag' }
    });

    // Check prerequisites for i2 (should need SCH_DATABASE_SELECTION)
    let prereqCheck = await dispatch('diverga_check_prerequisites', { agent_id: 'i2' });
    assert.equal(prereqCheck.approved, false, 'i2 should be blocked initially');
    assert.ok(
      prereqCheck.missing.includes('SCH_DATABASE_SELECTION'),
      'Should need SCH_DATABASE_SELECTION'
    );

    // Mark SCH_DATABASE_SELECTION checkpoint
    await dispatch('diverga_mark_checkpoint', {
      checkpoint_id: 'SCH_DATABASE_SELECTION',
      decision: 'Semantic Scholar + OpenAlex + arXiv',
      rationale: 'Comprehensive coverage with API access'
    });

    // Check prerequisites for i2 again (should be approved)
    prereqCheck = await dispatch('diverga_check_prerequisites', { agent_id: 'i2' });
    assert.equal(prereqCheck.approved, true, 'i2 should be approved after checkpoint');
    assert.deepEqual(prereqCheck.missing, [], 'Should have no missing prerequisites');

    // i1 sends message to i0
    const msgResult = await dispatch('diverga_message_send', {
      from: 'i1',
      to: 'i0',
      content: 'Database search complete: 150 papers retrieved',
      metadata: { papers_count: 150 }
    });
    assert.equal(msgResult.sent, true);

    // i0 reads mailbox
    const mailbox = await dispatch('diverga_message_mailbox', {
      agent_id: 'i0',
      unread_only: false,
      includeRead: true
    });
    assert.ok(mailbox.length > 0, 'i0 should have messages');

    // Update project state with stage info
    await dispatch('diverga_project_update', {
      updates: {
        stage: 'screening',
        papers_retrieved: 150,
        current_agent: 'i2'
      }
    });

    // Add decision for screening criteria
    await dispatch('diverga_decision_add', {
      checkpoint_id: 'SCH_SCREENING_CRITERIA',
      selected: 'AI-PRISMA 6-dimension screening',
      rationale: 'Comprehensive systematic approach',
      metadata: { agent: 'i2', dimensions: 6 }
    });

    // Verify checkpoint status
    const cpStatus = await dispatch('diverga_checkpoint_status', {});
    assert.ok(
      cpStatus.passed.includes('SCH_DATABASE_SELECTION'),
      'Should show database selection as passed'
    );

    // Verify decision list
    const decisions = await dispatch('diverga_decision_list', {});
    assert.ok(decisions.length >= 2, 'Should have at least 2 decisions');

    // Verify project state
    const projectState = await dispatch('diverga_project_status', {});
    assert.equal(projectState.stage, 'screening');
    assert.equal(projectState.papers_retrieved, 150);
  });

  it('should throw on unknown tool dispatch', async () => {
    await assert.rejects(
      async () => {
        await dispatch('nonexistent_tool', {});
      },
      /Unknown tool/,
      'Should throw for unknown tool'
    );
  });
});
