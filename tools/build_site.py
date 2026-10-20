#!/usr/bin/env python3
"""Render the bilingual static textbook from its manifest and chapter fragments."""
from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
MANIFEST_PATH = ROOT / "library-manifest.json"

TEXT = {
    "en": {
        "home": "Overview", "chapters": "Chapters", "lab": "Lab", "references": "References",
        "license": "License", "menu": "Open navigation", "theme": "Theme", "dark": "Dark theme", "light": "Light theme",
        "skip": "Skip to content", "eyebrow": "Semiconductor integration engineering",
        "hero_title": "Technology is decided across the flow.",
        "hero_copy": "A bilingual engineering textbook for connecting device targets, process interfaces, cumulative constraints, and the evidence needed to choose a technology architecture.",
        "start": "Start with the decision method", "open_lab": "Explore the integration lab",
        "chapter_count": "guided chapters", "languages": "languages", "outcomes": "What you will learn",
        "outcomes_copy": "Practice the work that sits between process modules: make assumptions explicit, compare feasible options, and ask for evidence that can change a decision.",
        "outcome_1": "Translate requirements", "outcome_1_copy": "Turn a product or device target into a shared set of process, design, and reliability constraints.",
        "outcome_2": "Trace interfaces", "outcome_2_copy": "Follow sequence, thermal, material, geometry, and measurement dependencies across module boundaries.",
        "outcome_3": "Plan evidence", "outcome_3_copy": "Separate reported facts, assumptions, and inference; then choose the next measurement or experiment.",
        "catalog": "Chapter guide", "catalog_copy": "Search all chapters by title or topic. Each chapter includes a worked decision and knowledge check.",
        "search_label": "Find a chapter", "search_placeholder": "Try “thermal”, “contact”, or “DTCO”", "no_results": "No chapters match this search. Try another engineering term.",
        "scope": "A decision book, not a process recipe", "scope_copy": "This book focuses on cross-module architecture and technology trade-offs. It links to specialist books for device physics, standalone processes, measurement, and yield methods. No foundry recipe or confidential data is included.",
        "chapter": "Chapter", "all_chapters": "All chapters", "previous": "Previous chapter", "next": "Next chapter", "back": "Chapter guide",
        "lab_title": "Integration laboratory", "lab_copy": "Explore one bounded quantitative model and two qualitative decision activities. Each activity states what it can and cannot conclude.",
        "model_checked": "Analytically checked · model-limited", "qualitative": "Qualitative activity · no physical model", "synthetic": "Synthetic teaching scenario",
        "thermal_title": "Thermal history and a reflected Gaussian profile estimate", "thermal_copy": "Accumulate a one-dimensional diffusion integral across constant-temperature holds. The model reflects an idealized Gaussian implant lobe at a no-flux surface, preserving the stated dose in silicon. Rp is the lobe center near the surface. This is not implant boundary chemistry, an activated profile, a measured junction depth, or a process recipe.",
        "profile_inputs": "Initial profile and background", "sigma0": "Initial Gaussian-component σ (nm)", "rp": "Profile center Rp (nm)", "dose": "Areal dose (cm⁻²)", "background": "Background (cm⁻³)",
        "holds": "Thermal holds", "temp": "Temperature (°C)", "duration": "Duration (s)", "remove": "Remove", "add_hold": "Add a hold", "hold_limit": "0–30 holds; zero holds shows the initial profile without thermal broadening.", "reset": "Reset reference case",
        "results": "Model output", "sigma_final": "Final Gaussian-component σ", "peak": "Profile peak", "crossing": "Right-side crossing", "no_crossing": "No crossing", "chart_x": "Depth", "chart_y": "Normalized chemical concentration", "chart_aria": "Normalized chemical concentration profile", "chart_bg": "The curve is normalized to its true peak. The horizontal dashed line is the uniform background; the vertical x* marker locates the right-side crossing even when that threshold is too low to resolve on this linear scale.", "chart_bg_no_crossing": "The curve is normalized to its true peak. The background is at or above that peak, so there is no descending right-side crossing and no threshold line or x* marker is drawn.",
        "model_status": "Illustrative model output. Not silicon validation or a process recipe.", "surface_warning": "The reflected Gaussian is an idealized no-flux surface model. Real implant boundary chemistry and near-surface profile formation are not represented.", "concentration_warning": "Literature caution: Fair (1975) reports concentration-dependent profiles for high-concentration boron diffusions (> about 2 × 10¹⁹ cm⁻³) in neutral ambients. This is only a heuristic trigger; this synthetic scenario does not reproduce those conditions and still uses constant dilute diffusivity.", "invalid_result": "No result: check each value and its stated range.",
        "dependency_title": "Process dependency explorer", "dependency_copy": "Select an integration question to highlight the interfaces worth reviewing. The map is qualitative bookkeeping, not a process simulator or recipe checker.",
        "choose_question": "Review focus", "gate_option": "Gate-stack choice", "contact_option": "Contact formation", "beol_option": "Interconnect compatibility",
        "node_device": "Device target", "node_gate": "Gate/material", "node_thermal": "Thermal history", "node_pattern": "Pattern transfer", "node_etch": "Etch interface", "node_contact": "Contact/MOL", "node_metal": "Interconnect", "node_reliability": "Reliability evidence",
        "gate_text": "Ask whether the selected gate materials and sequence are compatible with the device target, later thermal steps, and contact integration. Identify the measurement or model needed at each interface.",
        "relation_type_precedence": "Declared precedence", "relation_type_compatibility": "Compatibility question", "relation_type_inference": "Engineering inference",
        "relation_status_assumption": "Illustrative assumption · confirm sequence against the intended architecture.", "relation_status_measurement": "Engineering inference · ask which measurement or model can test this interface.", "relation_status_open": "Open compatibility question · evidence is needed before accepting the relationship.",
        "contact_text": "Trace the contact opening from pattern definition through etch, pre-contact surface state, fill, and local routing. Do not infer contact resistance from geometry alone.",
        "beol_text": "List the thermal, chemical, mechanical, and reliability constraints that a back-end stack imposes on earlier devices and later interconnect levels. The highlighted connections are prompts, not validated causality.",
        "challenge_title": "Integration evidence challenge", "challenge_copy": "A fictional split suggests a contact monitor shifted after a process change, while a neighboring dielectric-sensitive structure is not yet measured. Choose a useful next evidence step.",
        "choice_a": "Compare traceable baseline and candidate splits; repeat a contact-sensitive structure and check wafer/lot/temperature provenance.",
        "choice_b": "Declare the process change causal from the single monitor and release it immediately.",
        "choice_c": "Collect a broader measurement only after naming which competing hypotheses and interface it can distinguish.",
        "feedback_a": "Useful first step: this checks the signal and data lineage, but it does not yet isolate a physical mechanism. Add a structure or measurement that can discriminate among the remaining explanations.",
        "feedback_b": "Not enough evidence: a single monitor shift cannot distinguish process effect, measurement artifact, or an unrelated change. The unmeasured neighboring interface also leaves a stated risk open.",
        "feedback_c": "Strong decision framing: define competing hypotheses and the predicted observables before adding data. The next step should be specific enough that either outcome changes the decision.",
        "challenge_note": "No probabilities, yield estimates, or automatic root-cause ranking are produced.",
        "references_title": "References and scope links", "references_copy": "Public sources are cited for specific background claims. Independent books below remain separate projects; links are not reproduced material or endorsements.",
        "license_title": "License and attribution", "license_copy": "Original prose, translation, diagrams, and synthetic examples are CC BY 4.0. Original software is MIT. Third-party works keep their own rights and terms.",
        "related": "Related independent textbooks", "footer_copy": "An independent engineering textbook in the My Library collection.",
        "not_found": "The requested chapter is not present in this manifest.", "answer_correct": "Correct. Read the explanation and connect the answer back to the chapter's stated assumptions.", "answer_incorrect": "Review the explanation, then reconsider which assumptions and interfaces matter."
    },
    "ko": {
        "home": "책 소개", "chapters": "장 목록", "lab": "실습실", "references": "참고 문헌",
        "license": "라이선스", "menu": "탐색 메뉴 열기", "theme": "테마", "dark": "다크 테마", "light": "라이트 테마",
        "skip": "본문으로 건너뛰기", "eyebrow": "반도체 통합 엔지니어링",
        "hero_title": "기술은 전체 공정 흐름에서 결정됩니다.",
        "hero_copy": "소자 목표, 공정 인터페이스, 누적 제약, 기술 아키텍처 선택에 필요한 증거를 연결하는 이중 언어 공학 교재입니다.",
        "start": "의사결정 방법부터 읽기", "open_lab": "통합 실습 살펴보기",
        "chapter_count": "개 장", "languages": "개 언어", "outcomes": "학습 내용",
        "outcomes_copy": "공정 모듈 사이에 놓인 업무를 연습합니다. 가정을 분명히 하고, 가능한 대안을 비교하며, 결정을 바꿀 수 있는 증거를 찾습니다.",
        "outcome_1": "요구사항 변환", "outcome_1_copy": "제품 또는 소자 목표를 공정·설계·신뢰성의 공동 제약 조건으로 바꿉니다.",
        "outcome_2": "인터페이스 추적", "outcome_2_copy": "공정 순서, 열 이력, 재료, 형상, 측정 의존성을 모듈 경계 너머로 추적합니다.",
        "outcome_3": "증거 계획", "outcome_3_copy": "공개 사실, 가정, 추론을 구분하고 다음 측정이나 실험을 선택합니다.",
        "catalog": "장 안내", "catalog_copy": "제목이나 주제로 모든 장을 검색하세요. 각 장에는 의사결정 예제와 이해도 확인이 있습니다.",
        "search_label": "장 찾기", "search_placeholder": "열 이력, 콘택트, DTCO 검색", "no_results": "검색과 일치하는 장이 없습니다. 다른 공학 용어를 입력하세요.",
        "scope": "공정 레시피가 아닌 의사결정 교재", "scope_copy": "이 책은 모듈 간 아키텍처와 기술 절충에 초점을 둡니다. 소자 물리, 개별 공정, 측정, 수율 기초는 전문 교재로 연결합니다. 팹 레시피나 기밀 데이터는 포함하지 않습니다.",
        "chapter": "장", "all_chapters": "전체 장", "previous": "이전 장", "next": "다음 장", "back": "장 안내",
        "lab_title": "통합 실습실", "lab_copy": "범위를 한정한 정량 모델 하나와 정성적 의사결정 활동 두 가지를 제공합니다. 각 활동은 가능한 결론과 한계를 설명합니다.",
        "model_checked": "해석식 확인 · 모델 한정", "qualitative": "정성적 활동 · 물리 모델 없음", "synthetic": "합성 학습 시나리오",
        "thermal_title": "열 이력과 반사 가우시안 프로파일 추정", "thermal_copy": "일정 온도 유지 구간의 1차원 확산 적분을 누적합니다. 모델은 이상화된 가우시안 이온 주입 로브를 무유량 표면에서 반사하여 실리콘 내부 선량을 보존합니다. 표면 부근에서 Rp는 로브 중심입니다. 실제 주입 경계 화학, 활성화 프로파일, 측정 접합 깊이 또는 공정 레시피를 나타내지 않습니다.",
        "profile_inputs": "초기 프로파일과 배경 농도", "sigma0": "초기 가우시안 성분 σ (nm)", "rp": "프로파일 중심 Rp (nm)", "dose": "면적 선량 (cm⁻²)", "background": "배경 농도 (cm⁻³)",
        "holds": "열 유지 구간", "temp": "온도 (°C)", "duration": "시간 (s)", "remove": "삭제", "add_hold": "유지 구간 추가", "hold_limit": "유지 구간은 0~30개입니다. 0개이면 열적 확산이 없는 초기 프로파일을 표시합니다.", "reset": "기준 사례로 초기화",
        "results": "모델 출력", "sigma_final": "최종 가우시안 성분 σ", "peak": "프로파일 최대값", "crossing": "오른쪽 교차점", "no_crossing": "교차 없음", "chart_x": "깊이", "chart_y": "최대값 정규화 화학 농도", "chart_aria": "최대값 정규화 화학 농도 프로파일", "chart_bg": "곡선은 실제 최대 농도로 정규화했습니다. 가로 점선은 균일 배경 농도이며, 세로 x* 표지는 선형 눈금에서 임계값을 분해하기 어려울 때에도 오른쪽 교차점의 위치를 나타냅니다.", "chart_bg_no_crossing": "곡선은 실제 최대 농도로 정규화했습니다. 배경 농도가 최대 농도 이상이므로 하강하는 오른쪽 교차점이 없고 임계값 선과 x* 표지도 표시하지 않습니다.",
        "model_status": "설명용 모델 결과입니다. 실리콘 검증이나 공정 레시피가 아닙니다.", "surface_warning": "반사 가우시안은 이상화된 무유량 표면 모델입니다. 실제 주입 경계 화학과 표면 근처 프로파일 형성은 표현하지 않습니다.", "concentration_warning": "문헌상 주의: Fair(1975)는 중성 분위기의 고농도 보론 확산(약 2 × 10¹⁹ cm⁻³ 초과)에서 농도 의존 프로파일을 보고했습니다. 이 시나리오는 해당 조건을 재현하지 않으며, 이 값은 휴리스틱 경고 기준일 뿐입니다. 계산은 계속 일정한 희석 확산계수를 사용합니다.", "invalid_result": "결과가 없습니다. 각 값과 표시 범위를 확인하세요.",
        "dependency_title": "공정 의존성 탐색기", "dependency_copy": "통합 질문을 선택하면 검토할 인터페이스를 강조합니다. 물리적 공정 시뮬레이터나 레시피 검증기가 아니라 정성적 기록 도구입니다.",
        "choose_question": "검토 초점", "gate_option": "게이트 적층 선택", "contact_option": "콘택트 형성", "beol_option": "배선 호환성",
        "node_device": "소자 목표", "node_gate": "게이트·재료", "node_thermal": "열 이력", "node_pattern": "패턴 전사", "node_etch": "식각 인터페이스", "node_contact": "콘택트·MOL", "node_metal": "배선", "node_reliability": "신뢰성 증거",
        "gate_text": "선택한 게이트 재료와 순서가 소자 목표, 후속 열 단계, 콘택트 통합과 호환되는지 질문합니다. 각 인터페이스에서 필요한 측정 또는 모델을 정합니다.",
        "relation_type_precedence": "선언된 순서 관계", "relation_type_compatibility": "호환성 질문", "relation_type_inference": "공학적 추론",
        "relation_status_assumption": "설명용 가정 · 대상 아키텍처의 공정 순서로 확인하세요.", "relation_status_measurement": "공학적 추론 · 이 인터페이스를 검증할 측정 또는 모델을 질문하세요.", "relation_status_open": "미해결 호환성 질문 · 관계를 받아들이기 전에 증거가 필요합니다.",
        "contact_text": "패턴 정의에서 식각, 콘택트 전 표면 상태, 충전, 로컬 배선까지 콘택트 개구를 추적합니다. 형상만으로 콘택트 저항을 추정하지 않습니다.",
        "beol_text": "후공정 적층이 초기 소자와 이후 배선층에 부과하는 열·화학·기계·신뢰성 제약을 정리합니다. 강조된 연결은 질문일 뿐 인과관계가 검증된 것은 아닙니다.",
        "challenge_title": "통합 증거 판단 실습", "challenge_copy": "가상의 분할 실험에서 공정 변경 후 콘택트 모니터가 이동한 것으로 보이지만 인접 유전체 민감 구조는 아직 측정하지 않았습니다. 다음 증거 단계를 선택하세요.",
        "choice_a": "추적 가능한 기준·후보 분할을 비교하고, 콘택트 민감 구조를 반복 측정하며 웨이퍼·로트·온도 출처를 확인합니다.",
        "choice_b": "단일 모니터로 공정 변경의 인과성을 선언하고 즉시 릴리스합니다.",
        "choice_c": "경쟁 가설과 인터페이스를 구분할 수 있는지 먼저 정한 뒤 더 넓은 측정 데이터를 수집합니다.",
        "feedback_a": "유용한 첫 단계입니다. 신호와 데이터 출처를 확인하지만 물리 메커니즘을 분리하지는 못합니다. 남은 설명을 구분할 수 있는 구조나 측정을 추가해야 합니다.",
        "feedback_b": "증거가 부족합니다. 단일 모니터 변화만으로 공정 영향, 측정 아티팩트, 무관한 변화를 구분할 수 없습니다. 측정하지 않은 인접 계면 위험도 남습니다.",
        "feedback_c": "좋은 의사결정 틀입니다. 데이터를 추가하기 전에 경쟁 가설과 예상 관측값을 정의합니다. 어떤 결과든 결정에 영향을 줄 만큼 구체적인 다음 단계가 필요합니다.",
        "challenge_note": "확률, 수율 추정, 자동 근본원인 순위를 계산하지 않습니다.",
        "references_title": "참고 문헌 및 범위 연결", "references_copy": "공개 자료는 특정 배경 설명을 위해 인용합니다. 아래 독립 교재는 별도 프로젝트이며 링크는 자료를 복제하거나 보증한다는 뜻이 아닙니다.",
        "license_title": "라이선스와 저작자 표시", "license_copy": "원본 글, 번역, 도표, 합성 예시는 CC BY 4.0입니다. 원본 소프트웨어는 MIT입니다. 제3자 자료에는 원래 권리와 약관이 적용됩니다.",
        "related": "관련 독립 교재", "footer_copy": "My Library 컬렉션의 독립 공학 교재입니다.",
        "not_found": "매니페스트에 요청한 장이 없습니다.", "answer_correct": "정답입니다. 설명을 읽고 장에서 밝힌 가정과 연결해 보세요.", "answer_incorrect": "설명을 읽고 어떤 가정과 인터페이스가 중요한지 다시 생각해 보세요."
    }
}

