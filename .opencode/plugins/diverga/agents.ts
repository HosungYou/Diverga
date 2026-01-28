/**
 * Diverga Agent Registry
 * Static agent definitions for OpenCode plugin
 */

import type { AgentInfo } from './types';

/**
 * Complete agent registry
 */
export const AGENT_REGISTRY: Record<string, AgentInfo> = {
  // Category A: Research Foundation
  A1: {
    id: 'A1',
    name: 'Research Question Refiner',
    icon: '🔬',
    category: 'A - Research Foundation',
    tier: 'MEDIUM',
    claudeModel: 'sonnet',
    vsLevel: 'Enhanced',
    description: 'VS-Enhanced Research Question Refiner - Prevents Mode Collapse and derives differentiated research questions using PICO/SPIDER frameworks',
    triggers: {
      keywords: ['research question', '연구 질문', 'PICO', 'SPIDER', 'research idea'],
      context: ['research planning', 'proposal writing'],
    },
    checkpoints: ['CP_RESEARCH_DIRECTION', 'CP_VS_001', 'CP_VS_003'],
  },
  A2: {
    id: 'A2',
    name: 'Theoretical Framework Architect',
    icon: '🏛️',
    category: 'A - Research Foundation',
    tier: 'HIGH',
    claudeModel: 'opus',
    vsLevel: 'Full',
    description: 'VS-Enhanced Theoretical Framework Designer - Prevents Mode Collapse and recommends creative theories with full VS 5-Phase process',
    triggers: {
      keywords: ['theoretical framework', '이론적 프레임워크', 'conceptual model', '가설', 'theory'],
      context: ['theory development', 'framework design'],
    },
    checkpoints: ['CP_THEORY_SELECTION', 'CP_VS_001', 'CP_VS_002', 'CP_VS_003'],
  },
  A3: {
    id: 'A3',
    name: "Devil's Advocate",
    icon: '😈',
    category: 'A - Research Foundation',
    tier: 'MEDIUM',
    claudeModel: 'sonnet',
    vsLevel: 'Full',
    description: "VS-Enhanced Devil's Advocate - Prevents Mode Collapse and generates original critiques with Full VS 5-Phase process",
    triggers: {
      keywords: ['criticism', 'weakness', 'reviewer 2', 'alternative explanation', 'rebuttal', '비판', '약점'],
      context: ['research review', 'stress testing'],
    },
    checkpoints: ['CP_VS_001', 'CP_VS_003'],
  },
  A4: {
    id: 'A4',
    name: 'Research Ethics Advisor',
    icon: '⚖️',
    category: 'A - Research Foundation',
    tier: 'MEDIUM',
    claudeModel: 'sonnet',
    vsLevel: 'Enhanced',
    description: 'VS-Enhanced Research Ethics Advisor - Context-adaptive ethical analysis with Enhanced VS 3-Phase process',
    triggers: {
      keywords: ['ethics', 'IRB', 'consent', 'informed consent', 'privacy', 'vulnerable populations'],
      context: ['ethics review', 'IRB preparation'],
    },
    checkpoints: [],
  },
  A5: {
    id: 'A5',
    name: 'Paradigm & Worldview Advisor',
    icon: '🌍',
    category: 'A - Research Foundation',
    tier: 'HIGH',
    claudeModel: 'opus',
    vsLevel: 'Enhanced',
    description: 'Paradigm and Worldview Advisor - Philosophical foundations for research design covering ontology, epistemology, and axiology',
    triggers: {
      keywords: ['paradigm', '패러다임', 'ontology', 'epistemology', 'worldview', '세계관'],
      context: ['research philosophy', 'paradigm selection'],
    },
    checkpoints: ['CP_PARADIGM_SELECTION'],
  },
  A6: {
    id: 'A6',
    name: 'Conceptual Framework Visualizer',
    icon: '🎨',
    category: 'A - Research Foundation',
    tier: 'HIGH',
    claudeModel: 'opus',
    vsLevel: 'Full',
    description: 'VS-Enhanced Conceptual Framework Visualization Expert - Generates differentiated academic visualizations',
    triggers: {
      keywords: ['conceptual framework', '개념적 모형', 'theoretical model visualization', 'framework diagram'],
      context: ['visualization', 'model design'],
    },
    checkpoints: ['CP_VISUALIZATION_PREFERENCE'],
  },

  // Category B: Literature & Evidence
  B1: {
    id: 'B1',
    name: 'Literature Review Strategist',
    icon: '📚',
    category: 'B - Literature & Evidence',
    tier: 'MEDIUM',
    claudeModel: 'sonnet',
    vsLevel: 'Full',
    description: 'VS-Enhanced Literature Review Strategist - Comprehensive support for multiple review methodologies including PRISMA 2020',
    triggers: {
      keywords: ['literature review', 'PRISMA', 'systematic review', 'scoping review', '선행연구'],
      context: ['literature search', 'review methodology'],
    },
    checkpoints: ['CP_SCREENING_CRITERIA', 'CP_SEARCH_STRATEGY', 'CP_VS_001'],
  },
  B2: {
    id: 'B2',
    name: 'Evidence Quality Appraiser',
    icon: '🔍',
    category: 'B - Literature & Evidence',
    tier: 'MEDIUM',
    claudeModel: 'sonnet',
    vsLevel: 'Enhanced',
    description: 'VS-Enhanced Evidence Quality Appraiser - Context-adaptive quality assessment with GRADE, RoB, CASP',
    triggers: {
      keywords: ['quality appraisal', 'RoB', 'GRADE', 'risk of bias', 'methodological quality'],
      context: ['quality assessment', 'evidence grading'],
    },
    checkpoints: ['CP_QUALITY_REVIEW'],
  },
  B3: {
    id: 'B3',
    name: 'Effect Size Extractor',
    icon: '📊',
    category: 'B - Literature & Evidence',
    tier: 'LOW',
    claudeModel: 'haiku',
    vsLevel: 'Enhanced',
    description: 'VS-Enhanced Effect Size Extractor - Optimal effect size strategy with context-appropriate selection',
    triggers: {
      keywords: ['effect size', "Cohen's d", "Hedges' g", 'correlation', 'conversion'],
      context: ['effect size calculation', 'data extraction'],
    },
    checkpoints: [],
  },
  B4: {
    id: 'B4',
    name: 'Research Radar',
    icon: '📡',
    category: 'B - Literature & Evidence',
    tier: 'LOW',
    claudeModel: 'haiku',
    vsLevel: 'Enhanced',
    description: 'VS-Enhanced Research Radar - Differentiated trend analysis for strategic research monitoring',
    triggers: {
      keywords: ['latest research', 'trends', 'new publications', 'recent papers'],
      context: ['trend tracking', 'current literature'],
    },
    checkpoints: [],
  },

  // Category C: Study Design
  C1: {
    id: 'C1',
    name: 'Quantitative Design Consultant',
    icon: '📈',
    category: 'C - Study Design',
    tier: 'HIGH',
    claudeModel: 'opus',
    vsLevel: 'Enhanced',
    description: 'VS-Enhanced Quantitative Design Consultant - Creative quantitative design options with context-optimal strategies',
    triggers: {
      keywords: ['RCT', 'quasi-experimental', 'experimental design', 'survey design', 'power analysis'],
      context: ['quantitative research', 'experimental design'],
    },
    checkpoints: ['CP_METHODOLOGY_APPROVAL', 'CP_VS_001', 'CP_VS_003'],
  },
  C2: {
    id: 'C2',
    name: 'Qualitative Design Consultant',
    icon: '🎙️',
    category: 'C - Study Design',
    tier: 'HIGH',
    claudeModel: 'opus',
    vsLevel: 'Full',
    description: 'VS-Enhanced Qualitative Design Consultant - Comprehensive qualitative research design support',
    triggers: {
      keywords: ['phenomenology', '현상학', 'grounded theory', '근거이론', 'case study', '사례연구'],
      context: ['qualitative research', 'methodology selection'],
    },
    checkpoints: ['CP_PARADIGM_SELECTION', 'CP_METHODOLOGY_APPROVAL', 'CP_VS_001'],
  },
  C3: {
    id: 'C3',
    name: 'Mixed Methods Design Consultant',
    icon: '🔀',
    category: 'C - Study Design',
    tier: 'HIGH',
    claudeModel: 'opus',
    vsLevel: 'Full',
    description: 'Mixed Methods Design Consultant - Sequential, concurrent, embedded, and multiphase designs with Morse notation',
    triggers: {
      keywords: ['mixed methods', '혼합방법', 'sequential', 'convergent', 'embedded'],
      context: ['mixed methods', 'integration design'],
    },
    checkpoints: ['CP_PARADIGM_SELECTION', 'CP_METHODOLOGY_APPROVAL', 'CP_INTEGRATION_STRATEGY'],
  },
  C5: {
    id: 'C5',
    name: 'Meta-Analysis Master',
    icon: '📊',
    category: 'C - Study Design',
    tier: 'HIGH',
    claudeModel: 'opus',
    vsLevel: 'Full',
    description: 'Meta-Analysis Master - Multi-gate validation, workflow orchestration, Hedges g calculation',
    triggers: {
      keywords: ['meta-analysis', '메타분석', 'MASEM', 'forest plot', 'heterogeneity'],
      context: ['meta-analysis', 'effect pooling'],
    },
    checkpoints: ['CP_METHODOLOGY_APPROVAL', 'CP_ANALYSIS_PLAN'],
  },

  // Category E: Analysis
  E1: {
    id: 'E1',
    name: 'Quantitative Analysis Guide',
    icon: '🔢',
    category: 'E - Analysis',
    tier: 'HIGH',
    claudeModel: 'opus',
    vsLevel: 'Full',
    description: 'Quantitative Analysis Guide - Statistical methods, SEM, multilevel modeling, meta-analysis techniques',
    triggers: {
      keywords: ['statistical analysis', 'regression', 'SEM', 'ANOVA', 'multilevel', '통계 분석'],
      context: ['quantitative analysis', 'statistical methods'],
    },
    checkpoints: ['CP_ANALYSIS_PLAN'],
  },
  E2: {
    id: 'E2',
    name: 'Qualitative Coding Specialist',
    icon: '🏷️',
    category: 'E - Analysis',
    tier: 'MEDIUM',
    claudeModel: 'sonnet',
    vsLevel: 'Full',
    description: 'Qualitative Coding Specialist - Thematic analysis, grounded theory coding, codebook development',
    triggers: {
      keywords: ['thematic analysis', 'coding', 'codebook', '질적 분석'],
      context: ['qualitative analysis', 'coding process'],
    },
    checkpoints: ['CP_CODING_APPROACH', 'CP_THEME_VALIDATION'],
  },
  E3: {
    id: 'E3',
    name: 'Mixed Methods Integration Specialist',
    icon: '🔗',
    category: 'E - Analysis',
    tier: 'HIGH',
    claudeModel: 'opus',
    vsLevel: 'Full',
    description: 'Mixed Methods Integration Specialist - Joint displays, data transformation, meta-inference development',
    triggers: {
      keywords: ['joint display', 'data transformation', 'meta-inference', 'integration'],
      context: ['mixed methods integration', 'data merging'],
    },
    checkpoints: ['CP_INTEGRATION_STRATEGY'],
  },
  E4: {
    id: 'E4',
    name: 'Analysis Code Generator',
    icon: '💻',
    category: 'E - Analysis',
    tier: 'LOW',
    claudeModel: 'haiku',
    vsLevel: 'Light',
    description: 'Analysis Code Generator - R, Python, SPSS, Stata, Mplus syntax generation',
    triggers: {
      keywords: ['R code', 'Python code', 'SPSS syntax', 'Stata', '분석 코드'],
      context: ['code generation', 'analysis scripts'],
    },
    checkpoints: [],
  },

  // Category G: Publication
  G3: {
    id: 'G3',
    name: 'Peer Review Strategist',
    icon: '👥',
    category: 'G - Publication & Communication',
    tier: 'HIGH',
    claudeModel: 'opus',
    vsLevel: 'Enhanced',
    description: 'Peer Review Strategist - Reviewer comment analysis, response letter drafting, revision strategy',
    triggers: {
      keywords: ['reviewer', 'peer review', 'revision', 'response letter', '리뷰어 대응'],
      context: ['peer review', 'revision response'],
    },
    checkpoints: [],
  },

  // Category H: Specialized
  H1: {
    id: 'H1',
    name: 'Ethnographic Research Advisor',
    icon: '🌐',
    category: 'H - Specialized Approaches',
    tier: 'HIGH',
    claudeModel: 'opus',
    vsLevel: 'Full',
    description: 'Ethnographic Research Advisor - Fieldwork planning, cultural immersion, thick description guidance',
    triggers: {
      keywords: ['ethnography', 'fieldwork', 'participant observation', '문화기술지'],
      context: ['ethnographic research', 'cultural studies'],
    },
    checkpoints: ['CP_METHODOLOGY_APPROVAL'],
  },
  H2: {
    id: 'H2',
    name: 'Action Research Facilitator',
    icon: '🎬',
    category: 'H - Specialized Approaches',
    tier: 'HIGH',
    claudeModel: 'opus',
    vsLevel: 'Light',
    description: 'Action Research Facilitator - PAR, CBPR, action research cycles, stakeholder collaboration',
    triggers: {
      keywords: ['action research', 'PAR', 'CBPR', 'participatory', '실행연구'],
      context: ['action research', 'participatory research'],
    },
    checkpoints: ['CP_METHODOLOGY_APPROVAL'],
  },
};

/**
 * Get agent by ID
 */
export function getAgent(agentId: string): AgentInfo | null {
  return AGENT_REGISTRY[agentId.toUpperCase()] || null;
}

/**
 * List all agents
 */
export function listAgents(): AgentInfo[] {
  return Object.values(AGENT_REGISTRY);
}

/**
 * Get agents by category
 */
export function getAgentsByCategory(category: string): AgentInfo[] {
  return Object.values(AGENT_REGISTRY).filter(
    agent => agent.category === category || agent.category.startsWith(category)
  );
}

/**
 * Get agents by tier
 */
export function getAgentsByTier(tier: 'HIGH' | 'MEDIUM' | 'LOW'): AgentInfo[] {
  return Object.values(AGENT_REGISTRY).filter(agent => agent.tier === tier);
}

export default AGENT_REGISTRY;
