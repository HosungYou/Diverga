"""
Diverga Memory System v8.0 - Intent Detector

Detects research intent from user messages to enable automatic project initialization.
Supports both English and Korean.

Author: Diverga Project
Version: 8.0.0
"""

import re
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum


class ResearchType(Enum):
    """Research type enumeration."""
    SYSTEMATIC_REVIEW = "systematic_review"
    META_ANALYSIS = "meta_analysis"
    LITERATURE_REVIEW = "literature_review"
    EXPERIMENTAL = "experimental"
    QUALITATIVE = "qualitative"
    MIXED_METHODS = "mixed_methods"
    UNKNOWN = "unknown"


@dataclass
class IntentResult:
    """Result of intent detection."""
    is_research_intent: bool
    research_type: ResearchType
    topic: Optional[str]
    confidence: float
    matched_patterns: List[str]
    paradigm: Optional[str]  # quantitative, qualitative, mixed
    additional_context: Dict[str, Any]


# Detection patterns
PATTERNS = {
    # English patterns
    "en": {
        ResearchType.SYSTEMATIC_REVIEW: [
            r"systematic\s+review\s+(on|about|of)\s+(.+)",
            r"conduct\s+a?\s*systematic\s+review",
            r"want\s+to\s+(do|conduct|start)\s+a?\s*systematic\s+review",
            r"systematic\s+literature\s+review",
            r"PRISMA\s+review",
            r"systematic\s+search",
        ],
        ResearchType.META_ANALYSIS: [
            r"meta[- ]?analysis\s+(on|about|of)\s+(.+)",
            r"conduct\s+a?\s*meta[- ]?analysis",
            r"want\s+to\s+(do|conduct|start)\s+a?\s*meta[- ]?analysis",
            r"quantitative\s+synthesis",
            r"pooled\s+effect\s+(size)?",
            r"meta[- ]?analytic",
        ],
        ResearchType.LITERATURE_REVIEW: [
            r"literature\s+review\s+(on|about|of)\s+(.+)",
            r"review\s+the\s+literature",
            r"narrative\s+review",
            r"scoping\s+review",
            r"rapid\s+review",
        ],
        ResearchType.EXPERIMENTAL: [
            r"experimental\s+(study|research|design)",
            r"RCT",
            r"randomized\s+controlled",
            r"quasi[- ]?experiment",
            r"intervention\s+study",
            r"A/B\s+test",
        ],
        ResearchType.QUALITATIVE: [
            r"qualitative\s+(study|research|inquiry)",
            r"phenomenolog(y|ical)",
            r"grounded\s+theory",
            r"ethnograph(y|ic)",
            r"narrative\s+inquiry",
            r"case\s+study",
            r"interview\s+study",
            r"focus\s+group",
        ],
        ResearchType.MIXED_METHODS: [
            r"mixed\s+method",
            r"sequential\s+(explanatory|exploratory)",
            r"convergent\s+(design|parallel)",
            r"embedded\s+design",
            r"qual[- ]?quant",
            r"quant[- ]?qual",
        ],
    },
    # Korean patterns
    "ko": {
        ResearchType.SYSTEMATIC_REVIEW: [
            r"체계적\s*문헌\s*고찰",
            r"체계적\s*리뷰",
            r"체계적\s*검토",
            r"시스테마틱\s*리뷰",
            r"프리즈마",
            r"PRISMA",
        ],
        ResearchType.META_ANALYSIS: [
            r"메타\s*분석",
            r"메타분석",
            r"메타\s*연구",
            r"양적\s*종합",
            r"통합\s*분석",
        ],
        ResearchType.LITERATURE_REVIEW: [
            r"문헌\s*고찰",
            r"문헌\s*검토",
            r"문헌\s*리뷰",
            r"선행\s*연구\s*검토",
            r"범위\s*고찰",
            r"스코핑\s*리뷰",
        ],
        ResearchType.EXPERIMENTAL: [
            r"실험\s*연구",
            r"실험\s*설계",
            r"RCT",
            r"무작위\s*통제",
            r"유사\s*실험",
            r"중재\s*연구",
        ],
        ResearchType.QUALITATIVE: [
            r"질적\s*연구",
            r"현상학",
            r"근거\s*이론",
            r"민족지학",
            r"사례\s*연구",
            r"심층\s*면담",
            r"포커스\s*그룹",
        ],
        ResearchType.MIXED_METHODS: [
            r"혼합\s*방법",
            r"혼합\s*연구",
            r"혼합\s*설계",
            r"순차적\s*설명",
            r"수렴\s*설계",
        ],
    }
}

