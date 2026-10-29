"""Problem-selected methods from named blocks in the existing references."""
from __future__ import annotations
from pathlib import Path
from profile_policy import LITE_LOG

TOOLKIT = Path(__file__).resolve().parents[1]
# Agent-facing guidance for unresolved fields, not a questionnaire to forward.
BRIEF_FIELDS = {
    "question": "Use the stated topic; ask what the user wants to understand or decide only if unclear.",
    "audience": "Infer the reader and purpose from context; ask only if different uses would change the report.",
    "scope": "Propose specific subjects, places and dates to cover; explain consequential alternatives before asking the user to choose.",
    "output": "Propose a concrete deliverable in the requested format and language; clarify only constraints that cannot be inferred.",
    "depth": "Describe the questions to answer and the comparisons, explanations or evidence the result will contain; clarify consequential trade-offs with concrete examples.",
    "evidence_standard": "Apply suitable source standards and supplied materials; ask only about required materials, access or evidence constraints needing a user decision.",
}
BRIEF_FIELDS_ZH = {
    "question": "沿用已给出的题目；只有目标不明时，才询问用户想理解什么或据此决定什么。",
    "audience": "从上下文判断读者与用途；只有不同用途会改变报告时才询问。",
    "scope": "先提出具体覆盖哪些对象、地区和时段；需要用户取舍时，说明实际备选及其影响。",
    "output": "依据已知形式和语言提出具体交付物；仅澄清无法推断的必要限制。",
    "depth": "先说明要回答哪些问题、完成哪些比较和解释、提供什么证据；需要取舍时用具体成果差别提问。",
    "evidence_standard": "采用适当的来源标准并沿用已提供材料；仅询问需要用户决定的必读材料、访问条件或证据限制。",
}
STAGE_FILES = {
    "brief": ["references/research-workflow.md"],
    "collect": ["references/research-workflow.md", "references/research-standard.md"],
    "analyze": ["references/research-standard.md"],
    "draft": ["references/writing-style.md"],
    "review": ["references/subagents-and-review-loop.md"],
    "revise": ["references/writing-style.md", "references/subagents-and-review-loop.md"],
    "final": ["references/quality-gates.md", "docs/delivery-verification.md"],
}
def normalize_language(language: str) -> str:
    if language in ("zh", "zh-CN"):
        return "zh"
    if language == "en":
        return "en"
    raise ValueError('language must be "en" (English), "zh" or "zh-CN" (Chinese).')



# Named blocks survive heading renumbering and keep one maintained method original.
METHODS = {
    'brief': ('references/research-workflow.md', ['brief', 'spec', 'units', 'depth']),
    'collect': ('references/research-workflow.md', ['sources', 'claims']),
    'evidence': ('references/research-standard.md', ['evidence', 'source-safety']),
    'analyze': ('references/research-standard.md', ['research-loop', 'lenses']),
    'write': ('references/writing-style.md', ['writing', 'language-style']),
    'review': ('references/subagents-and-review-loop.md', ['review']),
    'deliver': ('references/quality-gates.md', None),
    'delivery-records': ('docs/delivery-verification.md', None),
    'compare': ('references/optional-analysis-lenses.md', ['compare']),
    'explain': ('references/optional-analysis-lenses.md', ['explain']),
    'synthesize': ('references/optional-analysis-lenses.md', ['synthesize']),
    'recommend': ('references/optional-analysis-lenses.md', ['recommend']),
    'depth': ('references/research-workflow.md', ['depth']),
    'assemble': ('references/research-workflow.md', ['assembly']),
    'delegate': ('references/subagents-and-review-loop.md', ['delegate']),
    'resume': ('references/task-continuity.md', None),
}
STAGE_METHODS = {
    'brief': ['brief'], 'collect': ['collect', 'evidence'],
    'analyze': ['analyze', 'evidence'], 'draft': ['write'],
    'review': ['review'], 'revise': ['write', 'review'],
    'final': ['deliver', 'delivery-records'],
}


def guidance(stage: str, language: str = 'en', profile: str = 'full', methods: list[str] | None = None) -> dict:
    language = normalize_language(language)
    if profile not in {'lite', 'full'}:
        raise ValueError('Profile must be lite or full.')
    if stage not in STAGE_METHODS:
        raise ValueError('stage must be brief/collect/analyze/draft/review/revise/final.')
    selected = STAGE_METHODS[stage] if methods is None else methods
    if not isinstance(selected, list) or not selected or any(not isinstance(m, str) or m not in METHODS for m in selected):
        raise ValueError('methods: use a nonempty list from ' + ', '.join(METHODS) + '.')
    files = {}
    for method in dict.fromkeys(selected):
        name, blocks = METHODS[method]
        if language == 'zh':
            name = name.replace('.md', '.zh-CN.md')
        text = (TOOLKIT / name).read_text(encoding='utf-8')
        entry = files.setdefault(name, {'path': name, 'content': '', 'methods': []})
        entry['methods'].append(method)
        if blocks is None:
            entry['content'] = text
            continue
        if not entry['content']:
            entry['content'] = text.split('<!-- method:', 1)[0].split('\n## ', 1)[0].strip() + '\n\n'
        for block in blocks:
            begin, end = f'<!-- method:{block} -->', f'<!-- /method:{block} -->'
            if text.count(begin) != 1 or text.count(end) != 1:
                raise ValueError(f'Method {block} is missing or duplicated in {name}.')
            section = text.split(begin, 1)[1].split(end, 1)[0].strip()
            if section not in entry['content']:
                entry['content'] += section + '\n\n'
    return {'stage': stage, 'guidance': list(files.values()), 'profile': profile,
            'available_methods': list(METHODS),
            'profile_policy': LITE_LOG if profile == 'lite' else ['Use the declared reviewer tier; unconfigured new tasks use author self-review.']}
