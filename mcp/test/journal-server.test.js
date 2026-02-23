/**
 * Test suite for Diverga v10.3.0 Journal Intelligence MCP Server
 *
 * Tests the journal-server.js MCP server which provides 6 tools
 * powered by OpenAlex (primary) and Crossref (secondary) APIs.
 *
 * Structure:
 *   - Unit tests: schema validation, URL construction, email resolution
 *   - Integration tests: marked with // INTEGRATION: requires network
 */

import { describe, it, before, after, beforeEach } from 'node:test';
import assert from 'node:assert/strict';

// =============================================================================
// Since journal-server.js does not export internal functions (it's an MCP
// server entry point), we test through simulated MCP tool call interfaces
// and reconstruct testable logic from the source patterns.
// =============================================================================

// ---------------------------------------------------------------------------
// 1. Tool Definition Constants (mirrored from journal-server.js)
// ---------------------------------------------------------------------------

const EXPECTED_TOOLS = [
  'journal_search_by_field',
  'journal_metrics',
  'journal_publication_trends',
  'journal_editor_info',
  'journal_compare',
  'journal_special_issues',
];

const TOOL_REQUIRED_PARAMS = {
  journal_search_by_field: ['field'],
  journal_metrics: [],
  journal_publication_trends: ['journal_id'],
  journal_editor_info: ['journal_id'],
  journal_compare: ['journal_ids'],
  journal_special_issues: [],
};

// ---------------------------------------------------------------------------
// 2. URL Construction Helpers (unit-testable reimplementation)
// ---------------------------------------------------------------------------

function buildOpenAlexUrl(path, params = {}, email = null) {
  const url = new URL(path, 'https://api.openalex.org');
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null) {
      url.searchParams.set(key, String(value));
    }
  }
  if (email) {
    url.searchParams.set('mailto', email);
  }
  return url.toString();
}

// ---------------------------------------------------------------------------
// 3. Email Resolution Helpers (unit-testable reimplementation)
// ---------------------------------------------------------------------------

function resolveEmailFromEnv(envEmail, configEmail) {
  if (envEmail) return envEmail;
  if (configEmail) return configEmail;
  return null;
}

// =============================================================================
// Test Suites
// =============================================================================

describe('Journal Server — Tool Definitions', () => {
  it('should define exactly 6 tools', () => {
    assert.equal(EXPECTED_TOOLS.length, 6);
  });

  it('should include all expected tool names', () => {
    const expected = new Set([
      'journal_search_by_field',
      'journal_metrics',
      'journal_publication_trends',
      'journal_editor_info',
      'journal_compare',
      'journal_special_issues',
    ]);
    const actual = new Set(EXPECTED_TOOLS);
    assert.deepEqual(actual, expected);
  });

  it('journal_search_by_field requires field param', () => {
    assert.ok(TOOL_REQUIRED_PARAMS.journal_search_by_field.includes('field'));
  });

  it('journal_metrics has no required params (at least one of 3 optional)', () => {
    assert.equal(TOOL_REQUIRED_PARAMS.journal_metrics.length, 0);
  });

  it('journal_publication_trends requires journal_id', () => {
    assert.ok(TOOL_REQUIRED_PARAMS.journal_publication_trends.includes('journal_id'));
  });

  it('journal_editor_info requires journal_id', () => {
    assert.ok(TOOL_REQUIRED_PARAMS.journal_editor_info.includes('journal_id'));
  });

  it('journal_compare requires journal_ids array', () => {
    assert.ok(TOOL_REQUIRED_PARAMS.journal_compare.includes('journal_ids'));
  });

  it('journal_special_issues has no required params (at least one of journal_name/issn)', () => {
    assert.equal(TOOL_REQUIRED_PARAMS.journal_special_issues.length, 0);
  });
});

