# Extraction evidence

Prepared 22 September 2026 from `tcballard/omarchy`, branch `feat/omarchy-news-panel`, commit `21e7913a10d6334428eaf4a066365d77c6858568` (upstream PR #10012).

The current upstream contract was inspected at `omacom/omarchy` branch `quattro`, commit `947e2fc` (the full revision is recorded in `source.json`). The ordinary `dev` branch does not contain this shell and is not the plugin's validation target.

## Scope

The reader's QML, Python fetcher, feed catalogue, JavaScript models and seven original test suites and their shared helper were extracted. Production changes are the third-party ID, a helper path resolved relative to the plugin, a plugin-owned category palette, and an explicitly hidden initial window. The layout, feed and collection models, fetch behaviour and state paths are preserved. The follow-up names the plugin RSS Feed (`io.github.tcballard.rss-feed`) and adds explicit, conflict-checked Super + Alt + N setup, a shipped Lua binding, and guarded removal. Installation and migration are explicit; there are no setup hooks or separate shell processes.

`agents/validate-plugin.sh` is the unmodified upstream validator from the recorded Quattro revision, covered by the retained MIT licence. It is included to make CI reproducible.

## Portable checks

- `bash test/all`: upstream validator; inherited parser, collection, catalogue, hardening, stream, recovery and performance tests; extraction tests; five migration tests and nine shortcut-setup tests.
- `python3 agents/generate-rss-catalog.py --check`: generated metadata current (also part of the suite).
- Omarchy plugin skill validator: valid. Its older settings whitelist warns about `multiselect`; current upstream uses that type and its validator accepts this manifest.
- Advisory security scan: no findings, with manual-review capability notices for QML processes and collected input. This is not marketplace certification.

The complete portable output is in `test-results.txt`. Source test assertions for a built-in shell colour property and a core-owned global binding were removed because those responsibilities now belong to the plugin palette and the user's shortcut. Other inherited assertions were retained with paths and the plugin ID updated.

The window-mode follow-up includes thirteen Python tests for exact PID/title/address targeting, explicit tile/float commands, monitor sizing, bounded mapping retries and dispatch failure; a JavaScript lifecycle test exercises hidden/open/close scheduling and settings preservation. The helper is a short-lived child of the hosting Quickshell process and only dispatches against its own matching RSS Feed window address. It never falls back to the active window. Closing cancels queued and running placement work; changes during a running operation queue the latest preference.

Dispatcher syntax follows the [Hyprland Lua examples](https://wiki.hypr.land/configuring/code-snippets/) and the targeted window dispatch pattern in Omarchy's `omarchy-hyprland-window-pop` at the recorded host revision. The opening path now installs a session-only rule matching the exact initial title `RSS Feed` before the window becomes visible, following `omarchy-launch-about`’s pre-map sizing pattern. It reuses the rule on repeated opens and replaces it when mode or fitted size changes. No configuration files are changed. Already-visible mode changes still use exact PID/title/address targeting. Tests verify that the window stays hidden until preparation completes and that late completion cannot reopen a closed reader.

## Maintainer feedback, 22 September 2026

Tom confirmed that explicit plugin summon opens the intended RSS Feed UI on his XPS. After commit `205580817744fc1e5a248795acf9b5ca46ae39e9`, he confirmed the opening behaviour was “much better”. This confirms that specific interaction, not every lifecycle state below. His exact installed Omarchy revision and display scale have not yet been recorded. The subsequent hardening candidate requires an update and recheck.

## Hardening evidence

`python3 test/fetch_security_test.py` covers DNS rebinding, mixed public/private answers, TLS hostname verification, socket cleanup/fallback, malformed URLs, XML entity/depth/byte limits, active markup and output size, malformed and oversized caches, truncated HTTP responses, and a real subprocess deadline with a blocked worker thread. All fixtures are local; they do not depend on publisher uptime.

The complete suite is also available through `tests/run`. The skill release preflight expects that path. Its bundled validator lookup assumes named skill directories; in this environment the skills use hashed package directories. Run the validator directly, or inject its resolved path into `release_preflight.validator_path` without changing the checks. The older validator’s multiselect warning is documented above. The release wrapper promotes this warning to an error, so its overall result is NOT READY; the unmodified Quattro validator passes. Do not label that wrapper result a pass or change the supported setting type merely to suppress its outdated whitelist.

## On-device checks still required

The original PR body reports live desktop testing of the original reader. That is not evidence that the extracted plugin has passed on-device testing. No Qt/Quickshell compositor is available in the development environment. Beyond the maintainer feedback above, QML compilation and the following lifecycle checks remain unrun:

1. Install on stock Quattro; enable once; verify one RSS bar icon and no unsolicited reader window.
2. Open, close and reopen by bar and IPC; check mouse, keyboard, independent scrolling, article links and source colours.
3. Add, edit, reorder and remove feeds; create and edit collections; restart the shell and confirm persistence.
4. Migrate a copied real configuration; verify placement, subscriptions, collections and unread state; confirm the old reader is disabled.
5. Refresh online and offline; confirm cached articles, partial failures, unread acknowledgement and no duplicated fetch processes.
6. Switch themes, including themes with missing category colours; verify fresh palette values and readable controls.
7. Install the shortcut, confirm it appears under Super + K and toggles RSS Feed, verify conflicts are refused, rerun setup, remove it and verify other bindings remain unchanged.
8. Disable during refresh, re-enable, update from Git once published, then remove; confirm processes stop and retained user data remains intact.
9. Select **F → Window mode → Centred floating** while open, switch back to Tiled, close/reopen, and restart the shell. Confirm the preference persists, only RSS Feed moves, and centring/sizing works on each monitor, including scaling and rotation. Change mode rapidly, close during placement and verify no other window moves. Open the mode dropdown and press Escape: only the dropdown should close first. Repeatedly open in floating mode and confirm there is no initial tiled frame or desktop reflow; repeat after reloading Hyprland.

The upstream PR is still open. Closing or superseding it is a separate action after the independent plugin is accepted; migration is optional for users who want their older settings.
