import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("migration", ROOT / "agents/migrate-settings.py")
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)


class MigrationTests(unittest.TestCase):
    def config(self):
        return {"version": 1, "bar": {"layout": {"right": [
            {"id": migration.OLD, "enabledFeeds": ["hacker-news"],
             "customFeeds": "Example|https://example.com/rss",
             "feedCollections": '[{"id":"work","name":"Work","sources":[]}]',
             "hiddenFeedUrls": ["https://example.com/hidden"], "itemLimit": 20},
            {"id": "other.widget", "answer": 42}
        ]}}, "unrelated": {"theme": "mine"}}

    def test_preserves_settings_and_is_idempotent(self):
        before = self.config()
        after, count = migration.migrate(before)
        self.assertEqual(count, 1)
        expected = dict(before["bar"]["layout"]["right"][0], id=migration.NEW)
        self.assertEqual(after["bar"]["layout"]["right"][0], expected)
        self.assertEqual(before["bar"]["layout"]["right"][0]["id"], migration.OLD)
        self.assertEqual(after["bar"]["layout"]["right"][1], before["bar"]["layout"]["right"][1])
        self.assertEqual(after["unrelated"], before["unrelated"])
        self.assertIn(migration.OLD, after["disabledPlugins"])
        self.assertEqual(migration.migrate(after), (after, 0))

    def test_conflict_does_not_discard_new_settings(self):
        config = self.config()
        config["plugins"] = [{"id": migration.NEW, "itemLimit": 5}]
        with self.assertRaises(ValueError):
            migration.migrate(config)

    def test_migrates_provisional_archive_id(self):
        config = self.config()
        old_id = "io.github.tcballard.rss-reader"
        config["bar"]["layout"]["right"][0]["id"] = old_id
        after, count = migration.migrate(config)
        self.assertEqual(count, 1)
        self.assertEqual(after["bar"]["layout"]["right"][0]["id"], migration.NEW)
        self.assertIn(old_id, after["disabledPlugins"])
        self.assertIn(migration.OLD, after["disabledPlugins"])

    def test_disabled_reader_stays_disabled(self):
        config = self.config()
        config["disabledPlugins"] = [migration.OLD, "other.widget"]
        after, _ = migration.migrate(config)
        self.assertIn(migration.NEW, after["disabledPlugins"])
        self.assertIn("other.widget", after["disabledPlugins"])

    def test_preview_backup_and_apply(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "shell.json"
            original = json.dumps(self.config()).encode()
            path.write_bytes(original)
            self.assertEqual(migration.migrate_file(path), (1, None))
            self.assertEqual(path.read_bytes(), original)
            count, backup = migration.migrate_file(path, True)
            self.assertEqual(count, 1)
            self.assertEqual(backup.read_bytes(), original)
            self.assertEqual(json.loads(path.read_bytes()), migration.migrate(self.config())[0])


if __name__ == "__main__":
    unittest.main()
