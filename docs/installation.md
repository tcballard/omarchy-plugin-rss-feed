# Installation and migration

The standalone repository is [tcballard/omarchy-plugin-rss-feed](https://github.com/tcballard/omarchy-plugin-rss-feed). The plugin is **RSS Feed**, ID `io.github.tcballard.rss-feed`. For a fresh install, use the commands in the [README](../README.md). The archive can also be tested locally.

## Local on-device test

Extract the source archive on the Omarchy machine, open a terminal in the extracted `omarchy-plugin-rss-feed` folder, then validate it:

```bash
omarchy plugin validate "$PWD"
```

Copy it into the standard plugin directory. This command refuses to overwrite an existing installation:

```bash
plugin_dir="$HOME/.config/omarchy/plugins/io.github.tcballard.rss-feed"
if [[ -e "$plugin_dir" ]]; then
  echo "RSS Feed already exists at $plugin_dir; stop and review that installation."
else
  mkdir -p "$(dirname "$plugin_dir")"
  cp -R "$PWD" "$plugin_dir"
fi
```

Only continue after the copy succeeds. A local archive installation is for testing; it does not have a Git remote for automatic plugin updates.

## If you already used the upstream reader or the provisional archive

For a Git install, add the repository without `--enable`, then run the migration from the installed plugin directory. Do this before enabling the new plugin. Close the reader and leave shell settings untouched while migrating. Preview the changes:

```bash
python3 agents/migrate-settings.py
```

Then apply:

```bash
python3 agents/migrate-settings.py --apply
omarchy-restart-shell
```

The script changes only reader IDs in bar and plugin entries, preserves all settings, disables the old built-in or provisional plugin ID, and writes an exact backup beside `shell.json`. It refuses to merge if both readers already have settings. With no old reader entry it changes nothing. It does not touch keybindings, caches or read history.

The state directory remains `${XDG_STATE_HOME:-$HOME/.local/state}/omarchy/news`, so unread history and feed caches continue in place. Do not run the old and new readers simultaneously: they share that state. Use a stock Quattro checkout rather than the old RSS PR branch for the independent-plugin test.

## Enable and open

For either a fresh install or a completed migration:

```bash
omarchy-shell shell rescanPlugins
omarchy plugin enable io.github.tcballard.rss-feed
omarchy-shell shell toggle io.github.tcballard.rss-feed
```

Install the global shortcut after enabling RSS Feed:

```bash
python3 ~/.config/omarchy/plugins/io.github.tcballard.rss-feed/scripts/keybindings.py
```

This checks for conflicts, backs up your bindings, and makes **Super + Alt + N** toggle RSS Feed. It also handles our original reader's shortcut. See [keybindings](keybindings.md) for alternatives and all in-reader controls.

## Removal and rollback

```bash
python3 ~/.config/omarchy/plugins/io.github.tcballard.rss-feed/scripts/keybindings.py --remove
omarchy plugin remove io.github.tcballard.rss-feed
```

The plugin has no uninstall hooks and does not delete your read history, cached articles or separately installed packages. To return to the old PR build, disable the standalone reader, review and restore the migration's `shell.json` backup, restore the old shortcut if used, and restart that shell. Restoring the complete backup also restores other shell settings to that point in time; review later changes first.

## Moving from an archive to a Git installation

Replace the local archive checkout with a Git installation through `omarchy plugin add https://github.com/tcballard/omarchy-plugin-rss-feed.git --enable`, from the published repository. Preserve the existing configuration and state. Live installation, update and removal checks are still pending.
