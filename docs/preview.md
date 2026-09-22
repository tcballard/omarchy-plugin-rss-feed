# Marketplace preview provenance

Root `preview.png` is the original screenshot supplied by Tom in this conversation, copied byte-for-byte from `upload/01-image.png`. It shows the **RSS FEED** header, centred floating window, headline list and article pane. Dimensions: 1352 × 1032 pixels. SHA-256: `0abb384f5306b673889c21f669363b80f1b3836751b418e85325d987fcb586f1`.

The screenshot was inspected on 22 September 2026. It depicts the existing plugin UI before the feed hardening changes, which do not alter that layout. The exact capture-time plugin commit, Omarchy revision, theme and display scale were not supplied, so the image is product evidence rather than proof of the complete release test matrix. No generated content, retouching or reconstructed UI has been added. Faint text from the window behind the translucent reader remains as supplied.

For a future refresh, open the installed plugin using `omarchy-shell shell summon io.github.tcballard.rss-feed`, choose Centred floating, select a public article, and capture the actual window with Omarchy's screenshot action. Record the plugin SHA (`git -C ~/.config/omarchy/plugins/io.github.tcballard.rss-feed rev-parse HEAD`) and Omarchy SHA (`git -C "$OMARCHY_PATH" rev-parse HEAD`) alongside the theme and scale. Inspect the image before replacing the root preview.
