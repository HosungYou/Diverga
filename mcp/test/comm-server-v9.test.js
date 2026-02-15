/**
 * TDD RED Tests for Diverga v9.0 Comm Server (New)
 *
 * Tests the new communication server that handles agent messaging.
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
import { createCommServer } from '../servers/comm-server.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

/**
 * Helper: create a fresh temp dir and server instance for each suite.
 */
function createTestContext() {
  const tmpDir = mkdtempSync(join(tmpdir(), 'comm-server-v9-test-'));
  const server = createCommServer(tmpDir);
  return { tmpDir, server };
}

function cleanup(tmpDir) {
  rmSync(tmpDir, { recursive: true, force: true });
}

/** Write a JSON file into the temp research dir */
function writeTestJson(tmpDir, filename, data) {
  const filepath = join(tmpDir, filename);
  const dir = dirname(filepath);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf8');
}

/** Read a JSON file from the temp research dir */
function readTestJson(tmpDir, filename) {
  const filepath = join(tmpDir, filename);
  if (!existsSync(filepath)) return null;
  return JSON.parse(readFileSync(filepath, 'utf8'));
}

// ===========================================================================
// 1. Server Factory
// ===========================================================================

describe('createCommServer factory', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('creates server instance with all comm tools', () => {
    assert.ok(server);
    assert.equal(typeof server.send, 'function');
    assert.equal(typeof server.broadcast, 'function');
    assert.equal(typeof server.mailbox, 'function');
    assert.equal(typeof server.acknowledge, 'function');
    assert.equal(typeof server.registerAgent, 'function');
    assert.equal(typeof server.listAgents, 'function');
    cleanup(tmpDir);
  });

  it('does NOT include checkpoint tools (in checkpoint-server)', () => {
    assert.equal(server.checkPrerequisites, undefined);
    assert.equal(server.markCheckpoint, undefined);
    assert.equal(server.checkpointStatus, undefined);
    cleanup(tmpDir);
  });

  it('does NOT include memory tools (in memory-server)', () => {
    assert.equal(server.readProjectState, undefined);
    assert.equal(server.addDecision, undefined);
    assert.equal(server.readPriorityContext, undefined);
    cleanup(tmpDir);
  });

  it('accepts research directory parameter', () => {
    const customDir = mkdtempSync(join(tmpdir(), 'custom-comm-'));
    const customServer = createCommServer(customDir);
    assert.ok(customServer);
    cleanup(customDir);
    cleanup(tmpDir);
  });

  it('throws error when research directory is missing', () => {
    assert.throws(() => {
      createCommServer(null);
    }, /research directory/i);
    cleanup(tmpDir);
  });

  it('creates .research/comm/ directory for message storage', () => {
    const newDir = mkdtempSync(join(tmpdir(), 'new-comm-'));
    const newServer = createCommServer(newDir);

    // Trigger message send
    newServer.registerAgent('a1', { name: 'Agent A1' });
    newServer.send('a1', 'a2', 'Test message');

    const commPath = join(newDir, '.research', 'comm');
    assert.equal(existsSync(commPath), true);
    cleanup(newDir);
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 2. registerAgent
// ===========================================================================

describe('registerAgent', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('registers new agent with metadata', () => {
    const result = server.registerAgent('a1', { name: 'ResearchQuestionRefiner', model: 'opus' });

    assert.equal(result.registered, true);
    assert.equal(result.agent_id, 'a1');
    cleanup(tmpDir);
  });

  it('creates agents.json file on first registration', () => {
    server.registerAgent('a1', { name: 'Agent A1' });

    const filepath = join(tmpDir, '.research', 'comm', 'agents.json');
    assert.equal(existsSync(filepath), true);
    cleanup(tmpDir);
  });

  it('stores agent metadata correctly', () => {
    server.registerAgent('a1', { name: 'Agent A1', model: 'opus', category: 'foundation' });

    const data = readTestJson(join(tmpDir, '.research', 'comm'), 'agents.json');
    assert.equal(data.agents.a1.name, 'Agent A1');
    assert.equal(data.agents.a1.model, 'opus');
    assert.equal(data.agents.a1.category, 'foundation');
    assert.ok(data.agents.a1.registered_at);
    cleanup(tmpDir);
  });

  it('updates existing agent metadata on re-registration', () => {
    server.registerAgent('a1', { name: 'Agent A1', status: 'idle' });
    server.registerAgent('a1', { name: 'Agent A1 Updated', status: 'active' });

    const data = readTestJson(join(tmpDir, '.research', 'comm'), 'agents.json');
    assert.equal(data.agents.a1.name, 'Agent A1 Updated');
    assert.equal(data.agents.a1.status, 'active');
    cleanup(tmpDir);
  });

  it('registers multiple agents', () => {
    server.registerAgent('a1', { name: 'Agent A1' });
    server.registerAgent('a2', { name: 'Agent A2' });
    server.registerAgent('c5', { name: 'MetaAnalysisMaster' });

    const data = readTestJson(join(tmpDir, '.research', 'comm'), 'agents.json');
    assert.equal(Object.keys(data.agents).length, 3);
    cleanup(tmpDir);
  });

  it('normalizes agent IDs to lowercase', () => {
    server.registerAgent('A1', { name: 'Agent A1' });
    server.registerAgent('C5-Meta', { name: 'C5' });

    const data = readTestJson(join(tmpDir, '.research', 'comm'), 'agents.json');
    assert.ok(data.agents.a1);
    assert.ok(data.agents['c5-meta']);
    cleanup(tmpDir);
  });

  it('preserves updated_at timestamp on re-registration', () => {
    server.registerAgent('a1', { name: 'Agent A1' });

    const data1 = readTestJson(join(tmpDir, '.research', 'comm'), 'agents.json');
    const registeredAt = data1.agents.a1.registered_at;

    // Wait a bit and re-register
    server.registerAgent('a1', { name: 'Agent A1 Updated' });

    const data2 = readTestJson(join(tmpDir, '.research', 'comm'), 'agents.json');
    assert.equal(data2.agents.a1.registered_at, registeredAt); // Preserved
    assert.ok(data2.agents.a1.updated_at);
    cleanup(tmpDir);
  });

  it('throws error for invalid agent ID', () => {
    assert.throws(() => {
      server.registerAgent('', { name: 'Invalid' });
    }, /agent.*id/i);

    assert.throws(() => {
      server.registerAgent(null, { name: 'Invalid' });
    }, /agent.*id/i);

    cleanup(tmpDir);
  });
});

// ===========================================================================
// 3. listAgents
// ===========================================================================

describe('listAgents', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('returns empty array when no agents registered', () => {
    const result = server.listAgents();
    assert.deepEqual(result, []);
    cleanup(tmpDir);
  });

  it('returns all registered agents', () => {
    server.registerAgent('a1', { name: 'Agent A1' });
    server.registerAgent('a2', { name: 'Agent A2' });
    server.registerAgent('c5', { name: 'C5' });

    const result = server.listAgents();
    assert.equal(result.length, 3);
    cleanup(tmpDir);
  });

  it('includes agent metadata in results', () => {
    server.registerAgent('a1', { name: 'ResearchQuestionRefiner', model: 'opus', category: 'foundation' });

    const result = server.listAgents();
    assert.equal(result[0].agent_id, 'a1');
    assert.equal(result[0].name, 'ResearchQuestionRefiner');
    assert.equal(result[0].model, 'opus');
    assert.equal(result[0].category, 'foundation');
    cleanup(tmpDir);
  });

  it('filters by status when provided', () => {
    server.registerAgent('a1', { name: 'A1', status: 'active' });
    server.registerAgent('a2', { name: 'A2', status: 'idle' });
    server.registerAgent('c5', { name: 'C5', status: 'active' });

    const result = server.listAgents({ status: 'active' });
    assert.equal(result.length, 2);
    assert.equal(result[0].agent_id, 'a1');
    assert.equal(result[1].agent_id, 'c5');
    cleanup(tmpDir);
  });

  it('filters by category when provided', () => {
    server.registerAgent('a1', { name: 'A1', category: 'foundation' });
    server.registerAgent('b1', { name: 'B1', category: 'evidence' });
    server.registerAgent('c1', { name: 'C1', category: 'design' });

    const result = server.listAgents({ category: 'foundation' });
    assert.equal(result.length, 1);
    assert.equal(result[0].agent_id, 'a1');
    cleanup(tmpDir);
  });

  it('filters by model when provided', () => {
    server.registerAgent('a1', { name: 'A1', model: 'opus' });
    server.registerAgent('a2', { name: 'A2', model: 'sonnet' });
    server.registerAgent('b3', { name: 'B3', model: 'haiku' });

    const result = server.listAgents({ model: 'opus' });
    assert.equal(result.length, 1);
    assert.equal(result[0].agent_id, 'a1');
    cleanup(tmpDir);
  });

  it('combines multiple filters', () => {
    server.registerAgent('a1', { name: 'A1', model: 'opus', category: 'foundation', status: 'active' });
    server.registerAgent('a2', { name: 'A2', model: 'opus', category: 'foundation', status: 'idle' });
    server.registerAgent('c5', { name: 'C5', model: 'opus', category: 'design', status: 'active' });

    const result = server.listAgents({ model: 'opus', category: 'foundation', status: 'active' });
    assert.equal(result.length, 1);
    assert.equal(result[0].agent_id, 'a1');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 4. send
// ===========================================================================

describe('send', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('sends message from one agent to another', () => {
    server.registerAgent('a1', { name: 'Agent A1' });
    server.registerAgent('a2', { name: 'Agent A2' });

    const result = server.send('a1', 'a2', 'Hello from A1');

    assert.equal(result.sent, true);
    assert.ok(result.message_id);
    cleanup(tmpDir);
  });

  it('creates messages.json file on first send', () => {
    server.registerAgent('a1', { name: 'A1' });
    server.registerAgent('a2', { name: 'A2' });

    server.send('a1', 'a2', 'Test message');

    const filepath = join(tmpDir, '.research', 'comm', 'messages.json');
    assert.equal(existsSync(filepath), true);
    cleanup(tmpDir);
  });

  it('stores message with correct structure', () => {
    server.registerAgent('a1', { name: 'A1' });
    server.registerAgent('a2', { name: 'A2' });

    server.send('a1', 'a2', 'Test message content');

    const data = readTestJson(join(tmpDir, '.research', 'comm'), 'messages.json');
    const msg = data.messages[0];

    assert.ok(msg.message_id);
    assert.equal(msg.from, 'a1');
    assert.equal(msg.to, 'a2');
    assert.equal(msg.content, 'Test message content');
    assert.equal(msg.status, 'unread');
    assert.ok(msg.sent_at);
    cleanup(tmpDir);
  });

  it('generates unique sequential message IDs', () => {
    server.registerAgent('a1', { name: 'A1' });
    server.registerAgent('a2', { name: 'A2' });

    const r1 = server.send('a1', 'a2', 'Message 1');
    const r2 = server.send('a1', 'a2', 'Message 2');
    const r3 = server.send('a2', 'a1', 'Message 3');

    assert.equal(r1.message_id, 'msg_001');
    assert.equal(r2.message_id, 'msg_002');
    assert.equal(r3.message_id, 'msg_003');
    cleanup(tmpDir);
  });

  it('allows unregistered agents to send (creates implicit registration)', () => {
    const result = server.send('unknown1', 'unknown2', 'Test');

    assert.equal(result.sent, true);
    cleanup(tmpDir);
  });

  it('supports metadata in messages', () => {
    server.registerAgent('a1', { name: 'A1' });
    server.registerAgent('a2', { name: 'A2' });

    server.send('a1', 'a2', 'Test', { priority: 'high', category: 'checkpoint' });

    const data = readTestJson(join(tmpDir, '.research', 'comm'), 'messages.json');
    const msg = data.messages[0];

    assert.equal(msg.metadata.priority, 'high');
    assert.equal(msg.metadata.category, 'checkpoint');
    cleanup(tmpDir);
  });

  it('throws error for empty content', () => {
    assert.throws(() => {
      server.send('a1', 'a2', '');
    }, /content/i);

    assert.throws(() => {
      server.send('a1', 'a2', null);
    }, /content/i);

    cleanup(tmpDir);
  });

  it('throws error for missing sender or recipient', () => {
    assert.throws(() => {
      server.send('', 'a2', 'Test');
    }, /from.*to/i);

    assert.throws(() => {
      server.send('a1', '', 'Test');
    }, /from.*to/i);

    cleanup(tmpDir);
  });
});

// ===========================================================================
// 5. mailbox
// ===========================================================================

describe('mailbox', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('returns empty array when no messages', () => {
    const result = server.mailbox('a1');
    assert.deepEqual(result, []);
    cleanup(tmpDir);
  });

  it('returns unread messages for agent', () => {
    server.send('a1', 'a2', 'Message 1');
    server.send('a1', 'a2', 'Message 2');
    server.send('a2', 'a1', 'Message 3');

    const result = server.mailbox('a2');
    assert.equal(result.length, 2);
    assert.equal(result[0].content, 'Message 1');
    assert.equal(result[1].content, 'Message 2');
    cleanup(tmpDir);
  });

  it('marks messages as read after retrieval', () => {
    server.send('a1', 'a2', 'Test message');

    const result1 = server.mailbox('a2');
    assert.equal(result1.length, 1);
    assert.equal(result1[0].status, 'unread');

    const result2 = server.mailbox('a2');
    assert.equal(result2.length, 0); // Already marked as read
    cleanup(tmpDir);
  });

  it('updates read_at timestamp when marking as read', () => {
    server.send('a1', 'a2', 'Test');

    server.mailbox('a2');

    const data = readTestJson(join(tmpDir, '.research', 'comm'), 'messages.json');
    const msg = data.messages[0];

    assert.equal(msg.status, 'read');
    assert.ok(msg.read_at);
    cleanup(tmpDir);
  });

  it('does not return messages for other agents', () => {
    server.send('a1', 'a2', 'For A2');
    server.send('a1', 'c5', 'For C5');

    const result = server.mailbox('a2');
    assert.equal(result.length, 1);
    assert.equal(result[0].content, 'For A2');
    cleanup(tmpDir);
  });

  it('returns messages in chronological order', () => {
    server.send('a1', 'a2', 'First');
    server.send('c5', 'a2', 'Second');
    server.send('a1', 'a2', 'Third');

    const result = server.mailbox('a2');
    assert.equal(result[0].content, 'First');
    assert.equal(result[1].content, 'Second');
    assert.equal(result[2].content, 'Third');
    cleanup(tmpDir);
  });

  it('filters by status when provided', () => {
    server.send('a1', 'a2', 'Message 1');
    server.send('a1', 'a2', 'Message 2');

    // First retrieval marks as read
    server.mailbox('a2');

    // Explicitly query read messages
    const read = server.mailbox('a2', { status: 'read' });
    assert.equal(read.length, 2);

    // Unread should be empty
    const unread = server.mailbox('a2', { status: 'unread' });
    assert.equal(unread.length, 0);

    cleanup(tmpDir);
  });

  it('filters by sender when provided', () => {
    server.send('a1', 'a2', 'From A1');
    server.send('c5', 'a2', 'From C5');
    server.send('a1', 'a2', 'From A1 again');

    const result = server.mailbox('a2', { from: 'a1' });
    assert.equal(result.length, 2);
    cleanup(tmpDir);
  });

  it('does not auto-mark as read when includeRead: true', () => {
    server.send('a1', 'a2', 'Test');

    const result1 = server.mailbox('a2', { includeRead: true, autoMark: false });
    assert.equal(result1.length, 1);
    assert.equal(result1[0].status, 'unread');

    const result2 = server.mailbox('a2', { includeRead: true, autoMark: false });
    assert.equal(result2.length, 1);
    assert.equal(result2[0].status, 'unread'); // Still unread

    cleanup(tmpDir);
  });
});

// ===========================================================================
// 6. acknowledge
// ===========================================================================

describe('acknowledge', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('marks message as acknowledged', () => {
    const { message_id } = server.send('a1', 'a2', 'Test message');

    const result = server.acknowledge(message_id);

    assert.equal(result.acknowledged, true);
    assert.equal(result.message_id, message_id);
    cleanup(tmpDir);
  });

  it('updates message status to acknowledged', () => {
    const { message_id } = server.send('a1', 'a2', 'Test');

    server.acknowledge(message_id);

    const data = readTestJson(join(tmpDir, '.research', 'comm'), 'messages.json');
    const msg = data.messages.find(m => m.message_id === message_id);

    assert.equal(msg.status, 'acknowledged');
    assert.ok(msg.acknowledged_at);
    cleanup(tmpDir);
  });

  it('allows acknowledging already-read messages', () => {
    const { message_id } = server.send('a1', 'a2', 'Test');

    server.mailbox('a2'); // Marks as read
    const result = server.acknowledge(message_id);

    assert.equal(result.acknowledged, true);
    cleanup(tmpDir);
  });

  it('throws error for non-existent message ID', () => {
    assert.throws(() => {
      server.acknowledge('msg_999');
    }, /not found/i);

    cleanup(tmpDir);
  });

  it('throws error for invalid message ID', () => {
    assert.throws(() => {
      server.acknowledge('');
    }, /message.*id/i);

    assert.throws(() => {
      server.acknowledge(null);
    }, /message.*id/i);

    cleanup(tmpDir);
  });

  it('supports optional response content', () => {
    const { message_id } = server.send('a1', 'a2', 'Question?');

    server.acknowledge(message_id, 'Answer received, will process.');

    const data = readTestJson(join(tmpDir, '.research', 'comm'), 'messages.json');
    const msg = data.messages.find(m => m.message_id === message_id);

    assert.equal(msg.response, 'Answer received, will process.');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 7. broadcast
// ===========================================================================

describe('broadcast', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('sends message to all registered agents except sender', () => {
    server.registerAgent('a1', { name: 'A1' });
    server.registerAgent('a2', { name: 'A2' });
    server.registerAgent('c5', { name: 'C5' });

    const result = server.broadcast('a1', 'Broadcast message');

    assert.equal(result.sent, true);
    assert.equal(result.recipient_count, 2); // a2 and c5, not a1
    cleanup(tmpDir);
  });

  it('creates individual messages for each recipient', () => {
    server.registerAgent('a1', { name: 'A1' });
    server.registerAgent('a2', { name: 'A2' });
    server.registerAgent('c5', { name: 'C5' });

    server.broadcast('a1', 'Broadcast test');

    const data = readTestJson(join(tmpDir, '.research', 'comm'), 'messages.json');
    assert.equal(data.messages.length, 2);

    const recipients = data.messages.map(m => m.to);
    assert.ok(recipients.includes('a2'));
    assert.ok(recipients.includes('c5'));
    assert.ok(!recipients.includes('a1')); // Sender excluded

    cleanup(tmpDir);
  });

  it('marks all broadcast messages with broadcast: true', () => {
    server.registerAgent('a1', { name: 'A1' });
    server.registerAgent('a2', { name: 'A2' });

    server.broadcast('a1', 'Broadcast');

    const data = readTestJson(join(tmpDir, '.research', 'comm'), 'messages.json');
    data.messages.forEach(msg => {
      assert.equal(msg.broadcast, true);
    });

    cleanup(tmpDir);
  });

  it('returns empty recipient_count when only sender registered', () => {
    server.registerAgent('a1', { name: 'A1' });

    const result = server.broadcast('a1', 'Lonely broadcast');

    assert.equal(result.sent, true);
    assert.equal(result.recipient_count, 0);
    cleanup(tmpDir);
  });

  it('includes all messages when no agents registered', () => {
    const result = server.broadcast('unknown', 'Test');

    assert.equal(result.sent, true);
    assert.equal(result.recipient_count, 0);
    cleanup(tmpDir);
  });

  it('supports metadata in broadcast messages', () => {
    server.registerAgent('a1', { name: 'A1' });
    server.registerAgent('a2', { name: 'A2' });

    server.broadcast('a1', 'Test', { priority: 'critical', category: 'system' });

    const data = readTestJson(join(tmpDir, '.research', 'comm'), 'messages.json');
    data.messages.forEach(msg => {
      assert.equal(msg.metadata.priority, 'critical');
      assert.equal(msg.metadata.category, 'system');
    });

    cleanup(tmpDir);
  });

  it('throws error for empty content', () => {
    assert.throws(() => {
      server.broadcast('a1', '');
    }, /content/i);

    cleanup(tmpDir);
  });

  it('throws error for missing sender', () => {
    assert.throws(() => {
      server.broadcast('', 'Test');
    }, /from/i);

    cleanup(tmpDir);
  });
});

// ===========================================================================
// 8. Message Persistence
// ===========================================================================

describe('message persistence', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('messages survive server restart', () => {
    server.send('a1', 'a2', 'Persistent message');

    // Create new server instance with same directory
    const server2 = createCommServer(tmpDir);

    const result = server2.mailbox('a2');
    assert.equal(result.length, 1);
    assert.equal(result[0].content, 'Persistent message');

    cleanup(tmpDir);
  });

  it('agent registrations survive restart', () => {
    server.registerAgent('a1', { name: 'Agent A1', model: 'opus' });
    server.registerAgent('a2', { name: 'Agent A2', model: 'sonnet' });

    const server2 = createCommServer(tmpDir);

    const agents = server2.listAgents();
    assert.equal(agents.length, 2);

    cleanup(tmpDir);
  });

  it('message status updates persist', () => {
    const { message_id } = server.send('a1', 'a2', 'Test');

    server.mailbox('a2'); // Marks as read

    const server2 = createCommServer(tmpDir);
    const unread = server2.mailbox('a2', { status: 'unread' });
    const read = server2.mailbox('a2', { status: 'read' });

    assert.equal(unread.length, 0);
    assert.equal(read.length, 1);

    cleanup(tmpDir);
  });

  it('acknowledgements persist', () => {
    const { message_id } = server.send('a1', 'a2', 'Test');
    server.acknowledge(message_id, 'Acknowledged');

    const server2 = createCommServer(tmpDir);
    const data = readTestJson(tmpDir, '.research/comm/messages.json');
    const msg = data.messages.find(m => m.message_id === message_id);

    assert.equal(msg.status, 'acknowledged');
    assert.equal(msg.response, 'Acknowledged');

    cleanup(tmpDir);
  });

  it('handles concurrent writes (last write wins)', () => {
    // This is a simplified test - real concurrent access would need locking
    const server2 = createCommServer(tmpDir);

    server.send('a1', 'a2', 'From server 1');
    server2.send('a3', 'a4', 'From server 2');

    // Both servers should see both messages after reload
    const server3 = createCommServer(tmpDir);
    const data = readTestJson(tmpDir, '.research/comm/messages.json');

    // Note: Without proper locking, one message might be lost
    // In production, use file locking or atomic operations
    assert.ok(data.messages.length >= 1);

    cleanup(tmpDir);
  });
});

// ===========================================================================
// 9. Integration: communication workflows
// ===========================================================================

describe('integration: communication workflows', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('complete agent coordination workflow', () => {
    // Step 1: Register agents
    server.registerAgent('i0', { name: 'ReviewPipelineOrchestrator', model: 'opus' });
    server.registerAgent('i1', { name: 'PaperRetrievalAgent', model: 'sonnet' });
    server.registerAgent('i2', { name: 'ScreeningAssistant', model: 'sonnet' });

    // Step 2: I0 broadcasts coordination message
    server.broadcast('i0', 'Starting systematic review pipeline');

    // Step 3: I0 sends task to I1
    server.send('i0', 'i1', 'Fetch papers from Semantic Scholar');

    // Step 4: I1 acknowledges task
    const i1Messages = server.mailbox('i1');
    assert.equal(i1Messages.length, 2); // Broadcast + direct message

    const taskMessage = i1Messages.find(m => m.from === 'i0' && !m.broadcast);
    server.acknowledge(taskMessage.message_id, 'Starting paper retrieval');

    // Step 5: I1 reports completion to I0
    server.send('i1', 'i0', 'Retrieved 150 papers');

    // Step 6: I0 receives completion report
    const i0Messages = server.mailbox('i0');
    assert.equal(i0Messages.length, 1);
    assert.ok(i0Messages[0].content.includes('Retrieved'));

    cleanup(tmpDir);
  });

  it('multi-agent parallel task coordination', () => {
    // Register parallel workers
    server.registerAgent('i0', { name: 'Orchestrator' });
    server.registerAgent('i1-ss', { name: 'Worker-SemanticScholar' });
    server.registerAgent('i1-oa', { name: 'Worker-OpenAlex' });
    server.registerAgent('i1-ar', { name: 'Worker-arXiv' });

    // I0 sends tasks to all workers
    server.send('i0', 'i1-ss', 'Fetch from Semantic Scholar');
    server.send('i0', 'i1-oa', 'Fetch from OpenAlex');
    server.send('i0', 'i1-ar', 'Fetch from arXiv');

    // Workers acknowledge
    server.mailbox('i1-ss');
    server.mailbox('i1-oa');
    server.mailbox('i1-ar');

    // Workers report back
    server.send('i1-ss', 'i0', 'Completed: 50 papers');
    server.send('i1-oa', 'i0', 'Completed: 75 papers');
    server.send('i1-ar', 'i0', 'Completed: 25 papers');

    // I0 receives all reports
    const reports = server.mailbox('i0');
    assert.equal(reports.length, 3);

    const totalPapers = reports.reduce((sum, msg) => {
      const match = msg.content.match(/(\d+) papers/);
      return sum + (match ? parseInt(match[1]) : 0);
    }, 0);

    assert.equal(totalPapers, 150);

    cleanup(tmpDir);
  });

  it('error notification and retry workflow', () => {
    server.registerAgent('i0', { name: 'Orchestrator' });
    server.registerAgent('i1', { name: 'Worker' });

    // Initial task
    server.send('i0', 'i1', 'Fetch papers', { attempt: 1 });

    // Worker reports error
    const tasks = server.mailbox('i1');
    server.send('i1', 'i0', 'ERROR: API rate limit exceeded', { error: true });

    // I0 receives error
    const errors = server.mailbox('i0');
    assert.ok(errors[0].content.includes('ERROR'));

    // I0 sends retry task
    server.send('i0', 'i1', 'Retry: Fetch papers', { attempt: 2, delay: 5000 });

    // Worker succeeds on retry
    const retries = server.mailbox('i1');
    assert.equal(retries[0].metadata.attempt, 2);
    server.send('i1', 'i0', 'SUCCESS: Retrieved 50 papers');

    cleanup(tmpDir);
  });

  it('checkpoint approval coordination', () => {
    server.registerAgent('orchestrator', { name: 'Orchestrator' });
    server.registerAgent('i1', { name: 'PaperRetrieval' });

    // I1 reaches checkpoint, asks orchestrator for approval
    server.send('i1', 'orchestrator', 'CHECKPOINT: SCH_DATABASE_SELECTION - Approve Semantic Scholar?', {
      checkpoint: 'SCH_DATABASE_SELECTION',
      requires_approval: true
    });

    // Orchestrator receives checkpoint request
    const checkpoints = server.mailbox('orchestrator');
    assert.equal(checkpoints[0].metadata.checkpoint, 'SCH_DATABASE_SELECTION');

    // Orchestrator approves
    server.send('orchestrator', 'i1', 'APPROVED: SCH_DATABASE_SELECTION', {
      checkpoint: 'SCH_DATABASE_SELECTION',
      approved: true
    });

    // I1 receives approval and continues
    const approvals = server.mailbox('i1');
    assert.equal(approvals[0].metadata.approved, true);

    cleanup(tmpDir);
  });

  it('broadcast with selective acknowledgement', () => {
    server.registerAgent('lead', { name: 'TeamLead' });
    server.registerAgent('a1', { name: 'Agent1' });
    server.registerAgent('a2', { name: 'Agent2' });
    server.registerAgent('a3', { name: 'Agent3' });

    // Lead broadcasts task
    server.broadcast('lead', 'All agents: Please report status', { requires_ack: true });

    // Only a1 and a3 acknowledge
    const a1Msgs = server.mailbox('a1');
    const a3Msgs = server.mailbox('a3');

    server.acknowledge(a1Msgs[0].message_id, 'Agent1: Ready');
    server.acknowledge(a3Msgs[0].message_id, 'Agent3: Ready');

    // a2 does not acknowledge (simulating failure)

    // Check which agents acknowledged
    const data = readTestJson(tmpDir, '.research/comm/messages.json');
    const acknowledged = data.messages.filter(m => m.status === 'acknowledged');
    const unacknowledged = data.messages.filter(m => m.status !== 'acknowledged');

    assert.equal(acknowledged.length, 2);
    assert.equal(unacknowledged.length, 1);

    cleanup(tmpDir);
  });
});

// ===========================================================================
// 10. Edge Cases
// ===========================================================================

describe('edge cases', () => {
  let tmpDir, server;

  beforeEach(() => {
    ({ tmpDir, server } = createTestContext());
  });

  it('handles empty mailbox for non-existent agent', () => {
    const result = server.mailbox('nonexistent');
    assert.deepEqual(result, []);
    cleanup(tmpDir);
  });

  it('handles duplicate agent registrations gracefully', () => {
    server.registerAgent('a1', { name: 'First' });
    server.registerAgent('a1', { name: 'Second' });

    const agents = server.listAgents();
    assert.equal(agents.length, 1);
    assert.equal(agents[0].name, 'Second'); // Latest registration

    cleanup(tmpDir);
  });

  it('handles very long message content', () => {
    const longContent = 'A'.repeat(10000);
    const result = server.send('a1', 'a2', longContent);

    assert.equal(result.sent, true);

    const messages = server.mailbox('a2');
    assert.equal(messages[0].content.length, 10000);

    cleanup(tmpDir);
  });

  it('handles special characters in message content', () => {
    const specialContent = 'Special: @#$%^&*() \n\t 한글 🎓 "quotes" \'apostrophes\'';
    server.send('a1', 'a2', specialContent);

    const messages = server.mailbox('a2');
    assert.equal(messages[0].content, specialContent);

    cleanup(tmpDir);
  });

  it('handles large number of messages', () => {
    for (let i = 0; i < 1000; i++) {
      server.send('a1', 'a2', `Message ${i}`);
    }

    const messages = server.mailbox('a2');
    assert.equal(messages.length, 1000);

    cleanup(tmpDir);
  });

  it('handles corrupted messages.json gracefully', () => {
    writeFileSync(join(tmpDir, '.research', 'comm', 'messages.json'), 'invalid json [', 'utf8');

    // Should not crash, should return empty or initialize fresh
    const result = server.mailbox('a1');
    assert.ok(Array.isArray(result));

    cleanup(tmpDir);
  });

  it('handles messages with missing fields', () => {
    writeTestJson(join(tmpDir, '.research', 'comm'), 'messages.json', {
      messages: [
        { message_id: 'msg_001', from: 'a1' } // Missing 'to', 'content', 'status'
      ]
    });

    const server2 = createCommServer(tmpDir);
    const result = server2.mailbox('a2');

    // Should handle gracefully, possibly skip malformed messages
    assert.ok(Array.isArray(result));

    cleanup(tmpDir);
  });
});