class FragmentAudit(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.ids = set()
        self.duplicates = []
        self.errors = []
        self.top_level_sections = 0
        self.links = []
        self.tags = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if not self.stack and tag == "section": self.top_level_sections += 1
        self.tags.append(tag)
        for key, value in attrs.items():
            if key.lower().startswith("on"): self.errors.append("inline event handler is forbidden")
            if key == "id" and value:
                if value in self.ids: self.duplicates.append(value)
                self.ids.add(value)
            if key == "href" and value: self.links.append(value)
        if tag in {"script", "iframe", "object", "embed"}: self.errors.append("active/external content element is forbidden: " + tag)
        if tag not in self.VOID: self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in self.VOID: return
        if not self.stack:
            self.errors.append("unexpected closing tag: " + tag)
        elif self.stack[-1] != tag:
            self.errors.append("misnested closing tag: " + tag + " after " + self.stack[-1])
        else:
            self.stack.pop()


def read_manifest():
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("cannot read library-manifest.json: " + str(exc)) from exc


def validate(manifest):
    required = ["id", "slug", "title", "subtitle", "description", "category", "tags", "status", "repositoryUrl", "productionUrl", "languages", "version", "lastUpdated", "chapterCount", "chapters", "experiments", "prerequisites", "relatedBooks", "attribution", "cover", "theme"]
    missing = [name for name in required if name not in manifest]
    if missing: raise ValueError("manifest missing fields: " + ", ".join(missing))
    if manifest["id"] != "processintegrationbook" or manifest["slug"] != "processintegrationbook": raise ValueError("book id and slug must remain processintegrationbook")
    if manifest["status"] not in {"in-progress", "published"}: raise ValueError("invalid publication status")
    base = manifest["productionUrl"]
    parsed = urlparse(base)
    if parsed.scheme != "https" or parsed.hostname != "frbread7.github.io" or not parsed.path.endswith("/processintegrationbook/") or parsed.query or parsed.fragment:
        raise ValueError("productionUrl must be the declared HTTPS GitHub Pages project URL")
    for field in ("title", "subtitle", "description"):
        if not all(isinstance(manifest[field].get(lang), str) and manifest[field][lang].strip() for lang in ("en", "ko")):
            raise ValueError("manifest " + field + " must provide English and Korean")
    if set(manifest["languages"]) != {"en", "ko"}: raise ValueError("only deployed English and Korean editions may be listed")
    if manifest["chapterCount"] != len(manifest["chapters"]): raise ValueError("chapterCount must match chapters")
    if not manifest["chapters"]: raise ValueError("at least one chapter is required")
    ids, numbers = set(), set()
    for expected, chapter in enumerate(manifest["chapters"], 1):
        if chapter["id"] in ids or chapter["number"] in numbers: raise ValueError("duplicate chapter id or number")
        if chapter["number"] != expected: raise ValueError("chapter numbers must be ordered and contiguous")
        if not isinstance(chapter.get("topics"), list) or not chapter["topics"]:
            raise ValueError("each chapter must provide bilingual topics as 'English / 한국어' strings")
        for topic in chapter["topics"]:
            localized_topic(topic, "en")
            localized_topic(topic, "ko")
        ids.add(chapter["id"]); numbers.add(chapter["number"])
        for lang in ("en", "ko"):
            fragment_path = ROOT / "content" / lang / "chapters" / (chapter["id"] + ".html")
            if not fragment_path.is_file(): raise ValueError("missing chapter fragment: " + str(fragment_path.relative_to(ROOT)))
            fragment = fragment_path.read_text(encoding="utf-8")
            audit = FragmentAudit(); audit.feed(fragment); audit.close()
            if audit.stack or audit.errors or audit.duplicates or audit.top_level_sections < 1:
                detail = audit.errors + (["unclosed tags: " + ", ".join(audit.stack)] if audit.stack else []) + (["duplicate ids: " + ", ".join(audit.duplicates)] if audit.duplicates else [])
                raise ValueError("invalid chapter fragment " + lang + "/" + chapter["id"] + ": " + ("; ".join(detail) or "expected at least one top-level section"))
            for link in audit.links:
                parsed_link = urlparse(link)
                if parsed_link.scheme and parsed_link.scheme != "https": raise ValueError("chapter links must be HTTPS: " + link)
            url = chapter["urls"].get(lang, "")
            if not url.startswith(base): raise ValueError("chapter URL must use production URL: " + url)
            if not chapter["title"].get(lang): raise ValueError("localized chapter title missing")
    experiment_ids = set()
    for experiment in manifest["experiments"]:
        if experiment["id"] in experiment_ids: raise ValueError("duplicate experiment id")
        experiment_ids.add(experiment["id"])
        if experiment["chapterId"] not in ids: raise ValueError("experiment refers to a missing chapter")
        if not experiment["url"].startswith(base) or "#" not in experiment["url"]: raise ValueError("experiment URL must be a production URL with an anchor")
    if manifest["cover"] != "assets/covers/processintegrationbook.svg": raise ValueError("manifest cover path is not the original book cover")
    if not (SITE / manifest["cover"]).is_file(): raise ValueError("cover asset is missing")
    return True


def e(value):
    return html.escape(str(value), quote=True)


def localized_topic(topic, lang):
    english, separator, korean = topic.partition(" / ")
    if not separator or not english.strip() or not korean.strip() or " / " in korean:
        raise ValueError("chapter topics must use the Book Factory-compatible 'English / 한국어' string format")
    return english.strip() if lang == "en" else korean.strip()


def relative(current_file, target_file):
    return posixpath.relpath(target_file, posixpath.dirname(current_file) or ".")


def language_target(current_file, lang, kind, chapter_id=None):
    if kind == "chapter":
        target = ("chapters/" if lang == "en" else "ko/chapters/") + chapter_id + ".html"
    else:
        route = {"home": "index.html", "lab": "lab.html", "references": "references.html", "license": "license.html"}[kind]
        target = ("" if lang == "en" else "ko/") + route
    return relative(current_file, target)


def page_context(current_file):
    if current_file.startswith("chapters/"):
        return "chapter", posixpath.basename(current_file)[:-5]
    if current_file.startswith("ko/chapters/"):
        return "chapter", posixpath.basename(current_file)[:-5]
    local = current_file[3:] if current_file.startswith("ko/") else current_file
    kind = {"index.html": "home", "lab.html": "lab", "references.html": "references", "license.html": "license"}.get(local)
    if kind is None:
        raise ValueError("unknown localized page route: " + current_file)
    return kind, None


def production_page_url(manifest, lang, kind, chapter_id=None):
    if kind == "chapter":
        route = ("chapters/" if lang == "en" else "ko/chapters/") + chapter_id + ".html"
    else:
        route = {"home": "" if lang == "en" else "ko/", "lab": "lab.html" if lang == "en" else "ko/lab.html",
                 "references": "references.html" if lang == "en" else "ko/references.html",
                 "license": "license.html" if lang == "en" else "ko/license.html"}[kind]
    return manifest["productionUrl"] + route


def shell(manifest, lang, current_file, page_title, description, active, body, extra_scripts=()):
    t = TEXT[lang]
    home = language_target(current_file, lang, "home")
    chapters_target = language_target(current_file, lang, "home") + "#chapters"
    lab = language_target(current_file, lang, "lab")
    refs = language_target(current_file, lang, "references")
    license_url = language_target(current_file, lang, "license")
    other_lang = "ko" if lang == "en" else "en"
    context_kind, chapter_id = page_context(current_file)
    lang_target = language_target(current_file, other_lang, context_kind, chapter_id)
    assets_css = relative(current_file, "assets/styles.css")
    assets_js = relative(current_file, "assets/site.js")
    cover_path = relative(current_file, "assets/covers/processintegrationbook.svg")
    route = "" if current_file == "index.html" else current_file[:-len("index.html")] if current_file.endswith("index.html") else current_file
    canonical = manifest["productionUrl"] + route
    alternate_en = production_page_url(manifest, "en", context_kind, chapter_id)
    alternate_ko = production_page_url(manifest, "ko", context_kind, chapter_id)
    scripts = "".join('<script defer src="' + e(relative(current_file, path)) + '"></script>' for path in extra_scripts)
    nav_items = [
        ("home", t["home"], home),
        ("chapters", t["chapters"], chapters_target),
        ("lab", t["lab"], lab),
        ("references", t["references"], refs)
    ]
    nav = "".join('<a href="' + e(href) + '"' + (' aria-current="page"' if key == active else "") + '>' + e(label) + '</a>' for key, label, href in nav_items)
    language_label = "한국어" if other_lang == "ko" else "English"
    theme_button = '<button class="nav-action" type="button" data-theme-toggle data-dark-label="' + e(t["dark"]) + '" data-light-label="' + e(t["light"]) + '" aria-label="' + e(t["theme"]) + '"><span data-theme-label>' + e(t["dark"]) + '</span></button>'
    return '<!doctype html>\n' + '<html lang="' + lang + '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + \
        '<meta name="description" content="' + e(description) + '"><meta name="theme-color" content="#f5f4ef">' + \
        '<link rel="canonical" href="' + e(canonical) + '"><link rel="alternate" hreflang="en" href="' + e(alternate_en) + '"><link rel="alternate" hreflang="ko" href="' + e(alternate_ko) + '">' + \
        '<meta property="og:type" content="website"><meta property="og:title" content="' + e(page_title) + '"><meta property="og:description" content="' + e(description) + '"><meta property="og:image" content="' + e(manifest["productionUrl"] + manifest["cover"]) + '">' + \
        '<title>' + e(page_title) + '</title><link rel="icon" href="' + e(cover_path) + '" type="image/svg+xml"><link rel="stylesheet" href="' + e(assets_css) + '">' + scripts + '<script defer src="' + e(assets_js) + '"></script></head><body>' + \
        '<a class="skip-link" href="#main">' + e(t["skip"]) + '</a><header class="site-header"><div class="nav-wrap"><a class="brand" href="' + e(home) + '"><img src="' + e(cover_path) + '" alt=""><span>ProcessIntegrationBook</span></a>' + \
        '<button class="button menu-toggle" type="button" data-menu-toggle aria-controls="main-navigation" aria-expanded="false" aria-label="' + e(t["menu"]) + '">☰</button><nav id="main-navigation" class="main-nav" aria-label="' + e(t["home"]) + '">' + nav + '</nav>' + \
        '<div class="nav-actions"><a class="nav-action" href="' + e(lang_target) + '" hreflang="' + other_lang + '" lang="' + other_lang + '" aria-label="' + e(language_label) + '">' + ("KO" if other_lang == "ko" else "EN") + '</a>' + theme_button + '</div></div></header>' + \
        '<main id="main" class="page-main"><div class="container">' + body + '</div></main><footer class="site-footer"><div class="container footer-wrap"><p>' + e(t["footer_copy"]) + '</p><p>' + e(t["related"]) + ': <a href="https://frbread7.github.io/pmicbook/">PMICBook</a> · <a href="https://frbread7.github.io/watbook/">WATBook</a></p><p class="license-note"><a href="' + e(license_url) + '">' + e(t["license"]) + '</a> · ' + e(manifest["version"]) + '</p></div></footer></body></html>\n'


def render_home(manifest, lang):
    t = TEXT[lang]
    current = "index.html" if lang == "en" else "ko/index.html"
    cards = []
    for chapter in manifest["chapters"]:
        target = chapter["urls"][lang]
        route = target.replace(manifest["productionUrl"], "")
        href = relative(current, route)
        title = chapter["title"][lang]
        topics = " · ".join(localized_topic(topic, lang) for topic in chapter["topics"][:3])
        search_terms = " ".join(chapter["topics"]) + " " + " ".join(chapter["title"].values())
        cards.append('<article class="chapter-card" data-chapter-card data-search="' + e(title + " " + search_terms) + '"><span class="number">' + e(t["chapter"] + " " + str(chapter["number"]).zfill(2)) + '</span><h3>' + e(title) + '</h3><p>' + e(topics) + '</p><a class="card-link" href="' + e(href) + '">' + e(t["start"]) + ' →</a></article>')
    cover = relative(current, "assets/covers/processintegrationbook.svg")
    body = '<section class="hero"><div class="hero-grid"><div><p class="eyebrow">' + e(t["eyebrow"]) + '</p><h1>' + e(t["hero_title"]) + '</h1><p>' + e(t["hero_copy"]) + '</p><div class="button-row"><a class="button primary" href="#chapters">' + e(t["start"]) + '</a><a class="button" href="' + e(relative(current, "lab.html" if lang == "en" else "ko/lab.html")) + '">' + e(t["open_lab"]) + '</a></div><div class="stats-row"><span class="stat-chip">' + str(manifest["chapterCount"]) + ' ' + e(t["chapter_count"]) + '</span><span class="stat-chip">2 ' + e(t["languages"]) + '</span><span class="stat-chip">' + e(t["model_checked"]) + '</span></div></div><img class="hero-cover" src="' + e(cover) + '" alt="' + e("Original cover illustration of connected semiconductor layers" if lang == "en" else "연결된 반도체 층을 그린 원본 표지 삽화") + '"></div></section>' + \
        '<section aria-labelledby="outcomes"><div class="section-heading"><div><p class="kicker">01 · ' + e(t["eyebrow"]) + '</p><h2 id="outcomes">' + e(t["outcomes"]) + '</h2></div><p>' + e(t["outcomes_copy"]) + '</p></div><div class="outcome-grid"><article class="outcome-card"><span class="card-mark">A</span><h3>' + e(t["outcome_1"]) + '</h3><p>' + e(t["outcome_1_copy"]) + '</p></article><article class="outcome-card"><span class="card-mark">B</span><h3>' + e(t["outcome_2"]) + '</h3><p>' + e(t["outcome_2_copy"]) + '</p></article><article class="outcome-card"><span class="card-mark">C</span><h3>' + e(t["outcome_3"]) + '</h3><p>' + e(t["outcome_3_copy"]) + '</p></article></div></section>' + \
        '<section id="chapters" aria-labelledby="chapters-heading"><div class="section-heading"><div><p class="kicker">02 · ' + e(t["catalog"]) + '</p><h2 id="chapters-heading">' + e(t["catalog"]) + '</h2><p>' + e(t["catalog_copy"]) + '</p></div></div><div class="catalog-tools"><div class="field"><label for="chapter-search">' + e(t["search_label"]) + '</label><input id="chapter-search" type="search" data-chapter-search placeholder="' + e(t["search_placeholder"]) + '"></div></div><div class="chapter-grid">' + "".join(cards) + '</div><p class="empty-state" data-empty-search role="status">' + e(t["no_results"]) + '</p></section>' + \
        '<section class="callout"><h2>' + e(t["scope"]) + '</h2><p>' + e(t["scope_copy"]) + '</p></section>'
    return shell(manifest, lang, current, "ProcessIntegrationBook · " + t["home"], manifest["description"][lang], "home", body)


def render_chapter(manifest, chapter, lang):
    current = ("chapters/" if lang == "en" else "ko/chapters/") + chapter["id"] + ".html"
    t = TEXT[lang]
    order = chapter["number"]
    source = ROOT / "content" / lang / "chapters" / (chapter["id"] + ".html")
    fragment = source.read_text(encoding="utf-8")
    fragment = fragment.replace(
        "data-quiz>",
        'data-quiz data-correct-message="' + e(t["answer_correct"]) + '" data-incorrect-message="' + e(t["answer_incorrect"]) + '">'
    )
    index_route = "../index.html#chapters"
    title = chapter["title"][lang]
    outline = '<aside class="chapter-aside"><details><summary>' + e(t["all_chapters"]) + '</summary><nav aria-label="' + e(t["all_chapters"]) + '">'
    for item in manifest["chapters"]:
        route = item["urls"][lang].replace(manifest["productionUrl"], "")
        outline += '<a href="' + e(relative(current, route)) + '"' + (' aria-current="page"' if item["id"] == chapter["id"] else "") + '>' + e(str(item["number"]).zfill(2) + " · " + item["title"][lang]) + '</a>'
    outline += '</nav></details></aside>'
    previous = manifest["chapters"][order - 2] if order > 1 else None
    following = manifest["chapters"][order] if order < len(manifest["chapters"]) else None
    previous_link = '<a href="' + e(relative(current, previous["urls"][lang].replace(manifest["productionUrl"], ""))) + '">← ' + e(t["previous"] + ": " + previous["title"][lang]) + '</a>' if previous else '<a href="' + e(index_route) + '">' + e(t["back"]) + '</a>'
    next_link = '<a href="' + e(relative(current, following["urls"][lang].replace(manifest["productionUrl"], ""))) + '">' + e(t["next"] + ": " + following["title"][lang]) + ' →</a>' if following else '<a href="' + e(index_route) + '">' + e(t["back"]) + '</a>'
    body = '<p class="breadcrumb"><a href="' + e(index_route) + '">' + e(t["chapters"]) + '</a> / ' + e(t["chapter"] + " " + str(order).zfill(2)) + '</p><div class="chapter-layout"><article class="chapter-content"><p class="eyebrow">' + e(t["chapter"] + " " + str(order).zfill(2)) + '</p><h1>' + e(title) + '</h1>' + fragment + '<nav class="chapter-footer" aria-label="' + e(t["chapters"]) + '">' + previous_link + next_link + '</nav></article>' + outline + '</div>'
    return shell(manifest, lang, current, title + " · ProcessIntegrationBook", manifest["description"][lang], "chapters", body)


def render_lab(manifest, lang):
    t = TEXT[lang]
    current = "lab.html" if lang == "en" else "ko/lab.html"
    thermal_sources = (
        'Method background: <a href="https://www.math.toronto.edu/ivrii/PDE-textbook/Chapter3/S3.1.V.html">Neumann image solution for a reflecting half-line</a>; '
        '<a href="https://ocw.mit.edu/courses/6-021j-quantitative-physiology-cells-and-tissues-fall-2004/2dec3d0ac557365b9b31de361b77e3ad_macro.pdf">MIT OpenCourseWare diffusion model</a>.'
        if lang == "en" else
        '경계 조건 방법 참고 자료: <a href="https://www.math.toronto.edu/ivrii/PDE-textbook/Chapter3/S3.1.V.html">반사 반직선의 노이만 이미지 해</a>; '
        '<a href="https://ocw.mit.edu/courses/6-021j-quantitative-physiology-cells-and-tissues-fall-2004/2dec3d0ac557365b9b31de361b77e3ad_macro.pdf">MIT OpenCourseWare 확산 모델</a>.'
    )
    thermal = '<section id="thermal-lab" class="lab-card wide" data-thermal-lab ' + \
        'data-temp-label="' + e(t["temp"]) + '" data-time-label="' + e(t["duration"]) + '" data-remove-label="' + e(t["remove"]) + '" ' + \
        'data-sigma-label="' + e(t["sigma_final"]) + '" data-peak-label="' + e(t["peak"]) + '" data-crossing-label="' + e(t["crossing"]) + '" data-no-crossing-label="' + e(t["no_crossing"]) + '" ' + \
        'data-surface-warning="' + e(t["surface_warning"]) + '" data-concentration-warning="' + e(t["concentration_warning"]) + '" data-model-status="' + e(t["model_status"]) + '" data-invalid-result="' + e(t["invalid_result"]) + '" ' + \
        'data-chart-x-label="' + e(t["chart_x"]) + '" data-chart-y-label="' + e(t["chart_y"]) + '" data-background-label="' + e(t["chart_bg"]) + '" data-no-crossing-chart-label="' + e(t["chart_bg_no_crossing"]) + '">' + \
        '<span class="evidence-label">' + e(t["model_checked"]) + '</span><h2>' + e(t["thermal_title"]) + '</h2><p>' + e(t["thermal_copy"]) + '</p><p class="status-line">' + thermal_sources + '</p>' + \
        '<h3>' + e(t["profile_inputs"]) + '</h3><div class="lab-form">' + \
        field("sigma0Nm", t["sigma0"], 20, 0.5, 100, "0.5", "data-profile-input") + field("projectedRangeNm", t["rp"], 80, 0, 500, "1", "data-profile-input") + \
        field("doseCm2", t["dose"], 2e13, 1e11, 1e15, "1", "data-profile-input") + field("backgroundCm3", t["background"], 1e16, 1e14, 1e19, "1", "data-profile-input") + '</div>' + \
        '<h3>' + e(t["holds"]) + '</h3><div class="hold-list" data-hold-list></div><div class="button-row"><button class="button" type="button" data-add-hold aria-describedby="hold-limit-note">' + e(t["add_hold"]) + '</button><button class="button" type="button" data-reset-thermal>' + e(t["reset"]) + '</button></div><p class="status-line" id="hold-limit-note">' + e(t["hold_limit"]) + '</p>' + \
        '<h3>' + e(t["results"]) + '</h3><div class="result-grid" data-thermal-output aria-live="polite"></div><p class="status-line" data-thermal-status role="status"></p>' + \
        '<figure class="chart-wrap"><svg data-profile-chart role="img" aria-label="' + e(t["chart_aria"]) + '" viewBox="0 0 720 260"></svg><figcaption class="chart-caption">' + e(t["chart_bg"]) + '</figcaption></figure>' + \
        '<p class="status-line">' + e(t["model_status"]) + ' <a href="' + e(relative(current, "references.html" if lang == "en" else "references.html")) + '">' + e(t["references"]) + '</a></p></section>'
    dependency = '<section id="dependency-explorer" class="lab-card" data-dependency-explorer ' + \
        'data-gate-text="' + e(t["gate_text"]) + '" data-contact-text="' + e(t["contact_text"]) + '" data-interconnect-text="' + e(t["beol_text"]) + '">' + \
        '<span class="evidence-label">' + e(t["qualitative"]) + '</span><h2>' + e(t["dependency_title"]) + '</h2><p>' + e(t["dependency_copy"]) + '</p>' + \
        '<div class="dependency-controls"><div class="field"><label for="dependency-focus">' + e(t["choose_question"]) + '</label><select id="dependency-focus"><option value="gate">' + e(t["gate_option"]) + '</option><option value="contact">' + e(t["contact_option"]) + '</option><option value="interconnect">' + e(t["beol_option"]) + '</option></select></div></div>' + \
        '<div class="dependency-map" aria-label="' + e(t["dependency_title"]) + '">' + \
        node("device", t["node_device"]) + node("gate", t["node_gate"]) + node("thermal", t["node_thermal"]) + node("pattern", t["node_pattern"]) + \
        node("etch", t["node_etch"]) + node("contact", t["node_contact"]) + node("metal", t["node_metal"]) + node("reliability", t["node_reliability"]) + '</div>' + \
        '<p class="decision-output" data-dependency-output aria-live="polite"></p>' + render_dependency_relations(t) + '</section>'
    challenge = '<section id="integration-review" class="lab-card" data-evidence-challenge><span class="evidence-label">' + e(t["synthetic"]) + '</span><h2>' + e(t["challenge_title"]) + '</h2><p>' + e(t["challenge_copy"]) + '</p><div class="choice-list">' + \
        choice("a", t["choice_a"], t["feedback_a"]) + choice("b", t["choice_b"], t["feedback_b"]) + choice("c", t["choice_c"], t["feedback_c"]) + '</div>' + \
        '<p class="decision-output" data-evidence-feedback aria-live="polite"></p><p class="status-line">' + e(t["challenge_note"]) + '</p></section>'
    body = '<section class="section-heading"><div><p class="kicker">' + e(t["eyebrow"]) + '</p><h1>' + e(t["lab_title"]) + '</h1><p>' + e(t["lab_copy"]) + '</p></div></section><div class="lab-grid">' + thermal + dependency + challenge + '</div>'
    return shell(manifest, lang, current, t["lab_title"] + " · ProcessIntegrationBook", t["lab_copy"], "lab", body, ("labs/thermal-model.js",))


def render_dependency_relations(t):
    cases = {
        "gate": [("device", "gate", "compatibility", "open"), ("gate", "thermal", "precedence", "assumption"), ("thermal", "contact", "inference", "measurement")],
        "contact": [("pattern", "etch", "precedence", "assumption"), ("etch", "contact", "compatibility", "measurement"), ("contact", "metal", "inference", "open")],
        "interconnect": [("thermal", "metal", "compatibility", "open"), ("gate", "thermal", "precedence", "assumption"), ("metal", "reliability", "inference", "measurement")],
    }
    labels = {key: t["node_" + key] for key in ("device", "gate", "thermal", "pattern", "etch", "contact", "metal", "reliability")}
    output = []
    for case, rows in cases.items():
        items = []
        for source, target, kind, status in rows:
            items.append('<li class="dependency-relation"><span class="relation-path"><span>' + e(labels[source]) + '</span><span class="relation-arrow" aria-hidden="true">→</span><span>' + e(labels[target]) + '</span></span><span class="relation-type">' + e(t["relation_type_" + kind]) + '</span><span class="relation-evidence">' + e(t["relation_status_" + status]) + '</span></li>')
        output.append('<ul class="relation-list" data-relation-case="' + case + '"' + ('' if case == "gate" else ' hidden') + '>' + ''.join(items) + '</ul>')
    return '<div class="dependency-relations" aria-label="' + e(t["dependency_title"]) + '">' + ''.join(output) + '</div>'


def field(name, label, value, minimum, maximum, step, marker):
    fid = "input-" + name
    return '<div class="field"><label for="' + e(fid) + '">' + e(label) + '</label><input id="' + e(fid) + '" type="number" min="' + e(minimum) + '" max="' + e(maximum) + '" step="' + e(step) + '" value="' + e(value) + '" data-profile-input="' + e(name) + '"></div>'


def node(key, label):
    return '<div class="dependency-node" data-dependency-node="' + e(key) + '" data-active="false">' + e(label) + '</div>'


def choice(key, label, feedback):
    return '<button type="button" data-evidence-choice="' + key + '" data-feedback="' + e(feedback) + '" aria-pressed="false">' + e(label) + '</button>'


REFERENCES = [
    ("Fair (1975)", "Boron diffusion: concentration, orientation, background, and profile estimation", "https://doi.org/10.1149/1.2134326", "DOI / publisher", "DOI / 출판사"),
    ("Bracht et al. (2007)", "Silicon diffusion measurements and native point-defect contributions", "https://doi.org/10.1103/PhysRevB.75.035211", "DOI / publisher", "DOI / 출판사"),
    ("Sadigh et al. (1999)", "Atomistic and kinetic Monte Carlo study of boron diffusion mechanism", "https://doi.org/10.1103/PhysRevLett.83.4341", "DOI / publisher", "DOI / 출판사"),
    ("Yeo (2004)", "Metal-gate material selection and process-integration issues", "https://doi.org/10.1016/j.tsf.2004.05.039", "DOI / publisher", "DOI / 출판사"),
    ("Aitken et al. (2016)", "Predictive technology and design-technology co-optimization", "https://doi.org/10.1049/iet-cdt.2015.0210", "DOI / publisher", "DOI / 출판사"),
    ("Mistry et al. (IEDM 2007)", "Publicly reported 45 nm platform feature list; source-limited case in chapter 13", "https://doi.org/10.1109/IEDM.2007.4418914", "DOI / publisher", "DOI / 출판사"),
    ("Esser et al. (2004)", "Public calculation reproducing the boron Arrhenius pair; cites Sze (1983) as the historical source", "https://doi.org/10.1149/1.1731558", "DOI / publisher", "DOI / 출판사"),
    ("Mostafa and Medraj (2017)", "Review reproducing the intrinsic boron diffusivity equation and units; cites Scotten (2000), whose source page was not independently checked", "https://doi.org/10.3390/ma10060676", "DOI / full text", "DOI / 원문"),
    ("Sze, ed. (1983)", "VLSI Technology; historical source cited by Esser et al., without an independently verified page locator", "https://openlibrary.org/books/OL3504531M/VLSI_technology", "Catalog record", "도서관 서지 기록"),
    ("Sze and Ng (2007)", "General semiconductor-device reference; not used as the source for the selected Arrhenius pair", "https://doi.org/10.1002/0470068329", "Publisher record", "출판사 서지 기록"),
]


def render_references(manifest, lang):
    t = TEXT[lang]
    current = "references.html" if lang == "en" else "ko/references.html"
    source_titles = ["Public papers and technical background", "공개 논문 및 기술 배경"]
    list_html = "".join('<li><strong>' + e(author) + '</strong> — ' + e(note) + '. <a href="' + e(url) + '" rel="noopener">' + e(link_en if lang == "en" else link_ko) + '</a>.</li>' for author, note, url, link_en, link_ko in REFERENCES)
    scope_names = ["Independent books used for scope comparison", "범위 비교에 사용한 독립 교재"]
    items = [
        ("ProcessBook", "https://github.com/geniuskey/processbook/tree/f583bc33c5dfdd31292f7ef6826ce24a2c8b7fed"),
        ("DopingBook", "https://github.com/geniuskey/dopingbook/tree/944526d6c2bb790d5d8f1e08d2614e1c5de22c3c"),
        ("LithoBook", "https://github.com/geniuskey/lithobook/tree/5a4fa0a5b79f3d5581af140caa0e7831ccf88a05"),
        ("EtchBook", "https://github.com/geniuskey/etchbook/tree/0881e61ba16003a1fe4579a8372dad2d63d2dcfb"),
        ("TCADBook", "https://github.com/geniuskey/tcadbook/tree/56d3c14f757a55caed574e720069cfdf2b7a2bf6"),
        ("YieldBook", "https://github.com/geniuskey/yieldbook/tree/2acd8844633274ebea91e808c4a22ed4035549b8"),
        ("PMICBook", "https://github.com/frbread7/pmicbook/"),
        ("WATBook", "https://github.com/frbread7/watbook/")
    ]
    scope_html = "".join('<li><a href="' + e(url) + '" rel="noopener">' + e(name) + '</a></li>' for name, url in items)
    if lang == "ko":
        source_heading = source_titles[1]
        scope_heading = scope_names[1]
        scope_note = '이 독립 교재들은 별도 프로젝트입니다. 본문, 그림, 코드, 실험을 복제하지 않았습니다. 샘플링 범위와 한계는 <a href="https://github.com/frbread7/processintegrationbook/blob/main/docs/OVERLAP_AUDIT.md">중복·차별화 감사</a>에서 확인할 수 있습니다.'
    else:
        source_heading = source_titles[0]
        scope_heading = scope_names[0]
        scope_note = 'These independent books are separate projects. No prose, figures, code, or experiments are reproduced. See the <a href="https://github.com/frbread7/processintegrationbook/blob/main/docs/OVERLAP_AUDIT.md">overlap audit</a> for sampling scope and limitations.'
    body = '<p class="eyebrow">' + e(t["eyebrow"]) + '</p><h1>' + e(t["references_title"]) + '</h1><p>' + e(t["references_copy"]) + '</p><section class="panel" style="padding:1rem"><h2>' + e(source_heading) + '</h2><ol class="reference-list">' + list_html + '</ol></section><section class="panel" style="padding:1rem;margin-top:1rem"><h2>' + e(scope_heading) + '</h2><ul>' + scope_html + '</ul><p>' + scope_note + '</p></section>'
    return shell(manifest, lang, current, t["references_title"] + " · ProcessIntegrationBook", t["references_copy"], "references", body)


def render_license(manifest, lang):
    t = TEXT[lang]
    current = "license.html" if lang == "en" else "ko/license.html"
    if lang == "ko":
        body = '<p class="eyebrow">ProcessIntegrationBook</p><h1>' + e(t["license_title"]) + '</h1><p>' + e(t["license_copy"]) + '</p><section class="panel" style="padding:1rem"><h2>원본 자료</h2><p>이 저장소의 원본 교육용 글, 한국어 번역, 도표, 합성 학습 예시는 <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>으로 제공됩니다. 원본 소프트웨어 코드는 <a href="https://opensource.org/license/mit/">MIT License</a>를 따릅니다.</p><p>인용한 제3자 자료와 독립 교재는 각자의 저작권 및 이용 조건을 유지합니다. 참고 문헌은 인용과 추가 학습을 위한 링크이며 해당 자료의 글, 도표, 코드, 실험을 포함하지 않습니다.</p><p>합성 예시는 팹 데이터가 아닙니다. 열 이력 계산은 분석식으로 교차 확인한 제한된 교육 모델이며, 실제 실리콘 검증 또는 공정 보정 결과가 아닙니다.</p><p><a href="https://github.com/frbread7/processintegrationbook/blob/main/THIRD_PARTY_NOTICES.md">제3자 고지</a> · <a href="https://github.com/frbread7/processintegrationbook/blob/main/docs/REFERENCES.md">참고 문헌</a></p></section>'
    else:
        body = '<p class="eyebrow">ProcessIntegrationBook</p><h1>' + e(t["license_title"]) + '</h1><p>' + e(t["license_copy"]) + '</p><section class="panel" style="padding:1rem"><h2>Original material</h2><p>Original educational prose, Korean translation, diagrams, and synthetic learning examples in this repository are offered under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Original software code is offered under the <a href="https://opensource.org/license/mit/">MIT License</a>.</p><p>Cited third-party papers and independent textbooks retain their own rights and terms. References are links for attribution and further reading; this site does not reproduce their text, figures, code, or experiments.</p><p>Synthetic examples are not fab data. The thermal-history calculation is a bounded educational model checked against its analytical equations, not a calibrated process or real-silicon validation.</p><p><a href="https://github.com/frbread7/processintegrationbook/blob/main/THIRD_PARTY_NOTICES.md">Third-party notices</a> · <a href="https://github.com/frbread7/processintegrationbook/blob/main/docs/REFERENCES.md">References</a></p></section>'
    return shell(manifest, lang, current, t["license_title"] + " · ProcessIntegrationBook", t["license_copy"], "", body)


def generated_pages(manifest):
    pages = {"index.html": render_home(manifest, "en"), "ko/index.html": render_home(manifest, "ko"),
             "lab.html": render_lab(manifest, "en"), "ko/lab.html": render_lab(manifest, "ko"),
             "references.html": render_references(manifest, "en"), "ko/references.html": render_references(manifest, "ko"),
             "license.html": render_license(manifest, "en"), "ko/license.html": render_license(manifest, "ko")}
    for chapter in manifest["chapters"]:
        pages["chapters/" + chapter["id"] + ".html"] = render_chapter(manifest, chapter, "en")
        pages["ko/chapters/" + chapter["id"] + ".html"] = render_chapter(manifest, chapter, "ko")
    paths = [manifest["productionUrl"]]
    for relative_path in pages:
        if relative_path == "index.html": paths.append(manifest["productionUrl"])
        elif relative_path == "ko/index.html": paths.append(manifest["productionUrl"] + "ko/")
        else: paths.append(manifest["productionUrl"] + relative_path)
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join("<url><loc>" + e(url) + "</loc></url>" for url in sorted(set(paths))) + "</urlset>\n"
    pages["sitemap.xml"] = sitemap
    pages["robots.txt"] = "User-agent: *\nAllow: /\nSitemap: " + manifest["productionUrl"] + "sitemap.xml\n"
    return pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated pages are current without writing files")
    args = parser.parse_args()
    try:
        manifest = read_manifest()
        validate(manifest)
        pages = generated_pages(manifest)
        stale, missing = [], []
        for name, content in pages.items():
            path = SITE / name
            if args.check:
                if not path.is_file(): missing.append(name)
                elif path.read_text(encoding="utf-8") != content: stale.append(name)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
        if args.check and (missing or stale):
            if missing: print("Missing generated pages: " + ", ".join(missing), file=sys.stderr)
            if stale: print("Stale generated pages: " + ", ".join(stale), file=sys.stderr)
            return 1
        if args.check: print("Site generation check passed: " + str(len(pages)) + " routes are current.")
        else: print("Generated " + str(len(pages)) + " pages from the validated manifest.")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("build_site: error: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