# General research intent patterns (lower confidence)
GENERAL_RESEARCH_PATTERNS = {
    "en": [
        r"(start|begin|conduct|do)\s+(a\s+)?research",
        r"research\s+(project|study)",
        r"(my|this)\s+research",
        r"study\s+(on|about)",
        r"investigate",
        r"analyze\s+(the\s+)?(effect|impact|relationship)",
    ],
    "ko": [
        r"연구\s*(를|을)\s*(시작|진행)",
        r"연구\s*프로젝트",
        r"(내|이)\s*연구",
        r"분석\s*(하고|해)",
        r"조사\s*(하고|해)",
        r"효과\s*분석",
        r"관계\s*분석",
    ]
}

# Topic extraction patterns
TOPIC_PATTERNS = {
    "en": [
        r"(?:on|about|of|regarding)\s+[\"']?(.+?)[\"']?(?:\s*\.|$|\s*,|\s*and)",
        r"(?:topic|subject|area)\s*(?:is|:)\s*[\"']?(.+?)[\"']?(?:\s*\.|$)",
        r"(?:study|research|analyze)\s+[\"']?(.+?)[\"']?(?:\s*\.|$)",
    ],
    "ko": [
        r"(?:에 대한|관련|주제[:：]?)\s*[「「\'\"']?(.+?)[」」\'\"']?(?:\s*\.|$|에)",
        r"[「「\'\"'](.+?)[」」\'\"']\s*(?:에 대한|관련|연구)",
    ]
}


def detect_language(text: str) -> str:
    """Detect if text is primarily Korean or English."""
    korean_chars = len(re.findall(r'[가-힣]', text))
    total_chars = len(re.findall(r'[a-zA-Z가-힣]', text))

    if total_chars == 0:
        return "en"

    korean_ratio = korean_chars / total_chars
    return "ko" if korean_ratio > 0.3 else "en"


def extract_topic(text: str, lang: str) -> Optional[str]:
    """Extract research topic from text."""
    patterns = TOPIC_PATTERNS.get(lang, TOPIC_PATTERNS["en"])

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            topic = match.group(1).strip()
            # Clean up topic
            topic = re.sub(r'\s+', ' ', topic)
            if len(topic) > 5:  # Minimum meaningful topic length
                return topic

    return None


def detect_paradigm(text: str, research_type: ResearchType) -> Optional[str]:
    """Infer research paradigm from text and research type."""
    # Type-based inference
    if research_type in [ResearchType.META_ANALYSIS, ResearchType.EXPERIMENTAL]:
        return "quantitative"
    elif research_type == ResearchType.QUALITATIVE:
        return "qualitative"
    elif research_type == ResearchType.MIXED_METHODS:
        return "mixed"

    # Pattern-based inference
    quant_patterns = [
        r"quantitative", r"statistic", r"measure", r"effect size",
        r"양적", r"통계", r"측정", r"효과크기"
    ]
    qual_patterns = [
        r"qualitative", r"interview", r"theme", r"lived experience",
        r"질적", r"면담", r"주제", r"체험"
    ]
    mixed_patterns = [
        r"mixed", r"both.*qualitative.*quantitative", r"integration",
        r"혼합", r"통합"
    ]

    text_lower = text.lower()

    if any(re.search(p, text_lower) for p in mixed_patterns):
        return "mixed"
    elif any(re.search(p, text_lower) for p in qual_patterns):
        return "qualitative"
    elif any(re.search(p, text_lower) for p in quant_patterns):
        return "quantitative"

    return None


