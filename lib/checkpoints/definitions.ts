/**
 * Diverga Checkpoint Definitions
 * Human checkpoint system for research workflow control
 */

import type { CheckpointDefinition, CheckpointLevel, AgentId } from '../agents/types';

/**
 * All checkpoint definitions
 */
export const CHECKPOINTS: CheckpointDefinition[] = [
  // ============================================
  // REQUIRED CHECKPOINTS (🔴 MANDATORY HALT)
  // ============================================
  {
    id: 'CP_RESEARCH_DIRECTION',
    name: 'Research Direction',
    level: 'REQUIRED',
    when: 'Research question finalized',
    whatToAsk: '연구 방향이 결정되었습니다. 이 방향으로 진행해도 될까요? / Research direction confirmed. Should we proceed?',
    icon: '🔴',
    category: 'Research Foundation',
    agentsUsing: ['A1', 'A2'],
  },
  {
    id: 'CP_PARADIGM_SELECTION',
    name: 'Paradigm Selection',
    level: 'REQUIRED',
    when: 'Methodology approach decision',
    whatToAsk: '연구 패러다임을 선택해 주세요: 양적/질적/혼합 / Please select research paradigm: quantitative/qualitative/mixed',
    icon: '🔴',
    category: 'Research Foundation',
    agentsUsing: ['A5', 'C1', 'C2', 'C3'],
  },
  {
    id: 'CP_THEORY_SELECTION',
    name: 'Theory Selection',
    level: 'REQUIRED',
    when: 'Framework chosen',
    whatToAsk: '이론적 프레임워크를 선택해 주세요 / Please select theoretical framework',
    icon: '🔴',
    category: 'Research Foundation',
    agentsUsing: ['A2'],
  },
  {
    id: 'CP_METHODOLOGY_APPROVAL',
    name: 'Methodology Approval',
    level: 'REQUIRED',
    when: 'Design complete',
    whatToAsk: '연구 방법론을 승인해 주세요 / Please approve the research methodology',
    icon: '🔴',
    category: 'Study Design',
    agentsUsing: ['C1', 'C2', 'C3', 'C4'],
  },

  // ============================================
  // RECOMMENDED CHECKPOINTS (🟠 SUGGESTED HALT)
  // ============================================
  {
    id: 'CP_ANALYSIS_PLAN',
    name: 'Analysis Plan',
    level: 'RECOMMENDED',
    when: 'Before analysis',
    whatToAsk: '분석 계획을 검토해 주시겠습니까? / Would you like to review the analysis plan?',
    icon: '🟠',
    category: 'Analysis',
    agentsUsing: ['E1', 'E2', 'E3', 'E4'],
  },
  {
    id: 'CP_INTEGRATION_STRATEGY',
    name: 'Integration Strategy',
    level: 'RECOMMENDED',
    when: 'Mixed methods only',
    whatToAsk: '통합 전략을 확인해 주세요 / Please confirm the integration strategy',
    icon: '🟠',
    category: 'Analysis',
    agentsUsing: ['C3', 'E3'],
  },
  {
    id: 'CP_QUALITY_REVIEW',
    name: 'Quality Review',
    level: 'RECOMMENDED',
    when: 'Assessment done',
    whatToAsk: '품질 평가 결과를 검토해 주세요 / Please review the quality assessment results',
    icon: '🟠',
    category: 'Quality & Validation',
    agentsUsing: ['B2', 'F1', 'F2', 'F3', 'F4'],
  },
  {
    id: 'CP_SCREENING_CRITERIA',
    name: 'Screening Criteria',
    level: 'RECOMMENDED',
    when: 'Inclusion/exclusion criteria set',
    whatToAsk: '선정/배제 기준을 확인해 주세요 / Please confirm inclusion/exclusion criteria',
    icon: '🟠',
    category: 'Literature & Evidence',
    agentsUsing: ['B1', 'B2'],
  },
  {
    id: 'CP_SAMPLING_STRATEGY',
    name: 'Sampling Strategy',
    level: 'RECOMMENDED',
    when: 'Sample determined',
    whatToAsk: '표본 전략을 승인해 주세요 / Please approve the sampling strategy',
    icon: '🟠',
    category: 'Data Collection',
    agentsUsing: ['D1', 'D2'],
  },
  {
    id: 'CP_CODING_APPROACH',
    name: 'Coding Approach',
    level: 'RECOMMENDED',
    when: 'Qualitative coding setup',
    whatToAsk: '코딩 접근법을 확인해 주세요 / Please confirm the coding approach',
    icon: '🟠',
    category: 'Analysis',
    agentsUsing: ['E2'],
  },
  {
    id: 'CP_THEME_VALIDATION',
    name: 'Theme Validation',
    level: 'RECOMMENDED',
    when: 'Themes identified',
    whatToAsk: '도출된 주제를 검증해 주세요 / Please validate the identified themes',
    icon: '🟠',
    category: 'Analysis',
    agentsUsing: ['E2', 'E3'],
  },

  // ============================================
  // OPTIONAL CHECKPOINTS (🟡 DEFAULTS AVAILABLE)
  // ============================================
  {
    id: 'CP_VISUALIZATION_PREFERENCE',
    name: 'Visualization Preference',
    level: 'OPTIONAL',
    when: 'Before generating visuals',
    whatToAsk: '시각화 스타일을 선택해 주세요 / Please select visualization style',
    icon: '🟡',
    category: 'Publication & Communication',
    agentsUsing: ['G2'],
  },
  {
    id: 'CP_SEARCH_STRATEGY',
    name: 'Search Strategy',
    level: 'OPTIONAL',
    when: 'Database selection',
    whatToAsk: '검색 전략을 확인해 주세요 / Please confirm search strategy',
    icon: '🟡',
    category: 'Literature & Evidence',
    agentsUsing: ['B1', 'B4'],
  },
  {
    id: 'CP_WRITING_STYLE',
    name: 'Writing Style',
    level: 'OPTIONAL',
    when: 'Before writing output',
    whatToAsk: '작성 스타일을 선택해 주세요 / Please select writing style',
    icon: '🟡',
    category: 'Publication & Communication',
    agentsUsing: ['G1', 'G2', 'G3', 'G4'],
  },
  {
    id: 'CP_PROTOCOL_DESIGN',
    name: 'Protocol Design',
    level: 'OPTIONAL',
    when: 'Interview/observation protocol',
    whatToAsk: '프로토콜 설계를 확인해 주세요 / Please confirm protocol design',
    icon: '🟡',
    category: 'Data Collection',
    agentsUsing: ['D2', 'D3'],
  },

  // ============================================
  // VS-SPECIFIC CHECKPOINTS
  // ============================================
  {
    id: 'CP_VS_001',
    name: 'VS Direction Selection',
    level: 'REQUIRED',
    when: 'After VS alternatives presented',
    whatToAsk: '어떤 방향으로 진행하시겠습니까? (A/B/C) / Which direction would you like to proceed? (A/B/C)',
    icon: '🔴',
    category: 'VS Methodology',
    agentsUsing: ['A1', 'A2', 'A3', 'B1', 'C1', 'C2', 'C3'],
  },
  {
    id: 'CP_VS_002',
    name: 'VS Risk Warning',
    level: 'RECOMMENDED',
    when: 'When T < 0.3 selected',
    whatToAsk: '선택하신 옵션의 T-Score가 낮습니다 (T < 0.3). 계속하시겠습니까? / Selected option has low T-Score (T < 0.3). Continue?',
    icon: '🟠',
    category: 'VS Methodology',
    agentsUsing: ['A2', 'A3', 'B1'],
  },
  {
    id: 'CP_VS_003',
    name: 'VS Final Confirmation',
    level: 'REQUIRED',
    when: 'Before executing selected option',
    whatToAsk: '선택하신 방향으로 진행합니다. 확인하시겠습니까? / Proceeding with selected direction. Confirm?',
    icon: '🔴',
    category: 'VS Methodology',
    agentsUsing: ['A1', 'A2', 'C1', 'C2', 'C3'],
  },

  // ============================================
  // INITIALIZATION CHECKPOINTS
  // ============================================
  {
    id: 'CP_INIT_001',
    name: 'Research Type Selection',
    level: 'REQUIRED',
    when: 'At project start',
    whatToAsk: '연구 유형을 선택해 주세요: 양적/질적/혼합/메타분석 / Please select research type',
    icon: '🔴',
    category: 'Initialization',
    agentsUsing: [],
  },
  {
    id: 'CP_INIT_002',
    name: 'Creativity Level Selection',
    level: 'OPTIONAL',
    when: 'At project start',
    whatToAsk: '창의성 수준을 선택해 주세요: Conservative/Balanced/Innovative/Extreme',
    icon: '🟡',
    category: 'Initialization',
    agentsUsing: [],
  },
  {
    id: 'CP_INIT_003',
    name: 'T-Score Mode Selection',
    level: 'OPTIONAL',
    when: 'At project start',
    whatToAsk: 'T-Score 모드를 선택해 주세요: Static/Dynamic/Hybrid',
    icon: '🟡',
    category: 'Initialization',
    agentsUsing: [],
  },
];

