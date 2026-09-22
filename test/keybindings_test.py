import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("keybindings", ROOT / "scripts/keybindings.py")
keys = importlib.util.module_from_spec(spec)
spec.loader.exec_module(keys)


class KeybindingTests(unittest.TestCase):
    def binding(self, command, **kwargs):
        return dict({"modmask": 72, "key": "N", "keycode": 0,
                     "dispatcher": "exec", "arg": command, "submap": ""}, **kwargs)

    def test_conflicts_refuse_unrelated_commands(self):
        binding = self.binding("some-other-app")
        self.assertEqual(keys.conflicts([binding]), [binding])
        numeric = self.binding("some-other-app", key="", keycode=57)
        self.assertEqual(keys.conflicts([numeric]), [numeric])
        self.assertEqual(keys.conflicts([self.binding("some-other-app", modmask=64)]), [])
        self.assertEqual(keys.conflicts([self.binding("some-other-app", submap="resize")]), [])

    def test_existing_reader_shortcuts_are_replaceable(self):
        for plugin in keys.READER_IDS:
            self.assertEqual(keys.conflicts([self.binding(f"omarchy-shell shell toggle {plugin}")]), [])
            self.assertEqual(keys.conflicts([self.binding(f"omarchy-shell shell toggle {plugin} '{{}}'")]), [])

    def test_similar_or_compound_commands_are_not_owned(self):
        self.assertFalse(keys.owned_command(f"omarchy-shell shell toggle {keys.PLUGIN_ID}; other-app"))
        self.assertFalse(keys.owned_command(f"omarchy-shell shell toggle {keys.PLUGIN_ID}-other"))
        self.assertFalse(keys.owned_command("'bad quote"))

    def test_active_check_requires_new_target_and_default_context(self):
        command = f"omarchy-shell shell toggle {keys.PLUGIN_ID}"
        self.assertTrue(keys.active_shortcut([self.binding(command)]))
        self.assertFalse(keys.active_shortcut([self.binding("omarchy-shell shell toggle omarchy.news")]))
        self.assertFalse(keys.active_shortcut([self.binding(command, submap="resize")]))
        self.assertFalse(keys.active_shortcut([self.binding(command, modmask=64)]))

    def test_roundtrip_retains_user_configuration(self):
        original = '-- personal settings\no.bind("SUPER + P", "Personal", "personal-app")\n'
        installed = keys.updated_text(original)
        self.assertEqual(keys.updated_text(installed), installed)
        self.assertEqual(keys.updated_text(installed, remove=True), original)
        self.assertEqual(keys.updated_text(original, remove=True), original)

    def test_remove_preserves_later_edits(self):
        original = "-- before\n"
        after = "-- my later config\n"
        self.assertEqual(keys.updated_text(keys.updated_text(original) + after, remove=True), original + after)

    def test_damaged_markers_are_not_overwritten(self):
        for text in [keys.BEGIN, keys.END, keys.BLOCK + keys.BLOCK, keys.END + keys.BEGIN]:
            with self.assertRaises(ValueError):
                keys.updated_text(text)

    def test_backup_is_exact_and_repeat_is_noop(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bindings.lua"
            original = b"-- personal config\n"
            path.write_bytes(original)
            backup, changed = keys.write_config(path)
            self.assertTrue(changed)
            self.assertEqual(Path(backup).read_bytes(), original)
            self.assertEqual(keys.write_config(path), (None, False))
            keys.write_config(path, remove=True)
            self.assertEqual(path.read_bytes(), original)

    def test_symlink_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "real.lua"
            target.write_text("-- keep")
            path = Path(folder) / "bindings.lua"
            path.symlink_to(target)
            with self.assertRaises(ValueError):
                keys.write_config(path)
            self.assertEqual(target.read_text(), "-- keep")


if __name__ == "__main__":
    unittest.main()
