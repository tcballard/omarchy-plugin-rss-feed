#!/usr/bin/python3
"""Install or remove RSS Feed's Super + Alt + N shortcut on Omarchy Quattro."""

import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

BEGIN = "-- BEGIN RSS Feed shortcut (managed)"
END = "-- END RSS Feed shortcut (managed)"
PLUGIN_ID = "io.github.tcballard.rss-feed"
READER_IDS = {PLUGIN_ID, "omarchy.news", "io.github.tcballard.rss-reader"}
BLOCK = '''-- BEGIN RSS Feed shortcut (managed)
do
  local path = os.getenv("HOME") .. "/.config/omarchy/plugins/io.github.tcballard.rss-feed/keybindings.lua"
  local file = io.open(path, "r")
  if file then
    file:close()
    dofile(path)
  end
end
-- END RSS Feed shortcut (managed)
'''


def owned_command(command):
    try:
        parts = shlex.split(command)
    except ValueError:
        return False
    return (len(parts) in (4, 5) and parts[:3] == ["omarchy-shell", "shell", "toggle"]
            and parts[3] in READER_IDS and (len(parts) == 4 or parts[4] == "{}"))


def conflicts(bindings):
    if not isinstance(bindings, list):
        raise ValueError("Hyprland did not return a binding list")
    result = []
    for binding in bindings:
        if not isinstance(binding, dict):
            raise ValueError("Hyprland returned an invalid binding")
        # XKB's N key is keycode 57 (evdev code 49 + 8); Hyprland's JSON
        # reports its keycode field in XKB units for code-based bindings.
        same_key = str(binding.get("key", "")).lower() == "n" or binding.get("keycode") == 57
        if binding.get("modmask") == 72 and same_key and not binding.get("submap"):
            if binding.get("dispatcher") != "exec" or not owned_command(str(binding.get("arg", ""))):
                result.append(binding)
    return result


def active_shortcut(bindings):
    expected = ["omarchy-shell", "shell", "toggle", PLUGIN_ID]
    for binding in bindings:
        if (binding.get("modmask") == 72 and str(binding.get("key", "")).lower() == "n"
                and not binding.get("submap") and binding.get("dispatcher") == "exec"):
            try:
                if shlex.split(str(binding.get("arg", ""))) == expected:
                    return True
            except ValueError:
                pass
    return False


def updated_text(original, remove=False):
    starts = original.count(BEGIN)
    ends = original.count(END)
    if starts != ends or starts > 1:
        raise ValueError("Managed shortcut markers are damaged; review bindings.lua manually")
    if starts:
        start = original.index(BEGIN)
        end = original.index(END)
        if end < start:
            raise ValueError("Managed shortcut markers are out of order")
        end += len(END)
        if original[end:end + 1] == "\n":
            end += 1
        return original[:start] + ("" if remove else BLOCK) + original[end:]
    if remove:
        return original
    return original + ("\n" if original and not original.endswith("\n") else "") + BLOCK


def write_config(path, remove=False):
    if path.is_symlink():
        raise ValueError("bindings.lua is a symlink; use the documented manual snippet instead")
    exists = path.exists()
    original = path.read_bytes() if exists else b""
    updated = updated_text(original.decode("utf-8"), remove).encode("utf-8")
    if original == updated:
        return None, False
    path.parent.mkdir(parents=True, exist_ok=True)
    backup_path = None
    if exists:
        fd, backup_path = tempfile.mkstemp(prefix="bindings.lua.before-rss-feed-", dir=path.parent)
        with os.fdopen(fd, "wb") as backup:
            backup.write(original)
    fd, temporary = tempfile.mkstemp(prefix=".rss-feed-binding-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(updated)
        if path.is_symlink() or path.exists() != exists or (exists and path.read_bytes() != original):
            raise ValueError("bindings.lua changed during setup; no configuration was replaced")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return backup_path, True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--remove", action="store_true", help="remove only the managed shortcut block")
    args = parser.parse_args()
    home = Path.home()
    try:
        if not args.remove:
            plugin = home / ".config/omarchy/plugins" / PLUGIN_ID
            if not (plugin / "keybindings.lua").is_file():
                raise ValueError("Install RSS Feed before setting up its shortcut")
            hyprland = home / ".config/hypr/hyprland.lua"
            if not hyprland.is_file():
                raise ValueError("This setup requires Quattro's Lua Hyprland configuration")
            result = subprocess.run(["hyprctl", "-j", "binds"], check=True,
                                    capture_output=True, text=True, timeout=10)
            collision = conflicts(json.loads(result.stdout))
            if collision:
                raise ValueError("Super + Alt + N is already used by another action; choose a different shortcut using docs/keybindings.md")
        backup, _ = write_config(home / ".config/hypr/bindings.lua", args.remove)
        if backup:
            print(f"Backup: {backup}")
        # Reload even after an idempotent install, so a previously failed
        # reload can be recovered by rerunning the same command.
        result = subprocess.run(["hyprctl", "reload"], capture_output=True, text=True, timeout=10)
        if result.returncode:
            parser.exit(1, "Configuration saved, but Hyprland reload failed. Run hyprctl reload in your desktop session.\n")
        errors = subprocess.run(["hyprctl", "configerrors"], capture_output=True, text=True, timeout=10)
        if errors.returncode or errors.stdout.strip():
            parser.exit(1, "Configuration saved; Hyprland reports configuration errors. Run hyprctl configerrors and review them before continuing.\n")
        if not args.remove:
            active = subprocess.run(["hyprctl", "-j", "binds"], check=True,
                                    capture_output=True, text=True, timeout=10)
            bindings = json.loads(active.stdout)
            if not isinstance(bindings, list) or not active_shortcut(bindings):
                parser.exit(1, "Configuration saved, but the shortcut is not active. Check that hyprland.lua loads hypr.bindings and no later binding overrides it.\n")
        print("Managed shortcut removed." if args.remove else "Super + Alt + N is ready: RSS Feed.")
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        parser.exit(1, f"Shortcut setup failed: {error}\n")


if __name__ == "__main__":
    main()
