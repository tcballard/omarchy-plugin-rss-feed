# RSS Feed

Your feeds, collections and articles in a proper desktop reader. Open it from the bar, pick a story, and read it alongside your headlines without switching to a browser.

This is the reader originally built in [Omarchy PR #10012](https://github.com/omacom/omarchy/pull/10012), extracted into an optional plugin with its own release cycle.

- The existing two-pane reader, source rail and keyboard navigation.
- Omarchy news, ten curated technology feeds, and your own RSS or Atom subscriptions.
- Feed management and named collections inside the reader.
- Unread tracking, cached articles for offline reading, and background refresh.
- Theme colours, clickable article links, and an action to open the original story.
- Choose a tiled reader or a centred floating window; RSS Feed remembers your choice.

![RSS Feed floating reader with headline list and article pane](preview.png)

## Install

Requires Omarchy Quattro with its plugin-capable Quickshell shell, Lua-enabled Hyprland (`hyprctl`), Python 3.12 or newer, system CA certificates, and coreutils (`mkdir`). No Python packages are needed. This is the **v0.1.0 candidate**. Opening and floating behaviour have been confirmed on the maintainer’s XPS; the full release checklist is still in progress. See [compatibility and validation](docs/validation.md).

```bash
omarchy plugin add https://github.com/tcballard/omarchy-plugin-rss-feed.git --enable
python3 ~/.config/omarchy/plugins/io.github.tcballard.rss-feed/scripts/keybindings.py
```

Already using the original reader? Follow [migration](docs/installation.md) before enabling this plugin to keep your subscriptions, collections, placement, unread history and caches.

Press **Super + Alt + N** or click the RSS icon to open RSS Feed. Right-click the icon to refresh. Inside, **F** manages feeds, **R** refreshes, **O** opens the original article, and **Esc** returns or closes. [All keyboard and mouse controls →](docs/keybindings.md)

For a pop-out reader, press **F** and set **Window mode → Centred floating**. It applies immediately and stays selected after a restart. Choose **Tiled** to put the reader back into your layout.

## Update and remove

```bash
omarchy plugin update io.github.tcballard.rss-feed
omarchy-restart-shell
```

To remove the shortcut and plugin:

```bash
python3 ~/.config/omarchy/plugins/io.github.tcballard.rss-feed/scripts/keybindings.py --remove
omarchy plugin remove io.github.tcballard.rss-feed
```

Subscriptions and window preferences live in the shell configuration; cached articles and read history live in `${XDG_STATE_HOME:-$HOME/.local/state}/omarchy/news`. Removal retains this data and any setup backups. The optional shortcut installer changes `~/.config/hypr/bindings.lua` only when you explicitly run it, with conflict checks and a backup. [Installation, migration and rollback →](docs/installation.md)

## Privacy and support

RSS Feed connects directly to enabled publishers over HTTPS. Custom feeds must resolve to public addresses; local-network feeds and authenticated URLs are unsupported. It does not use analytics or fetch article images. Article links open in your default browser only when activated. Feed URLs and cached content are stored locally in plain text: avoid secret-bearing subscription URLs. [Network, processes and data details →](docs/security.md)

Report bugs through [GitHub Issues](https://github.com/tcballard/omarchy-plugin-rss-feed/issues). See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## Development

```bash
bash test/all
```

See [validation](docs/validation.md), [the feed catalogue](docs/feed-catalog.md) and [marketplace alternatives](docs/marketplace.md). This repository contains the reader, its helper and its tests; installation does not patch the shell or run setup hooks.

MIT licensed. Extracted from work in the Omarchy repository; its original licence is retained. Maintained by Tom Ballard.
