import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'plugins/plugin-creator-plus/skills/plugin-creator-plus/scripts/release.py'
spec = importlib.util.spec_from_file_location('release', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'demo-plugin'
        (self.root / '.codex-plugin').mkdir(parents=True)
        (self.root / 'skills/demo').mkdir(parents=True)
        (self.root / 'skills/demo/SKILL.md').write_text('---\nname: demo\ndescription: Demonstrate one task.\n---\nDo it.\n')
        self.manifest = {'name': 'demo-plugin', 'version': '1.2.3+codex.20260910',
                         'description': 'A useful plugin', 'author': {'name': 'Test Publisher'},
                         'skills': './skills/', 'interface': {'displayName': 'Demo Plugin',
                         'shortDescription': 'A useful workflow', 'longDescription': 'Runs a useful local task.',
                         'developerName': 'Test Publisher', 'category': 'Developer Tools'}}
        self.save()

    def save(self):
        (self.root / module.MANIFEST).write_text(json.dumps(self.manifest))

    def test_deterministic_archive_and_source_preserved(self):
        a = module.release(self.root, self.base / 'dist')
        b = module.release(self.root, self.base / 'dist')
        self.assertEqual(a['sha256'], b['sha256'])
        with zipfile.ZipFile(a['zip']) as archive:
            self.assertEqual(json.loads(archive.read(module.MANIFEST))['version'], '1.2.3')
            self.assertEqual(set(archive.namelist()), set(a['files']))
        self.assertEqual(json.loads((self.root / module.MANIFEST).read_text())['version'], '1.2.3+codex.20260910')

    def test_rejects_directory_category_and_length_blockers(self):
        for key, value in [('category', 'Developer'), ('displayName', 'a' * 31), ('shortDescription', 'b' * 31)]:
            with self.subTest(key=key):
                original = self.manifest['interface'][key]
                self.manifest['interface'][key] = value
                self.save()
                with self.assertRaises(ValueError):
                    module.release(self.root)
                self.manifest['interface'][key] = original

    def test_sensitive_file_prevents_archive_creation(self):
        (self.root / 'skills/demo/.env').write_text('sample-only')
        with self.assertRaisesRegex(ValueError, 'Sensitive filename'):
            module.release(self.root, self.base / 'dist')
        self.assertFalse((self.base / 'dist').exists())

    def test_rejects_external_symlink(self):
        outside = self.base / 'private.txt'
        outside.write_text('sample-only')
        (self.root / 'skills/demo/link').symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'Symlinks'):
            module.release(self.root)

    def test_rejects_mcp_instead_of_silently_removing_it(self):
        self.manifest['mcpServers'] = './.mcp.json'
        self.save()
        with self.assertRaisesRegex(ValueError, 'With MCP'):
            module.release(self.root)

    def test_output_cannot_contaminate_plugin(self):
        with self.assertRaisesRegex(ValueError, 'outside'):
            module.release(self.root, self.root / 'assets/dist')

    def test_optional_urls_and_invalid_url(self):
        module.release(self.root)
        self.manifest['interface']['privacyPolicyURL'] = 'https://user:password@example.com/policy'
        self.save()
        with self.assertRaisesRegex(ValueError, 'HTTPS URL'):
            module.release(self.root)

    def test_rejects_duplicate_prompts(self):
        self.manifest['interface']['defaultPrompt'] = ['Do the task', 'Do  the task']
        self.save()
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            module.release(self.root)

    def test_rejects_missing_asset(self):
        self.manifest['interface']['logo'] = './assets/missing.png'
        self.save()
        with self.assertRaisesRegex(ValueError, 'missing packaged image'):
            module.release(self.root)


if __name__ == '__main__':
    unittest.main()