/**
 * Get checkpoint by ID
 */
export function getCheckpoint(id: string): CheckpointDefinition | undefined {
  return CHECKPOINTS.find(cp => cp.id === id);
}

/**
 * Get checkpoints by level
 */
export function getCheckpointsByLevel(level: CheckpointLevel): CheckpointDefinition[] {
  return CHECKPOINTS.filter(cp => cp.level === level);
}

/**
 * Get checkpoints for an agent
 */
export function getCheckpointsForAgent(agentId: AgentId): CheckpointDefinition[] {
  return CHECKPOINTS.filter(cp => cp.agentsUsing.includes(agentId));
}

/**
 * Get checkpoints by category
 */
export function getCheckpointsByCategory(category: string): CheckpointDefinition[] {
  return CHECKPOINTS.filter(cp => cp.category === category);
}

/**
 * Validate a checkpoint is satisfied
 */
export function validateCheckpoint(
  checkpointId: string,
  userResponse: string | null
): { valid: boolean; message: string } {
  const checkpoint = getCheckpoint(checkpointId);

  if (!checkpoint) {
    return { valid: false, message: `Unknown checkpoint: ${checkpointId}` };
  }

  if (checkpoint.level === 'REQUIRED' && !userResponse) {
    return {
      valid: false,
      message: `${checkpoint.icon} ${checkpoint.name}: Requires explicit user approval`,
    };
  }

  if (checkpoint.level === 'RECOMMENDED' && !userResponse) {
    return {
      valid: true,
      message: `${checkpoint.icon} ${checkpoint.name}: Proceeding without explicit approval (recommended)`,
    };
  }

  return {
    valid: true,
    message: `${checkpoint.icon} ${checkpoint.name}: Approved`,
  };
}

/**
 * Format checkpoint prompt for display
 */
export function formatCheckpointPrompt(checkpoint: CheckpointDefinition): string {
  return `
${checkpoint.icon} **${checkpoint.name}** (${checkpoint.level})

${checkpoint.whatToAsk}

_When: ${checkpoint.when}_
`;
}

/**
 * Get all required checkpoints that must be satisfied
 */
export function getRequiredCheckpoints(): CheckpointDefinition[] {
  return CHECKPOINTS.filter(cp => cp.level === 'REQUIRED');
}

/**
 * Export checkpoints as YAML-compatible object
 */
export function exportCheckpointsAsYaml(): string {
  const yaml: string[] = ['checkpoints:'];

  for (const cp of CHECKPOINTS) {
    yaml.push(`  ${cp.id}:`);
    yaml.push(`    name: "${cp.name}"`);
    yaml.push(`    level: ${cp.level}`);
    yaml.push(`    when: "${cp.when}"`);
    yaml.push(`    icon: "${cp.icon}"`);
    yaml.push(`    category: "${cp.category}"`);
    yaml.push(`    agents: [${cp.agentsUsing.map(a => `"${a}"`).join(', ')}]`);
    yaml.push('');
  }

  return yaml.join('\n');
}
