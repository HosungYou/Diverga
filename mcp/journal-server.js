#!/usr/bin/env node

/**
 * journal-server.js
 *
 * MCP Server: Journal Intelligence
 * Uses OpenAlex (primary) and Crossref (secondary) APIs for real-time journal data.
 * Part of Diverga v10.3.0
 *
 * 6 tools:
 *   - journal_search_by_field: Search journals by research field
 *   - journal_metrics: Get detailed journal metrics
 *   - journal_publication_trends: Publication trend data over years
 *   - journal_editor_info: Top authors/contributors for a journal
 *   - journal_compare: Compare multiple journals side by side
 *   - journal_special_issues: Recent themed publications from Crossref
 *
 * Email loading order (OpenAlex polite pool):
 *   1. process.env.OPENALEX_EMAIL
 *   2. .omc/config.json → openalex_email
 *   3. No email → works but slower rate limit (warning logged)
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

// ---------------------------------------------------------------------------
// Email resolution for OpenAlex polite pool
// ---------------------------------------------------------------------------

function resolveEmail() {
  // 1. Environment variable
  if (process.env.OPENALEX_EMAIL) {
    return process.env.OPENALEX_EMAIL;
  }

  // 2. Project config
  try {
    const configPath = join(process.cwd(), '.omc', 'config.json');
    if (existsSync(configPath)) {
      const config = JSON.parse(readFileSync(configPath, 'utf8'));
      if (config.openalex_email) {
        return config.openalex_email;
      }
    }
  } catch {
    // Ignore config read errors
  }

  // 3. No email available
  process.stderr.write(
    '[journal] Warning: No OpenAlex email configured. API responses may be rate-limited.\n' +
    '[journal] Set OPENALEX_EMAIL env var or add openalex_email to .omc/config.json\n'
  );
  return null;
}

const OPENALEX_EMAIL = resolveEmail();

// ---------------------------------------------------------------------------
// HTTP helpers
// ---------------------------------------------------------------------------

function buildOpenAlexUrl(path, params = {}) {
  const url = new URL(path, 'https://api.openalex.org');
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null) {
      url.searchParams.set(key, String(value));
    }
  }
  if (OPENALEX_EMAIL) {
    url.searchParams.set('mailto', OPENALEX_EMAIL);
  }
  return url.toString();
}

async function fetchJSON(url) {
  const response = await fetch(url, {
    headers: { 'User-Agent': 'Diverga/10.3.0 (Journal Intelligence MCP)' },
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText} — ${url}`);
  }
  return response.json();
}

// ---------------------------------------------------------------------------
// Tool: journal_search_by_field
// ---------------------------------------------------------------------------

async function journalSearchByField({ field, subfield, per_page = 10 }) {
  const searchQuery = subfield ? `${field} ${subfield}` : field;
  const url = buildOpenAlexUrl('/sources', {
    search: searchQuery,
    filter: 'type:journal',
    per_page: Math.min(per_page, 50),
    sort: 'cited_by_count:desc',
  });

  const data = await fetchJSON(url);
  const results = (data.results || []).map((s) => ({
    id: s.id,
    display_name: s.display_name,
    issn: s.issn || [],
    cited_by_count: s.cited_by_count,
    works_count: s.works_count,
    h_index: s.summary_stats?.h_index ?? null,
    is_oa: s.is_oa ?? null,
  }));

  return {
    count: data.meta?.count ?? results.length,
    query: searchQuery,
    results,
  };
}

// ---------------------------------------------------------------------------
// Tool: journal_metrics
// ---------------------------------------------------------------------------

async function journalMetrics({ journal_id, issn, journal_name }) {
  let source;

  if (journal_id) {
    // Direct ID lookup
    const url = buildOpenAlexUrl(`/sources/${encodeURIComponent(journal_id)}`);
    source = await fetchJSON(url);
  } else if (issn) {
    // ISSN filter
    const url = buildOpenAlexUrl('/sources', {
      filter: `issn:${issn}`,
      per_page: 1,
    });
    const data = await fetchJSON(url);
    if (!data.results || data.results.length === 0) {
      throw new Error(`No journal found with ISSN: ${issn}`);
    }
    source = data.results[0];
  } else if (journal_name) {
    // Name search
    const url = buildOpenAlexUrl('/sources', {
      search: journal_name,
      filter: 'type:journal',
      per_page: 1,
    });
    const data = await fetchJSON(url);
    if (!data.results || data.results.length === 0) {
      throw new Error(`No journal found matching name: ${journal_name}`);
    }
    source = data.results[0];
  } else {
    throw new Error('Provide at least one of: journal_id, issn, or journal_name');
  }

  return {
    id: source.id,
    display_name: source.display_name,
    issn: source.issn || [],
    h_index: source.summary_stats?.h_index ?? null,
    i10_index: source.summary_stats?.i10_index ?? null,
    cited_by_count: source.cited_by_count,
    works_count: source.works_count,
    '2yr_mean_citedness': source.summary_stats?.['2yr_mean_citedness'] ?? null,
    is_oa: source.is_oa ?? null,
    type: source.type,
    country_code: source.country_code ?? null,
    homepage_url: source.homepage_url ?? null,
    updated_date: source.updated_date ?? null,
    apc_usd: source.apc_usd ?? null,
    host_organization_name: source.host_organization_display_name ?? null,
  };
}

// ---------------------------------------------------------------------------
// Tool: journal_publication_trends
// ---------------------------------------------------------------------------

async function journalPublicationTrends({ journal_id, years = 5 }) {
  const url = buildOpenAlexUrl(`/sources/${encodeURIComponent(journal_id)}`);
  const source = await fetchJSON(url);

  const countsByYear = source.counts_by_year || [];
  const trends = countsByYear
    .slice(0, years)
    .map((entry) => ({
      year: entry.year,
      works_count: entry.works_count,
      cited_by_count: entry.cited_by_count,
      oa_count: entry.oa_count ?? null,
    }));

  return {
    journal: source.display_name,
    journal_id: source.id,
    years_requested: years,
    trends,
  };
}

// ---------------------------------------------------------------------------
// Tool: journal_editor_info (top contributors)
// ---------------------------------------------------------------------------

async function journalEditorInfo({ journal_id, per_page = 10 }) {
  // Use works group_by to find top authors by publication count in this journal
  const url = buildOpenAlexUrl('/works', {
    filter: `primary_location.source.id:${journal_id}`,
    group_by: 'authorships.author.id',
    per_page: Math.min(per_page, 25),
  });

  const data = await fetchJSON(url);
  const groups = data.group_by || [];

  const topAuthors = groups.map((g) => ({
    author_id: g.key,
    author_name: g.key_display_name,
    works_count: g.count,
  }));

  return {
    journal_id,
    total_grouped: data.meta?.count ?? topAuthors.length,
    top_authors: topAuthors,
  };
}

// ---------------------------------------------------------------------------
// Tool: journal_compare
// ---------------------------------------------------------------------------

async function journalCompare({ journal_ids }) {
  if (!Array.isArray(journal_ids) || journal_ids.length < 2) {
    throw new Error('Provide at least 2 journal IDs to compare');
  }
  if (journal_ids.length > 5) {
    throw new Error('Maximum 5 journals for comparison');
  }

  // Fetch all journal metrics in parallel
  const metrics = await Promise.all(
    journal_ids.map((id) => journalMetrics({ journal_id: id }))
  );

  return {
    count: metrics.length,
    journals: metrics,
  };
}

// ---------------------------------------------------------------------------
// Tool: journal_special_issues (via Crossref)
// ---------------------------------------------------------------------------

async function journalSpecialIssues({ journal_name, field, issn }) {
  let url;
  const query = field || journal_name || '';

  if (issn) {
    // Crossref journal works endpoint
    url = `https://api.crossref.org/journals/${encodeURIComponent(issn)}/works?` +
      new URLSearchParams({
        query: query,
        sort: 'published',
        order: 'desc',
        rows: '10',
        select: 'DOI,title,published,subject,type',
      }).toString();
  } else if (journal_name) {
    // Crossref general works search filtered by container-title
    url = `https://api.crossref.org/works?` +
      new URLSearchParams({
        'query.container-title': journal_name,
        query: query,
        sort: 'published',
        order: 'desc',
        rows: '10',
        select: 'DOI,title,published,subject,type,container-title',
      }).toString();
  } else {
    throw new Error('Provide at least one of: journal_name, issn');
  }

  const data = await fetchJSON(url);
  const items = data.message?.items || [];

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

  return {
    query: query,
    issn: issn ?? null,
    journal_name: journal_name ?? null,
    count: results.length,
    results,
  };
}

// ---------------------------------------------------------------------------
// Tool definitions
// ---------------------------------------------------------------------------

const TOOLS = [
  {
    name: 'journal_search_by_field',
    description:
      'Search for academic journals by research field or subfield. Returns journals sorted by citation count with key metrics. Uses OpenAlex API.',
    inputSchema: {
      type: 'object',
      properties: {
        field: {
          type: 'string',
          description: 'Research field to search (e.g., "educational technology", "organizational psychology")',
        },
        subfield: {
          type: 'string',
          description: 'Optional subfield to narrow results (e.g., "meta-analysis", "AI in education")',
        },
        per_page: {
          type: 'number',
          description: 'Number of results to return (default: 10, max: 50)',
        },
      },
      required: ['field'],
    },
  },
  {
    name: 'journal_metrics',
    description:
      'Get detailed metrics for a specific journal including h-index, citation count, works count, OA status, APC, and more. Accepts journal ID, ISSN, or name. Uses OpenAlex API.',
    inputSchema: {
      type: 'object',
      properties: {
        journal_id: {
          type: 'string',
          description: 'OpenAlex source ID (e.g., "https://openalex.org/S137773608")',
        },
        issn: {
          type: 'string',
          description: 'Journal ISSN (e.g., "0360-1315")',
        },
        journal_name: {
          type: 'string',
          description: 'Journal name for search-based lookup',
        },
      },
    },
  },
  {
    name: 'journal_publication_trends',
    description:
      'Get publication and citation trends for a journal over recent years. Shows works count, citation count, and OA count per year. Uses OpenAlex API.',
    inputSchema: {
      type: 'object',
      properties: {
        journal_id: {
          type: 'string',
          description: 'OpenAlex source ID',
        },
        years: {
          type: 'number',
          description: 'Number of years of trend data (default: 5)',
        },
      },
      required: ['journal_id'],
    },
  },
  {
    name: 'journal_editor_info',
    description:
      'Find top authors/contributors for a journal by publication count. Useful for identifying potential reviewers and understanding the journal community. Uses OpenAlex API.',
    inputSchema: {
      type: 'object',
      properties: {
        journal_id: {
          type: 'string',
          description: 'OpenAlex source ID',
        },
        per_page: {
          type: 'number',
          description: 'Number of top authors to return (default: 10, max: 25)',
        },
      },
      required: ['journal_id'],
    },
  },
  {
    name: 'journal_compare',
    description:
      'Compare 2-5 journals side by side on all metrics (h-index, citations, works count, OA status, APC, etc.). Uses OpenAlex API.',
    inputSchema: {
      type: 'object',
      properties: {
        journal_ids: {
          type: 'array',
          items: { type: 'string' },
          description: 'Array of 2-5 OpenAlex source IDs to compare',
          minItems: 2,
          maxItems: 5,
        },
      },
      required: ['journal_ids'],
    },
  },
  {
    name: 'journal_special_issues',
    description:
      'Find recent themed publications and special issue content for a journal. Returns recent works with subject tags. Uses Crossref API.',
    inputSchema: {
      type: 'object',
      properties: {
        journal_name: {
          type: 'string',
          description: 'Journal name for search',
        },
        field: {
          type: 'string',
          description: 'Field/topic to search within the journal',
        },
        issn: {
          type: 'string',
          description: 'Journal ISSN for precise lookup',
        },
      },
    },
  },
];

// ---------------------------------------------------------------------------
// Dispatch
// ---------------------------------------------------------------------------

const HANDLERS = {
  journal_search_by_field: journalSearchByField,
  journal_metrics: journalMetrics,
  journal_publication_trends: journalPublicationTrends,
  journal_editor_info: journalEditorInfo,
  journal_compare: journalCompare,
  journal_special_issues: journalSpecialIssues,
};

// ---------------------------------------------------------------------------
// MCP Server
// ---------------------------------------------------------------------------

const server = new Server(
  { name: 'journal', version: '10.3.0' },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: TOOLS,
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const handler = HANDLERS[name];

  if (!handler) {
    return {
      content: [{ type: 'text', text: `Error: Unknown tool "${name}"` }],
      isError: true,
    };
  }

  try {
    const result = await handler(args || {});
    return {
      content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
    };
  } catch (error) {
    return {
      content: [{ type: 'text', text: `Error: ${error.message}` }],
      isError: true,
    };
  }
});

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
