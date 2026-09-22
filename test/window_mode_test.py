import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("window_mode", ROOT / "window_mode.py")
mode = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mode)


class WindowModeTests(unittest.TestCase):
    def test_prepare_installs_static_rule_without_mapping_or_dispatch(self):
        responses = [json.dumps([self.monitor(focused=True)]), "ok"]
        with patch.object(mode, "hyprctl", side_effect=responses) as ipc:
            mode.prepare("Centred floating")
        self.assertEqual(ipc.call_args_list[0].args, ("-j", "monitors"))
        operation, rule = ipc.call_args_list[1].args
        self.assertEqual(operation, "eval")
        self.assertIn('initial_title = "^RSS Feed$"', rule)
        self.assertIn('float = true, center = true, size = { 1040, 720 }', rule)
        self.assertIn('rss_feed_mode_rule:set_enabled(false)', rule)
        self.assertIn('rss_feed_mode_key == "floating-1040-720"', rule)

    def test_prepare_tiled_needs_no_window_or_monitor_lookup(self):
        with patch.object(mode, "hyprctl", return_value="ok") as ipc:
            mode.prepare("Tiled")
        self.assertEqual(ipc.call_count, 1)
        self.assertIn('tile = true', ipc.call_args.args[1])
        self.assertNotIn('float = true', ipc.call_args.args[1])

    def test_prepare_fits_focused_monitor_and_rejects_missing_focus(self):
        monitors = [self.monitor(id=2, width=3840), self.monitor(focused=True, scale=1.5)]
        self.assertIn('size = { 1040, 656 }', mode.preparation_rule('Centred floating', monitors))
        with self.assertRaises(ValueError):
            mode.preparation_rule('Centred floating', [self.monitor()])

    def test_prepare_reports_compositor_failure(self):
        with patch.object(mode, 'hyprctl', return_value='Lua error: unavailable'):
            with self.assertRaises(RuntimeError):
                mode.prepare('Tiled')

    def client(self, **changes):
        return dict({"address": "0x123abc", "pid": 123, "title": "RSS Feed",
                     "mapped": True, "hidden": False, "monitor": 1}, **changes)

    def monitor(self, **changes):
        return dict({"id": 1, "width": 1920, "height": 1080, "scale": 1,
                     "transform": 0, "reserved": [0, 32, 0, 0]}, **changes)

    def test_only_this_shells_reader_is_selected(self):
        own = self.client()
        clients = [self.client(pid=999), self.client(title="Terminal"), own]
        self.assertEqual(mode.reader_client(clients, 123), own)
        self.assertIsNone(mode.reader_client([self.client(hidden=True)], 123))
        self.assertIsNone(mode.reader_client([self.client(mapped=False)], 123))

    def test_ambiguous_or_invalid_addresses_are_refused(self):
        with self.assertRaises(ValueError):
            mode.reader_client([self.client(), self.client(address="0x456")], 123)
        for address in ["", "activewindow", '0x1\" }); evil()']:
            with self.assertRaises(ValueError):
                mode.commands(self.client(address=address), "Tiled", [])

    def test_tiled_is_explicit_and_targets_the_reader(self):
        self.assertEqual(mode.commands(self.client(), "Tiled", []), [
            'hl.dsp.window.float({ window = "address:0x123abc", action = "unset" })'])

    def test_floating_sets_resizes_and_centres_same_window(self):
        commands = mode.commands(self.client(), "Centred floating", [self.monitor()])
        self.assertEqual(len(commands), 3)
        self.assertIn('action = "set"', commands[0])
        self.assertIn('x = 1040, y = 720', commands[1])
        self.assertIn('window.center', commands[2])
        self.assertTrue(all('window = "address:0x123abc"' in command for command in commands))
        self.assertFalse(any('pin' in command or 'focus' in command for command in commands))

    def test_sizing_uses_own_scaled_rotated_monitor(self):
        monitors = [self.monitor(id=2, width=3840, height=2160),
                    self.monitor(width=1920, height=1080, scale=1.5, transform=1)]
        # Rotated logical size is 720 x 1280, constrained by the reader's
        # existing 720-pixel minimum width; height remains at the usual 720.
        self.assertEqual(mode.floating_size(self.client(), monitors), (720, 720))
        self.assertEqual(mode.floating_size(self.client(), [self.monitor(scale=1.5)]), (1040, 656))

    def test_unknown_mode_or_missing_monitor_is_refused(self):
        with self.assertRaises(ValueError):
            mode.commands(self.client(), "anything", [])
        with self.assertRaises(ValueError):
            mode.commands(self.client(), "Centred floating", [])

    def test_waits_for_own_window_mapping_before_dispatch(self):
        responses = ["[]", json.dumps([self.client()]), json.dumps([self.monitor()]), "ok", "ok", "ok"]
        with patch.object(mode, "hyprctl", side_effect=responses) as ipc, patch.object(mode.time, "sleep") as sleep:
            mode.apply("Centred floating", 123)
        self.assertEqual(sleep.call_count, 1)
        self.assertEqual([call.args[0] for call in ipc.call_args_list],
                         ["-j", "-j", "-j", "dispatch", "dispatch", "dispatch"])

    def test_timeout_never_falls_back_to_active_window(self):
        with patch.object(mode, "hyprctl", return_value=json.dumps([self.client(pid=999)])) as ipc, patch.object(mode.time, "sleep"):
            with self.assertRaises(RuntimeError):
                mode.apply("Tiled", 123, attempts=2)
        self.assertEqual(ipc.call_count, 2)
        self.assertTrue(all(call.args == ("-j", "clients") for call in ipc.call_args_list))

    def test_dispatch_failure_stops_remaining_operations(self):
        responses = [json.dumps([self.client()]), json.dumps([self.monitor()]), "unknown dispatcher"]
        with patch.object(mode, "hyprctl", side_effect=responses) as ipc:
            with self.assertRaises(RuntimeError):
                mode.apply("Centred floating", 123)
        self.assertEqual(ipc.call_count, 3)


if __name__ == "__main__":
    unittest.main()
