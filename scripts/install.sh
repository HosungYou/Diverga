#!/bin/bash

# ============================================
# Research Coordinator 설치 스크립트
# ============================================

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 버전 정보
VERSION="3.1.0"

# 로고 출력
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║     Research Coordinator Installer v${VERSION}           ║"
echo "║     사회과학 연구 에이전트 시스템                      ║"
echo "║     VS-Research: Mode Collapse 방지 시스템            ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 변수 설정
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$(dirname "$SCRIPT_DIR")"
TARGET_DIR="$HOME/.claude/skills"

echo -e "${YELLOW}설치 정보:${NC}"
echo "  소스 디렉토리: $SOURCE_DIR"
echo "  대상 디렉토리: $TARGET_DIR"
echo ""

# 소스 디렉토리 확인
if [ ! -d "$SOURCE_DIR/.claude/skills/research-coordinator" ]; then
    echo -e "${RED}오류: 소스 디렉토리를 찾을 수 없습니다.${NC}"
    echo "  예상 경로: $SOURCE_DIR/.claude/skills/research-coordinator"
    exit 1
fi

if [ ! -d "$SOURCE_DIR/.claude/skills/research-agents" ]; then
    echo -e "${RED}오류: 에이전트 디렉토리를 찾을 수 없습니다.${NC}"
    echo "  예상 경로: $SOURCE_DIR/.claude/skills/research-agents"
    exit 1
fi

# 대상 디렉토리 생성
echo -e "${BLUE}[1/4] 대상 디렉토리 생성 중...${NC}"
if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
    echo -e "  ${GREEN}✓${NC} 생성됨: $TARGET_DIR"
else
    echo -e "  ${GREEN}✓${NC} 이미 존재함: $TARGET_DIR"
fi

# 기존 설치 확인 및 제거
echo -e "${BLUE}[2/4] 기존 설치 확인 중...${NC}"
if [ -L "$TARGET_DIR/research-coordinator" ] || [ -d "$TARGET_DIR/research-coordinator" ]; then
    echo -e "  ${YELLOW}!${NC} 기존 설치 발견. 제거 중..."
    rm -rf "$TARGET_DIR/research-coordinator"
    echo -e "  ${GREEN}✓${NC} 기존 research-coordinator 제거됨"
fi

if [ -L "$TARGET_DIR/research-agents" ] || [ -d "$TARGET_DIR/research-agents" ]; then
    rm -rf "$TARGET_DIR/research-agents"
    echo -e "  ${GREEN}✓${NC} 기존 research-agents 제거됨"
fi

# 심볼릭 링크 생성
echo -e "${BLUE}[3/4] 심볼릭 링크 생성 중...${NC}"

ln -sf "$SOURCE_DIR/.claude/skills/research-coordinator" "$TARGET_DIR/research-coordinator"
echo -e "  ${GREEN}✓${NC} research-coordinator 링크 생성됨"

ln -sf "$SOURCE_DIR/.claude/skills/research-agents" "$TARGET_DIR/research-agents"
echo -e "  ${GREEN}✓${NC} research-agents 링크 생성됨"

# 설치 확인
echo -e "${BLUE}[4/4] 설치 확인 중...${NC}"

if [ -f "$TARGET_DIR/research-coordinator/SKILL.md" ]; then
    echo -e "  ${GREEN}✓${NC} 마스터 스킬 확인됨"
else
    echo -e "  ${RED}✗${NC} 마스터 스킬 확인 실패"
    exit 1
fi

AGENT_COUNT=$(ls -d "$TARGET_DIR/research-agents"/*/ 2>/dev/null | wc -l | tr -d ' ')
echo -e "  ${GREEN}✓${NC} 에이전트 스킬: ${AGENT_COUNT}개 확인됨"

# 완료 메시지
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Research Coordinator v${VERSION} 설치 완료!           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}v3.0 새로운 기능:${NC}"
echo "  • VS-Research 방법론: LLM Mode Collapse 방지"
echo "  • Dynamic T-Score: 권장안의 전형성(0.0-1.0) 평가"
echo "  • 5가지 창의적 장치: 강제 비유, 반복 루프, 의미적 거리, 시간 재구성, 커뮤니티 시뮬레이션"
echo "  • User Checkpoints: 14개 확인 지점"
echo "  • 3-Tier Agent Upgrade: FULL(5) / ENHANCED(6) / LIGHT(9)"
echo ""
echo -e "${YELLOW}사용 방법:${NC}"
echo "  Claude Code에서 다음 명령어로 시작하세요:"
echo ""
echo -e "    ${BLUE}/research-coordinator${NC}    - 마스터 코디네이터"
echo -e "    ${BLUE}/research-question-refiner${NC} - 개별 에이전트"
echo ""
echo -e "${YELLOW}설치 위치:${NC}"
echo "  $TARGET_DIR/research-coordinator"
echo "  $TARGET_DIR/research-agents"
echo ""
echo -e "문서: ${BLUE}https://github.com/HosungYou/research-coordinator${NC}"
echo ""
