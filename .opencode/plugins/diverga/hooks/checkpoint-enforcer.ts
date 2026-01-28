/**
 * Checkpoint Enforcer Hook
 * Ensures human checkpoints are respected in research workflow
 */

import type { PluginContext, HookResult, ToolParams, CheckpointPrompt } from '../types';
import { CHECKPOINTS } from '../checkpoints';
import { loadContext } from './context-manager';

/**
 * Map of tool actions to checkpoints they should trigger
 */
const CHECKPOINT_TRIGGERS: Record<string, string[]> = {
  // Research direction decisions
  'research_question': ['CP_RESEARCH_DIRECTION', 'CP_VS_001'],
  'refine_question': ['CP_RESEARCH_DIRECTION', 'CP_VS_001'],

  // Paradigm selection
  'select_paradigm': ['CP_PARADIGM_SELECTION'],
  'methodology_selection': ['CP_PARADIGM_SELECTION'],

  // Theory selection
  'select_theory': ['CP_THEORY_SELECTION', 'CP_VS_001'],
  'framework_design': ['CP_THEORY_SELECTION', 'CP_VS_001'],

  // Methodology approval
  'design_methodology': ['CP_METHODOLOGY_APPROVAL'],
  'approve_design': ['CP_METHODOLOGY_APPROVAL'],

  // Analysis
  'start_analysis': ['CP_ANALYSIS_PLAN'],
  'analyze': ['CP_ANALYSIS_PLAN'],

  // Quality review
  'quality_assessment': ['CP_QUALITY_REVIEW'],
  'assess_quality': ['CP_QUALITY_REVIEW'],

  // VS methodology
  'vs_selection': ['CP_VS_001', 'CP_VS_003'],
  'select_direction': ['CP_VS_001', 'CP_VS_003'],
};

/**
 * Check if checkpoint is already completed
 */
function isCheckpointCompleted(checkpointId: string, context: PluginContext): boolean {
  const researchContext = loadContext();
  if (!researchContext) return false;
  return researchContext.completedCheckpoints.includes(checkpointId);
}

/**
 * Get checkpoint definition
 */
function getCheckpointDefinition(checkpointId: string) {
  return CHECKPOINTS.find(cp => cp.id === checkpointId);
}

/**
 * Create checkpoint prompt for user
 */
function createCheckpointPrompt(checkpointId: string): CheckpointPrompt | null {
  const checkpoint = getCheckpointDefinition(checkpointId);
  if (!checkpoint) return null;

  return {
    id: checkpoint.id,
    level: checkpoint.level,
    message: `
${checkpoint.icon} **${checkpoint.name}** (${checkpoint.level})

${checkpoint.whatToAsk}

_When: ${checkpoint.when}_
`,
    options: [
      { id: 'approve', label: 'Approve / 승인', description: 'Proceed with current direction' },
      { id: 'modify', label: 'Modify / 수정', description: 'Request changes before proceeding' },
      { id: 'cancel', label: 'Cancel / 취소', description: 'Stop and reconsider' },
    ],
  };
}

/**
 * Main checkpoint enforcer hook
 */
export async function checkpointEnforcer(
  params: ToolParams,
  context: PluginContext
): Promise<HookResult> {
  // Get tool action
  const action = params.arguments?.action as string;
  const toolName = params.tool;

  // Check if this action triggers any checkpoints
  const triggerKey = action || toolName;
  const checkpointIds = CHECKPOINT_TRIGGERS[triggerKey] || [];

  if (checkpointIds.length === 0) {
    // No checkpoint required
    return { proceed: true };
  }

  // Check each checkpoint
  for (const checkpointId of checkpointIds) {
    const checkpoint = getCheckpointDefinition(checkpointId);
    if (!checkpoint) continue;

    // Skip if already completed
    if (isCheckpointCompleted(checkpointId, context)) {
      continue;
    }

    // For REQUIRED checkpoints, always stop
    if (checkpoint.level === 'REQUIRED') {
      const prompt = createCheckpointPrompt(checkpointId);
      return {
        proceed: false,
        message: `🔴 CHECKPOINT HALT: ${checkpoint.name}`,
        checkpoint: prompt || undefined,
      };
    }

    // For RECOMMENDED checkpoints, pause and suggest
    if (checkpoint.level === 'RECOMMENDED') {
      const prompt = createCheckpointPrompt(checkpointId);
      return {
        proceed: false,
        message: `🟠 CHECKPOINT PAUSE: ${checkpoint.name} (recommended)`,
        checkpoint: prompt || undefined,
      };
    }

    // For OPTIONAL checkpoints, just note it
    // (but still continue)
  }

  return { proceed: true };
}

/**
 * Mark checkpoint as completed
 */
export function completeCheckpoint(
  checkpointId: string,
  selectedOption: string,
  context: PluginContext
): void {
  const researchContext = loadContext();
  if (!researchContext) return;

  // Add to completed
  if (!researchContext.completedCheckpoints.includes(checkpointId)) {
    researchContext.completedCheckpoints.push(checkpointId);
  }

  // Remove from pending
  researchContext.pendingCheckpoints = researchContext.pendingCheckpoints.filter(
    cp => cp !== checkpointId
  );

  // Record decision
  researchContext.decisions.push({
    checkpoint: checkpointId,
    timestamp: new Date().toISOString(),
    optionsPresented: ['approve', 'modify', 'cancel'],
    selected: selectedOption,
  });

  // Save context
  // (Context manager will handle persistence)
}

/**
 * Get pending checkpoints for current stage
 */
export function getPendingCheckpoints(context: PluginContext): string[] {
  const researchContext = loadContext();
  if (!researchContext) return [];
  return researchContext.pendingCheckpoints;
}

/**
 * Reset checkpoint (for testing/debugging)
 */
export function resetCheckpoint(checkpointId: string, context: PluginContext): void {
  const researchContext = loadContext();
  if (!researchContext) return;

  researchContext.completedCheckpoints = researchContext.completedCheckpoints.filter(
    cp => cp !== checkpointId
  );
}
