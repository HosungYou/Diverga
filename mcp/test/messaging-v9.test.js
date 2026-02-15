import { describe, it, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { createMessaging } from '../lib/messaging.js';
import { createStateStore } from '../lib/sqlite-state.js';
import { mkdtemp, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

/**
 * TDD RED Tests for Diverga v9.0 Agent Messaging System
 *
 * Tests MCP-based agent-to-agent messaging for pipeline coordination.
 * Currently FAILING - messaging.js does not exist yet.
 */

// Test helper to create isolated context
async function createTestContext() {
  const tempDir = await mkdtemp(join(tmpdir(), 'messaging-test-'));
  const dbPath = join(tempDir, 'test.db');
  const store = await createStateStore(dbPath);
  const messaging = createMessaging(store);

  return { tempDir, dbPath, store, messaging };
}

async function cleanup(context) {
  await context.store.close();
  await rm(context.tempDir, { recursive: true, force: true });
}

// ============================================================================
// Suite 1: Agent Registration (~6 tests)
// ============================================================================

describe('Agent Registration', () => {
  let ctx;

  before(async () => {
    ctx = await createTestContext();
  });

  after(async () => {
    await cleanup(ctx);
  });

  it('should register agent with metadata', async () => {
    const result = await ctx.messaging.registerAgent('i1-ss', {
      role: 'fetcher',
      model: 'haiku',
      capabilities: ['semantic-scholar']
    });

    assert.ok(result);
    assert.equal(result.agentId, 'i1-ss');
    assert.equal(result.role, 'fetcher');
  });

  it('should list all registered agents', async () => {
    await ctx.messaging.registerAgent('i1-ss', { role: 'fetcher' });
    await ctx.messaging.registerAgent('i2-screen', { role: 'screener' });

    const agents = await ctx.messaging.listAgents();

    assert.equal(agents.length, 2);
    assert.ok(agents.find(a => a.agentId === 'i1-ss'));
    assert.ok(agents.find(a => a.agentId === 'i2-screen'));
  });

  it('should get single agent by ID', async () => {
    await ctx.messaging.registerAgent('i1-oa', { role: 'fetcher', model: 'haiku' });

    const agent = await ctx.messaging.getAgent('i1-oa');

    assert.ok(agent);
    assert.equal(agent.agentId, 'i1-oa');
    assert.equal(agent.role, 'fetcher');
    assert.equal(agent.model, 'haiku');
  });

  it('should return null for non-existent agent', async () => {
    const agent = await ctx.messaging.getAgent('non-existent');

    assert.equal(agent, null);
  });

  it('should unregister agent', async () => {
    await ctx.messaging.registerAgent('temp-agent', { role: 'temp' });

    const removed = await ctx.messaging.unregisterAgent('temp-agent');

    assert.ok(removed);

    const agent = await ctx.messaging.getAgent('temp-agent');
    assert.equal(agent, null);
  });

  it('should update metadata on duplicate registration', async () => {
    await ctx.messaging.registerAgent('i1-arxiv', {
      role: 'fetcher',
      model: 'haiku'
    });

    await ctx.messaging.registerAgent('i1-arxiv', {
      role: 'fetcher',
      model: 'sonnet',
      capabilities: ['arxiv-api']
    });

    const agent = await ctx.messaging.getAgent('i1-arxiv');

    assert.equal(agent.model, 'sonnet');
    assert.deepEqual(agent.capabilities, ['arxiv-api']);
  });
});

// ============================================================================
// Suite 2: Direct Messaging (~8 tests)
// ============================================================================

describe('Direct Messaging', () => {
  let ctx;

  before(async () => {
    ctx = await createTestContext();
    await ctx.messaging.registerAgent('i0-orchestrator', { role: 'orchestrator' });
    await ctx.messaging.registerAgent('i1-ss', { role: 'fetcher' });
  });

  after(async () => {
    await cleanup(ctx);
  });

  it('should send message and return messageId', async () => {
    const messageId = await ctx.messaging.send(
      'i0-orchestrator',
      'i1-ss',
      'Start fetching papers from Semantic Scholar'
    );

    assert.ok(messageId);
    assert.equal(typeof messageId, 'string');
    assert.ok(messageId.length > 0);
  });

  it('should store message with metadata', async () => {
    const messageId = await ctx.messaging.send(
      'i0-orchestrator',
      'i1-ss',
      'Fetch papers',
      { type: 'data', priority: 'high' }
    );

    const mailbox = await ctx.messaging.mailbox('i1-ss');
    const msg = mailbox.find(m => m.messageId === messageId);

    assert.ok(msg);
    assert.equal(msg.from, 'i0-orchestrator');
    assert.equal(msg.to, 'i1-ss');
    assert.equal(msg.content, 'Fetch papers');
    assert.equal(msg.type, 'data');
    assert.equal(msg.priority, 'high');
    assert.ok(msg.timestamp);
  });

  it('should throw error when sending to non-existent agent', async () => {
    await assert.rejects(
      async () => {
        await ctx.messaging.send('i0-orchestrator', 'non-existent', 'Test');
      },
      { message: /Agent .* not found/ }
    );
  });

  it('should allow sending from unregistered agent (anonymous)', async () => {
    const messageId = await ctx.messaging.send(
      'unknown-agent',
      'i1-ss',
      'Anonymous message'
    );

    assert.ok(messageId);

    const mailbox = await ctx.messaging.mailbox('i1-ss');
    const msg = mailbox.find(m => m.messageId === messageId);

    assert.equal(msg.from, 'unknown-agent');
  });

  it('should support message types', async () => {
    const types = ['data', 'status', 'checkpoint', 'error'];

    for (const type of types) {
      const messageId = await ctx.messaging.send(
        'i0-orchestrator',
        'i1-ss',
        `Message of type ${type}`,
        { type }
      );

      const mailbox = await ctx.messaging.mailbox('i1-ss', { type });
      const msg = mailbox.find(m => m.messageId === messageId);

      assert.equal(msg.type, type);
    }
  });

  it('should support priority levels', async () => {
    const priorities = ['low', 'normal', 'high', 'urgent'];

    for (const priority of priorities) {
      const messageId = await ctx.messaging.send(
        'i0-orchestrator',
        'i1-ss',
        `Priority: ${priority}`,
        { priority }
      );

      const mailbox = await ctx.messaging.mailbox('i1-ss');
      const msg = mailbox.find(m => m.messageId === messageId);

      assert.equal(msg.priority, priority);
    }
  });

  it('should default to normal priority', async () => {
    const messageId = await ctx.messaging.send(
      'i0-orchestrator',
      'i1-ss',
      'Default priority'
    );

    const mailbox = await ctx.messaging.mailbox('i1-ss');
    const msg = mailbox.find(m => m.messageId === messageId);

    assert.equal(msg.priority, 'normal');
  });

  it('should handle object content (JSON serialization)', async () => {
    const content = {
      query: 'machine learning',
      databases: ['semantic-scholar', 'openalex'],
      yearRange: [2020, 2024]
    };

    const messageId = await ctx.messaging.send(
      'i0-orchestrator',
      'i1-ss',
      content,
      { type: 'data' }
    );

    const mailbox = await ctx.messaging.mailbox('i1-ss');
    const msg = mailbox.find(m => m.messageId === messageId);

    assert.deepEqual(msg.content, content);
  });
});

// ============================================================================
// Suite 3: Mailbox (~8 tests)
// ============================================================================

describe('Mailbox', () => {
  let ctx;

  before(async () => {
    ctx = await createTestContext();
    await ctx.messaging.registerAgent('i1-ss', { role: 'fetcher' });
    await ctx.messaging.registerAgent('i0-orchestrator', { role: 'orchestrator' });
  });

  after(async () => {
    await cleanup(ctx);
  });

  it('should return unread messages by default', async () => {
    await ctx.messaging.send('i0-orchestrator', 'i1-ss', 'Message 1');
    await ctx.messaging.send('i0-orchestrator', 'i1-ss', 'Message 2');

    const mailbox = await ctx.messaging.mailbox('i1-ss');

    assert.equal(mailbox.length, 2);
    assert.ok(mailbox.every(m => m.delivered === false));
  });

  it('should include read messages with option', async () => {
    await ctx.messaging.send('i0-orchestrator', 'i1-ss', 'Message 3');

    // First read marks as delivered
    await ctx.messaging.mailbox('i1-ss');

    // Second read with includeRead
    const allMessages = await ctx.messaging.mailbox('i1-ss', { includeRead: true });

    assert.ok(allMessages.length >= 1);
    assert.ok(allMessages.some(m => m.delivered === true));
  });

  it('should filter by message type', async () => {
    await ctx.messaging.send('i0-orchestrator', 'i1-ss', 'Data msg', { type: 'data' });
    await ctx.messaging.send('i0-orchestrator', 'i1-ss', 'Status msg', { type: 'status' });
    await ctx.messaging.send('i0-orchestrator', 'i1-ss', 'Checkpoint msg', { type: 'checkpoint' });

    const checkpointMessages = await ctx.messaging.mailbox('i1-ss', { type: 'checkpoint' });

    assert.equal(checkpointMessages.length, 1);
    assert.equal(checkpointMessages[0].type, 'checkpoint');
    assert.equal(checkpointMessages[0].content, 'Checkpoint msg');
  });

  it('should mark messages as delivered after reading', async () => {
    const messageId = await ctx.messaging.send('i0-orchestrator', 'i1-ss', 'Test delivery');

    // First read
    const unread = await ctx.messaging.mailbox('i1-ss');
    assert.ok(unread.some(m => m.messageId === messageId));

    // Second read (should be empty without includeRead)
    const empty = await ctx.messaging.mailbox('i1-ss');
    assert.ok(!empty.some(m => m.messageId === messageId));

    // Check with includeRead
    const all = await ctx.messaging.mailbox('i1-ss', { includeRead: true });
    const deliveredMsg = all.find(m => m.messageId === messageId);
    assert.equal(deliveredMsg.delivered, true);
  });

  it('should acknowledge messages', async () => {
    const messageId = await ctx.messaging.send('i0-orchestrator', 'i1-ss', 'Ack test');

    const ackResult = await ctx.messaging.acknowledge(messageId);

    assert.ok(ackResult);

    const all = await ctx.messaging.mailbox('i1-ss', { includeRead: true });
    const msg = all.find(m => m.messageId === messageId);
    assert.equal(msg.acknowledged, true);
    assert.ok(msg.acknowledgedAt);
  });

  it('should return empty array for empty mailbox', async () => {
    await ctx.messaging.registerAgent('i2-screen', { role: 'screener' });

    const mailbox = await ctx.messaging.mailbox('i2-screen');

    assert.deepEqual(mailbox, []);
  });

  it('should order messages by timestamp (oldest first)', async () => {
    await ctx.messaging.send('i0-orchestrator', 'i1-ss', 'First');
    await new Promise(resolve => setTimeout(resolve, 10)); // Small delay
    await ctx.messaging.send('i0-orchestrator', 'i1-ss', 'Second');
    await new Promise(resolve => setTimeout(resolve, 10));
    await ctx.messaging.send('i0-orchestrator', 'i1-ss', 'Third');

    const mailbox = await ctx.messaging.mailbox('i1-ss');

    assert.equal(mailbox[0].content, 'First');
    assert.equal(mailbox[1].content, 'Second');
    assert.equal(mailbox[2].content, 'Third');

    // Verify timestamps are ascending
    assert.ok(mailbox[0].timestamp <= mailbox[1].timestamp);
    assert.ok(mailbox[1].timestamp <= mailbox[2].timestamp);
  });

  it('should return empty array for non-existent agent mailbox', async () => {
    const mailbox = await ctx.messaging.mailbox('non-existent-agent');

    assert.deepEqual(mailbox, []);
  });
});

// ============================================================================
// Suite 4: Broadcast (~6 tests)
// ============================================================================

describe('Broadcast', () => {
  let ctx;

  before(async () => {
    ctx = await createTestContext();
    await ctx.messaging.registerAgent('i0-orchestrator', { role: 'orchestrator' });
    await ctx.messaging.registerAgent('i1-ss', { role: 'fetcher' });
    await ctx.messaging.registerAgent('i1-oa', { role: 'fetcher' });
    await ctx.messaging.registerAgent('i1-arxiv', { role: 'fetcher' });
    await ctx.messaging.registerAgent('i2-screen', { role: 'screener' });
  });

  after(async () => {
    await cleanup(ctx);
  });

  it('should broadcast to all agents', async () => {
    const messageIds = await ctx.messaging.broadcast(
      'i0-orchestrator',
      'Pipeline started'
    );

    // 4 recipients (excludeSelf=true by default)
    assert.equal(messageIds.length, 4);
    assert.ok(Array.isArray(messageIds));
    assert.ok(messageIds.every(id => typeof id === 'string'));
  });

  it('should exclude self by default', async () => {
    await ctx.messaging.broadcast('i0-orchestrator', 'Broadcast test');

    const mailbox = await ctx.messaging.mailbox('i0-orchestrator');

    assert.equal(mailbox.length, 0);
  });

  it('should include self when excludeSelf=false', async () => {
    await ctx.messaging.broadcast(
      'i0-orchestrator',
      'Include self test',
      { excludeSelf: false }
    );

    const mailbox = await ctx.messaging.mailbox('i0-orchestrator');

    assert.equal(mailbox.length, 1);
    assert.equal(mailbox[0].content, 'Include self test');
  });

  it('should return empty array for empty agent registry', async () => {
    const freshCtx = await createTestContext();

    const messageIds = await freshCtx.messaging.broadcast(
      'unknown',
      'No agents'
    );

    assert.deepEqual(messageIds, []);

    await cleanup(freshCtx);
  });

  it('should support message type in broadcast', async () => {
    await ctx.messaging.broadcast(
      'i0-orchestrator',
      'Status broadcast',
      { type: 'status' }
    );

    const mailbox = await ctx.messaging.mailbox('i1-ss', { type: 'status' });

    assert.ok(mailbox.length > 0);
    assert.equal(mailbox[0].type, 'status');
  });

  it('should filter broadcast by agent roles', async () => {
    const messageIds = await ctx.messaging.broadcast(
      'i0-orchestrator',
      'Fetchers only',
      { roles: ['fetcher'] }
    );

    // 3 fetchers: i1-ss, i1-oa, i1-arxiv
    assert.equal(messageIds.length, 3);

    // Verify screener didn't receive
    const screenerMailbox = await ctx.messaging.mailbox('i2-screen');
    assert.ok(!screenerMailbox.some(m => m.content === 'Fetchers only'));

    // Verify fetchers received
    const fetcherMailbox = await ctx.messaging.mailbox('i1-ss');
    assert.ok(fetcherMailbox.some(m => m.content === 'Fetchers only'));
  });
});

// ============================================================================
// Suite 5: Pipeline Coordination (~8 tests)
// ============================================================================

describe('Pipeline Coordination', () => {
  let ctx;

  before(async () => {
    ctx = await createTestContext();
    await ctx.messaging.registerAgent('i0-orchestrator', { role: 'orchestrator' });
    await ctx.messaging.registerAgent('i1-ss', { role: 'fetcher' });
    await ctx.messaging.registerAgent('i1-oa', { role: 'fetcher' });
    await ctx.messaging.registerAgent('i1-arxiv', { role: 'fetcher' });
  });

  after(async () => {
    await cleanup(ctx);
  });

  it('should create named channel', async () => {
    const channel = await ctx.messaging.createChannel(
      'scholarag-pipeline',
      ['i1-ss', 'i1-oa', 'i1-arxiv']
    );

    assert.ok(channel);
    assert.equal(channel.name, 'scholarag-pipeline');
    assert.deepEqual(channel.members, ['i1-ss', 'i1-oa', 'i1-arxiv']);
  });

  it('should send to channel members', async () => {
    await ctx.messaging.createChannel(
      'test-channel',
      ['i1-ss', 'i1-oa']
    );

    const messageIds = await ctx.messaging.sendToChannel(
      'test-channel',
      'i0-orchestrator',
      'Start fetching'
    );

    assert.equal(messageIds.length, 2);

    const ssMailbox = await ctx.messaging.mailbox('i1-ss');
    const oaMailbox = await ctx.messaging.mailbox('i1-oa');

    assert.ok(ssMailbox.some(m => m.content === 'Start fetching'));
    assert.ok(oaMailbox.some(m => m.content === 'Start fetching'));
  });

  it('should get channel message history', async () => {
    await ctx.messaging.createChannel('history-test', ['i1-ss']);

    await ctx.messaging.sendToChannel('history-test', 'i0-orchestrator', 'Msg 1');
    await ctx.messaging.sendToChannel('history-test', 'i0-orchestrator', 'Msg 2');

    const history = await ctx.messaging.getChannelMessages('history-test');

    assert.equal(history.length, 2);
    assert.equal(history[0].content, 'Msg 1');
    assert.equal(history[1].content, 'Msg 2');
  });

  it('should support pipeline pattern (I0→I1s)', async () => {
    await ctx.messaging.createChannel(
      'scholarag-pipeline',
      ['i1-ss', 'i1-oa', 'i1-arxiv']
    );

    // I0 orchestrates fetching
    await ctx.messaging.sendToChannel(
      'scholarag-pipeline',
      'i0-orchestrator',
      {
        query: 'machine learning education',
        yearRange: [2020, 2024]
      },
      { type: 'data' }
    );

    // All fetchers receive
    for (const fetcher of ['i1-ss', 'i1-oa', 'i1-arxiv']) {
      const mailbox = await ctx.messaging.mailbox(fetcher, { type: 'data' });
      assert.ok(mailbox.length > 0);
      assert.equal(mailbox[0].content.query, 'machine learning education');
    }
  });

  it('should report progress', async () => {
    const progressId = await ctx.messaging.reportProgress('i1-ss', {
      stage: 'fetching',
      percent: 45,
      detail: 'Retrieved 450/1000 papers'
    });

    assert.ok(progressId);

    // Progress is a special message type
    const mailbox = await ctx.messaging.mailbox('i0-orchestrator', { type: 'progress' });
    const progressMsg = mailbox.find(m => m.messageId === progressId);

    assert.ok(progressMsg);
    assert.equal(progressMsg.content.percent, 45);
    assert.equal(progressMsg.content.detail, 'Retrieved 450/1000 papers');
  });

  it('should get progress for channel members', async () => {
    await ctx.messaging.createChannel('progress-test', ['i1-ss', 'i1-oa']);

    await ctx.messaging.reportProgress('i1-ss', {
      stage: 'fetching',
      percent: 60
    });

    await ctx.messaging.reportProgress('i1-oa', {
      stage: 'fetching',
      percent: 40
    });

    const progress = await ctx.messaging.getProgress('progress-test');

    assert.equal(progress.length, 2);
    assert.ok(progress.some(p => p.agentId === 'i1-ss' && p.percent === 60));
    assert.ok(progress.some(p => p.agentId === 'i1-oa' && p.percent === 40));
  });

  it('should add/remove channel members dynamically', async () => {
    await ctx.messaging.createChannel('dynamic-channel', ['i1-ss']);

    await ctx.messaging.addChannelMember('dynamic-channel', 'i1-oa');

    const channel = await ctx.messaging.getChannel('dynamic-channel');
    assert.ok(channel.members.includes('i1-oa'));

    await ctx.messaging.removeChannelMember('dynamic-channel', 'i1-ss');

    const updated = await ctx.messaging.getChannel('dynamic-channel');
    assert.ok(!updated.members.includes('i1-ss'));
    assert.ok(updated.members.includes('i1-oa'));
  });

  it('should archive messages when closing channel', async () => {
    await ctx.messaging.createChannel('close-test', ['i1-ss']);
    await ctx.messaging.sendToChannel('close-test', 'i0-orchestrator', 'Test msg');

    await ctx.messaging.closeChannel('close-test');

    const channel = await ctx.messaging.getChannel('close-test');
    assert.equal(channel.status, 'closed');

    // Messages still accessible
    const history = await ctx.messaging.getChannelMessages('close-test');
    assert.equal(history.length, 1);
  });
});

// ============================================================================
// Suite 6: Persistence & Reliability (~5 tests)
// ============================================================================

describe('Persistence & Reliability', () => {
  let tempDir;
  let dbPath;

  before(async () => {
    tempDir = await mkdtemp(join(tmpdir(), 'messaging-persist-'));
    dbPath = join(tempDir, 'persist.db');
  });

  after(async () => {
    await rm(tempDir, { recursive: true, force: true });
  });

  it('should persist messages across messaging instances', async () => {
    // First instance
    const store1 = await createStateStore(dbPath);
    const msg1 = createMessaging(store1);

    await msg1.registerAgent('i1-ss', { role: 'fetcher' });
    await msg1.send('system', 'i1-ss', 'Persistent message');

    await store1.close();

    // Second instance (same DB)
    const store2 = await createStateStore(dbPath);
    const msg2 = createMessaging(store2);

    const mailbox = await msg2.mailbox('i1-ss');

    assert.equal(mailbox.length, 1);
    assert.equal(mailbox[0].content, 'Persistent message');

    await store2.close();
  });

  it('should preserve undelivered messages across agent restart', async () => {
    const store = await createStateStore(dbPath);
    const msg = createMessaging(store);

    await msg.registerAgent('i1-oa', { role: 'fetcher' });
    await msg.send('system', 'i1-oa', 'Undelivered 1');
    await msg.send('system', 'i1-oa', 'Undelivered 2');

    // Agent "restarts" (we just query again without reading)
    const mailbox = await msg.mailbox('i1-oa');

    assert.equal(mailbox.length, 2);

    await store.close();
  });

  it('should query message history with filters', async () => {
    const store = await createStateStore(dbPath);
    const msg = createMessaging(store);

    await msg.registerAgent('i0', { role: 'orchestrator' });
    await msg.registerAgent('i1', { role: 'fetcher' });

    const now = Date.now();

    await msg.send('i0', 'i1', 'Old message');
    await new Promise(resolve => setTimeout(resolve, 100));
    await msg.send('i0', 'i1', 'Recent message');

    // Query: from i0, since timestamp
    const history = await msg.history({
      from: 'i0',
      since: now + 50,
      limit: 10
    });

    assert.equal(history.length, 1);
    assert.equal(history[0].content, 'Recent message');

    await store.close();
  });

  it('should handle large message content (>10KB)', async () => {
    const store = await createStateStore(dbPath);
    const msg = createMessaging(store);

    await msg.registerAgent('i1-ss', { role: 'fetcher' });

    const largeContent = {
      papers: Array.from({ length: 1000 }, (_, i) => ({
        title: `Paper ${i}`,
        abstract: 'A'.repeat(500), // 500 chars each
        authors: ['Author 1', 'Author 2']
      }))
    };

    const contentSize = JSON.stringify(largeContent).length;
    assert.ok(contentSize > 10000, 'Content should be >10KB');

    const messageId = await msg.send('system', 'i1-ss', largeContent);

    const mailbox = await msg.mailbox('i1-ss');
    const retrieved = mailbox.find(m => m.messageId === messageId);

    assert.ok(retrieved);
    assert.equal(retrieved.content.papers.length, 1000);
    assert.equal(retrieved.content.papers[0].abstract.length, 500);

    await store.close();
  });

  it('should preserve special characters in content', async () => {
    const store = await createStateStore(dbPath);
    const msg = createMessaging(store);

    await msg.registerAgent('i1-test', { role: 'test' });

    const specialContent = {
      query: 'machine learning "deep neural networks" (2020-2024)',
      unicode: '한글 测试 العربية 🚀',
      escapes: 'Quotes: \' " \n Backslash: \\ Tab: \t'
    };

    await msg.send('system', 'i1-test', specialContent);

    const mailbox = await msg.mailbox('i1-test');

    assert.equal(mailbox[0].content.query, specialContent.query);
    assert.equal(mailbox[0].content.unicode, specialContent.unicode);
    assert.equal(mailbox[0].content.escapes, specialContent.escapes);

    await store.close();
  });
});

// ============================================================================
// Suite 7: Checkpoint Relay (~4 tests)
// ============================================================================

describe('Checkpoint Relay', () => {
  let ctx;

  before(async () => {
    ctx = await createTestContext();
    await ctx.messaging.registerAgent('i0-orchestrator', { role: 'orchestrator' });
    await ctx.messaging.registerAgent('i1-ss', { role: 'fetcher' });
    await ctx.messaging.registerAgent('i1-oa', { role: 'fetcher' });
    await ctx.messaging.registerAgent('i2-screen', { role: 'screener' });
  });

  after(async () => {
    await cleanup(ctx);
  });

  it('should relay checkpoint decision to agents', async () => {
    const messageIds = await ctx.messaging.relayCheckpoint(
      'SCH_DATABASE_SELECTION',
      'approved',
      'i0-orchestrator',
      ['i1-ss', 'i1-oa']
    );

    assert.equal(messageIds.length, 2);

    const ssMailbox = await ctx.messaging.mailbox('i1-ss', { type: 'checkpoint' });

    assert.equal(ssMailbox.length, 1);
    assert.equal(ssMailbox[0].content.checkpointId, 'SCH_DATABASE_SELECTION');
    assert.equal(ssMailbox[0].content.decision, 'approved');
  });

  it('should use high priority for checkpoint messages', async () => {
    await ctx.messaging.relayCheckpoint(
      'SCH_SCREENING_CRITERIA',
      'approved',
      'i0-orchestrator',
      ['i2-screen']
    );

    const mailbox = await ctx.messaging.mailbox('i2-screen');
    const checkpointMsg = mailbox.find(m => m.type === 'checkpoint');

    assert.equal(checkpointMsg.priority, 'high');
  });

  it('should await checkpoint message', async () => {
    // Send checkpoint in background
    setTimeout(async () => {
      await ctx.messaging.relayCheckpoint(
        'SCH_RAG_READINESS',
        'approved',
        'i0-orchestrator',
        ['i1-ss']
      );
    }, 100);

    // Await it
    const result = await ctx.messaging.awaitCheckpoint(
      'i1-ss',
      'SCH_RAG_READINESS',
      2000 // 2 second timeout
    );

    assert.ok(result);
    assert.equal(result.checkpointId, 'SCH_RAG_READINESS');
    assert.equal(result.decision, 'approved');
  });

  it('should return null on timeout', async () => {
    const result = await ctx.messaging.awaitCheckpoint(
      'i1-ss',
      'NON_EXISTENT_CHECKPOINT',
      100 // 100ms timeout
    );

    assert.equal(result, null);
  });
});

// ============================================================================
// Summary
// ============================================================================

/**
 * Test Summary:
 *
 * Suite 1: Agent Registration (6 tests)
 * Suite 2: Direct Messaging (8 tests)
 * Suite 3: Mailbox (8 tests)
 * Suite 4: Broadcast (6 tests)
 * Suite 5: Pipeline Coordination (8 tests)
 * Suite 6: Persistence & Reliability (5 tests)
 * Suite 7: Checkpoint Relay (4 tests)
 *
 * Total: 45 tests
 *
 * Current Status: RED (failing)
 * Reason: mcp/lib/messaging.js does not exist
 *
 * Next Step: Implement messaging.js to make these tests pass (GREEN)
 */
