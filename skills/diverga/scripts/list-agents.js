#!/usr/bin/env node
/**
 * List all Diverga agents
 * This script outputs a formatted list of all 40 agents
 */

const AGENTS = {
  'A1': { name: 'Research Question Refiner', tier: 'MEDIUM', category: 'Research Foundation' },
  'A2': { name: 'Theoretical Framework Architect', tier: 'HIGH', category: 'Research Foundation' },
  'A3': { name: "Devil's Advocate", tier: 'MEDIUM', category: 'Research Foundation' },
  'A4': { name: 'Research Ethics Advisor', tier: 'MEDIUM', category: 'Research Foundation' },
  'A5': { name: 'Paradigm & Worldview Advisor', tier: 'HIGH', category: 'Research Foundation' },
  'A6': { name: 'Conceptual Framework Visualizer', tier: 'HIGH', category: 'Research Foundation' },
  'B1': { name: 'Literature Review Strategist', tier: 'MEDIUM', category: 'Literature & Evidence' },
  'B2': { name: 'Evidence Quality Appraiser', tier: 'MEDIUM', category: 'Literature & Evidence' },
  'B3': { name: 'Effect Size Extractor', tier: 'LOW', category: 'Literature & Evidence' },
  'B4': { name: 'Research Radar', tier: 'LOW', category: 'Literature & Evidence' },
  'B5': { name: 'Parallel Document Processor', tier: 'MEDIUM', category: 'Literature & Evidence' },
  'C1': { name: 'Quantitative Design Consultant', tier: 'HIGH', category: 'Study Design' },
  'C2': { name: 'Qualitative Design Consultant', tier: 'HIGH', category: 'Study Design' },
  'C3': { name: 'Mixed Methods Design Consultant', tier: 'HIGH', category: 'Study Design' },
  'C4': { name: 'Experimental Materials Developer', tier: 'MEDIUM', category: 'Study Design' },
  'C5': { name: 'Meta-Analysis Master', tier: 'HIGH', category: 'Study Design' },
  'C6': { name: 'Data Integrity Guard', tier: 'MEDIUM', category: 'Study Design' },
  'C7': { name: 'Error Prevention Engine', tier: 'MEDIUM', category: 'Study Design' },
  'D1': { name: 'Sampling Strategy Advisor', tier: 'MEDIUM', category: 'Data Collection' },
  'D2': { name: 'Interview & Focus Group Specialist', tier: 'MEDIUM', category: 'Data Collection' },
  'D3': { name: 'Observation Protocol Designer', tier: 'LOW', category: 'Data Collection' },
  'D4': { name: 'Measurement Instrument Developer', tier: 'HIGH', category: 'Data Collection' },
  'E1': { name: 'Quantitative Analysis Guide', tier: 'HIGH', category: 'Analysis' },
  'E2': { name: 'Qualitative Coding Specialist', tier: 'MEDIUM', category: 'Analysis' },
  'E3': { name: 'Mixed Methods Integration', tier: 'HIGH', category: 'Analysis' },
  'E4': { name: 'Analysis Code Generator', tier: 'LOW', category: 'Analysis' },
  'E5': { name: 'Sensitivity Analysis Designer', tier: 'MEDIUM', category: 'Analysis' },
  'F1': { name: 'Internal Consistency Checker', tier: 'LOW', category: 'Quality & Validation' },
  'F2': { name: 'Checklist Manager', tier: 'LOW', category: 'Quality & Validation' },
  'F3': { name: 'Reproducibility Auditor', tier: 'MEDIUM', category: 'Quality & Validation' },
  'F4': { name: 'Bias & Trustworthiness Detector', tier: 'MEDIUM', category: 'Quality & Validation' },
  'F5': { name: 'Humanization Verifier', tier: 'MEDIUM', category: 'Quality & Validation' },
  'G1': { name: 'Journal Matcher', tier: 'MEDIUM', category: 'Publication' },
  'G2': { name: 'Academic Communicator', tier: 'MEDIUM', category: 'Publication' },
  'G3': { name: 'Peer Review Strategist', tier: 'HIGH', category: 'Publication' },
  'G4': { name: 'Pre-registration Composer', tier: 'MEDIUM', category: 'Publication' },
  'G5': { name: 'Academic Style Auditor', tier: 'MEDIUM', category: 'Publication' },
  'G6': { name: 'Academic Style Humanizer', tier: 'MEDIUM', category: 'Publication' },
  'H1': { name: 'Ethnographic Research Advisor', tier: 'HIGH', category: 'Specialized' },
  'H2': { name: 'Action Research Facilitator', tier: 'HIGH', category: 'Specialized' },
};

const MODEL_MAP = {
  HIGH: 'o1',
  MEDIUM: 'gpt-4',
  LOW: 'gpt-3.5-turbo',
};

console.log('Diverga Agent Catalog - 40 Specialized Research Agents\n');
console.log('='.repeat(60) + '\n');

// Group by category
const categories = {};
for (const [id, agent] of Object.entries(AGENTS)) {
  if (!categories[agent.category]) {
    categories[agent.category] = [];
  }
  categories[agent.category].push({ id, ...agent });
}

for (const [category, agents] of Object.entries(categories)) {
  console.log(`## ${category}\n`);
  for (const agent of agents) {
    const model = MODEL_MAP[agent.tier];
    console.log(`  ${agent.id}: ${agent.name} (${model})`);
  }
  console.log('');
}

console.log('='.repeat(60));
console.log(`Total: ${Object.keys(AGENTS).length} agents`);
console.log('HIGH=o1  MEDIUM=gpt-4  LOW=gpt-3.5-turbo');
