/**
 * openalex-frequency.js
 *
 * VS T-Score Frequency Calibration via OpenAlex
 *
 * Provides literature-based frequency data for grounding T-Score estimates.
 * Queries the OpenAlex API to count how frequently a methodology or theory
 * appears in a given research field, then maps the resulting ratio to a
 * calibrated T-Score range.
 *
 * OpenAlex is a free, open catalog of the global research system
 * (https://openalex.org). No API key is required; adding a contact email
 * grants access to the "polite pool" with higher rate limits (10 req/s
 * vs 1 req/s).
 *
 * Field resolution strategy:
 *   The OpenAlex /works endpoint does not support filtering by concept
 *   display name directly. Instead, we resolve the user-provided field
 *   string to an OpenAlex concept ID via the /concepts?search= endpoint,
 *   then filter works with `concepts.id:<resolved_id>`.
 *
 * Part of Diverga v11.0 Phase 5 -- VS T-Score rigor improvements.
 */

const OPENALEX_BASE = 'https://api.openalex.org';

/** Minimum delay between consecutive requests (ms). */
const REQUEST_DELAY_MS = 150;

/** Timestamp of the last request, used for rate limiting. */
let lastRequestTime = 0;

/**
 * Simple in-memory cache for concept ID resolution.
 * Keys are lowercased field names, values are { id, displayName }.
 * @type {Map<string, { id: string, displayName: string }>}
 */
const conceptCache = new Map();

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

/**
 * Enforce a minimum inter-request delay to respect OpenAlex rate limits.
 * @returns {Promise<void>}
 */
async function rateLimit() {
  const now = Date.now();
  const elapsed = now - lastRequestTime;
  if (elapsed < REQUEST_DELAY_MS) {
    await new Promise((resolve) => setTimeout(resolve, REQUEST_DELAY_MS - elapsed));
  }
  lastRequestTime = Date.now();
}

/**
 * Make a rate-limited GET request to OpenAlex and return the parsed JSON.
 * @param {string} url - Full URL to fetch
 * @returns {Promise<object>}
 */
async function fetchJSON(url) {
  await rateLimit();

  const response = await fetch(url);

  if (!response.ok) {
    const body = await response.text().catch(() => '');
    throw new Error(
      `OpenAlex request failed (${response.status} ${response.statusText}): ${body.slice(0, 500)}`
    );
  }

  return response.json();
}

/**
 * Resolve a human-readable field name (e.g., "education", "psychology")
 * to an OpenAlex concept ID by searching the /concepts endpoint.
 *
 * Returns the top result by relevance. Results are cached in memory so
 * repeated queries for the same field don't hit the API again.
 *
 * @param {string} field - The research field to resolve
 * @param {string} [email] - Optional polite-pool email
 * @returns {Promise<{ id: string, displayName: string }>}
 */
async function resolveConceptId(field, email) {
  const cacheKey = field.toLowerCase().trim();
  if (conceptCache.has(cacheKey)) {
    return conceptCache.get(cacheKey);
  }

  const params = new URLSearchParams();
  params.set('search', field);
  params.set('per_page', '1');
  if (email) {
    params.set('mailto', email);
  }

  const url = `${OPENALEX_BASE}/concepts?${params.toString()}`;
  const data = await fetchJSON(url);

  if (!data?.results?.length) {
    throw new Error(
      `No OpenAlex concept found for field "${field}". ` +
      `Try a broader term (e.g., "psychology" instead of "social cognition").`
    );
  }

  const concept = data.results[0];
  const resolved = {
    id: concept.id,               // e.g., "https://openalex.org/C15744967"
    displayName: concept.display_name, // e.g., "Psychology"
  };

  conceptCache.set(cacheKey, resolved);
  return resolved;
}

/**
 * Build the query-string parameters shared by every OpenAlex works request.
 * @param {string} filter - The filter expression
 * @param {string} [email] - Optional polite-pool email
 * @returns {URLSearchParams}
 */
function buildWorksParams(filter, email) {
  const params = new URLSearchParams();
  params.set('filter', filter);
  params.set('per_page', '1'); // we only need the meta.count
  if (email) {
    params.set('mailto', email);
  }
  return params;
}

/**
 * Fetch a count of works from OpenAlex matching the given filter.
 * @param {string} filter - OpenAlex filter expression
 * @param {string} [email] - Optional polite-pool email
 * @returns {Promise<{ count: number, url: string }>}
 */
