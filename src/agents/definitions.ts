/**
 * Diverga Agent Runtime - Agent Definitions
 *
 * Registry of all 44 research agents for the Diverga system.
 * Prompts are dynamically loaded from SKILL.md files (Source of Truth).
 *
 * This module provides:
 * 1. Agent definitions with metadata
 * 2. getAgentDefinitions() for runtime registry
 * 3. Individual agent exports
 */

import type {
  AgentConfig,
  AgentRegistry,
  ModelType,
  TierLevel,
  CategoryId,
  AgentIdMapping,
} from './types.js';

import {
  loadAgentPrompt,
  loadAgentMetadata,
  buildEnhancedPrompt,
} from './prompt-loader.js';

// ============================================================
// AGENT ID MAPPINGS
// Maps shorthand IDs (a1, b1, etc.) to directory names
// ============================================================

export const AGENT_MAPPINGS: AgentIdMapping[] = [
  // Category A: Research Foundation (6 agents)
  { shortId: 'a1', fullId: 'diverga:a1', directoryName: 'A1-research-question-refiner' },
  { shortId: 'a2', fullId: 'diverga:a2', directoryName: 'A2-theoretical-framework-architect' },
  { shortId: 'a3', fullId: 'diverga:a3', directoryName: 'A3-devils-advocate' },
  { shortId: 'a4', fullId: 'diverga:a4', directoryName: 'A4-research-ethics-advisor' },
  { shortId: 'a5', fullId: 'diverga:a5', directoryName: 'A5-paradigm-worldview-advisor' },
  { shortId: 'a6', fullId: 'diverga:a6', directoryName: 'A6-conceptual-framework-visualizer' },

  // Category B: Literature & Evidence (5 agents)
  { shortId: 'b1', fullId: 'diverga:b1', directoryName: 'B1-systematic-literature-scout' },
  { shortId: 'b2', fullId: 'diverga:b2', directoryName: 'B2-evidence-quality-appraiser' },
  { shortId: 'b3', fullId: 'diverga:b3', directoryName: 'B3-effect-size-extractor' },
  { shortId: 'b4', fullId: 'diverga:b4', directoryName: 'B4-research-radar' },
  { shortId: 'b5', fullId: 'diverga:b5', directoryName: 'B5-parallel-document-processor' },

  // Category C: Study Design (7 agents)
  { shortId: 'c1', fullId: 'diverga:c1', directoryName: 'C1-quantitative-design-consultant' },
  { shortId: 'c2', fullId: 'diverga:c2', directoryName: 'C2-qualitative-design-consultant' },
  { shortId: 'c3', fullId: 'diverga:c3', directoryName: 'C3-mixed-methods-design-consultant' },
  { shortId: 'c4', fullId: 'diverga:c4', directoryName: 'C4-experimental-materials-developer' },
  { shortId: 'c5', fullId: 'diverga:c5', directoryName: 'C5-meta-analysis-master' },
  { shortId: 'c6', fullId: 'diverga:c6', directoryName: 'C6-data-integrity-guard' },
  { shortId: 'c7', fullId: 'diverga:c7', directoryName: 'C7-error-prevention-engine' },

  // Category D: Data Collection (4 agents)
  { shortId: 'd1', fullId: 'diverga:d1', directoryName: 'D1-sampling-strategy-advisor' },
  { shortId: 'd2', fullId: 'diverga:d2', directoryName: 'D2-interview-focus-group-specialist' },
  { shortId: 'd3', fullId: 'diverga:d3', directoryName: 'D3-observation-protocol-designer' },
  { shortId: 'd4', fullId: 'diverga:d4', directoryName: 'D4-measurement-instrument-developer' },

  // Category E: Analysis (5 agents)
  { shortId: 'e1', fullId: 'diverga:e1', directoryName: 'E1-quantitative-analysis-guide' },
  { shortId: 'e2', fullId: 'diverga:e2', directoryName: 'E2-qualitative-coding-specialist' },
  { shortId: 'e3', fullId: 'diverga:e3', directoryName: 'E3-mixed-methods-integration' },
  { shortId: 'e4', fullId: 'diverga:e4', directoryName: 'E4-analysis-code-generator' },
  { shortId: 'e5', fullId: 'diverga:e5', directoryName: 'E5-sensitivity-analysis-designer' },

  // Category F: Quality & Validation (5 agents)
  { shortId: 'f1', fullId: 'diverga:f1', directoryName: 'F1-internal-consistency-checker' },
  { shortId: 'f2', fullId: 'diverga:f2', directoryName: 'F2-checklist-manager' },
  { shortId: 'f3', fullId: 'diverga:f3', directoryName: 'F3-reproducibility-auditor' },
  { shortId: 'f4', fullId: 'diverga:f4', directoryName: 'F4-bias-trustworthiness-detector' },
  { shortId: 'f5', fullId: 'diverga:f5', directoryName: 'F5-humanization-verifier' },

  // Category G: Publication & Communication (6 agents)
  { shortId: 'g1', fullId: 'diverga:g1', directoryName: 'G1-journal-matcher' },
  { shortId: 'g2', fullId: 'diverga:g2', directoryName: 'G2-academic-communicator' },
  { shortId: 'g3', fullId: 'diverga:g3', directoryName: 'G3-peer-review-strategist' },
  { shortId: 'g4', fullId: 'diverga:g4', directoryName: 'G4-preregistration-composer' },
  { shortId: 'g5', fullId: 'diverga:g5', directoryName: 'G5-academic-style-auditor' },
  { shortId: 'g6', fullId: 'diverga:g6', directoryName: 'G6-academic-style-humanizer' },

  // Category H: Specialized Approaches (2 agents)
  { shortId: 'h1', fullId: 'diverga:h1', directoryName: 'H1-ethnographic-research-advisor' },
  { shortId: 'h2', fullId: 'diverga:h2', directoryName: 'H2-action-research-facilitator' },

  // Category I: Systematic Review Automation (4 agents)
  { shortId: 'i0', fullId: 'diverga:i0', directoryName: 'I0-scholar-agent-orchestrator' },
  { shortId: 'i1', fullId: 'diverga:i1', directoryName: 'I1-paper-retrieval-agent' },
  { shortId: 'i2', fullId: 'diverga:i2', directoryName: 'I2-screening-assistant' },
  { shortId: 'i3', fullId: 'diverga:i3', directoryName: 'I3-rag-builder' },
];

