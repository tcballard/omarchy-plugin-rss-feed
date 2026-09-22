# Changelog

## 0.1.0 — release candidate, not yet tagged

- Extract the existing RSS reader into an independent Omarchy Quattro plugin, named RSS Feed.
- Preserve feeds, named collections, unread history, cached reading, theme colours and keyboard navigation.
- Ship an optional conflict-checked Super + Alt + N shortcut with guarded removal.
- Remember tiled or centred floating mode and prepare the opening rule before showing the window.
- Harden public HTTPS connections against DNS rebinding, bound refresh duration and XML/cache input, sanitize cached markup, and recover from malformed URLs and incomplete HTTP responses.

Opening and floating were confirmed on the maintainer’s XPS before the hardening pass. See `docs/validation.md` for portable evidence and the remaining on-device release checks. No tagged release has been published.
