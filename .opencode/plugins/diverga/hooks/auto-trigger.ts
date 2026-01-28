/**
 * Auto-Trigger Hook
 * Detects keywords in user prompts and activates appropriate agents
 */

import type { AgentInfo } from '../types';
import { AGENT_REGISTRY, getAgent } from '../agents';

/**
 * Keyword to agent mapping with priority
 */
const KEYWORD_TRIGGERS: Array<{
  keywords: string[];
  agentId: string;
  priority: number;
}> = [
  // Category A: Research Foundation
  {
    keywords: ['research question', '연구 질문', 'pico', 'spider', 'research idea', '연구 아이디어'],
    agentId: 'A1',
    priority: 1,
  },
  {
    keywords: ['theoretical framework', '이론적 프레임워크', 'conceptual model', '개념적 모형', 'theory selection'],
    agentId: 'A2',
    priority: 1,
  },
  {
    keywords: ["devil's advocate", 'criticism', 'weakness', 'reviewer 2', 'reviewer critique', '비판', '약점'],
    agentId: 'A3',
    priority: 2,
  },
  {
    keywords: ['ethics', 'irb', 'consent', 'informed consent', '윤리', '동의서'],
    agentId: 'A4',
    priority: 2,
  },
  {
    keywords: ['paradigm', '패러다임', 'worldview', 'epistemology', 'ontology', '세계관'],
    agentId: 'A5',
    priority: 1,
  },
  {
    keywords: ['conceptual framework', 'framework visualization', 'model diagram', '개념도'],
    agentId: 'A6',
    priority: 2,
  },

  // Category B: Literature & Evidence
  {
    keywords: ['literature review', '문헌 검토', 'prisma', 'systematic review', 'scoping review', '선행연구'],
    agentId: 'B1',
    priority: 1,
  },
  {
    keywords: ['quality appraisal', 'rob', 'grade', 'risk of bias', '품질 평가'],
    agentId: 'B2',
    priority: 2,
  },
  {
    keywords: ['effect size', "cohen's d", "hedges' g", '효과크기', 'effect extraction'],
    agentId: 'B3',
    priority: 2,
  },
  {
    keywords: ['recent publications', 'research trends', 'new papers', '최신 연구'],
    agentId: 'B4',
    priority: 3,
  },

  // Category C: Study Design
  {
    keywords: ['experimental design', 'rct', 'quasi-experimental', '실험 설계', 'quantitative design'],
    agentId: 'C1',
    priority: 1,
  },
  {
    keywords: ['phenomenology', '현상학', 'grounded theory', '근거이론', 'case study', '사례연구', 'qualitative design'],
    agentId: 'C2',
    priority: 1,
  },
  {
    keywords: ['mixed methods', '혼합방법', 'convergent', 'sequential', 'embedded design'],
    agentId: 'C3',
    priority: 1,
  },
  {
    keywords: ['meta-analysis', '메타분석', 'masem', 'pooled effect', 'heterogeneity'],
    agentId: 'C5',
    priority: 1,
  },

  // Category D: Data Collection
  {
    keywords: ['sampling', 'sample size', '표본', 'participant selection'],
    agentId: 'D1',
    priority: 2,
  },
  {
    keywords: ['interview', 'focus group', '면담', '초점집단', 'interview protocol'],
    agentId: 'D2',
    priority: 2,
  },
  {
    keywords: ['observation', 'field notes', '관찰', 'observation protocol'],
    agentId: 'D3',
    priority: 3,
  },
  {
    keywords: ['scale development', 'instrument', 'measurement', '척도 개발', 'validity'],
    agentId: 'D4',
    priority: 2,
  },

  // Category E: Analysis
  {
    keywords: ['statistical analysis', 'regression', 'sem', 'anova', '통계 분석', 'multilevel'],
    agentId: 'E1',
    priority: 1,
  },
  {
    keywords: ['thematic analysis', 'coding', '주제 분석', 'qualitative coding', '질적 분석'],
    agentId: 'E2',
    priority: 1,
  },
  {
    keywords: ['joint display', 'integration', 'meta-inference', '통합 분석'],
    agentId: 'E3',
    priority: 2,
  },
  {
    keywords: ['r code', 'python code', 'spss', 'stata', '분석 코드'],
    agentId: 'E4',
    priority: 3,
  },

  // Category F: Quality & Validation
  {
    keywords: ['consistency check', '일관성', 'alignment verification'],
    agentId: 'F1',
    priority: 3,
  },
  {
    keywords: ['consort', 'strobe', 'coreq', 'checklist', '보고 지침'],
    agentId: 'F2',
    priority: 3,
  },
  {
    keywords: ['osf', 'open science', 'reproducibility', '재현성'],
    agentId: 'F3',
    priority: 3,
  },
  {
    keywords: ['bias detection', 'trustworthiness', 'p-hacking', '편향'],
    agentId: 'F4',
    priority: 2,
  },

  // Category G: Publication
  {
    keywords: ['journal selection', 'impact factor', '저널 선택', 'where to publish'],
    agentId: 'G1',
    priority: 3,
  },
  {
    keywords: ['abstract', 'plain language', '초록', 'summary'],
    agentId: 'G2',
    priority: 3,
  },
  {
    keywords: ['reviewer response', 'peer review', 'revision', '리뷰어 대응'],
    agentId: 'G3',
    priority: 2,
  },
  {
    keywords: ['pre-registration', 'aspredicted', '사전등록'],
    agentId: 'G4',
    priority: 3,
  },

  // Category H: Specialized
  {
    keywords: ['ethnography', 'fieldwork', '문화기술지', 'participant observation'],
    agentId: 'H1',
    priority: 1,
  },
  {
    keywords: ['action research', 'par', 'cbpr', '실행연구'],
    agentId: 'H2',
    priority: 1,
  },
];

