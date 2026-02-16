/**
 * Test suite for Diverga v9.0 MCP Tool Registry
 *
 * Tests the tool registration layer that routes MCP tool calls
 * to the appropriate server (checkpoint, memory, comm).
 *
 * TDD RED Phase: All tests written to fail until implementation.
 */

import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { createToolRegistry } from '../lib/tool-registry.js';

// =============================================================================
// Mock Servers
// =============================================================================

const createMockCheckpointServer = () => ({
  checkPrerequisites: (agentId) => ({
    approved: true,
    agent_id: agentId,
    pending: [],
    blocked: []
  }),
  markCheckpoint: (checkpointId, decision, rationale) => ({
    recorded: true,
    checkpoint_id: checkpointId,
    decision,
    rationale,
    timestamp: new Date().toISOString()
  }),
  checkpointStatus: () => ({
    passed: ['CP001', 'CP002'],
    pending: ['CP003'],
    blocked: []
  })
});

const createMockMemoryServer = () => ({
  readProjectState: () => ({
    category: 'research',
    currentStage: 'analysis',
    decisions: [],
    metadata: {}
  }),
  updateProjectState: (updates) => ({
    updated: true,
    changes: Object.keys(updates),
    newState: { ...updates }
  }),
  addDecision: (checkpointId, selected, rationale, alternatives, metadata) => ({
    decision_id: 'DEC001',
    checkpoint_id: checkpointId,
    selected,
    rationale,
    alternatives: alternatives || [],
    metadata: metadata || {},
    timestamp: new Date().toISOString()
  }),
  listDecisions: (filters) => ({
    decisions: [
      { decision_id: 'DEC001', checkpoint_id: 'CP001', selected: 'option_a' },
      { decision_id: 'DEC002', checkpoint_id: 'CP002', selected: 'option_b' }
    ],
    filters,
    total: 2
  }),
  readPriorityContext: () => ({
    context: 'High-priority research project on AI education',
    lastUpdated: new Date().toISOString()
  }),
  writePriorityContext: (context, maxChars) => ({
    written: true,
    length: context.length,
    maxChars: maxChars || 500
  }),
  exportToYaml: () => ({
    yaml: '---\nproject:\n  status: active\n',
    exported: true
  })
});

const createMockCommServer = () => ({
  registerAgent: (agentId, metadata) => ({
    registered: true,
    agent_id: agentId,
    metadata: metadata || {},
    timestamp: new Date().toISOString()
  }),
  listAgents: (filters) => ({
    agents: [
      { agent_id: 'I1-paper-retrieval-agent', status: 'active' },
      { agent_id: 'I2-screening-assistant', status: 'idle' }
    ],
    filters: filters || {},
    total: 2
  }),
  send: (from, to, content, metadata) => ({
    sent: true,
    message_id: 'MSG001',
    from,
    to,
    content,
    metadata: metadata || {},
    timestamp: new Date().toISOString()
  }),
  mailbox: (agentId, args) => ({
    messages: [
      { message_id: 'MSG001', from: 'I0', to: agentId, content: 'Test message' }
    ],
    agent_id: agentId,
    unread: 1,
    ...args
  }),
  acknowledge: (messageId, response) => ({
    acknowledged: true,
    message_id: messageId,
    response: response || null,
    timestamp: new Date().toISOString()
  }),
  broadcast: (from, content, metadata) => ({
    broadcast: true,
    message_id: 'BCAST001',
    from,
    content,
    metadata: metadata || {},
    recipients: 5,
    timestamp: new Date().toISOString()
  })
});

// =============================================================================
// Test Suite 1: createToolRegistry Validation
// =============================================================================

describe('createToolRegistry - Validation', () => {
  it('should throw error when called without arguments', () => {
    assert.throws(
      () => createToolRegistry(),
      /requires.*checkpoint.*memory.*comm/i,
      'Should require all three server arguments'
    );
  });

  it('should throw error when checkpoint server is missing', () => {
    const memory = createMockMemoryServer();
    const comm = createMockCommServer();

    assert.throws(
      () => createToolRegistry(null, memory, comm),
      /checkpoint.*server.*required/i,
      'Should validate checkpoint server presence'
    );
  });

  it('should throw error when memory server is missing', () => {
    const checkpoint = createMockCheckpointServer();
    const comm = createMockCommServer();

    assert.throws(
      () => createToolRegistry(checkpoint, null, comm),
      /memory.*server.*required/i,
      'Should validate memory server presence'
    );
  });

  it('should throw error when comm server is missing', () => {
    const checkpoint = createMockCheckpointServer();
    const memory = createMockMemoryServer();

    assert.throws(
      () => createToolRegistry(checkpoint, memory, null),
      /comm.*server.*required/i,
      'Should validate comm server presence'
    );
  });

  it('should return object with tools and dispatch properties', () => {
    const registry = createToolRegistry(
      createMockCheckpointServer(),
      createMockMemoryServer(),
      createMockCommServer()
    );

    assert.ok(registry.tools, 'Should have tools array');
    assert.ok(typeof registry.dispatch === 'function', 'Should have dispatch function');
  });
});

