"""Readable, lossless views of existing research inputs; no workflow decisions."""
from __future__ import annotations

import hashlib
import html
import json
import posixpath
import re
from urllib.parse import quote

from task_storage import safe_path


def reading_view(root, value):
    """Keep JSON authoritative and expose its text without JSON string escaping.

    Content-addressed pages share unchanged text across work and review roles.
    Returned references are presentation only: never add them to review bindings
    or use them as evidence that someone read or approved the input.
    """
    folder = 'logs/reading'

    def store(text, suffix):
        data = text.encode('utf-8')
        checksum = hashlib.sha256(data).hexdigest()
        name = f'{folder}/{checksum[:20]}.{suffix}'
        path = safe_path(root, name)
        if path.exists():
            if path.read_bytes() != data:
                raise ValueError('Retained reading view changed: ' + name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        return {'path': name, 'sha256': checksum}

    def link(ref, label):
        target = quote(posixpath.relpath(ref['path'], folder), safe='/')
        escaped = re.sub(r'([\\\[\]`*_])', r'\\\1', html.escape(label))
        return f'[{escaped}]({target})'

    def literal(item):
        return '<code>' + html.escape(json.dumps(item, ensure_ascii=False)) + '</code>'

    def leaf(item, key):
        if isinstance(item, str):
            if '\n' in item or '\r' in item or len(item) > 240:
                ref = store(item, 'txt')
                return link(ref, 'Full text / 完整原文') + f' ({len(item.splitlines())} lines / 行)'
            if key == 'path':
                try:
                    safe_path(root, item)
                except ValueError:
                    pass
                else:
                    return link({'path': item}, item)
        return literal(item)

    def rows(item, depth=0, key=''):
        # Keep all fields and list order, including false, zero, null and empty values.
        if not isinstance(item, (dict, list)) or not item:
            return ['  ' * depth + '- ' + leaf(item, key)]
        result = []
        entries = item.items() if isinstance(item, dict) else enumerate(item)
        for name, child in entries:
            label = link({'path': str(name)}, str(name)) if key == 'source_files' else literal(name)
            if isinstance(child, (dict, list)) and child:
                result.append('  ' * depth + '- ' + label + ':')
                result.extend(rows(child, depth + 1, str(name)))
            else:
                result.append('  ' * depth + '- ' + label + ': ' + leaf(child, str(name)))
        return result

    def document(item, title):
        lines = ['# ' + html.escape(title), '',
                 'Read the linked full text and original references as needed for this assignment. '
                 'Long files can be read by line range; this view does not summarize or shorten them.',
                 '按当前任务读取链接中的完整文本和原件；长文件可按行段阅读，本视图不摘要或删减原文。', '']
        for key, child in item.items():
            lines.extend(['## ' + html.escape(str(key)), ''])
            if isinstance(child, dict) and key in {
                    'assignment', 'files', 'sources', 'analyses', 'reviews', 'audit', 'revision_context'}:
                ref = document(child, str(key))
                lines.append(link(ref, 'Open / 打开 ' + str(key)))
            elif isinstance(child, (dict, list)) and child:
                ref = store('# ' + html.escape(str(key)) + '\n\n' + '\n'.join(rows(child, key=str(key))) + '\n', 'md')
                lines.append(link(ref, 'Open / 打开 ' + str(key)))
            else:
                lines.append(leaf(child, str(key)))
            lines.append('')
        return store('\n'.join(lines), 'md')

    return document(value, 'Research input / 研究输入')