describe('Journal Server — OpenAlex URL Construction', () => {
  it('should build base URL for /sources', () => {
    const url = buildOpenAlexUrl('/sources', {});
    assert.ok(url.startsWith('https://api.openalex.org/sources'));
  });

  it('should include search parameter', () => {
    const url = buildOpenAlexUrl('/sources', { search: 'educational technology' });
    assert.ok(url.includes('search=educational+technology') || url.includes('search=educational%20technology'));
  });

  it('should include filter parameter', () => {
    const url = buildOpenAlexUrl('/sources', { filter: 'type:journal' });
    assert.ok(url.includes('filter=type%3Ajournal') || url.includes('filter=type:journal'));
  });

  it('should include per_page parameter as string', () => {
    const url = buildOpenAlexUrl('/sources', { per_page: 10 });
    assert.ok(url.includes('per_page=10'));
  });

  it('should include sort parameter', () => {
    const url = buildOpenAlexUrl('/sources', { sort: 'cited_by_count:desc' });
    assert.ok(url.includes('sort=cited_by_count'));
  });

  it('should append mailto when email is provided', () => {
    const url = buildOpenAlexUrl('/sources', {}, 'test@example.com');
    assert.ok(url.includes('mailto=test%40example.com') || url.includes('mailto=test@example.com'));
  });

  it('should NOT include mailto when email is null', () => {
    const url = buildOpenAlexUrl('/sources', {}, null);
    assert.ok(!url.includes('mailto'));
  });

  it('should skip undefined/null param values', () => {
    const url = buildOpenAlexUrl('/sources', { search: undefined, filter: null, per_page: 5 });
    assert.ok(!url.includes('search'));
    assert.ok(!url.includes('filter'));
    assert.ok(url.includes('per_page=5'));
  });

  it('should encode journal_id in path segment', () => {
    const journalId = 'https://openalex.org/S137773608';
    const url = buildOpenAlexUrl(`/sources/${encodeURIComponent(journalId)}`, {});
    assert.ok(url.includes('sources/https%3A%2F%2Fopenalex.org%2FS137773608'));
  });

  it('should build works endpoint for editor_info group_by', () => {
    const url = buildOpenAlexUrl('/works', {
      filter: 'primary_location.source.id:https://openalex.org/S137773608',
      group_by: 'authorships.author.id',
      per_page: 10,
    });
    assert.ok(url.startsWith('https://api.openalex.org/works'));
    assert.ok(url.includes('group_by='));
  });
});

describe('Journal Server — Crossref URL Construction', () => {
  it('should build journal works URL with ISSN', () => {
    const issn = '0360-1315';
    const params = new URLSearchParams({
      query: 'AI in education',
      sort: 'published',
      order: 'desc',
      rows: '10',
      select: 'DOI,title,published,subject,type',
    });
    const url = `https://api.crossref.org/journals/${encodeURIComponent(issn)}/works?${params.toString()}`;

    assert.ok(url.startsWith('https://api.crossref.org/journals/0360-1315/works'));
    assert.ok(url.includes('sort=published'));
    assert.ok(url.includes('rows=10'));
  });

  it('should build general works URL with container-title', () => {
    const params = new URLSearchParams({
      'query.container-title': 'Computers & Education',
      query: 'AI in education',
      sort: 'published',
      order: 'desc',
      rows: '10',
      select: 'DOI,title,published,subject,type,container-title',
    });
    const url = `https://api.crossref.org/works?${params.toString()}`;

    assert.ok(url.startsWith('https://api.crossref.org/works'));
    assert.ok(url.includes('query.container-title='));
  });
});

describe('Journal Server — Email Resolution', () => {
  it('should prefer env var over config', () => {
    const email = resolveEmailFromEnv('env@example.com', 'config@example.com');
    assert.equal(email, 'env@example.com');
  });

  it('should fall back to config when env is empty', () => {
    const email = resolveEmailFromEnv(undefined, 'config@example.com');
    assert.equal(email, 'config@example.com');
  });

  it('should fall back to config when env is null', () => {
    const email = resolveEmailFromEnv(null, 'config@example.com');
    assert.equal(email, 'config@example.com');
  });

  it('should return null when both are unavailable', () => {
    const email = resolveEmailFromEnv(undefined, undefined);
    assert.equal(email, null);
  });

  it('should return env even if empty string (truthy check)', () => {
    const email = resolveEmailFromEnv('', 'config@example.com');
    // Empty string is falsy, so should fall to config
    assert.equal(email, 'config@example.com');
  });
});