// =============================================================================
// Test Suite 2: Tools Array Structure
// =============================================================================

describe('Tools Array - Structure and Completeness', () => {
  let registry;

  beforeEach(() => {
    registry = createToolRegistry(
      createMockCheckpointServer(),
      createMockMemoryServer(),
      createMockCommServer()
    );
  });

  it('should contain exactly 16 tools', () => {
    assert.equal(
      registry.tools.length,
      16,
      'Registry should contain all 16 MCP tools (3 checkpoint + 7 memory + 6 comm)'
    );
  });

  it('should have unique tool names (no duplicates)', () => {
    const names = registry.tools.map(t => t.name);
    const uniqueNames = new Set(names);

    assert.equal(
      names.length,
      uniqueNames.size,
      'All tool names should be unique'
    );
  });

  it('should have name, description, and inputSchema for each tool', () => {
    registry.tools.forEach(tool => {
      assert.ok(tool.name, `Tool should have name: ${JSON.stringify(tool)}`);
      assert.ok(tool.description, `Tool ${tool.name} should have description`);
      assert.ok(tool.inputSchema, `Tool ${tool.name} should have inputSchema`);
      assert.equal(tool.inputSchema.type, 'object', `Tool ${tool.name} inputSchema should be object type`);
    });
  });

  it('should prefix all tool names with "diverga_"', () => {
    registry.tools.forEach(tool => {
      assert.match(
        tool.name,
        /^diverga_/,
        `Tool name ${tool.name} should start with "diverga_"`
      );
    });
  });

  it('should have non-empty descriptions', () => {
    registry.tools.forEach(tool => {
      assert.ok(
        tool.description.length > 10,
        `Tool ${tool.name} should have meaningful description (>10 chars)`
      );
    });
  });
});

// =============================================================================
// Test Suite 3: Backward Compatibility (v8 Tool Names)
// =============================================================================

describe('Backward Compatibility - v8 Tool Names', () => {
  let registry;
  let toolNames;

  beforeEach(() => {
    registry = createToolRegistry(
      createMockCheckpointServer(),
      createMockMemoryServer(),
      createMockCommServer()
    );
    toolNames = registry.tools.map(t => t.name);
  });

  it('should include all 3 checkpoint tools with v8 names', () => {
    const checkpointTools = [
      'diverga_check_prerequisites',
      'diverga_mark_checkpoint',
      'diverga_checkpoint_status'
    ];

    checkpointTools.forEach(name => {
      assert.ok(
        toolNames.includes(name),
        `Should include backward-compatible checkpoint tool: ${name}`
      );
    });
  });

  it('should include all 7 memory tools (v8 compatible where applicable)', () => {
    const memoryTools = [
      'diverga_project_status',
      'diverga_project_update',
      'diverga_decision_add',
      'diverga_decision_list',
      'diverga_priority_read',
      'diverga_priority_write',
      'diverga_export_yaml'
    ];

    memoryTools.forEach(name => {
      assert.ok(
        toolNames.includes(name),
        `Should include memory tool: ${name}`
      );
    });
  });

  it('should include all 6 new comm tools', () => {
    const commTools = [
      'diverga_agent_register',
      'diverga_agent_list',
      'diverga_message_send',
      'diverga_message_mailbox',
      'diverga_message_acknowledge',
      'diverga_message_broadcast'
    ];

    commTools.forEach(name => {
      assert.ok(
        toolNames.includes(name),
        `Should include new comm tool: ${name}`
      );
    });
  });
});

// =============================================================================
// Test Suite 4: Dispatch Routing - Checkpoint Server
// =============================================================================

