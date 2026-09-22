# Marketplace comparison

Checked against the [marketplace catalogue](https://omarchyplugins.com/catalog.json) generated 2026-09-22T05:20:35.253Z. The descriptions below are listing claims, not independent feature or performance tests.

| Listing | Advertised scope |
| --- | --- |
| [RSS](https://github.com/rafaelvzago/omarchy-rss-plugin) | Recent posts from RSS 2.0 feeds, with an unread count on the Omarchy bar. |
| [RSS-Reeder](https://github.com/sanjyay/rss-reeder) | Native RSS and Atom reader for the Omarchy bar with OPML, categories, search, unread tracking, and configurable retention. |
| [News](https://github.com/alejandro-llanes/omarchy-news) | A news reader in the bar. Hacker News out of the box, any RSS/Atom feed you add, with article artwork, bookmarks, and a cache you control. |
| [RSS Headlines](https://github.com/flaviomedeiros/rssheadlines) | RSS headlines in the Menu Bar, powered by Newsboat. |
| [Feader RSS](https://github.com/KitsuneSemCalda/Feader-RSS) | Persistent RSS reader for the Omarchy shell. |
| [Microsoft Dev Blogs](https://github.com/sinannar/sinannar.omarchy.plugin.msftdevblogs) | Recent posts from the Microsoft for Developers RSS feed, with a panel to browse and open them |
| [News Reader](https://github.com/ranjithrajv/news-reader) | Fullscreen overlay RSS news reader — bring your own RSS/Atom feeds, search, filter by source, and open stories in your browser. No hard-coded feeds or articles; configure via Settings or import OPML/JSON. Summon from the bar or with omarchy-shell shell summon. |
| [News Feed](https://github.com/joisephdev/omarchy-news-feed) | Read headlines from an RSS news feed, Yahoo Finance by default, from the bar. |
| [RSS news](https://github.com/MariusGhizdavet/omarchy-rss) | An RSS reader in the Omarchy bar: the unread count, the items in a panel, mark-all-read, and feed management. Speaks 10 languages, following the system locale by default. |
| [NewsFlash](https://github.com/Shirak-Semonian/newsflash-omarchy-plugin) | Daily world news in a minimalist bar widget. One-time IP geolocation opens the edition of the country you are in (190+ countries; localized sections, English search feed elsewhere). Lead story with optional image over a compact list with LIVE markers and relative times. Click a headline to read the full article inside the panel (local extraction). Read-aloud in the edition's own language (edge-tts). Quiet polling (5-60 min) via Google News RSS with BBC/Guardian fallback. No key, no tracking. |
| [RSS-Feeder](https://github.com/keegan-sucks/rss-feeder) | Native RSS and Atom reader for the Omarchy bar with OPML, per-feed category editing, YouTube Shorts filtering, search, unread tracking, and configurable retention. |
| [Omarchy RSS Client](https://github.com/siygle/omarchy-rss-client) | Built on sanjyay/rss-reeder, adding more RSS client features and bug fixes. |
| [OmaRSS](https://github.com/ozdil/omarchy-omarss) | Ultra-fast, native, lightweight RSS & Atom feed reader and notification hub for Omarchy written in Rust. |
| [Omarchy Briefing](https://github.com/shaggyrs6-netizen/omarchy-briefing) | Completed package changes and a quiet, source-labelled Omarchy news reader |

RSS-Reeder and its derivatives overlap substantially with our feed management and unread tracking; News and News Reader also cover substantial reading workflows. The listed ecosystem already has alternatives. This extraction therefore preserves a reader Tom already uses and likes, while removing dependence on upstream shell merges. It makes no exclusivity or superiority claim.

Our retained scope is the two-pane desktop reader, source rail, curated and custom feeds, collections, incremental refresh, read tracking and offline caches. OPML import/export, search, article artwork, bookmarks, localization and speech are not claimed as features of this extraction. If those become priorities, compare or contribute to the existing readers before expanding scope.

A subset of the fetched catalogue is preserved in `marketplace-snapshot.json`, including repository and observed revision references.