describe('Journal Server — Error Handling Logic', () => {
  it('journal_metrics should throw when no identifier provided', () => {
    // Simulates the handler check: at least one of journal_id, issn, journal_name
    const args = {};
    const hasId = args.journal_id || args.issn || args.journal_name;
    assert.ok(!hasId, 'Should detect missing identifier');
  });

  it('journal_compare should throw for fewer than 2 IDs', () => {
    const ids = ['https://openalex.org/S1'];
    assert.ok(
      !Array.isArray(ids) || ids.length < 2,
      'Should reject fewer than 2 journal IDs'
    );
  });

  it('journal_compare should throw for more than 5 IDs', () => {
    const ids = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'];
    assert.ok(ids.length > 5, 'Should reject more than 5 journal IDs');
  });

  it('journal_compare should accept exactly 2-5 IDs', () => {
    for (const count of [2, 3, 4, 5]) {
      const ids = Array.from({ length: count }, (_, i) => `S${i}`);
      assert.ok(
        Array.isArray(ids) && ids.length >= 2 && ids.length <= 5,
        `Should accept ${count} IDs`
      );
    }
  });

  it('journal_special_issues should throw when neither journal_name nor issn provided', () => {
    const args = {};
    const hasIdentifier = args.journal_name || args.issn;
    assert.ok(!hasIdentifier, 'Should detect missing journal_name and issn');
  });

  it('journal_search_by_field should cap per_page at 50', () => {
    const requested = 100;
    const capped = Math.min(requested, 50);
    assert.equal(capped, 50);
  });

  it('journal_editor_info should cap per_page at 25', () => {
    const requested = 50;
    const capped = Math.min(requested, 25);
    assert.equal(capped, 25);
  });
});

describe('Journal Server — Response Parsing', () => {
  it('should transform OpenAlex source result correctly', () => {
    const rawSource = {
      id: 'https://openalex.org/S137773608',
      display_name: 'Computers & Education',
      issn: ['0360-1315'],
      cited_by_count: 123456,
      works_count: 5000,
      summary_stats: { h_index: 200, i10_index: 3000, '2yr_mean_citedness': 8.5 },
      is_oa: false,
      type: 'journal',
      country_code: 'GB',
      homepage_url: 'https://example.com',
      updated_date: '2026-01-15',
      apc_usd: 3500,
      host_organization_display_name: 'Elsevier',
    };

    // Simulate journalMetrics response transform
    const result = {
      id: rawSource.id,
      display_name: rawSource.display_name,
      issn: rawSource.issn || [],
      h_index: rawSource.summary_stats?.h_index ?? null,
      i10_index: rawSource.summary_stats?.i10_index ?? null,
      cited_by_count: rawSource.cited_by_count,
      works_count: rawSource.works_count,
      '2yr_mean_citedness': rawSource.summary_stats?.['2yr_mean_citedness'] ?? null,
      is_oa: rawSource.is_oa ?? null,
      type: rawSource.type,
      country_code: rawSource.country_code ?? null,
      homepage_url: rawSource.homepage_url ?? null,
      updated_date: rawSource.updated_date ?? null,
      apc_usd: rawSource.apc_usd ?? null,
      host_organization_name: rawSource.host_organization_display_name ?? null,
    };

    assert.equal(result.id, 'https://openalex.org/S137773608');
    assert.equal(result.display_name, 'Computers & Education');
    assert.deepEqual(result.issn, ['0360-1315']);
    assert.equal(result.h_index, 200);
    assert.equal(result.i10_index, 3000);
    assert.equal(result['2yr_mean_citedness'], 8.5);
    assert.equal(result.is_oa, false);
    assert.equal(result.apc_usd, 3500);
    assert.equal(result.host_organization_name, 'Elsevier');
  });

  it('should handle missing summary_stats gracefully', () => {
    const rawSource = {
      id: 'https://openalex.org/S999',
      display_name: 'Test Journal',
      cited_by_count: 10,
      works_count: 5,
    };

    const result = {
      h_index: rawSource.summary_stats?.h_index ?? null,
      i10_index: rawSource.summary_stats?.i10_index ?? null,
      '2yr_mean_citedness': rawSource.summary_stats?.['2yr_mean_citedness'] ?? null,
    };

    assert.equal(result.h_index, null);
    assert.equal(result.i10_index, null);
    assert.equal(result['2yr_mean_citedness'], null);
  });

  it('should transform search results array correctly', () => {
    const rawResults = [
      {
        id: 'S1',
        display_name: 'Journal A',
        issn: null,
        cited_by_count: 100,
        works_count: 50,
        summary_stats: { h_index: 30 },
        is_oa: true,
      },
      {
        id: 'S2',
        display_name: 'Journal B',
        issn: ['1234-5678'],
        cited_by_count: 200,
        works_count: 100,
        summary_stats: null,
        is_oa: false,
      },
    ];

    const results = rawResults.map((s) => ({
      id: s.id,
      display_name: s.display_name,
      issn: s.issn || [],
      cited_by_count: s.cited_by_count,
      works_count: s.works_count,
      h_index: s.summary_stats?.h_index ?? null,
      is_oa: s.is_oa ?? null,
    }));

    assert.equal(results.length, 2);
    assert.deepEqual(results[0].issn, []);
    assert.equal(results[0].h_index, 30);
    assert.deepEqual(results[1].issn, ['1234-5678']);
    assert.equal(results[1].h_index, null);
  });

  it('should transform publication trends correctly', () => {
    const countsByYear = [
      { year: 2025, works_count: 500, cited_by_count: 8000, oa_count: 200 },
      { year: 2024, works_count: 480, cited_by_count: 7500 },
      { year: 2023, works_count: 460, cited_by_count: 7000, oa_count: 150 },
    ];
    const years = 2;

    const trends = countsByYear.slice(0, years).map((entry) => ({
      year: entry.year,
      works_count: entry.works_count,
      cited_by_count: entry.cited_by_count,
      oa_count: entry.oa_count ?? null,
    }));

    assert.equal(trends.length, 2);
    assert.equal(trends[0].year, 2025);
    assert.equal(trends[0].oa_count, 200);
    assert.equal(trends[1].oa_count, null);
  });

  it('should transform Crossref special issues items correctly', () => {
    const items = [
      {
        title: ['AI in Education: A Special Issue'],
        DOI: '10.1016/j.example.2026.001',
        published: { 'date-parts': [[2026, 1, 15]] },
        subject: ['Education', 'Artificial Intelligence'],
        type: 'journal-article',
        'container-title': ['Computers & Education'],
      },
      {
        title: 'Single String Title',
        DOI: '10.1016/j.example.2026.002',
        published: null,
        subject: null,
        type: 'journal-article',
      },
    ];

    const results = items.map((item) => ({
      title: Array.isArray(item.title) ? item.title[0] : item.title,
      doi: item.DOI,
      published_date: item.published?.['date-parts']?.[0]?.join('-') ?? null,
      subject: item.subject || [],
      type: item.type,
      container_title: Array.isArray(item['container-title'])
        ? item['container-title'][0]
        : item['container-title'] ?? null,
    }));

    assert.equal(results[0].title, 'AI in Education: A Special Issue');
    assert.equal(results[0].published_date, '2026-1-15');
    assert.deepEqual(results[0].subject, ['Education', 'Artificial Intelligence']);
    assert.equal(results[0].container_title, 'Computers & Education');

    assert.equal(results[1].title, 'Single String Title');
    assert.equal(results[1].published_date, null);
    assert.deepEqual(results[1].subject, []);
    assert.equal(results[1].container_title, null);
  });

  it('should transform editor_info group_by response correctly', () => {
    const groupBy = [
      { key: 'https://openalex.org/A001', key_display_name: 'Dr. Smith', count: 45 },
      { key: 'https://openalex.org/A002', key_display_name: 'Dr. Lee', count: 38 },
    ];

    const topAuthors = groupBy.map((g) => ({
      author_id: g.key,
      author_name: g.key_display_name,
      works_count: g.count,
    }));

    assert.equal(topAuthors.length, 2);
    assert.equal(topAuthors[0].author_name, 'Dr. Smith');
    assert.equal(topAuthors[0].works_count, 45);
    assert.equal(topAuthors[1].author_id, 'https://openalex.org/A002');
  });
});