describe('Dispatch Routing - Checkpoint Server', () => {
  let registry;
  let checkpointServer;

  beforeEach(() => {
    checkpointServer = createMockCheckpointServer();
    registry = createToolRegistry(
      checkpointServer,
      createMockMemoryServer(),
      createMockCommServer()
    );
  });

  it('should route diverga_check_prerequisites to checkPrerequisites method', async () => {
    const result = await registry.dispatch('diverga_check_prerequisites', {
      agent_id: 'I1-paper-retrieval-agent'
    });

    assert.equal(result.approved, true);
    assert.equal(result.agent_id, 'I1-paper-retrieval-agent');
  });

  it('should route diverga_mark_checkpoint to markCheckpoint method', async () => {
    const result = await registry.dispatch('diverga_mark_checkpoint', {
      checkpoint_id: 'SCH_DATABASE_SELECTION',
      decision: 'semantic_scholar',
      rationale: 'Best API coverage'
    });

    assert.equal(result.recorded, true);
    assert.equal(result.checkpoint_id, 'SCH_DATABASE_SELECTION');
    assert.equal(result.decision, 'semantic_scholar');
  });

  it('should route diverga_checkpoint_status to checkpointStatus method', async () => {
    const result = await registry.dispatch('diverga_checkpoint_status', {});

    assert.ok(Array.isArray(result.passed));
    assert.ok(Array.isArray(result.pending));
    assert.ok(Array.isArray(result.blocked));
  });
});

// =============================================================================
// Test Suite 5: Dispatch Routing - Memory Server
// =============================================================================

describe('Dispatch Routing - Memory Server', () => {
  let registry;
  let memoryServer;

  beforeEach(() => {
    memoryServer = createMockMemoryServer();
    registry = createToolRegistry(
      createMockCheckpointServer(),
      memoryServer,
      createMockCommServer()
    );
  });

  it('should route diverga_project_status to readProjectState method', async () => {
    const result = await registry.dispatch('diverga_project_status', {});

    assert.ok(result.category);
    assert.ok(result.currentStage);
  });

  it('should route diverga_project_update to updateProjectState method', async () => {
    const result = await registry.dispatch('diverga_project_update', {
      updates: { currentStage: 'synthesis', progress: 75 }
    });

    assert.equal(result.updated, true);
    assert.ok(Array.isArray(result.changes));
  });

  it('should route diverga_decision_add to addDecision method', async () => {
    const result = await registry.dispatch('diverga_decision_add', {
      checkpoint_id: 'SCH_DATABASE_SELECTION',
      selected: 'semantic_scholar',
      rationale: 'Best coverage',
      alternatives: ['openalex', 'arxiv'],
      metadata: { confidence: 'high' }
    });

    assert.ok(result.decision_id);
    assert.equal(result.checkpoint_id, 'SCH_DATABASE_SELECTION');
    assert.equal(result.selected, 'semantic_scholar');
  });

  it('should route diverga_decision_list to listDecisions method', async () => {
    const result = await registry.dispatch('diverga_decision_list', {
      filters: { checkpoint_id: 'CP001' }
    });

    assert.ok(Array.isArray(result.decisions));
    assert.ok(result.total >= 0);
  });

  it('should route diverga_priority_read to readPriorityContext method', async () => {
    const result = await registry.dispatch('diverga_priority_read', {});

    assert.ok(result.context);
    assert.ok(result.lastUpdated);
  });

  it('should route diverga_priority_write to writePriorityContext method', async () => {
    const result = await registry.dispatch('diverga_priority_write', {
      context: 'Updated priority: Focus on ScholaRAG Stage 3',
      max_chars: 500
    });

    assert.equal(result.written, true);
    assert.ok(result.length > 0);
  });

  it('should route diverga_export_yaml to exportToYaml method', async () => {
    const result = await registry.dispatch('diverga_export_yaml', {});

    assert.ok(result.yaml);
    assert.equal(result.exported, true);
  });
});

// =============================================================================
// Test Suite 6: Dispatch Routing - Comm Server
// =============================================================================

