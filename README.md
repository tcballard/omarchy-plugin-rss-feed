# RSS Feed

Your feeds, collections and articles in a proper desktop reader. Open it from the bar, pick a story, and read it alongside your headlines without switching to a browser.

This is the reader originally built in [Omarchy PR #10012](https://github.com/omacom/omarchy/pull/10012), extracted into an optional plugin with its own release cycle.

- The existing two-pane reader, source rail and keyboard navigation.
- Omarchy news, ten curated technology feeds, and your own RSS or Atom subscriptions.
- Feed management and named collections inside the reader.
- Unread tracking, cached articles for offline reading, and background refresh.
- Theme colours, clickable article links, and an action to open the original story.
- Choose a tiled reader or a centred floating window; RSS Feed remembers your choice.

## Install

Requires Omarchy Quattro with its plugin-capable shell and Python 3. This is the **v0.1.0 candidate**; the extracted plugin still needs its on-device smoke test.

```bash
omarchy plugin add https://github.com/tcballard/omarchy-plugin-rss-feed.git --enable
python3 ~/.config/omarchy/plugins/io.github.tcballard.rss-feed/scripts/keybindings.py
```

Already using the original reader? Follow [migration](docs/installation.md) before enabling this plugin to keep your subscriptions, collections, placement, unread history and caches.

Press **Super + Alt + N** or click the RSS icon to open RSS Feed. Right-click the icon to refresh. Inside, **F** manages feeds, **R** refreshes, **O** opens the original article, and **Esc** returns or closes. [All keyboard and mouse controls →](docs/keybindings.md)

For a pop-out reader, press **F** and set **Window mode → Centred floating**. It applies immediately and stays selected after a restart. Choose **Tiled** to put the reader back into your layout.

## Development

```bash
bash test/all
```

See [validation](docs/validation.md), [the feed catalogue](docs/feed-catalog.md) and [marketplace alternatives](docs/marketplace.md). This repository contains the reader, its helper and its tests; installation does not patch the shell or run setup hooks.

MIT licensed. Extracted from work in the Omarchy repository; its original licence is retained. Maintained by Tom Ballard.
