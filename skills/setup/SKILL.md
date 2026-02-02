---
name: setup
description: |
  Diverga initial configuration wizard. Sets up LLM API, checkpoints, paradigm, language.
  Triggers: setup, configure, 설정
version: "6.9.0"
---

# /diverga:setup

**Version**: 1.0.0
**Trigger**: `/diverga:setup`

## Description

Initial configuration wizard for Diverga. Sets up LLM API, human checkpoints, research paradigm, and language preferences.

## Workflow

When user invokes `/diverga:setup`, execute this interactive wizard:

### Step 1: Welcome Message

```
╔══════════════════════════════════════════════════════════════════╗
║                    Welcome to Diverga v6.4.0                     ║
║         AI Research Assistant for the Complete Lifecycle         ║
╠══════════════════════════════════════════════════════════════════╣
║  40 specialized agents across 8 categories (A-H)                 ║
║  Human-centered design with mandatory checkpoints                ║
║  Verbalized Sampling (VS) methodology for creative alternatives  ║
╚══════════════════════════════════════════════════════════════════╝

Let's configure Diverga for your research environment.
```

### Step 2: LLM API Selection

Use AskUserQuestion tool:

```
question: "Which LLM provider would you like to use?"
header: "LLM API"
options:
  - label: "Anthropic Claude (Recommended)"
    description: "Best for academic writing and research. Requires ANTHROPIC_API_KEY."
  - label: "OpenAI GPT"
    description: "General purpose. Requires OPENAI_API_KEY."
  - label: "Groq (Free tier available)"
    description: "Fast inference, free tier. Requires GROQ_API_KEY."
  - label: "Local (Ollama)"
    description: "Privacy-focused, no API key needed. Requires Ollama installed."
```

### Step 3: Human Checkpoint Configuration

Use AskUserQuestion tool:

```
question: "Enable human checkpoints for critical research decisions?"
header: "Checkpoints"
options:
  - label: "Yes, enable checkpoints (Recommended)"
    description: "AI stops at paradigm selection, methodology approval, and data validation."
  - label: "Minimal checkpoints"
    description: "Only CP_PARADIGM and CP_METHODOLOGY required."
  - label: "No checkpoints"
    description: "Fully autonomous mode. Not recommended for research."
```

### Step 4: Default Research Paradigm

Use AskUserQuestion tool:

```
question: "What is your default research paradigm?"
header: "Paradigm"
options:
  - label: "Auto-detect (Recommended)"
    description: "Diverga detects paradigm from conversation context."
  - label: "Quantitative"
    description: "Experimental, survey, meta-analysis research."
  - label: "Qualitative"
    description: "Phenomenology, grounded theory, ethnography."
  - label: "Mixed Methods"
    description: "Sequential, convergent, or embedded designs."
```

### Step 5: Language Preference

Use AskUserQuestion tool:

```
question: "Preferred language for Diverga responses?"
header: "Language"
options:
  - label: "Auto (match user input)"
    description: "Responds in the same language as your input."
  - label: "English"
    description: "Always respond in English."
  - label: "한국어 (Korean)"
    description: "Always respond in Korean."
```

### Step 6: Generate Configuration

After collecting all preferences, generate `~/.claude/plugins/diverga/config/diverga-config.json`:

```json
{
  "version": "6.4.0",
  "llm_provider": "<selected_provider>",
  "llm_api_key_env": "<API_KEY_ENV_VAR>",
  "human_checkpoints": {
    "enabled": true,
    "required": ["CP_PARADIGM", "CP_METHODOLOGY"],
    "optional": ["CP_THEORY", "CP_DATA_VALIDATION"]
  },
  "default_paradigm": "auto",
  "language": "auto",
  "model_routing": {
    "high": "opus",
    "medium": "sonnet",
    "low": "haiku"
  }
}
```

### Step 7: Verification

```bash
# Create config directory
mkdir -p ~/.claude/plugins/diverga/config

# Write config file
cat > ~/.claude/plugins/diverga/config/diverga-config.json << 'EOF'
{config_json}
EOF

# Verify installation
echo "✅ Diverga configuration saved!"
```

### Step 8: Completion Message

```
╔══════════════════════════════════════════════════════════════════╗
║                   Diverga Setup Complete! ✅                     ║
╠══════════════════════════════════════════════════════════════════╣
║  Configuration saved to:                                         ║
║  ~/.claude/plugins/diverga/config/diverga-config.json            ║
║                                                                  ║
║  Quick Commands:                                                 ║
║  • /diverga:help     - View all 40 agents                       ║
║  • diverga:a1        - Research Question Refiner                ║
║  • diverga:c5        - Meta-Analysis Master                     ║
║                                                                  ║
║  Auto-Trigger Keywords:                                          ║
║  • "research question" → A1-ResearchQuestionRefiner             ║
║  • "meta-analysis"     → C5-MetaAnalysisMaster                  ║
║  • "theoretical framework" → A2-TheoreticalFrameworkArchitect   ║
╚══════════════════════════════════════════════════════════════════╝

Start by saying: "I want to conduct a systematic review on [topic]"
```

## Error Handling

### Missing API Key

If selected provider's API key is not set:

```
⚠️  ANTHROPIC_API_KEY not found in environment.

Please set it:
  export ANTHROPIC_API_KEY="your-key-here"

Or add to your shell profile (~/.zshrc or ~/.bashrc).
```

### Ollama Not Installed

If Local (Ollama) selected but not installed:

```
⚠️  Ollama not detected.

Install from: https://ollama.ai/download

After installation, run:
  ollama pull llama3.2
```

## Implementation Notes

- Config file location: `~/.claude/plugins/diverga/config/diverga-config.json`
- All user selections saved immediately
- Re-running `/diverga:setup` overwrites existing config
- API keys should be in environment variables, not config file