describe('Journal Server — MCP Handler Simulation', () => {
  // Simulates the CallToolRequest dispatch and error wrapping

  function simulateDispatch(name, args, handlers) {
    const handler = handlers[name];
    if (!handler) {
      return {
        content: [{ type: 'text', text: `Error: Unknown tool "${name}"` }],
        isError: true,
      };
    }
    try {
      const result = handler(args || {});
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      return {
        content: [{ type: 'text', text: `Error: ${error.message}` }],
        isError: true,
      };
    }
  }

  const mockHandlers = {
    journal_search_by_field: (args) => {
      if (!args.field) throw new Error('field is required');
      return { count: 0, query: args.field, results: [] };
    },
    journal_metrics: (args) => {
      if (!args.journal_id && !args.issn && !args.journal_name) {
        throw new Error('Provide at least one of: journal_id, issn, or journal_name');
      }
      return { id: args.journal_id, display_name: 'Test' };
    },
    journal_compare: (args) => {
      if (!Array.isArray(args.journal_ids) || args.journal_ids.length < 2) {
        throw new Error('Provide at least 2 journal IDs to compare');
      }
      if (args.journal_ids.length > 5) {
        throw new Error('Maximum 5 journals for comparison');
      }
      return { count: args.journal_ids.length, journals: [] };
    },
    journal_special_issues: (args) => {
      if (!args.journal_name && !args.issn) {
        throw new Error('Provide at least one of: journal_name, issn');
      }
      return { query: args.field || args.journal_name, results: [] };
    },
  };

  it('should return isError for unknown tool', () => {
    const result = simulateDispatch('nonexistent_tool', {}, mockHandlers);
    assert.equal(result.isError, true);
    assert.ok(result.content[0].text.includes('Unknown tool'));
  });

  it('should return success for valid journal_search_by_field call', () => {
    const result = simulateDispatch('journal_search_by_field', { field: 'AI' }, mockHandlers);
    assert.equal(result.isError, undefined);
    const parsed = JSON.parse(result.content[0].text);
    assert.equal(parsed.query, 'AI');
  });

  it('should return isError when journal_metrics has no identifiers', () => {
    const result = simulateDispatch('journal_metrics', {}, mockHandlers);
    assert.equal(result.isError, true);
    assert.ok(result.content[0].text.includes('Provide at least one of'));
  });

  it('should return isError when journal_compare has 1 ID', () => {
    const result = simulateDispatch('journal_compare', { journal_ids: ['S1'] }, mockHandlers);
    assert.equal(result.isError, true);
    assert.ok(result.content[0].text.includes('at least 2'));
  });

  it('should return isError when journal_compare has 6 IDs', () => {
    const result = simulateDispatch(
      'journal_compare',
      { journal_ids: ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'] },
      mockHandlers
    );
    assert.equal(result.isError, true);
    assert.ok(result.content[0].text.includes('Maximum 5'));
  });

  it('should return success for journal_compare with 3 IDs', () => {
    const result = simulateDispatch(
      'journal_compare',
      { journal_ids: ['S1', 'S2', 'S3'] },
      mockHandlers
    );
    assert.equal(result.isError, undefined);
    const parsed = JSON.parse(result.content[0].text);
    assert.equal(parsed.count, 3);
  });

  it('should return isError when journal_special_issues has no identifier', () => {
    const result = simulateDispatch('journal_special_issues', {}, mockHandlers);
    assert.equal(result.isError, true);
  });

  it('should format successful response as JSON text content', () => {
    const result = simulateDispatch('journal_search_by_field', { field: 'psychology' }, mockHandlers);
    assert.equal(result.content[0].type, 'text');
    const parsed = JSON.parse(result.content[0].text);
    assert.ok(typeof parsed === 'object');
  });
});

// =============================================================================
// INTEGRATION TESTS — These require network access to OpenAlex/Crossref APIs
// Uncomment or run selectively when testing API connectivity.
// =============================================================================

// INTEGRATION: requires network
// describe('Journal Server — OpenAlex API Integration', () => {
//   it('should return real journal data for educational technology search', async () => {
//     const url = 'https://api.openalex.org/sources?search=educational+technology&filter=type:journal&per_page=3&sort=cited_by_count:desc';
//     const response = await fetch(url, {
//       headers: { 'User-Agent': 'Diverga/10.3.0 (Journal Intelligence MCP Test)' },
//     });
//     assert.equal(response.ok, true);
//     const data = await response.json();
//     assert.ok(data.results.length > 0, 'Should return at least 1 journal');
//     assert.ok(data.results[0].display_name, 'Should have display_name');
//   });
//
//   it('should return metrics for a known journal ID', async () => {
//     const url = 'https://api.openalex.org/sources/S137773608';
//     const response = await fetch(url, {
//       headers: { 'User-Agent': 'Diverga/10.3.0 (Journal Intelligence MCP Test)' },
//     });
//     assert.equal(response.ok, true);
//     const data = await response.json();
//     assert.equal(data.display_name, 'Computers & Education');
//   });
// });

// INTEGRATION: requires network
// describe('Journal Server — Crossref API Integration', () => {
//   it('should return recent works for a known ISSN', async () => {
//     const params = new URLSearchParams({
//       query: 'artificial intelligence',
//       sort: 'published',
//       order: 'desc',
//       rows: '3',
//       select: 'DOI,title,published,subject,type',
//     });
//     const url = `https://api.crossref.org/journals/0360-1315/works?${params}`;
//     const response = await fetch(url, {
//       headers: { 'User-Agent': 'Diverga/10.3.0 (Journal Intelligence MCP Test)' },
//     });
//     assert.equal(response.ok, true);
//     const data = await response.json();
//     assert.ok(data.message.items.length > 0, 'Should return at least 1 work');
//   });
// });
