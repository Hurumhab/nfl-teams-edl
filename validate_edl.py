"""Validate the list locally and, optionally, the public HTTPS response."""

import argparse
import hashlib
from pathlib import Path
import re
import urllib.request


def validate(data):
    assert data.endswith(b'\n'), 'Missing final LF'
    assert b'\r' not in data, 'Use LF, not CRLF'
    lines = data.decode('ascii').splitlines()
    assert len(lines) == 64, f'Expected 64 entries, got {len(lines)}'
    assert lines == sorted(set(lines)), 'Entries must be unique and sorted'
    assert all(re.fullmatch(r'(?:www\.)?[a-z0-9]+(?:-[a-z0-9]+)*\.com', line) for line in lines), 'Invalid domain entry'
    roots = {line for line in lines if not line.startswith('www.')}
    assert len(roots) == 32, 'Expected 32 team roots'
    assert set(lines) == roots | {'www.' + root for root in roots}, 'Missing root/www pair'
    return roots


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', help='Also check the published HTTPS text file')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    data = (root / 'docs/nfl-teams.txt').read_bytes()
    roots = validate(data)
    sources = (root / 'SOURCES.md').read_text(encoding='utf-8')
    documented = re.findall(r'^\| ([^|]+) \| `([^`]+)` \| \[www\.([^\]]+)\]\(https://www\.([^/]+)/\) \|$', sources, re.M)
    assert len(documented) == 32 and len({row[0] for row in documented}) == 32, 'Expected 32 distinct documented teams'
    assert {row[1] for row in documented} == roots, 'Sources and EDL differ'
    assert all(row[1] == row[2] == row[3] for row in documented), 'Source host mismatch'
    assert hashlib.sha256(data).hexdigest() in sources, 'Update the documented SHA-256'

    # Exercise the format guard against accidental web pages and malformed edits.
    for bad in (b'<html>error</html>\n', b'\xef\xbb\xbf' + data, data.replace(b'\n', b'\r\n'), b'https://' + data, data.replace(b'.com\n', b'.com/path\n', 1), data + b'\n', data + data.splitlines(keepends=True)[0], data.replace(b'49ers.com\n', b'49ers.net\n', 1)):
        try:
            validate(bad)
        except (AssertionError, UnicodeError):
            continue
        raise AssertionError('Format guard accepted a malformed fixture')

    if args.url:
        assert args.url.startswith('https://'), 'Use HTTPS'
        with urllib.request.urlopen(args.url, timeout=30) as response:
            assert response.status == 200, f'HTTP {response.status}'
            assert response.geturl() == args.url, 'Unexpected redirect'
            assert response.headers.get_content_type() == 'text/plain', response.headers.get('Content-Type')
            published = response.read()
            validate(published)
            assert published == data, 'Published bytes differ from local file'
            print(f'HTTP {response.status}; {response.headers.get("Content-Type")}; no redirect; exact byte match')
    print(f'PASS: 32 teams, 64 domain entries, {len(data)} bytes; SHA-256 {hashlib.sha256(data).hexdigest()}')


if __name__ == '__main__':
    main()
