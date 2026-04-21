import type {
  ArtifactStakes,
  ClosureDisposition,
  CheckpointLevel,
  GuidanceQuestionType,
  InteractionMode,
  PromptStyle,
  ResearcherProfile,
  ResearchStage,
  RuntimeGuidance,
  StudyContract
} from "@longtable/core";

export interface CheckpointSignal {
  checkpointKey: string;
  baseLevel: CheckpointLevel;
  mode: InteractionMode;
  artifactStakes: ArtifactStakes;
  researchStage: ResearchStage;
  unresolvedTensions?: string[];
  studyContract?: StudyContract;
}

export type CheckpointTriggerFamily =
  | "exploration"
  | "review"
  | "commitment"
  | "submission"
  | "meta_decision"
  | "evidence"
  | "authorship"
  | "advisory";

export interface CheckpointTriggerClassification {
  signal: CheckpointSignal;
  family: CheckpointTriggerFamily;
  confidence: "low" | "medium" | "high";
  matchedCues: string[];
  requiresQuestionBeforeClosure: boolean;
  advisoryOnly: boolean;
  rationale: string[];
}

export interface CheckpointTriggerClassificationOptions {
  preferredMode?: InteractionMode;
  fallbackMode?: InteractionMode;
  researchStage?: ResearchStage;
  artifactStakes?: ArtifactStakes;
  checkpointKey?: string;
  unresolvedTensions?: string[];
  studyContract?: StudyContract;
}

export interface ResolvedCheckpointPolicy {
  checkpointKey: string;
  level: CheckpointLevel;
  blocking: boolean;
  promptStyle: PromptStyle;
  requiresDecisionLog: boolean;
  updateExplicitState: boolean;
  rationale: string[];
}

export type {
  ArtifactStakes,
  ClosureDisposition,
  CheckpointLevel,
  GuidanceQuestionType,
  InteractionMode,
  PromptStyle,
  ResearcherProfile,
  ResearchStage,
  RuntimeGuidance,
  StudyContract
} from "@longtable/core";