describe('Dispatch Routing - Comm Server', () => {
  let registry;
  let commServer;

  beforeEach(() => {
    commServer = createMockCommServer();
    registry = createToolRegistry(
      createMockCheckpointServer(),
      createMockMemoryServer(),
      commServer
    );
  });

  it('should route diverga_agent_register to registerAgent method', async () => {
    const result = await registry.dispatch('diverga_agent_register', {
      agent_id: 'I1-paper-retrieval-agent',
      metadata: { category: 'I', checkpoint: 'SCH_DATABASE_SELECTION' }
    });

    assert.equal(result.registered, true);
    assert.equal(result.agent_id, 'I1-paper-retrieval-agent');
  });

  it('should route diverga_agent_list to listAgents method', async () => {
    const result = await registry.dispatch('diverga_agent_list', {
      filters: { status: 'active' }
    });

    assert.ok(Array.isArray(result.agents));
    assert.ok(result.total >= 0);
  });

  it('should route diverga_message_send to send method', async () => {
    const result = await registry.dispatch('diverga_message_send', {
      from: 'I0-ScholarAgentOrchestrator',
      to: 'I1-paper-retrieval-agent',
      content: 'Start database fetch',
      metadata: { priority: 'high' }
    });

    assert.equal(result.sent, true);
    assert.ok(result.message_id);
    assert.equal(result.from, 'I0-ScholarAgentOrchestrator');
  });

  it('should route diverga_message_mailbox to mailbox method', async () => {
    const result = await registry.dispatch('diverga_message_mailbox', {
      agent_id: 'I1-paper-retrieval-agent',
      limit: 10,
      unread_only: true
    });

    assert.ok(Array.isArray(result.messages));
    assert.equal(result.agent_id, 'I1-paper-retrieval-agent');
  });

  it('should route diverga_message_acknowledge to acknowledge method', async () => {
    const result = await registry.dispatch('diverga_message_acknowledge', {
      message_id: 'MSG001',
      response: 'Database fetch started'
    });

    assert.equal(result.acknowledged, true);
    assert.equal(result.message_id, 'MSG001');
  });

  it('should route diverga_message_broadcast to broadcast method', async () => {
    const result = await registry.dispatch('diverga_message_broadcast', {
      from: 'I0-ScholarAgentOrchestrator',
      content: 'Project initialization complete',
      metadata: { stage: 'setup' }
    });

    assert.equal(result.broadcast, true);
    assert.ok(result.message_id);
    assert.ok(result.recipients >= 0);
  });
});

// =============================================================================
// Test Suite 7: Dispatch Error Handling
// =============================================================================

describe('Dispatch - Error Handling', () => {
  let registry;

  beforeEach(() => {
    registry = createToolRegistry(
      createMockCheckpointServer(),
      createMockMemoryServer(),
      createMockCommServer()
    );
  });

  it('should throw error for unknown tool name', async () => {
    await assert.rejects(
      async () => registry.dispatch('diverga_nonexistent_tool', {}),
      /unknown.*tool.*diverga_nonexistent_tool/i,
      'Should reject with unknown tool error'
    );
  });

  it('should propagate server method errors', async () => {
    const errorCheckpoint = {
      ...createMockCheckpointServer(),
      checkPrerequisites: () => {
        throw new Error('Database connection failed');
      }
    };

    const errorRegistry = createToolRegistry(
      errorCheckpoint,
      createMockMemoryServer(),
      createMockCommServer()
    );

    await assert.rejects(
      async () => errorRegistry.dispatch('diverga_check_prerequisites', { agent_id: 'I1' }),
      /database.*connection.*failed/i,
      'Should propagate server errors to caller'
    );
  });

  it('should handle missing required arguments gracefully', async () => {
    // This should either throw validation error or pass args as-is to server
    // Implementation can decide, but should not crash
    const result = await registry.dispatch('diverga_mark_checkpoint', {
      // Missing checkpoint_id, decision, rationale
    });

    // If validation happens in registry, expect error
    // If validation happens in server, result will be returned
    assert.ok(result !== undefined, 'Should return result or throw validation error');
  });
});

// =============================================================================
// Test Suite 8: Input Schema Validation
// =============================================================================