// ============================================================
// AGENT METADATA DEFINITIONS
// Static metadata for each agent (tools, model, tier, etc.)
// ============================================================

interface AgentStaticConfig {
  displayName: string;
  description: string;
  model: ModelType;
  tier: TierLevel;
  tools: string[];
  icon: string;
  vsLevel: 'Full' | 'Enhanced' | 'Light';
  vsPhases: number[];
  triggers: string[];
  paradigmAffinity: string[];
  checkpoints: string[];
  creativityModules: string[];
  category: CategoryId;
  categoryName: string;
}

const AGENT_CONFIGS: Record<string, AgentStaticConfig> = {
  // ============================================================
  // CATEGORY A: RESEARCH FOUNDATION (6 agents)
  // ============================================================

  'a1': {
    displayName: 'Research Question Refiner',
    description: 'VS-Enhanced Research Question Refiner - Prevents Mode Collapse and derives differentiated research questions. Enhanced VS 3-Phase process.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'WebSearch'],
    icon: '🎯',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['research question', '연구 질문', 'PICO', 'SPIDER', 'research idea'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-002', 'CP-VS-001', 'CP-VS-003'],
    creativityModules: ['forced-analogy', 'iterative-loop', 'semantic-distance'],
    category: 'A',
    categoryName: 'Research Foundation',
  },

  'a2': {
    displayName: 'Theoretical Framework Architect',
    description: 'VS-Enhanced Theoretical Framework Designer - Prevents Mode Collapse and recommends creative theories. Full VS 5-Phase process.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'WebSearch'],
    icon: '🏛️',
    vsLevel: 'Full',
    vsPhases: [0, 1, 2, 3, 4, 5],
    triggers: ['theoretical framework', '이론적 프레임워크', 'conceptual model', '개념적 모형', 'hypothesis derivation'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-001', 'CP-INIT-002', 'CP-INIT-003', 'CP-VS-001', 'CP-VS-002', 'CP-VS-003'],
    creativityModules: ['forced-analogy', 'iterative-loop', 'semantic-distance', 'temporal-reframing', 'community-simulation'],
    category: 'A',
    categoryName: 'Research Foundation',
  },

  'a3': {
    displayName: "Devil's Advocate",
    description: "VS-Enhanced Devil's Advocate - Prevents Mode Collapse and generates original critiques. Full VS 5-Phase process.",
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep'],
    icon: '😈',
    vsLevel: 'Full',
    vsPhases: [0, 1, 2, 3, 4, 5],
    triggers: ['criticism', 'weakness', 'reviewer 2', 'alternative explanation', 'rebuttal', '비판', '약점'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-001', 'CP-INIT-002', 'CP-INIT-003', 'CP-VS-001', 'CP-VS-002', 'CP-VS-003'],
    creativityModules: ['forced-analogy', 'iterative-loop', 'semantic-distance', 'temporal-reframing', 'community-simulation'],
    category: 'A',
    categoryName: 'Research Foundation',
  },

  'a4': {
    displayName: 'Research Ethics Advisor',
    description: 'VS-Enhanced Research Ethics Advisor - Prevents Mode Collapse with context-adaptive ethical analysis. Enhanced VS 3-Phase process.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep'],
    icon: '⚖️',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['ethics', 'IRB', 'consent', 'informed consent', 'privacy', 'vulnerable populations'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-001', 'CP-INIT-002', 'CP-VS-001'],
    creativityModules: ['forced-analogy', 'semantic-distance'],
    category: 'A',
    categoryName: 'Research Foundation',
  },

  'a5': {
    displayName: 'Paradigm & Worldview Advisor',
    description: 'Paradigm & Worldview Advisor - Philosophical foundations for research design. Covers ontology, epistemology, axiology.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep'],
    icon: '🌐',
    vsLevel: 'Full',
    vsPhases: [0, 1, 2, 3, 4, 5],
    triggers: ['paradigm', '패러다임', 'ontology', 'epistemology', 'worldview', '세계관', 'philosophical foundations'],
    paradigmAffinity: ['qualitative', 'mixed'],
    checkpoints: ['CP-PARADIGM-001', 'CP-PARADIGM-002', 'CP-VS-001', 'CP-VS-002'],
    creativityModules: ['forced-analogy', 'iterative-loop', 'semantic-distance', 'temporal-reframing', 'community-simulation'],
    category: 'A',
    categoryName: 'Research Foundation',
  },

  'a6': {
    displayName: 'Conceptual Framework Visualizer',
    description: 'VS-Enhanced Conceptual Framework Visualization Expert - Generates differentiated academic visualizations.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep', 'Write'],
    icon: '🎨',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['conceptual framework', '개념적 모형', 'theoretical model visualization', 'Discussion figure', 'framework diagram'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-001', 'CP-VS-001'],
    creativityModules: ['semantic-distance'],
    category: 'A',
    categoryName: 'Research Foundation',
  },

  // ============================================================
  // CATEGORY B: LITERATURE & EVIDENCE (5 agents)
  // ============================================================

  'b1': {
    displayName: 'Systematic Literature Scout',
    description: 'VS-Enhanced Literature Review Strategist - Comprehensive support for multiple review methodologies including PRISMA 2020.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep', 'WebSearch', 'Bash'],
    icon: '📚',
    vsLevel: 'Full',
    vsPhases: [0, 1, 2, 3, 4, 5],
    triggers: ['literature review', 'PRISMA', 'systematic review', 'scoping review', 'meta-synthesis'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-001', 'CP-INIT-002', 'CP-INIT-003', 'CP-VS-001', 'CP-VS-002', 'CP-VS-003'],
    creativityModules: ['forced-analogy', 'iterative-loop', 'semantic-distance', 'temporal-reframing', 'community-simulation'],
    category: 'B',
    categoryName: 'Literature & Evidence',
  },

  'b2': {
    displayName: 'Evidence Quality Appraiser',
    description: 'VS-Enhanced Evidence Quality Appraiser - Context-adaptive quality assessment with GRADE, RoB, CASP.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep'],
    icon: '⭐',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['quality appraisal', 'RoB', 'GRADE', 'Newcastle-Ottawa', 'risk of bias', 'methodological quality'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-001', 'CP-INIT-002', 'CP-VS-001'],
    creativityModules: ['forced-analogy', 'semantic-distance'],
    category: 'B',
    categoryName: 'Literature & Evidence',
  },

  'b3': {
    displayName: 'Effect Size Extractor',
    description: 'VS-Enhanced Effect Size Extractor - Optimal effect size strategy with context-appropriate selection.',
    model: 'haiku',
    tier: 'LOW',
    tools: ['Read', 'Glob', 'Grep'],
    icon: '📊',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['effect size', "Cohen's d", "Hedges' g", 'correlation', 'conversion', 'meta-analysis data'],
    paradigmAffinity: ['quantitative'],
    checkpoints: ['CP-INIT-001', 'CP-INIT-002', 'CP-VS-001'],
    creativityModules: ['forced-analogy', 'semantic-distance'],
    category: 'B',
    categoryName: 'Literature & Evidence',
  },

  'b4': {
    displayName: 'Research Radar',
    description: 'VS-Enhanced Research Radar - Differentiated trend analysis for strategic research monitoring.',
    model: 'haiku',
    tier: 'LOW',
    tools: ['Read', 'Glob', 'Grep', 'WebSearch'],
    icon: '📡',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['latest research', 'trends', 'new publications', 'recent papers', 'research developments'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-001', 'CP-INIT-002', 'CP-VS-001'],
    creativityModules: ['forced-analogy', 'semantic-distance'],
    category: 'B',
    categoryName: 'Literature & Evidence',
  },

  'b5': {
    displayName: 'Parallel Document Processor',
    description: 'Parallel Document Processor - High-throughput PDF/document reading with distributed workload.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'Bash'],
    icon: '📄⚡',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 4],
    triggers: ['batch PDF', 'parallel reading', 'multiple documents', 'large files', 'document extraction'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-001', 'CP-PROGRESS-001', 'CP-COMPLETE-001'],
    creativityModules: [],
    category: 'B',
    categoryName: 'Literature & Evidence',
  },

  // ============================================================
  // CATEGORY C: STUDY DESIGN (7 agents)
  // ============================================================

  'c1': {
    displayName: 'Quantitative Design Consultant',
    description: 'VS-Enhanced Quantitative Design Consultant - Creative quantitative design options with context-optimal strategies.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
    icon: '📐',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['RCT', 'quasi-experimental', 'experimental design', 'survey design', 'power analysis', 'sample size', 'factorial design'],
    paradigmAffinity: ['quantitative'],
    checkpoints: ['CP-DESIGN-001', 'CP-DESIGN-002', 'CP-VS-001'],
    creativityModules: ['forced-analogy', 'semantic-distance'],
    category: 'C',
    categoryName: 'Study Design',
  },

  'c2': {
    displayName: 'Qualitative Design Consultant',
    description: 'VS-Enhanced Qualitative Design Consultant - Comprehensive qualitative research design support.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
    icon: '🔮',
    vsLevel: 'Full',
    vsPhases: [0, 1, 2, 3, 4, 5],
    triggers: ['phenomenology', '현상학', 'grounded theory', '근거이론', 'case study', '사례연구', 'narrative inquiry', 'ethnography', 'qualitative design'],
    paradigmAffinity: ['qualitative'],
    checkpoints: ['CP-QUAL-001', 'CP-QUAL-002', 'CP-QUAL-003', 'CP-VS-001', 'CP-VS-002', 'CP-VS-003'],
    creativityModules: ['forced-analogy', 'iterative-loop', 'semantic-distance', 'temporal-reframing', 'community-simulation'],
    category: 'C',
    categoryName: 'Study Design',
  },

  'c3': {
    displayName: 'Mixed Methods Design Consultant',
    description: 'Mixed Methods Design Consultant - Sequential, concurrent, embedded, and multiphase designs with Morse notation.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
    icon: '🔄',
    vsLevel: 'Full',
    vsPhases: [0, 1, 2, 3, 4, 5],
    triggers: ['mixed methods', 'sequential design', 'convergent', 'explanatory', 'exploratory', 'Morse notation'],
    paradigmAffinity: ['mixed'],
    checkpoints: ['CP-MIXED-001', 'CP-MIXED-002', 'CP-MIXED-003', 'CP-VS-001', 'CP-VS-002', 'CP-VS-003'],
    creativityModules: ['forced-analogy', 'iterative-loop', 'semantic-distance', 'temporal-reframing', 'community-simulation'],
    category: 'C',
    categoryName: 'Study Design',
  },

  'c4': {
    displayName: 'Experimental Materials Developer',
    description: 'Experimental Materials Developer - Treatment and control condition design with manipulation checks.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
    icon: '🧪',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['intervention materials', 'experimental materials', 'treatment design', 'manipulation check'],
    paradigmAffinity: ['quantitative'],
    checkpoints: ['CP-DESIGN-001', 'CP-DESIGN-002', 'CP-VS-001'],
    creativityModules: ['forced-analogy', 'semantic-distance'],
    category: 'C',
    categoryName: 'Study Design',
  },

  'c5': {
    displayName: 'Meta-Analysis Master',
    description: 'Meta-Analysis Master - Multi-gate validation, workflow orchestration, Hedges g calculation.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
    icon: '📈',
    vsLevel: 'Full',
    vsPhases: [0, 1, 2, 3, 4, 5],
    triggers: ['meta-analysis', 'pooled effect', 'heterogeneity', 'forest plot', 'funnel plot'],
    paradigmAffinity: ['quantitative'],
    checkpoints: ['CP-META-001', 'CP-META-002', 'CP-META-003', 'CP-VS-001', 'CP-VS-002'],
    creativityModules: ['forced-analogy', 'iterative-loop', 'semantic-distance'],
    category: 'C',
    categoryName: 'Study Design',
  },

  'c6': {
    displayName: 'Data Integrity Guard',
    description: 'Data Integrity Guard - Data completeness, Hedges g calculation, SD recovery for meta-analysis.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep'],
    icon: '🛡️',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['data extraction', 'PDF extract', 'extract data', 'data integrity'],
    paradigmAffinity: ['quantitative'],
    checkpoints: ['CP-DATA-001', 'CP-VS-001'],
    creativityModules: ['semantic-distance'],
    category: 'C',
    categoryName: 'Study Design',
  },

  'c7': {
    displayName: 'Error Prevention Engine',
    description: 'Error Prevention Engine - Pattern detection, anomaly alerts, error prevention for meta-analysis.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep'],
    icon: '⚠️',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['error prevention', 'validation', 'data check', 'anomaly detection'],
    paradigmAffinity: ['quantitative'],
    checkpoints: ['CP-ERROR-001', 'CP-VS-001'],
    creativityModules: ['semantic-distance'],
    category: 'C',
    categoryName: 'Study Design',
  },

  // ============================================================
  // CATEGORY D: DATA COLLECTION (4 agents)
  // ============================================================

  'd1': {
    displayName: 'Sampling Strategy Advisor',
    description: 'Sampling Strategy Advisor - Probability and non-probability sampling with sample size justification.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep', 'Edit'],
    icon: '🎯',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['sampling', 'sample size', "G*Power", 'recruitment', 'theoretical sampling'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-SAMPLING-001', 'CP-VS-001'],
    creativityModules: ['forced-analogy', 'semantic-distance'],
    category: 'D',
    categoryName: 'Data Collection',
  },

  'd2': {
    displayName: 'Interview & Focus Group Specialist',
    description: 'Interview & Focus Group Specialist - Protocol development, probing strategies, transcription guidance.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
    icon: '🎙️',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['interview', 'focus group', 'interview protocol', 'probing questions'],
    paradigmAffinity: ['qualitative', 'mixed'],
    checkpoints: ['CP-INTERVIEW-001', 'CP-INTERVIEW-002', 'CP-VS-001'],
    creativityModules: ['forced-analogy', 'semantic-distance'],
    category: 'D',
    categoryName: 'Data Collection',
  },

  'd3': {
    displayName: 'Observation Protocol Designer',
    description: 'Observation Protocol Designer - Structured observation, field notes, coding schemes.',
    model: 'haiku',
    tier: 'LOW',
    tools: ['Read', 'Glob', 'Grep', 'Edit'],
    icon: '👁️',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['observation', 'field notes', 'participant observation', 'observational study'],
    paradigmAffinity: ['qualitative', 'mixed'],
    checkpoints: ['CP-OBSERVATION-001', 'CP-VS-001'],
    creativityModules: ['forced-analogy', 'semantic-distance'],
    category: 'D',
    categoryName: 'Data Collection',
  },

  'd4': {
    displayName: 'Measurement Instrument Developer',
    description: 'Measurement Instrument Developer - Scale construction, validity evidence, reliability testing.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
    icon: '📏',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['instrument', 'measurement', 'scale development', 'reliability', 'validity'],
    paradigmAffinity: ['quantitative', 'mixed'],
    checkpoints: ['CP-INSTRUMENT-001', 'CP-INSTRUMENT-002', 'CP-VS-001'],
    creativityModules: ['forced-analogy', 'semantic-distance'],
    category: 'D',
    categoryName: 'Data Collection',
  },

  // ============================================================
  // CATEGORY E: ANALYSIS (5 agents)
  // ============================================================

  'e1': {
    displayName: 'Quantitative Analysis Guide',
    description: 'Quantitative Analysis Guide - Statistical methods, SEM, multilevel modeling, meta-analysis techniques.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'Bash', 'Edit'],
    icon: '📈',
    vsLevel: 'Full',
    vsPhases: [0, 1, 2, 3, 4, 5],
    triggers: ['statistical analysis', 'ANOVA', 'regression', 'SEM', 'multilevel modeling'],
    paradigmAffinity: ['quantitative', 'mixed'],
    checkpoints: ['CP-ANALYSIS-001', 'CP-ANALYSIS-002', 'CP-ANALYSIS-003', 'CP-VS-001', 'CP-VS-002', 'CP-VS-003'],
    creativityModules: ['forced-analogy', 'iterative-loop', 'semantic-distance', 'temporal-reframing', 'community-simulation'],
    category: 'E',
    categoryName: 'Analysis',
  },

  'e2': {
    displayName: 'Qualitative Coding Specialist',
    description: 'Qualitative Coding Specialist - Thematic analysis, grounded theory coding, codebook development.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'Edit'],
    icon: '🏷️',
    vsLevel: 'Full',
    vsPhases: [0, 1, 2, 3, 4, 5],
    triggers: ['qualitative coding', 'thematic analysis', 'grounded theory coding', 'NVivo', 'ATLAS.ti'],
    paradigmAffinity: ['qualitative', 'mixed'],
    checkpoints: ['CP-QUAL-ANALYSIS-001', 'CP-QUAL-ANALYSIS-002', 'CP-VS-001', 'CP-VS-002'],
    creativityModules: ['forced-analogy', 'iterative-loop', 'semantic-distance', 'temporal-reframing', 'community-simulation'],
    category: 'E',
    categoryName: 'Analysis',
  },

  'e3': {
    displayName: 'Mixed Methods Integration',
    description: 'Mixed Methods Integration Specialist - Joint displays, data transformation, meta-inference development.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'Edit'],
    icon: '🔗',
    vsLevel: 'Full',
    vsPhases: [0, 1, 2, 3, 4, 5],
    triggers: ['integration', 'joint display', 'mixed methods analysis', 'meta-inference'],
    paradigmAffinity: ['mixed'],
    checkpoints: ['CP-INTEGRATION-001', 'CP-INTEGRATION-002', 'CP-VS-001', 'CP-VS-002'],
    creativityModules: ['forced-analogy', 'iterative-loop', 'semantic-distance', 'temporal-reframing', 'community-simulation'],
    category: 'E',
    categoryName: 'Analysis',
  },

  'e4': {
    displayName: 'Analysis Code Generator',
    description: 'Analysis Code Generator - R, Python, SPSS, Stata, Mplus syntax generation.',
    model: 'haiku',
    tier: 'LOW',
    tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash'],
    icon: '💻',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['R code', 'Python code', 'analysis code', 'SPSS syntax', 'Mplus syntax'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-CODE-001', 'CP-VS-001'],
    creativityModules: ['forced-analogy', 'semantic-distance'],
    category: 'E',
    categoryName: 'Analysis',
  },

  'e5': {
    displayName: 'Sensitivity Analysis Designer',
    description: 'Sensitivity Analysis Designer - Robustness checks, sensitivity analyses for meta-analysis.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep', 'Edit'],
    icon: '🔬',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['sensitivity analysis', 'robustness check', 'leave-one-out'],
    paradigmAffinity: ['quantitative'],
    checkpoints: ['CP-SENSITIVITY-001', 'CP-VS-001'],
    creativityModules: ['semantic-distance'],
    category: 'E',
    categoryName: 'Analysis',
  },

  // ============================================================
  // CATEGORY F: QUALITY & VALIDATION (5 agents)
  // ============================================================

  'f1': {
    displayName: 'Internal Consistency Checker',
    description: 'Internal Consistency Checker - Logical consistency, alignment verification, terminology consistency.',
    model: 'haiku',
    tier: 'LOW',
    tools: ['Read', 'Glob', 'Grep'],
    icon: '✅',
    vsLevel: 'Light',
    vsPhases: [0, 1, 4],
    triggers: ['consistency', 'alignment', 'logical verification'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-001'],
    creativityModules: [],
    category: 'F',
    categoryName: 'Quality & Validation',
  },

  'f2': {
    displayName: 'Checklist Manager',
    description: 'Checklist Manager - PRISMA 2020, CONSORT, STROBE, COREQ, GRAMMS compliance.',
    model: 'haiku',
    tier: 'LOW',
    tools: ['Read', 'Glob', 'Grep'],
    icon: '📋',
    vsLevel: 'Light',
    vsPhases: [0, 1, 4],
    triggers: ['PRISMA', 'CONSORT', 'STROBE', 'COREQ', 'checklist'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-001'],
    creativityModules: [],
    category: 'F',
    categoryName: 'Quality & Validation',
  },

  'f3': {
    displayName: 'Reproducibility Auditor',
    description: 'Reproducibility Auditor - OSF setup, open science practices, data sharing protocols.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep'],
    icon: '🛡️',
    vsLevel: 'Light',
    vsPhases: [0, 1, 4],
    triggers: ['reproducibility', 'OSF', 'open science', 'replication'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-001'],
    creativityModules: [],
    category: 'F',
    categoryName: 'Quality & Validation',
  },

  'f4': {
    displayName: 'Bias & Trustworthiness Detector',
    description: 'Bias & Trustworthiness Detector - p-hacking detection, HARKing, QRP screening, trustworthiness criteria.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep'],
    icon: '🔎',
    vsLevel: 'Full',
    vsPhases: [0, 1, 2, 3, 4, 5],
    triggers: ['bias', 'p-hacking', 'HARKing', 'QRP', 'trustworthiness', 'credibility'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-BIAS-001', 'CP-TRUST-001', 'CP-VS-001', 'CP-VS-002', 'CP-VS-003'],
    creativityModules: ['forced-analogy', 'iterative-loop', 'semantic-distance', 'temporal-reframing', 'community-simulation'],
    category: 'F',
    categoryName: 'Quality & Validation',
  },

  'f5': {
    displayName: 'Humanization Verifier',
    description: 'Humanization Verifier - Citation integrity, statistical accuracy, meaning preservation validation.',
    model: 'haiku',
    tier: 'LOW',
    tools: ['Read', 'Glob', 'Grep'],
    icon: '✅',
    vsLevel: 'Light',
    vsPhases: [0, 1, 4],
    triggers: ['verify humanization', 'check transformation', 'validate changes'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP_HUMANIZATION_VERIFY'],
    creativityModules: [],
    category: 'F',
    categoryName: 'Quality & Validation',
  },

  // ============================================================
  // CATEGORY G: PUBLICATION & COMMUNICATION (6 agents)
  // ============================================================

  'g1': {
    displayName: 'Journal Matcher',
    description: 'Journal Matcher - Journal recommendation, impact factor analysis, scope matching.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep', 'WebSearch'],
    icon: '📝',
    vsLevel: 'Light',
    vsPhases: [0, 1, 4],
    triggers: ['journal', 'where to publish', 'target journal', 'impact factor'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-001'],
    creativityModules: [],
    category: 'G',
    categoryName: 'Publication & Communication',
  },

  'g2': {
    displayName: 'Academic Communicator',
    description: 'Academic Communicator - Abstract writing, plain language summaries, conference presentations.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
    icon: '🎤',
    vsLevel: 'Light',
    vsPhases: [0, 1, 4],
    triggers: ['abstract', 'plain language', 'academic writing', 'manuscript'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-INIT-001'],
    creativityModules: [],
    category: 'G',
    categoryName: 'Publication & Communication',
  },

  'g3': {
    displayName: 'Peer Review Strategist',
    description: 'Peer Review Strategist - Reviewer comment analysis, response letter drafting, revision strategy.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
    icon: '🔄',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['peer review', 'reviewer response', 'revision', 'rebuttal'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP-REVIEW-001', 'CP-VS-001'],
    creativityModules: ['forced-analogy', 'semantic-distance'],
    category: 'G',
    categoryName: 'Publication & Communication',
  },

  'g4': {
    displayName: 'Pre-registration Composer',
    description: 'Pre-registration Composer - OSF pre-registration, AsPredicted templates, registered reports.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
    icon: '📄',
    vsLevel: 'Light',
    vsPhases: [0, 1, 4],
    triggers: ['preregistration', 'OSF', 'pre-register', 'registered report'],
    paradigmAffinity: ['quantitative', 'mixed'],
    checkpoints: ['CP-INIT-001'],
    creativityModules: [],
    category: 'G',
    categoryName: 'Publication & Communication',
  },

  'g5': {
    displayName: 'Academic Style Auditor',
    description: 'Academic Style Auditor - AI pattern detection (24 categories), probability scoring, risk classification.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep'],
    icon: '🔍',
    vsLevel: 'Light',
    vsPhases: [0, 1, 4],
    triggers: ['AI pattern', 'check AI writing', 'style audit', 'AI probability'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP_HUMANIZATION_REVIEW'],
    creativityModules: [],
    category: 'G',
    categoryName: 'Publication & Communication',
  },

  'g6': {
    displayName: 'Academic Style Humanizer',
    description: 'Academic Style Humanizer - Transform AI patterns to natural prose with citation preservation.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
    icon: '✨',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['humanize', 'humanization', 'natural writing', 'reduce AI patterns'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['CP_HUMANIZATION_REVIEW', 'CP_HUMANIZATION_VERIFY'],
    creativityModules: ['semantic-distance'],
    category: 'G',
    categoryName: 'Publication & Communication',
  },

  // ============================================================
  // CATEGORY H: SPECIALIZED APPROACHES (2 agents)
  // ============================================================

  'h1': {
    displayName: 'Ethnographic Research Advisor',
    description: 'Ethnographic Research Advisor - Fieldwork planning, cultural immersion, thick description guidance.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'WebSearch'],
    icon: '🌍',
    vsLevel: 'Full',
    vsPhases: [0, 1, 2, 3, 4, 5],
    triggers: ['ethnography', 'fieldwork', 'participant observation', 'thick description'],
    paradigmAffinity: ['qualitative'],
    checkpoints: ['CP-ETHNO-001', 'CP-ETHNO-002', 'CP-VS-001', 'CP-VS-002', 'CP-VS-003'],
    creativityModules: ['forced-analogy', 'iterative-loop', 'semantic-distance', 'temporal-reframing', 'community-simulation'],
    category: 'H',
    categoryName: 'Specialized Approaches',
  },

  'h2': {
    displayName: 'Action Research Facilitator',
    description: 'Action Research Facilitator - PAR, CBPR, action research cycles, stakeholder collaboration.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
    icon: '🔄',
    vsLevel: 'Light',
    vsPhases: [0, 1, 4],
    triggers: ['action research', 'PAR', 'CBPR', 'participatory', 'practitioner'],
    paradigmAffinity: ['qualitative', 'mixed'],
    checkpoints: ['CP-ACTION-001'],
    creativityModules: [],
    category: 'H',
    categoryName: 'Specialized Approaches',
  },

  // ============================================================
  // CATEGORY I: SYSTEMATIC REVIEW AUTOMATION (4 agents)
  // ============================================================

  'i0': {
    displayName: 'ScholaRAG Pipeline Orchestrator',
    description: 'ScholaRAG Pipeline Orchestrator - Coordinates systematic literature review automation.',
    model: 'opus',
    tier: 'HIGH',
    tools: ['Read', 'Glob', 'Grep', 'Bash', 'Task'],
    icon: '🔬',
    vsLevel: 'Enhanced',
    vsPhases: [0, 1, 2, 4],
    triggers: ['systematic review', 'PRISMA', 'ScholaRAG', '체계적 문헌고찰', '프리즈마', '스콜라랙'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['SCH_DATABASE_SELECTION', 'SCH_SCREENING_CRITERIA', 'SCH_RAG_READINESS', 'SCH_PRISMA_GENERATION'],
    creativityModules: ['forced-analogy', 'semantic-distance'],
    category: 'I',
    categoryName: 'Systematic Review Automation',
  },

  'i1': {
    displayName: 'Paper Retrieval Agent',
    description: 'Paper Retrieval Agent - Multi-database paper fetching from Semantic Scholar, OpenAlex, arXiv.',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep', 'Bash', 'WebFetch'],
    icon: '📄',
    vsLevel: 'Light',
    vsPhases: [0, 1, 4],
    triggers: ['fetch papers', 'retrieve papers', 'database search', '논문 수집', '데이터베이스 검색'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['SCH_DATABASE_SELECTION'],
    creativityModules: [],
    category: 'I',
    categoryName: 'Systematic Review Automation',
  },

  'i2': {
    displayName: 'Screening Assistant',
    description: 'Screening Assistant - AI-PRISMA 6-dimension screening with Groq LLM (100x cheaper).',
    model: 'sonnet',
    tier: 'MEDIUM',
    tools: ['Read', 'Glob', 'Grep', 'Bash'],
    icon: '🔍',
    vsLevel: 'Light',
    vsPhases: [0, 1, 4],
    triggers: ['screen papers', 'inclusion criteria', 'AI screening', '논문 스크리닝', '포함 기준'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['SCH_SCREENING_CRITERIA'],
    creativityModules: [],
    category: 'I',
    categoryName: 'Systematic Review Automation',
  },

  'i3': {
    displayName: 'RAG Builder',
    description: 'RAG Builder - Vector database construction with local embeddings (zero cost).',
    model: 'haiku',
    tier: 'LOW',
    tools: ['Read', 'Glob', 'Grep', 'Bash'],
    icon: '🗄️',
    vsLevel: 'Light',
    vsPhases: [0, 1, 4],
    triggers: ['build RAG', 'vector database', 'PDF download', 'RAG 구축', 'PDF 다운로드'],
    paradigmAffinity: ['quantitative', 'qualitative', 'mixed'],
    checkpoints: ['SCH_RAG_READINESS'],
    creativityModules: [],
    category: 'I',
    categoryName: 'Systematic Review Automation',
  },
};

// ============================================================
// BUILD AGENT CONFIGURATION
// ============================================================

/**
 * Build a complete AgentConfig from static config and SKILL.md
 */
function buildAgentConfig(shortId: string): AgentConfig | null {
  const mapping = AGENT_MAPPINGS.find(m => m.shortId === shortId);
  if (!mapping) {
    console.warn(`Warning: No mapping found for agent ${shortId}`);
    return null;
  }

  const staticConfig = AGENT_CONFIGS[shortId];
  if (!staticConfig) {
    console.warn(`Warning: No static config found for agent ${shortId}`);
    return null;
  }

  // Load prompt from SKILL.md
  const basePrompt = loadAgentPrompt(mapping.directoryName);

  // Build enhanced prompt with VS methodology and checkpoints
  const enhancedPrompt = buildEnhancedPrompt(
    basePrompt,
    staticConfig.vsLevel,
    staticConfig.checkpoints.length > 0
  );

  return {
    name: mapping.fullId,
    displayName: staticConfig.displayName,
    description: staticConfig.description,
    prompt: enhancedPrompt,
    tools: staticConfig.tools,
    model: staticConfig.model,
    defaultModel: staticConfig.model,
    metadata: {
      category: staticConfig.category,
      categoryName: staticConfig.categoryName,
      tier: staticConfig.tier,
      vsLevel: staticConfig.vsLevel,
      vsPhases: staticConfig.vsPhases,
      checkpoints: staticConfig.checkpoints,
      creativityModules: staticConfig.creativityModules,
      triggers: staticConfig.triggers,
      icon: staticConfig.icon,
      paradigmAffinity: staticConfig.paradigmAffinity,
    },
  };
}

// ============================================================
// PUBLIC API
// ============================================================

/**
 * Get all agent definitions as a registry
 * This is the main entry point for the Task tool integration
 */
export function getAgentDefinitions(
  overrides?: Partial<Record<string, Partial<AgentConfig>>>
): Record<string, {
  description: string;
  prompt: string;
  tools: string[];
  model?: ModelType;
  defaultModel?: ModelType;
}> {
  const result: Record<string, {
    description: string;
    prompt: string;
    tools: string[];
    model?: ModelType;
    defaultModel?: ModelType;
  }> = {};

  for (const mapping of AGENT_MAPPINGS) {
    const config = buildAgentConfig(mapping.shortId);
    if (!config) continue;

    const override = overrides?.[mapping.shortId];
    result[mapping.shortId] = {
      description: override?.description ?? config.description,
      prompt: override?.prompt ?? config.prompt,
      tools: override?.tools ?? config.tools,
      model: (override?.model ?? config.model) as ModelType | undefined,
      defaultModel: (override?.defaultModel ?? config.defaultModel) as ModelType | undefined,
    };
  }

  return result;
}

/**
 * Get a single agent configuration by ID
 */
export function getAgent(shortId: string): AgentConfig | null {
  return buildAgentConfig(shortId);
}

/**
 * Get all agent IDs
 */
export function getAgentIds(): string[] {
  return AGENT_MAPPINGS.map(m => m.shortId);
}

/**
 * Get agent mappings
 */
export function getAgentMappings(): AgentIdMapping[] {
  return [...AGENT_MAPPINGS];
}

/**
 * Lookup agent by trigger keyword
 */
export function findAgentByTrigger(keyword: string): AgentConfig | null {
  const lowered = keyword.toLowerCase();
  for (const mapping of AGENT_MAPPINGS) {
    const config = AGENT_CONFIGS[mapping.shortId];
    if (!config) continue;
    if (config.triggers.some(t => t.toLowerCase().includes(lowered))) {
      return buildAgentConfig(mapping.shortId);
    }
  }
  return null;
}

/**
 * Get agents by category
 */
export function getAgentsByCategory(category: CategoryId): AgentConfig[] {
  const result: AgentConfig[] = [];
  for (const mapping of AGENT_MAPPINGS) {
    const config = AGENT_CONFIGS[mapping.shortId];
    if (config && config.category === category) {
      const agent = buildAgentConfig(mapping.shortId);
      if (agent) result.push(agent);
    }
  }
  return result;
}

/**
 * Get agents by tier
 */
export function getAgentsByTier(tier: TierLevel): AgentConfig[] {
  const result: AgentConfig[] = [];
  for (const mapping of AGENT_MAPPINGS) {
    const config = AGENT_CONFIGS[mapping.shortId];
    if (config && config.tier === tier) {
      const agent = buildAgentConfig(mapping.shortId);
      if (agent) result.push(agent);
    }
  }
  return result;
}
