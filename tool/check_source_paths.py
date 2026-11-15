"""Validate canonical Flutter source paths in Git checkouts and downloaded ZIPs."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent.parent
result = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'], capture_output=True)
tracked = (result.stdout.decode().split('\0') if result.returncode == 0 else [])
paths = {p for p in tracked if p and (root / p).is_file()}
paths.update(str(p.relative_to(root)) for folder in ('lib', 'test', 'tool')
             for p in (root / folder).rglob('*') if p.is_file())
by_case = {}
for path in sorted(paths):
    old = by_case.setdefault(path.casefold(), path)
    if old != path:
        raise SystemExit(f'Conflicting source paths: {old} / {path}')
if not (root / 'lib/main.dart').is_file():
    raise SystemExit('Missing canonical lib/main.dart')
print(f'Source paths are unambiguous ({len(paths)} checked)')
