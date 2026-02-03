"""
Diverga QA Protocol v3.0 - Runners Module

Provides:
- v2.x: Conversation extraction and simulation tools
- v3.0: True automated CLI-based testing

Usage:
    # v3.0 - True automated testing (recommended)
    from qa.runners import CLITestRunner
    runner = CLITestRunner(scenario_id='QUAL-002', cli_tool='claude')
    session = runner.run()
    runner.save_results('qa/reports/sessions')

    # v2.x - Simulation and extraction
    from qa.runners import ConversationExtractor, AutomatedTestSimulator
"""

from .extract_conversation import (
    ConversationExtractor,
    ConversationEvaluator,
    ExtractionResult,
    Turn,
    Checkpoint,
    AgentInvocation,
)

from .cli_test_runner import (
    CLITestRunner,
    TestSession,
    Turn as CLITurn,
)

from .automated_test import (
    AutomatedTestSimulator,
    SimulatedTurn,
    TestSession as SimulatedTestSession,
)

__all__ = [
    # v3.0 - True automated CLI testing
    'CLITestRunner',
    'TestSession',
    'CLITurn',
    # v2.x - Simulation
    'AutomatedTestSimulator',
    'SimulatedTurn',
    'SimulatedTestSession',
    # Extraction
    'ConversationExtractor',
    'ConversationEvaluator',
    'ExtractionResult',
    'Turn',
    'Checkpoint',
    'AgentInvocation',
]