async function fetchWorkCount(filter, email) {
  const params = buildWorksParams(filter, email);
  const url = `${OPENALEX_BASE}/works?${params.toString()}`;

  const data = await fetchJSON(url);

  if (!data?.meta?.count && data?.meta?.count !== 0) {
    throw new Error('Unexpected OpenAlex response: missing meta.count');
  }

  return { count: data.meta.count, url };
}

/**
 * Determine the publication year filter fragment.
 * @param {number} fromYear
 * @param {number} toYear
 * @returns {string} e.g. "publication_year:2021-2026"
 */
function yearFilter(fromYear, toYear) {
  return `publication_year:${fromYear}-${toYear}`;
}

/**
 * Derive confidence level from the size of the field corpus.
 * @param {number} fieldWorkCount
 * @returns {"high" | "medium" | "low"}
 */
function deriveConfidence(fieldWorkCount) {
  if (fieldWorkCount > 1000) return 'high';
  if (fieldWorkCount > 100) return 'medium';
  return 'low';
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Map a frequency ratio (methodology works / field works) to an estimated
 * T-Score and a human-readable interpretation.
 *
 * | Ratio range      | T-Score range | Interpretation          |
 * |------------------|---------------|-------------------------|
 * | > 0.15           | 0.70 - 1.00   | Common / Modal          |
 * | 0.05 - 0.15      | 0.40 - 0.70   | Established alternative |
 * | 0.01 - 0.05      | 0.20 - 0.40   | Innovative              |
 * | < 0.01           | 0.00 - 0.20   | Experimental / Novel    |
 *
 * Within each band, the score is linearly interpolated.
 *
 * @param {number} ratio - Usage frequency ratio in [0, 1].
 * @returns {{ tScore: number, interpretation: string }}
 */
export function ratioToTScore(ratio) {
  // Clamp to [0, 1]
  const r = Math.max(0, Math.min(1, ratio));

  let tScore;
  let interpretation;

  if (r > 0.15) {
    // 0.15 -> 0.70,  1.0 -> 1.0  (linear)
    tScore = 0.70 + ((r - 0.15) / (1.0 - 0.15)) * (1.0 - 0.70);
    interpretation = 'Common';
  } else if (r >= 0.05) {
    // 0.05 -> 0.40,  0.15 -> 0.70
    tScore = 0.40 + ((r - 0.05) / (0.15 - 0.05)) * (0.70 - 0.40);
    interpretation = 'Established';
  } else if (r >= 0.01) {
    // 0.01 -> 0.20,  0.05 -> 0.40
    tScore = 0.20 + ((r - 0.01) / (0.05 - 0.01)) * (0.40 - 0.20);
    interpretation = 'Innovative';
  } else {
    // 0.0 -> 0.00,  0.01 -> 0.20
    tScore = (r / 0.01) * 0.20;
    interpretation = 'Novel';
  }

  return {
    tScore: Math.round(tScore * 100) / 100,
    interpretation,
  };
}

/**
 * Query OpenAlex for how frequently a methodology or theory appears within
 * a given research field.
 *
 * Three API calls are made:
 *   1. Resolve the field name to an OpenAlex concept ID (cached after first call).
 *   2. Count total works tagged with that concept in the time window.
 *   3. Count works matching both the concept and the methodology search term.
 *
 * The ratio (3 / 2) is then mapped to an estimated T-Score.
 *
 * @param {string} methodology - The methodology or theory to search
 *   (e.g., "TAM", "grounded theory").
 * @param {string} field - The research field
 *   (e.g., "education", "psychology").
 * @param {object} [options] - Optional parameters.
 * @param {number} [options.fromYear] - Start year (default: 5 years ago).
 * @param {number} [options.toYear]   - End year (default: current year).
 * @param {string} [options.email]    - Polite-pool email for OpenAlex.
 * @returns {Promise<FrequencyResult>}
 *
 * @typedef {object} FrequencyResult
 * @property {string}  methodology          - The queried methodology.
 * @property {string}  field                - The queried field.
 * @property {string}  resolvedField        - The OpenAlex concept name used.
 * @property {number}  fieldWorkCount       - Total works in the field.
 * @property {number}  methodologyWorkCount - Works using this methodology
 *   in the field.
 * @property {number}  ratio                - methodologyWorkCount / fieldWorkCount.
 * @property {number}  tScoreEstimate       - Mapped T-Score (0-1).
 * @property {string}  interpretation       - "Common", "Established",
 *   "Innovative", or "Novel".
 * @property {string}  confidence           - "high" | "medium" | "low"
 *   based on fieldWorkCount.
 * @property {string}  period               - e.g., "2021-2026".
 * @property {string}  queryUrl             - The methodology query URL
 *   for transparency / reproducibility.
 */
export async function queryMethodologyFrequency(methodology, field, options = {}) {
  if (!methodology || typeof methodology !== 'string') {
    throw new TypeError('methodology must be a non-empty string');
  }
  if (!field || typeof field !== 'string') {
    throw new TypeError('field must be a non-empty string');
  }

  const currentYear = new Date().getFullYear();
  const fromYear = options.fromYear ?? currentYear - 5;
  const toYear = options.toYear ?? currentYear;
  const email = options.email ?? undefined;

  const years = yearFilter(fromYear, toYear);

  // Step 1: Resolve field to concept ID
  const concept = await resolveConceptId(field, email);

  // Step 2: Total works in the field
  const fieldFilter = `concepts.id:${concept.id},${years}`;
  const fieldResult = await fetchWorkCount(fieldFilter, email);

  // Step 3: Works matching field + methodology
  const methodologyFilter = `default.search:${methodology},concepts.id:${concept.id},${years}`;
  const methodologyResult = await fetchWorkCount(methodologyFilter, email);

  const fieldWorkCount = fieldResult.count;
  const methodologyWorkCount = methodologyResult.count;
  const ratio = fieldWorkCount > 0 ? methodologyWorkCount / fieldWorkCount : 0;

  const { tScore, interpretation } = ratioToTScore(ratio);

  return {
    methodology,
    field,
    resolvedField: concept.displayName,
    fieldWorkCount,
    methodologyWorkCount,
    ratio,
    tScoreEstimate: tScore,
    interpretation,
    confidence: deriveConfidence(fieldWorkCount),
    period: `${fromYear}-${toYear}`,
    queryUrl: methodologyResult.url,
  };
}

/**
 * Batch-query OpenAlex for multiple methodologies within a single field.
 *
 * Useful when an agent needs to compare T-Scores of several candidate
 * methodologies side by side. The field concept is resolved once and the
 * field-wide count is fetched once, then each methodology is queried
 * sequentially (rate-limited). Results are returned sorted by frequency
 * (most common first).
 *
 * @param {string[]} methodologies - Array of methodology / theory names.
 * @param {string} field - The research field.
 * @param {object} [options] - Same options as {@link queryMethodologyFrequency}.
 * @param {number} [options.fromYear]
 * @param {number} [options.toYear]
 * @param {string} [options.email]
 * @returns {Promise<FrequencyResult[]>} Sorted descending by ratio.
 */
export async function compareMethodologyFrequencies(methodologies, field, options = {}) {
  if (!Array.isArray(methodologies) || methodologies.length === 0) {
    throw new TypeError('methodologies must be a non-empty array of strings');
  }
  if (!field || typeof field !== 'string') {
    throw new TypeError('field must be a non-empty string');
  }

  const currentYear = new Date().getFullYear();
  const fromYear = options.fromYear ?? currentYear - 5;
  const toYear = options.toYear ?? currentYear;
  const email = options.email ?? undefined;

  const years = yearFilter(fromYear, toYear);

  // Resolve field to concept ID (cached)
  const concept = await resolveConceptId(field, email);

  // Fetch field-wide count once
  const fieldFilter = `concepts.id:${concept.id},${years}`;
  const fieldResult = await fetchWorkCount(fieldFilter, email);
  const fieldWorkCount = fieldResult.count;

  // Fetch each methodology sequentially (rate-limited)
  const results = [];

  for (const methodology of methodologies) {
    if (!methodology || typeof methodology !== 'string') {
      throw new TypeError(`Each methodology must be a non-empty string, got: ${methodology}`);
    }

    const methodologyFilter = `default.search:${methodology},concepts.id:${concept.id},${years}`;
    const methodologyResult = await fetchWorkCount(methodologyFilter, email);

    const methodologyWorkCount = methodologyResult.count;
    const ratio = fieldWorkCount > 0 ? methodologyWorkCount / fieldWorkCount : 0;
    const { tScore, interpretation } = ratioToTScore(ratio);

    results.push({
      methodology,
      field,
      resolvedField: concept.displayName,
      fieldWorkCount,
      methodologyWorkCount,
      ratio,
      tScoreEstimate: tScore,
      interpretation,
      confidence: deriveConfidence(fieldWorkCount),
      period: `${fromYear}-${toYear}`,
      queryUrl: methodologyResult.url,
    });
  }

  // Sort descending by ratio (most common first)
  results.sort((a, b) => b.ratio - a.ratio);

  return results;
}
