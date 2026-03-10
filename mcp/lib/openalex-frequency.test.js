/**
 * openalex-frequency.test.js
 *
 * Quick integration test for the OpenAlex frequency lookup utility.
 * Run with: node mcp/lib/openalex-frequency.test.js
 *
 * Hits the live OpenAlex API — requires network access.
 */

import {
  queryMethodologyFrequency,
  compareMethodologyFrequencies,
  ratioToTScore,
} from './openalex-frequency.js';

// ---------------------------------------------------------------------------
// Unit tests for ratioToTScore (no network needed)
// ---------------------------------------------------------------------------

function testRatioToTScore() {
  console.log('--- ratioToTScore unit tests ---\n');

  const cases = [
    { ratio: 0.0, expectedInterp: 'Novel' },
    { ratio: 0.005, expectedInterp: 'Novel' },
    { ratio: 0.01, expectedInterp: 'Innovative' },
    { ratio: 0.03, expectedInterp: 'Innovative' },
    { ratio: 0.05, expectedInterp: 'Established' },
    { ratio: 0.10, expectedInterp: 'Established' },
    { ratio: 0.15, expectedInterp: 'Established' },
    { ratio: 0.20, expectedInterp: 'Common' },
    { ratio: 0.50, expectedInterp: 'Common' },
    { ratio: 1.0, expectedInterp: 'Common' },
  ];

  let passed = 0;
  for (const { ratio, expectedInterp } of cases) {
    const { tScore, interpretation } = ratioToTScore(ratio);
    const ok = interpretation === expectedInterp && tScore >= 0 && tScore <= 1;
    const status = ok ? 'PASS' : 'FAIL';
    if (!ok) {
      console.log(
        `  ${status}: ratio=${ratio} → tScore=${tScore}, interp="${interpretation}" (expected "${expectedInterp}")`
      );
    } else {
      console.log(
        `  ${status}: ratio=${ratio.toFixed(3)} → tScore=${tScore.toFixed(2)}, interp="${interpretation}"`
      );
      passed++;
    }
  }

  console.log(`\n  ${passed}/${cases.length} passed\n`);
}

// ---------------------------------------------------------------------------
// Integration tests (live API)
// ---------------------------------------------------------------------------

async function testSingleQuery() {
  console.log('--- Test 1: Single methodology query ---\n');

  const result = await queryMethodologyFrequency('TAM technology acceptance', 'education');

  console.log('  TAM in Education:', JSON.stringify(result, null, 2));
  console.log();

  // Basic shape assertions
  const requiredKeys = [
    'methodology', 'field', 'resolvedField', 'fieldWorkCount', 'methodologyWorkCount',
    'ratio', 'tScoreEstimate', 'interpretation', 'confidence', 'period', 'queryUrl',
  ];
  for (const key of requiredKeys) {
    if (!(key in result)) {
      console.log(`  FAIL: missing key "${key}"`);
      return false;
    }
  }

  if (result.fieldWorkCount <= 0) {
    console.log('  FAIL: fieldWorkCount should be > 0');
    return false;
  }
  if (result.tScoreEstimate < 0 || result.tScoreEstimate > 1) {
    console.log('  FAIL: tScoreEstimate out of range');
    return false;
  }

  console.log('  PASS: Single query returned valid result\n');
  return true;
}

async function testComparativeQuery() {
  console.log('--- Test 2: Comparative methodology query ---\n');

  const methodologies = [
    'TAM technology acceptance',
    'UTAUT',
    'self-determination theory',
    'actor-network theory',
  ];

  const results = await compareMethodologyFrequencies(methodologies, 'education');

  console.log('  Comparative frequencies:');
  for (const r of results) {
    console.log(
      `    ${r.methodology}: ratio=${r.ratio.toFixed(4)}, ` +
      `T-Score\u2248${r.tScoreEstimate.toFixed(2)} (${r.interpretation})`
    );
  }
  console.log();

  if (results.length !== methodologies.length) {
    console.log(`  FAIL: expected ${methodologies.length} results, got ${results.length}`);
    return false;
  }

  // Verify sorted descending by ratio
  for (let i = 1; i < results.length; i++) {
    if (results[i].ratio > results[i - 1].ratio) {
      console.log('  FAIL: results not sorted descending by ratio');
      return false;
    }
  }

  console.log('  PASS: Comparative query returned sorted valid results\n');
  return true;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  console.log('=== OpenAlex Frequency Lookup Tests ===\n');

  // Unit tests (offline)
  testRatioToTScore();

  // Integration tests (online)
  console.log('Running live API tests (requires network)...\n');

  try {
    const t1 = await testSingleQuery();
    const t2 = await testComparativeQuery();

    console.log('=== Summary ===');
    console.log(`  ratioToTScore: PASS`);
    console.log(`  Single query:  ${t1 ? 'PASS' : 'FAIL'}`);
    console.log(`  Comparative:   ${t2 ? 'PASS' : 'FAIL'}`);
  } catch (err) {
    console.error('\nAPI test failed with error:', err.message);
    console.error('(This is expected if you have no network access.)\n');
    process.exitCode = 1;
  }
}

main();
