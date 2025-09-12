from __future__ import annotations
import sys, pathlib, ast
ROOT = pathlib.Path('.')
INCLUDE = ('.py', '.md', '.yaml', '.yml')
MAXLEN = 120
violations = []


def check(path: pathlib.Path):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception as e:
        violations.append((str(path), f'unreadable: {e}'))
        return
    if '\r\n' in text:
        violations.append((str(path), 'CRLF line endings'))
    if not text.endswith('\n'):
        violations.append((str(path), 'no trailing newline'))
    for i, line in enumerate(text.splitlines(), 1):
        if line.rstrip() != line:
            violations.append((f"{path}:{i}", 'trailing whitespace'))
        if path.suffix == '.py' and len(line) > MAXLEN:
            violations.append((f"{path}:{i}", f'len {len(line)}>{MAXLEN}'))
    if path.suffix == '.py':
        try:
            ast.parse(text)
        except SyntaxError as e:
            violations.append((str(path), f'syntax error: {e}'))


def main():
    for p in ROOT.rglob('*'):
        if p.is_file() and p.suffix.lower() in INCLUDE:
            check(p)
    if violations:
        print('[GUARDIAN] Air-gapped format violations:')
        for v in violations:
            print(' -', *v)
        sys.exit(2)
    print('[GUARDIAN] Air-gapped formatting gate: PASS')


if __name__ == '__main__':
    main()
