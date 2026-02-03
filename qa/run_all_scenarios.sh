#!/bin/bash
#
# Diverga QA Protocol v3.0 - Run All Scenarios
#
# Executes all test scenarios using the CLI test runner.
#
# Usage:
#   ./run_all_scenarios.sh                # Run all with real AI
#   ./run_all_scenarios.sh --dry-run      # Dry run (no API calls)
#   ./run_all_scenarios.sh --cli opencode # Use different CLI tool
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/reports/sessions"
CLI_TOOL="${CLI_TOOL:-claude}"
DRY_RUN=""
VERBOSE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN="--dry-run"
            shift
            ;;
        --cli)
            CLI_TOOL="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="-v"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Scenarios to run
SCENARIOS=(
    "QUAL-002"
    "META-002"
    "MIXED-002"
    "HUMAN-002"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "============================================================"
echo "Diverga QA Protocol v3.0 - Batch Test Runner"
echo "============================================================"
echo "CLI Tool: ${CLI_TOOL}"
echo "Output: ${OUTPUT_DIR}"
echo "Mode: ${DRY_RUN:-LIVE}"
echo "Scenarios: ${SCENARIOS[*]}"
echo "============================================================"
echo ""

# Track results
PASSED=0
FAILED=0
ERRORS=0

# Run each scenario
for scenario in "${SCENARIOS[@]}"; do
    echo -e "${YELLOW}[${scenario}]${NC} Starting..."

    # Check if protocol exists
    protocol_file="${SCRIPT_DIR}/protocol/test_$(echo ${scenario} | tr '[:upper:]' '[:lower:]' | tr '-' '_').yaml"
    if [[ ! -f "$protocol_file" ]]; then
        echo -e "${RED}[${scenario}]${NC} Protocol file not found: ${protocol_file}"
        ((ERRORS++))
        continue
    fi

    # Run the test
    if python3 "${SCRIPT_DIR}/runners/cli_test_runner.py" \
        --scenario "${scenario}" \
        --cli "${CLI_TOOL}" \
        --output "${OUTPUT_DIR}" \
        ${DRY_RUN} \
        ${VERBOSE}; then
        echo -e "${GREEN}[${scenario}]${NC} PASSED"
        ((PASSED++))
    else
        exit_code=$?
        if [[ $exit_code -eq 1 ]]; then
            echo -e "${YELLOW}[${scenario}]${NC} LOW COMPLIANCE"
            ((FAILED++))
        else
            echo -e "${RED}[${scenario}]${NC} FAILED (exit: ${exit_code})"
            ((FAILED++))
        fi
    fi

    echo ""
done

# Summary
echo "============================================================"
echo "BATCH TEST SUMMARY"
echo "============================================================"
echo -e "Passed:  ${GREEN}${PASSED}${NC}"
echo -e "Failed:  ${RED}${FAILED}${NC}"
echo -e "Errors:  ${RED}${ERRORS}${NC}"
echo "============================================================"

# Generate summary report
SUMMARY_FILE="${OUTPUT_DIR}/batch_summary_$(date +%Y%m%d_%H%M%S).md"
cat > "${SUMMARY_FILE}" << EOF
# Diverga QA Batch Test Summary

**Date**: $(date +%Y-%m-%d\ %H:%M:%S)
**CLI Tool**: ${CLI_TOOL}
**Mode**: ${DRY_RUN:-LIVE}

## Results

| Metric | Count |
|--------|-------|
| Passed | ${PASSED} |
| Failed | ${FAILED} |
| Errors | ${ERRORS} |
| Total | $((PASSED + FAILED + ERRORS)) |

## Scenarios

EOF

for scenario in "${SCENARIOS[@]}"; do
    result_file="${OUTPUT_DIR}/${scenario}/${scenario}_test_result.yaml"
    if [[ -f "$result_file" ]]; then
        status=$(grep "^status:" "$result_file" | cut -d: -f2 | tr -d ' ')
        echo "- **${scenario}**: ${status}" >> "${SUMMARY_FILE}"
    else
        echo "- **${scenario}**: NOT RUN" >> "${SUMMARY_FILE}"
    fi
done

echo ""
echo "Summary saved to: ${SUMMARY_FILE}"

# Exit with appropriate code
if [[ $FAILED -gt 0 ]] || [[ $ERRORS -gt 0 ]]; then
    exit 1
fi
exit 0
