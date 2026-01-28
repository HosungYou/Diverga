#!/usr/bin/env node

/**
 * Diverga Setup CLI Entry Point
 * Supports both --no-tui flag for automation and interactive mode
 */

import('../dist/index.js').catch((err) => {
  console.error('Error loading Diverga setup:', err.message);
  console.error('Run "npm run build" first if you are developing locally.');
  process.exit(1);
});
