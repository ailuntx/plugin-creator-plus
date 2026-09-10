#!/usr/bin/env python3
"""Check common directory blockers and package one skills-only plugin. No network."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import unicodedata
from urllib.parse import urlsplit
import zipfile

MANIFEST = '.codex-plugin/plugin.json'
CATEGORIES = {'Productivity', 'Creativity', 'Developer Tools', 'Business & Operations',
              'Data & Analytics', 'Communication', 'Education & Research', 'Security',
              'Finance', 'Healthcare', 'Travel', 'Entertainment', 'Other'}
SKIP = {'.git', '__pycache__', '.DS_Store'}
ROOTS = {'.codex-plugin', 'skills', 'assets', 'docs', 'scripts', 'LICENSE', 'LICENSE.md',
         'NOTICE', 'README.md'}
SECRET_NAMES = {'credentials.json', 'auth.json', 'id_rsa', 'id_ed25519', 'authorized_keys'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text_field(obj, key, limit, single=True):
    value = obj.get(key)
    require(isinstance(value, str) and bool(value.strip()), f'{key}: nonempty text required')
    require(len(value) <= limit, f'{key}: maximum {limit} characters for directory release')
    require(not single or not any(c in value for c in '\r\n'), f'{key}: must be one line')
    require(not any(ord(c) < 32 and c not in '\n\r\t' for c in value), f'{key}: control character')
    return value


def collect(root):
    """Snapshot selected bytes so checks, digest, and ZIP all describe the same content."""
    root = Path(root).expanduser().resolve(strict=True)
    require(root.is_dir(), 'Select the plugin directory, not its containing repository')
    entries = {}
    normalized = set()
    total = 0
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if any(part in SKIP for part in rel.parts) or path.suffix == '.pyc':
            continue
        name = rel.as_posix()
        require(not path.is_symlink(), f'Symlinks are not packaged: {name}')
        require(not path.name.startswith('.env') and path.name not in SECRET_NAMES
                and path.suffix.lower() not in {'.key', '.p12', '.pfx', '.pem'},
                f'Sensitive filename must be outside the plugin: {name}')
        require(rel.parts[0] not in {'.mcp.json', 'mcp.json', '.app.json'},
                'MCP/apps configuration requires the With MCP portal workflow')
        require(rel.parts[0] in ROOTS, f'Unexpected plugin-root content: {name}')
        require(len(rel.parts) <= 20 and all(p == p.strip() for p in rel.parts)
                and '\\' not in name, f'Invalid archive path: {name}')
        key = unicodedata.normalize('NFC', name).casefold()
        require(key not in normalized, f'Case/Unicode path collision: {name}')
        normalized.add(key)
        if path.is_dir():
            continue
        info = path.stat()
        require(stat.S_ISREG(info.st_mode), f'Not a regular file: {name}')
        require(info.st_size <= 100 * 1024**2, f'File too large: {name}')
        total += info.st_size
        require(total <= 512 * 1024**2, 'Uncompressed package exceeds 512 MiB')
        require(len(entries) < 5000, 'Package exceeds 5000 files')
        entries[name] = (path.read_bytes(), bool(info.st_mode & 0o111))
    require(MANIFEST in entries, 'Missing .codex-plugin/plugin.json; select the plugin root')
    manifest = json.loads(entries[MANIFEST][0])
    require(isinstance(manifest, dict), 'Manifest must be an object')
    require(not any(k in manifest for k in ('mcpServers', 'apps')),
            'MCP/apps configuration requires the With MCP portal workflow')
    name = text_field(manifest, 'name', 64)
    require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name), 'Use a lower-case hyphenated plugin name')
    require(root.name == name, 'Plugin folder name must match manifest name')
    version = text_field(manifest, 'version', 64)
    # Plugin Creator's local cache metadata is not part of the public version.
    version = re.sub(r'\+codex\.[0-9A-Za-z.-]+$', '', version)
    require(re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)'
                         r'(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?'
                         r'(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?', version),
            'version: semantic version required')
    prerelease = version.split('+')[0].partition('-')[2]
    require(not any(p.isdigit() and len(p) > 1 and p.startswith('0')
                    for p in prerelease.split('.')), 'version: numeric prerelease has leading zero')
    manifest['version'] = version
    text_field(manifest, 'description', 1024, single=False)
    author = manifest.get('author')
    require(isinstance(author, dict), 'author: object required')
    text_field(author, 'name', 120)
    interface = manifest.get('interface')
    require(isinstance(interface, dict), 'interface: object required')
    for field, limit in [('displayName', 30), ('shortDescription', 30), ('developerName', 80)]:
        text_field(interface, field, limit)
    text_field(interface, 'longDescription', 4000, single=False)
    require(interface.get('category', 'Other') in CATEGORIES, 'Unsupported public directory category')
    require(not interface.get('screenshots'), 'Screenshots require With MCP and custom UI')
    prompts = interface.get('defaultPrompt', [])
    require(isinstance(prompts, list) and len(prompts) <= 3, 'Use at most three starter prompts')
    seen = set()
    for prompt in prompts:
        text_field({'prompt': prompt}, 'prompt', 128)
        normalized_prompt = ' '.join(unicodedata.normalize('NFKC', prompt).split())
        require(normalized_prompt not in seen, 'Duplicate starter prompt')
        seen.add(normalized_prompt)
    for field in ['websiteURL', 'privacyPolicyURL', 'termsOfServiceURL', 'supportURL']:
        if field in interface:
            value = text_field(interface, field, 1024)
            url = urlsplit(value)
            require(url.scheme == 'https' and bool(url.hostname) and not url.username
                    and not url.password, f'{field}: public HTTPS URL required')
    for field in ['logo', 'composerIcon', 'logoDark']:
        if field in interface:
            value = interface[field]
            require(isinstance(value, str) and value.startswith('./assets/'), f'{field}: use ./assets/')
            require(value[2:] in entries, f'{field}: missing packaged image')
    require(any(re.fullmatch(r'skills/[^/]+/SKILL\.md', p) for p in entries),
            'At least one skills/<name>/SKILL.md is required')
    require(manifest.get('skills', './skills/').rstrip('/') == './skills', 'Use ./skills/')
    entries[MANIFEST] = ((json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode(), False)
    return manifest, entries


def release(root, output=None):
    manifest, entries = collect(root)
    result = {'name': manifest['name'], 'version': manifest['version'], 'files': sorted(entries),
              'checks': 'passed', 'scope': 'common skills-only directory blockers; not server review'}
    if output is None:
        return result
    output = Path(output).expanduser().resolve()
    plugin_root = Path(root).expanduser().resolve()
    require(not output.is_relative_to(plugin_root), 'Output directory must be outside the plugin root')
    output.mkdir(parents=True, exist_ok=True)
    final = output / f"{manifest['name']}-{manifest['version']}.zip"
    fd, temporary = tempfile.mkstemp(prefix='.release-', suffix='.zip', dir=output)
    os.close(fd)
    try:
        with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as archive:
            for name, (data, executable) in sorted(entries.items()):
                item = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
                item.compress_type = zipfile.ZIP_DEFLATED
                item.create_system = 3
                item.external_attr = (stat.S_IFREG | (0o755 if executable else 0o644)) << 16
                archive.writestr(item, data)
        require(Path(temporary).stat().st_size <= 100_000_000, 'Compressed ZIP exceeds 100 MB')
        result['sha256'] = hashlib.sha256(Path(temporary).read_bytes()).hexdigest()
        os.replace(temporary, final)
    finally:
        Path(temporary).unlink(missing_ok=True)
    result['zip'] = str(final)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'package'])
    parser.add_argument('plugin', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if args.command == 'package' and args.out is None:
        parser.error('package requires --out outside the plugin root')
    if args.command == 'check' and args.out is not None:
        parser.error('--out applies only to package')
    try:
        print(json.dumps(release(args.plugin, args.out), ensure_ascii=False, indent=2))
    except (ValueError, OSError, TypeError) as exc:
        print(json.dumps({'checks': 'failed', 'error': str(exc)}, ensure_ascii=False))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
