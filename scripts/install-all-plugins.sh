#!/bin/bash
# =============================================================================
# Research Coordinator - 플러그인 설치 스크립트
# =============================================================================
#
# v2.1.0부터 단일 플러그인에 21개 스킬이 모두 포함됩니다.
# 이 스크립트는 편의를 위해 제공됩니다.
#
# 사용법:
#   curl -sL https://raw.githubusercontent.com/HosungYou/research-coordinator/main/scripts/install-all-plugins.sh | bash
#
# =============================================================================

set -e

echo "=============================================="
echo "  Research Coordinator Plugin Installer"
echo "  Version: 2.1.0"
echo "=============================================="
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# claude CLI 확인
if ! command -v claude &> /dev/null; then
    echo -e "${RED}Error: claude CLI not found${NC}"
    echo "Please install Claude Code first: https://claude.ai/code"
    exit 1
fi

echo -e "${BLUE}Step 1/2: 마켓플레이스 추가 중...${NC}"
echo ""

# 마켓플레이스가 이미 추가되어 있는지 확인
if claude plugin marketplace list 2>&1 | grep -q "research-coordinator-skills"; then
    echo -e "${GREEN}✓ 마켓플레이스가 이미 추가되어 있습니다${NC}"
else
    if claude plugin marketplace add HosungYou/research-coordinator 2>&1; then
        echo -e "${GREEN}✓ 마켓플레이스 추가 완료${NC}"
    else
        echo -e "${RED}✗ 마켓플레이스 추가 실패${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}Step 2/2: 플러그인 설치 중 (21개 스킬 포함)...${NC}"
echo ""

# 이미 설치되어 있는지 확인
if claude plugin list 2>&1 | grep -q "research-coordinator@research-coordinator-skills"; then
    echo -e "${YELLOW}○ research-coordinator가 이미 설치되어 있습니다${NC}"
    echo ""
    echo "업데이트하려면:"
    echo "  claude plugin update research-coordinator"
else
    if claude plugin install research-coordinator 2>&1 | grep -q "Successfully installed"; then
        echo -e "${GREEN}✓ research-coordinator 설치 완료${NC}"
    else
        echo -e "${RED}✗ 설치 실패${NC}"
        exit 1
    fi
fi

echo ""
echo "=============================================="
echo -e "${GREEN}  설치 완료!${NC}"
echo "=============================================="
echo ""
echo "포함된 스킬 (21개):"
echo "  - /research-coordinator (마스터)"
echo "  - /research-question-refiner"
echo "  - /theoretical-framework-architect"
echo "  - /devils-advocate"
echo "  - /research-ethics-advisor"
echo "  - /systematic-literature-scout"
echo "  - /evidence-quality-appraiser"
echo "  - /effect-size-extractor"
echo "  - /research-radar"
echo "  - /research-design-consultant"
echo "  - /statistical-analysis-guide"
echo "  - /analysis-code-generator"
echo "  - /sensitivity-analysis-designer"
echo "  - /internal-consistency-checker"
echo "  - /checklist-manager"
echo "  - /reproducibility-auditor"
echo "  - /bias-detector"
echo "  - /journal-matcher"
echo "  - /academic-communicator"
echo "  - /peer-review-strategist"
echo "  - /preregistration-composer"
echo ""