/**
 * Detect agent from prompt text
 */
export function autoTrigger(prompt: string): AgentInfo | null {
  const lowerPrompt = prompt.toLowerCase();

  // Find all matching triggers
  const matches: Array<{ agentId: string; priority: number; matchCount: number }> = [];

  for (const trigger of KEYWORD_TRIGGERS) {
    let matchCount = 0;
    for (const keyword of trigger.keywords) {
      if (lowerPrompt.includes(keyword.toLowerCase())) {
        matchCount++;
      }
    }

    if (matchCount > 0) {
      matches.push({
        agentId: trigger.agentId,
        priority: trigger.priority,
        matchCount,
      });
    }
  }

  if (matches.length === 0) {
    return null;
  }

  // Sort by: 1) match count (desc), 2) priority (asc)
  matches.sort((a, b) => {
    if (b.matchCount !== a.matchCount) {
      return b.matchCount - a.matchCount;
    }
    return a.priority - b.priority;
  });

  // Get the best match
  const bestMatch = matches[0];
  return getAgent(bestMatch.agentId);
}

/**
 * Get all triggered agents (for multi-agent scenarios)
 */
export function getAllTriggeredAgents(prompt: string): AgentInfo[] {
  const lowerPrompt = prompt.toLowerCase();
  const triggered: Set<string> = new Set();

  for (const trigger of KEYWORD_TRIGGERS) {
    for (const keyword of trigger.keywords) {
      if (lowerPrompt.includes(keyword.toLowerCase())) {
        triggered.add(trigger.agentId);
        break;
      }
    }
  }

  return Array.from(triggered)
    .map(id => getAgent(id))
    .filter((agent): agent is AgentInfo => agent !== null);
}

/**
 * Check if specific agent should be triggered
 */
export function shouldTriggerAgent(prompt: string, agentId: string): boolean {
  const lowerPrompt = prompt.toLowerCase();
  const trigger = KEYWORD_TRIGGERS.find(t => t.agentId === agentId);

  if (!trigger) return false;

  return trigger.keywords.some(keyword =>
    lowerPrompt.includes(keyword.toLowerCase())
  );
}

/**
 * Get trigger keywords for an agent
 */
export function getTriggerKeywords(agentId: string): string[] {
  const trigger = KEYWORD_TRIGGERS.find(t => t.agentId === agentId);
  return trigger?.keywords || [];
}
