#!/usr/bin/python3
"""Move the built-in reader's shell entries to the standalone plugin, explicitly."""

import argparse
import copy
import json
import os
from pathlib import Path
import tempfile

OLD = "omarchy.news"
NEW = "io.github.tcballard.rss-feed"
OLD_IDS = {OLD, "io.github.tcballard.rss-reader"}


def migrate(config):
    if not isinstance(config, dict) or config.get("version") != 1:
        raise ValueError("Expected a version 1 shell configuration")
    result = copy.deepcopy(config)
    layout = result.get("bar", {}).get("layout", {})
    groups = [layout.get(section, []) for section in ("left", "center", "right")]
    groups.append(result.get("plugins", []))
    if any(not isinstance(group, list) for group in groups):
        raise ValueError("Unexpected shell entry format")
    entries = [entry for group in groups for entry in group]
    entry_id = lambda entry: entry.get("id") if isinstance(entry, dict) else entry
    source_ids = {entry_id(entry) for entry in entries if entry_id(entry) in OLD_IDS}
    if not source_ids:
        return result, 0
    if len(source_ids) > 1:
        raise ValueError("Multiple old readers have settings; review them before migrating")
    source_id = next(iter(source_ids))
    if any(entry_id(entry) == NEW for entry in entries):
        raise ValueError("Both readers have settings; refusing to overwrite or merge them automatically")
    count = 0
    for group in groups:
        for index, entry in enumerate(group):
            if entry_id(entry) == source_id:
                if isinstance(entry, dict):
                    entry["id"] = NEW
                else:
                    group[index] = NEW
                count += 1
    disabled = result.setdefault("disabledPlugins", [])
    if not isinstance(disabled, list):
        raise ValueError("Unexpected disabledPlugins format")
    # Preserve a previously disabled reader's state and disable its built-in
    # counterpart so only one service can write the shared read/cache files.
    if source_id in disabled and NEW not in disabled:
        disabled.append(NEW)
    if OLD not in disabled:
        disabled.append(OLD)
    if source_id not in disabled:
        disabled.append(source_id)
    return result, count


def migrate_file(path, apply=False):
    path = path.expanduser()
    if path.is_symlink():
        raise ValueError("Resolve your shell.json symlink explicitly before migrating")
    original = path.read_bytes()
    config, count = migrate(json.loads(original))
    if not count or not apply:
        return count, None
    # An exclusive backup preserves the exact original, including formatting.
    fd, backup_name = tempfile.mkstemp(prefix=path.name + ".before-rss-plugin-", dir=path.parent)
    with os.fdopen(fd, "wb") as backup:
        backup.write(original)
    fd, temporary = tempfile.mkstemp(prefix=".rss-migration-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as output:
            output.write(json.dumps(config, ensure_ascii=False, indent=2) + "\n")
        if path.is_symlink() or path.read_bytes() != original:
            raise ValueError("shell.json changed during migration; no settings were replaced")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return count, Path(backup_name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path.home() / ".config/omarchy/shell.json")
    parser.add_argument("--apply", action="store_true", help="write the migration, with a backup; default is preview")
    args = parser.parse_args()
    try:
        count, backup = migrate_file(args.config, args.apply)
    except (OSError, ValueError, AttributeError) as error:
        parser.exit(1, f"Cannot migrate: {error}\n")
    print(f"{'Migrated' if args.apply else 'Would migrate'} {count} reader entries.")
    if backup:
        print(f"Backup: {backup}")
        print("Run omarchy-restart-shell before opening the standalone reader.")


if __name__ == "__main__":
    main()
