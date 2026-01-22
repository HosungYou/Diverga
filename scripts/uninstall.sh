#!/bin/bash

# ============================================
# Research Coordinator 제거 스크립트
# ============================================

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로고 출력
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════╗"
echo "║     Research Coordinator Uninstaller      ║"
echo "║     사회과학 연구 에이전트 시스템 제거    ║"
echo "╚═══════════════════════════════════════════╝"
echo -e "${NC}"

# 변수 설정
TARGET_DIR="$HOME/.claude/skills"

echo -e "${YELLOW}제거 대상:${NC}"
echo "  $TARGET_DIR/research-coordinator"
echo "  $TARGET_DIR/research-agents"
echo ""

# 설치 확인
if [ ! -L "$TARGET_DIR/research-coordinator" ] && [ ! -d "$TARGET_DIR/research-coordinator" ]; then
    if [ ! -L "$TARGET_DIR/research-agents" ] && [ ! -d "$TARGET_DIR/research-agents" ]; then
        echo -e "${YELLOW}Research Coordinator가 설치되어 있지 않습니다.${NC}"
        exit 0
    fi
fi

# 확인 프롬프트
echo -e "${YELLOW}정말로 Research Coordinator를 제거하시겠습니까? (y/N)${NC}"
read -r response
if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}제거가 취소되었습니다.${NC}"
    exit 0
fi

# 제거 수행
echo ""
echo -e "${BLUE}[1/2] 스킬 제거 중...${NC}"

if [ -L "$TARGET_DIR/research-coordinator" ] || [ -d "$TARGET_DIR/research-coordinator" ]; then
    rm -rf "$TARGET_DIR/research-coordinator"
    echo -e "  ${GREEN}✓${NC} research-coordinator 제거됨"
else
    echo -e "  ${YELLOW}!${NC} research-coordinator가 존재하지 않음"
fi

if [ -L "$TARGET_DIR/research-agents" ] || [ -d "$TARGET_DIR/research-agents" ]; then
    rm -rf "$TARGET_DIR/research-agents"
    echo -e "  ${GREEN}✓${NC} research-agents 제거됨"
else
    echo -e "  ${YELLOW}!${NC} research-agents가 존재하지 않음"
fi

# 확인
echo -e "${BLUE}[2/2] 제거 확인 중...${NC}"

if [ ! -e "$TARGET_DIR/research-coordinator" ] && [ ! -e "$TARGET_DIR/research-agents" ]; then
    echo -e "  ${GREEN}✓${NC} 모든 파일이 제거되었습니다"
else
    echo -e "  ${RED}✗${NC} 일부 파일이 남아있을 수 있습니다"
fi

# 완료 메시지
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     제거가 완료되었습니다!                 ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}참고:${NC}"
echo "  소스 파일은 삭제되지 않았습니다."
echo "  소스 파일도 삭제하려면 레포지토리 디렉토리를 직접 삭제하세요."
echo ""
echo -e "재설치: ${BLUE}./scripts/install.sh${NC}"
echo ""