def detect_intent(text: str) -> IntentResult:
    """
    Detect research intent from user message.

    Args:
        text: User message text

    Returns:
        IntentResult with detection results
    """
    # Detect language
    lang = detect_language(text)

    # Initialize result
    matched_patterns = []
    best_type = ResearchType.UNKNOWN
    best_confidence = 0.0
    topic = None

    # Check specific research type patterns
    lang_patterns = PATTERNS.get(lang, PATTERNS["en"])

    for research_type, patterns in lang_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                matched_patterns.append(f"{research_type.value}:{pattern}")
                # Higher confidence for more specific patterns
                confidence = 0.9 if len(match.group(0)) > 15 else 0.8
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_type = research_type

                # Try to extract topic from match groups
                if topic is None and len(match.groups()) > 1:
                    topic = match.group(2) if match.lastindex >= 2 else match.group(1)

    # Check general research patterns (lower confidence)
    if best_type == ResearchType.UNKNOWN:
        general_patterns = GENERAL_RESEARCH_PATTERNS.get(lang, GENERAL_RESEARCH_PATTERNS["en"])
        for pattern in general_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matched_patterns.append(f"general:{pattern}")
                best_confidence = max(best_confidence, 0.5)

    # Extract topic if not found
    if topic is None:
        topic = extract_topic(text, lang)

    # Detect paradigm
    paradigm = detect_paradigm(text, best_type)

    # Determine if this is a research intent
    is_research = best_confidence > 0.4 or len(matched_patterns) > 0

    return IntentResult(
        is_research_intent=is_research,
        research_type=best_type,
        topic=topic,
        confidence=best_confidence,
        matched_patterns=matched_patterns,
        paradigm=paradigm,
        additional_context={
            "language": lang,
            "text_length": len(text),
            "pattern_count": len(matched_patterns)
        }
    )


def should_initialize_project(text: str) -> Tuple[bool, Optional[IntentResult]]:
    """
    Check if the user message indicates a new research project should be initialized.

    This is the main entry point for automatic project detection.

    Args:
        text: User message text

    Returns:
        Tuple of (should_initialize, intent_result)
    """
    intent = detect_intent(text)

    # Conditions for initialization:
    # 1. High confidence research intent (>= 0.7)
    # 2. Specific research type detected (not UNKNOWN)
    # 3. Topic is extractable
    should_init = (
        intent.is_research_intent and
        intent.confidence >= 0.7 and
        intent.research_type != ResearchType.UNKNOWN
    )

    return (should_init, intent) if should_init else (False, intent)


def get_suggested_prompt(intent: IntentResult) -> str:
    """
    Generate a suggested prompt based on detected intent.

    Args:
        intent: Detected intent result

    Returns:
        Suggested prompt for user confirmation
    """
    type_names = {
        ResearchType.SYSTEMATIC_REVIEW: "체계적 문헌고찰 / systematic review",
        ResearchType.META_ANALYSIS: "메타분석 / meta-analysis",
        ResearchType.LITERATURE_REVIEW: "문헌고찰 / literature review",
        ResearchType.EXPERIMENTAL: "실험연구 / experimental study",
        ResearchType.QUALITATIVE: "질적연구 / qualitative study",
        ResearchType.MIXED_METHODS: "혼합연구 / mixed methods study",
    }

    type_name = type_names.get(intent.research_type, "연구 / research")
    topic_str = f"'{intent.topic}'" if intent.topic else "(주제 미지정 / topic TBD)"

    if intent.additional_context.get("language") == "ko":
        return f"""
{type_name}을(를) 시작하시겠습니까?

📋 감지된 연구:
   • 유형: {type_name}
   • 주제: {topic_str}
   • 패러다임: {intent.paradigm or '자동 감지'}

[예] 프로젝트를 초기화합니다
[아니오] 취소합니다
[수정] 주제를 수정합니다
""".strip()
    else:
        return f"""
Would you like to start a {type_name}?

📋 Detected research:
   • Type: {type_name}
   • Topic: {topic_str}
   • Paradigm: {intent.paradigm or 'auto-detect'}

[Yes] Initialize project
[No] Cancel
[Edit] Modify topic
""".strip()


# Convenience functions

def detect(text: str) -> IntentResult:
    """Alias for detect_intent."""
    return detect_intent(text)


def should_init(text: str) -> bool:
    """Quick check if project initialization is suggested."""
    should, _ = should_initialize_project(text)
    return should


if __name__ == "__main__":
    # Test examples
    test_messages = [
        "I want to conduct a systematic review on AI in education",
        "메타분석 연구를 시작하고 싶어요. 주제는 AI 학습 효과",
        "Help me with my literature review about language learning",
        "체계적 문헌고찰을 하려고 해요",
        "Can you analyze some data for me?",
        "What's the weather today?",
    ]

    print("Intent Detection Test Results")
    print("=" * 60)

    for msg in test_messages:
        result = detect_intent(msg)
        print(f"\nMessage: {msg[:50]}...")
        print(f"  Is Research: {result.is_research_intent}")
        print(f"  Type: {result.research_type.value}")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Topic: {result.topic}")
        print(f"  Paradigm: {result.paradigm}")

        should, _ = should_initialize_project(msg)
        print(f"  Should Initialize: {should}")