describe('Input Schema - Required Fields', () => {
  let registry;
  let toolSchemas;

  beforeEach(() => {
    registry = createToolRegistry(
      createMockCheckpointServer(),
      createMockMemoryServer(),
      createMockCommServer()
    );
    toolSchemas = Object.fromEntries(
      registry.tools.map(t => [t.name, t.inputSchema])
    );
  });

  it('diverga_check_prerequisites should require agent_id', () => {
    const schema = toolSchemas.diverga_check_prerequisites;
    assert.ok(schema.properties.agent_id, 'Should have agent_id property');
    assert.ok(
      schema.required?.includes('agent_id'),
      'agent_id should be required'
    );
  });

  it('diverga_mark_checkpoint should require checkpoint_id, decision, rationale', () => {
    const schema = toolSchemas.diverga_mark_checkpoint;
    const required = ['checkpoint_id', 'decision', 'rationale'];

    required.forEach(field => {
      assert.ok(schema.properties[field], `Should have ${field} property`);
      assert.ok(
        schema.required?.includes(field),
        `${field} should be required`
      );
    });
  });

  it('diverga_decision_add should require checkpoint_id and selected', () => {
    const schema = toolSchemas.diverga_decision_add;
    const required = ['checkpoint_id', 'selected'];

    required.forEach(field => {
      assert.ok(schema.properties[field], `Should have ${field} property`);
      assert.ok(
        schema.required?.includes(field),
        `${field} should be required`
      );
    });
  });

  it('diverga_message_send should require from, to, content', () => {
    const schema = toolSchemas.diverga_message_send;
    const required = ['from', 'to', 'content'];

    required.forEach(field => {
      assert.ok(schema.properties[field], `Should have ${field} property`);
      assert.ok(
        schema.required?.includes(field),
        `${field} should be required`
      );
    });
  });

  it('diverga_priority_write should require context field', () => {
    const schema = toolSchemas.diverga_priority_write;
    assert.ok(schema.properties.context, 'Should have context property');
    assert.ok(
      schema.required?.includes('context'),
      'context should be required'
    );
  });

  it('all schemas should have properties object', () => {
    registry.tools.forEach(tool => {
      assert.ok(
        tool.inputSchema.properties,
        `Tool ${tool.name} should have properties in inputSchema`
      );
      assert.equal(
        typeof tool.inputSchema.properties,
        'object',
        `Tool ${tool.name} properties should be an object`
      );
    });
  });
});

// =============================================================================
// Test Suite 9: Async/Promise Handling
// =============================================================================

describe('Dispatch - Async/Promise Handling', () => {
  let registry;

  beforeEach(() => {
    // Create async mock servers
    const asyncCheckpoint = {
      checkPrerequisites: async (agentId) => {
        return new Promise(resolve => {
          setTimeout(() => {
            resolve({ approved: true, agent_id: agentId });
          }, 10);
        });
      },
      markCheckpoint: async (checkpointId, decision, rationale) => {
        return { recorded: true, checkpoint_id: checkpointId };
      },
      checkpointStatus: async () => {
        return { passed: [], pending: [], blocked: [] };
      }
    };

    registry = createToolRegistry(
      asyncCheckpoint,
      createMockMemoryServer(),
      createMockCommServer()
    );
  });

  it('should handle async server methods correctly', async () => {
    const result = await registry.dispatch('diverga_check_prerequisites', {
      agent_id: 'I1-paper-retrieval-agent'
    });

    assert.equal(result.approved, true);
    assert.equal(result.agent_id, 'I1-paper-retrieval-agent');
  });

  it('should return Promise from dispatch', () => {
    const promise = registry.dispatch('diverga_check_prerequisites', {
      agent_id: 'I1'
    });

    assert.ok(promise instanceof Promise, 'dispatch should return a Promise');
  });
});

// =============================================================================
// Test Suite 10: Tool Descriptions
// =============================================================================

describe('Tool Descriptions - Quality Check', () => {
  let registry;

  beforeEach(() => {
    registry = createToolRegistry(
      createMockCheckpointServer(),
      createMockMemoryServer(),
      createMockCommServer()
    );
  });

  it('checkpoint tools should mention prerequisite/checkpoint/status', () => {
    const checkpointTools = registry.tools.filter(t =>
      t.name.includes('prerequisite') || t.name.includes('checkpoint')
    );

    checkpointTools.forEach(tool => {
      assert.match(
        tool.description.toLowerCase(),
        /prerequisite|checkpoint|status|validation/,
        `Tool ${tool.name} should have relevant description`
      );
    });
  });

  it('memory tools should mention project/decision/priority/export', () => {
    const memoryKeywords = /project|decision|priority|export|yaml|state/i;
    const memoryTools = registry.tools.filter(t =>
      t.name.includes('project') ||
      t.name.includes('decision') ||
      t.name.includes('priority') ||
      t.name.includes('export')
    );

    memoryTools.forEach(tool => {
      assert.match(
        tool.description,
        memoryKeywords,
        `Tool ${tool.name} should have relevant description`
      );
    });
  });

  it('comm tools should mention agent/message/mailbox/broadcast', () => {
    const commKeywords = /agent|message|mailbox|broadcast|send|communication/i;
    const commTools = registry.tools.filter(t =>
      t.name.includes('agent') || t.name.includes('message')
    );

    commTools.forEach(tool => {
      assert.match(
        tool.description,
        commKeywords,
        `Tool ${tool.name} should have relevant description`
      );
    });
  });
});

// =============================================================================
// End of Test Suite
// =============================================================================
