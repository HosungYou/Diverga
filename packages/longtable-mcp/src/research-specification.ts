import type { QuestionOption } from "@longtable/core";

export interface ResearchSpecification {
  title: string;
  status?: "draft" | "confirmed" | "deferred";
  createdAt?: string;
  updatedAt?: string;
  sourceHookId?: string;
  researchDirection: {
    question?: string;
    purpose: string;
    scopeBoundary?: string;
    inclusionCriteria?: string[];
    exclusionCriteria?: string[];
  };
  constructOntology: {
    coreConstructs: string[];
    distinctions: string[];
    termsToAvoidCollapsing?: string[];
  };
  theoryAndFraming: {
    anchors: string[];
    alternatives?: string[];
    overreachRisks?: string[];
  };
  measurementCoding: {
    variablesOrConstructs: string[];
    evidenceTypes: string[];
    codingRules: string[];
    openStandards?: string[];
  };
  methodAnalysis: {
    design?: string;
    analysisOptions: string[];
    dataSufficiencyCriteria?: string[];
    unsettledChoices?: string[];
  };
  evidenceAccess: {
    requiredSources?: string[];
    accessRequirements?: string[];
    evidenceStandards?: string[];
  };
  epistemicAlignment: {
    researcherKnowledge?: string[];
    projectStatePriority?: string[];
    aiInferenceLimits?: string[];
    conflictResolutionRule?: string;
  };
  protectedDecisions: string[];
  openQuestions: string[];
  nextActions: string[];
  confidence: "low" | "medium" | "high";
  confirmedAt?: string;
}

export interface ResearchSpecificationQuestionSpec {
  prompt: string;
  title: string;
  question: string;
  checkpointKey: string;
  options: QuestionOption[];
  displayReason: string;
}

function compactList(values: string[] | undefined, limit = 3): string {
  const kept = (values ?? []).map((value) => value.trim()).filter(Boolean).slice(0, limit);
  return kept.length > 0 ? kept.join("; ") : "not specified";
}

function usesKorean(specification: ResearchSpecification): boolean {
  const values = [
    specification.title,
    specification.researchDirection.question,
    specification.researchDirection.purpose,
    specification.researchDirection.scopeBoundary,
    ...specification.constructOntology.coreConstructs,
    ...specification.constructOntology.distinctions,
    ...specification.theoryAndFraming.anchors,
    ...specification.measurementCoding.codingRules,
    ...specification.methodAnalysis.analysisOptions,
    specification.epistemicAlignment.conflictResolutionRule,
    ...specification.protectedDecisions,
    ...specification.openQuestions,
    ...specification.nextActions
  ];
  return values.some((value) => typeof value === "string" && /[ㄱ-ㅎㅏ-ㅣ가-힣]/.test(value));
}

export function renderResearchSpecificationPreview(specification: ResearchSpecification): string {
  const korean = usesKorean(specification);
  const lines = [
    korean ? "Research Specification Preview" : "Research Specification Preview",
    `${korean ? "제목" : "Title"}: ${specification.title}`,
    `${korean ? "목적" : "Purpose"}: ${specification.researchDirection.purpose}`,
    specification.researchDirection.scopeBoundary
      ? `${korean ? "범위" : "Scope"}: ${specification.researchDirection.scopeBoundary}`
      : undefined,
    `${korean ? "핵심 construct" : "Core constructs"}: ${compactList(specification.constructOntology.coreConstructs)}`,
    `${korean ? "구분" : "Distinctions"}: ${compactList(specification.constructOntology.distinctions)}`,
    `${korean ? "이론 앵커" : "Theory anchors"}: ${compactList(specification.theoryAndFraming.anchors)}`,
    `${korean ? "코딩 규칙" : "Coding rules"}: ${compactList(specification.measurementCoding.codingRules)}`,
    `${korean ? "분석 옵션" : "Analysis options"}: ${compactList(specification.methodAnalysis.analysisOptions)}`,
    specification.epistemicAlignment.conflictResolutionRule
      ? `${korean ? "충돌 조정" : "Conflict rule"}: ${specification.epistemicAlignment.conflictResolutionRule}`
      : undefined,
    `${korean ? "열린 질문" : "Open questions"}: ${compactList(specification.openQuestions, 2)}`,
    `${korean ? "다음 행동" : "Next actions"}: ${compactList(specification.nextActions, 2)}`,
    `${korean ? "신뢰도" : "Confidence"}: ${specification.confidence}`
  ].filter(Boolean);
  return lines.join("\n");
}

function baseOptions(specification: ResearchSpecification): QuestionOption[] {
  const korean = usesKorean(specification);
  return [
    {
      value: "confirm_specification",
      label: korean ? "저장/확정" : "Confirm and save",
      description: korean
        ? "이 Research Specification을 현재 연구 명세로 저장하고 이어갑니다."
        : "Save this Research Specification as the current research specification.",
      recommended: specification.confidence !== "low"
    },
    {
      value: "ask_one_more",
      label: korean ? "한 질문 더" : "Ask one more question",
      description: korean
        ? "저장하기 전에 가장 위험한 빈칸 하나를 더 묻습니다."
        : "Ask one more high-risk clarification before saving it.",
      recommended: specification.confidence === "low"
    },
    {
      value: "revise_section",
      label: korean ? "섹션 수정" : "Revise a section",
      description: korean
        ? "범위, construct, 이론, 코딩, 방법, 접근, 정렬 중 특정 섹션을 수정합니다."
        : "Revise one section such as scope, constructs, theory, coding, method, access, or alignment."
    },
    {
      value: "keep_open",
      label: korean ? "열어두기" : "Keep open",
      description: korean
        ? "아직 이 명세를 확정하지 않고 draft로 둡니다."
        : "Keep this specification as a draft instead of confirming it."
    }
  ];
}

export function buildResearchSpecificationQuestion(specification: ResearchSpecification): ResearchSpecificationQuestionSpec {
  const korean = usesKorean(specification);
  const preview = renderResearchSpecificationPreview(specification);
  return {
    prompt: preview,
    title: korean ? "Research Specification 확인" : "Research Specification Confirmation",
    question: korean
      ? "이 Research Specification을 어떻게 처리할까요?"
      : "How should LongTable handle this Research Specification?",
    checkpointKey: "research_specification_confirmation",
    options: baseOptions(specification),
    displayReason: korean
      ? `${preview}\n\n인터뷰가 단순한 방향 요약을 넘어 연구 명세를 만들 만큼 구체화되었습니다. 저장 전에 범위, construct, 이론, 코딩, 방법, 접근, 정렬을 명시적으로 확인해야 합니다.`
      : `${preview}\n\nThe interview has moved beyond a short direction summary into a research specification. Scope, constructs, theory, coding, method, access, and epistemic alignment should be explicit before saving.`
  };
}

export function researchSpecificationAnswerConfirms(answer: string): boolean {
  return answer === "confirm_specification";
}

export function researchSpecificationAnswerStatus(answer: string): "confirmed" | "active" | "deferred" {
  if (researchSpecificationAnswerConfirms(answer)) {
    return "confirmed";
  }
  if (answer === "keep_open") {
    return "deferred";
  }
  return "active";
}
