# Contributing

## Changes

Use a branch and a pull request for changes, including documentation and release preparation. Batch related fixes or polish into one reviewable PR; avoid a separate push for each small adjustment. Explain the user-facing result and the checks performed. Keep unrelated work separate.

Run `bash test/all` for code changes and release candidates. For documentation-only changes, check links, assets and factual claims. CI must pass before merge. Publishing a release or changing marketplace verification is a separate step from merging a PR.

## README style

The README is the front door to the product:

- Centre the product title and the single **Built for Omarchy: Plugin** badge. No extra badge row.
- Explain what the plugin does in plain language, with a real screenshot close to the opening.
- Tell the short product story, then give copyable installation and everyday-use instructions.
- Keep update and removal instructions easy to find.
- Put detailed implementation, validation and release checklists in linked documentation.
- Recognise actual on-device testing and screenshots without inventing wider compatibility or certification.

Keep the opening concise and free of engineering clutter. Use this style for future RSS Feed README edits.

## Releases

Prepare each release in one PR with its changelog, screenshot-backed release notes and current evidence. Follow [the release checklist](docs/publishing.md); record the final merged commit before tagging. Never move a published tag.
