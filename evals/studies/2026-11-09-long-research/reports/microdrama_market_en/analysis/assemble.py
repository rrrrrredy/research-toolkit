"""Assemble the independently authored English units. No external model or network calls."""
from pathlib import Path
import json, re, hashlib

here = Path(__file__).resolve().parent
pack = here.parents[2] / 'frozen-alternate-inputs' / 'microdrama_market_en'
sources = json.loads((pack / 'sources.json').read_text(encoding='utf-8-sig'))
units = sorted((here / 'units').glob('*.md'))
body = '\n\n'.join(p.read_text(encoding='utf-8').strip() for p in units)
used = set(re.findall(r'\[((?:MDX?|CP)\d+)\]', body))
refs = '\n'.join(f'[{s["source_id"]}]: {s["url"]}' for s in sources if s['source_id'] in used)
assembled = body + '\n\n' + refs + '\n'
for name in ['draft-first.md', 'author-original-complete-response.md']:
    target = here / name
    if target.exists():
        raise FileExistsError(f'Preserved first manuscript must not be overwritten: {target}')
    target.write_text(assembled, encoding='utf-8')
(here / 'draft-current.md').write_text(assembled, encoding='utf-8')
receipt = {
    'author': 'Current Codex agent /root/microdrama_english_independent_author',
    'independent_english_context': True,
    'api_used': False,
    'chinese_answer_or_reviews_read': False,
    'units': [{'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in units],
    'first_manuscript_sha256': hashlib.sha256((here/'draft-first.md').read_bytes()).hexdigest(),
    'normalized_lf_content_sha256': hashlib.sha256(assembled.encode()).hexdigest(),
    'body_words_whitespace': len(body.split()),
    'used_source_ids': sorted(used),
    'status': 'First complete author draft; independent review and acceptance pending',
    'original_response_note': 'The complete authored report is preserved verbatim; it was written through local unit-file tool calls, not obtained from an API response.'
}
(here / 'assembly-record.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: receipt[k] for k in ['body_words_whitespace', 'first_manuscript_sha256', 'status']}))
