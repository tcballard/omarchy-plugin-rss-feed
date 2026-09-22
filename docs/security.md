# Network, processes and local data

## Runtime dependencies and permissions

RSS Feed uses the hosting Omarchy Quattro shell, Qt/Quickshell imports, Python 3.12+ standard library, the system CA bundle (`/etc/ssl/certs/ca-certificates.crt`), coreutils `mkdir`, and Hyprland's Lua-capable `hyprctl`. There are no pip dependencies, downloaded executables, install hooks, background daemons, credentials or telemetry. Runtime processes run as the desktop user.

The shell launches `mkdir -p` for state initialization, `python3 fetch_news.py` for refresh, and `python3 window_mode.py` for placement. Arguments are passed as arrays rather than shell commands. The placement helper invokes `hyprctl` with two-second command timeouts, validates window addresses, and targets the hosting shell's PID/title for mapped windows. Initial placement installs a session-only rule matching the exact initial title `RSS Feed`; that rule can also match another application deliberately using that title. It persists until replaced or Hyprland reloads. No window configuration file is written.

## Feed boundary

Only enabled feed URLs are requested. Omarchy announcements remain pinned. At most ten custom feeds are accepted. Requests use HTTPS, system CA verification, no environment proxies or URL credentials, a one-MiB response ceiling, eight-second socket timeouts, and at most three redirects. Catalogue redirects stay on the publisher hostname (allowing its www variant). Custom redirects undergo the public-HTTPS policy again. Every socket validates all DNS answers as public and connects to a validated numeric address without resolving again; TLS still verifies the original hostname. Local feeds and private-network DNS answers are rejected.

The entire refresh helper has a 45-second wall deadline, including DNS and worker threads. On expiry it exits with an error; articles already streamed to the shell remain visible. The helper has no child processes. Concurrent refresh requests are coalesced by the service. A fetch failure can fall back to locally cached articles.

XML document types/entities are rejected, XML nesting is limited to 128 levels, and item counts are bounded. Article text is capped at 12,000 characters; rich markup input/output is bounded at 65,536 characters. Active elements and images are removed, with only safe HTTP(S) links retained. Cache files are read with an eight-MiB ceiling, item fields are checked, and cached markup is sanitized again. Both rich-text links and original-story actions are scheme checked before deliberate browser activation. Browsing an article then follows your browser's own security and privacy behaviour.

## Files written and removal

| Location | Purpose | Retained after removal |
| --- | --- | --- |
| Shell-managed `~/.config/omarchy/shell.json` | Feed choices, collections, placement and window preference | Host-managed settings may remain |
| `${XDG_STATE_HOME:-$HOME/.local/state}/omarchy/news/feed*.json` | Atomically replaced publisher caches | Yes |
| Same directory, `read.json` | Atomically saved read history | Yes |
| `~/.config/hypr/bindings.lua` | Guarded shortcut include, only through explicit setup | Removed by `scripts/keybindings.py --remove` |
| Adjacent timestamp/unique backups | Exact pre-edit bindings or optional migrated shell configuration | Yes |

Caches and subscription URLs are plain text. Do not use secret-bearing feed URLs. The old built-in reader shares the state directory and should remain disabled while this plugin is enabled. To erase retained reader data, close/disable both readers and remove only the `omarchy/news` directory after reviewing anything you want to keep. No automatic removal deletes it.

## Review scope

Portable validation and adversarial fixtures are evidence for the tested source, not a security audit or marketplace approval. QML still runs inside the shell with user privileges. Files controlled by the desktop user, theme files and the installed plugin checkout are part of that local trust boundary. Live disable/update/removal behaviour and exact host compatibility remain on the release checklist.
