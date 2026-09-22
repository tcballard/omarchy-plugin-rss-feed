# Plugin Store submission preparation

Repository: [tcballard/omarchy-plugin-rss-feed](https://github.com/tcballard/omarchy-plugin-rss-feed). Version: **0.1.0 candidate**, untagged. GitHub Actions runs the portable checks on each push and pull request. The full candidate identity is the commit containing this draft (`git rev-parse HEAD`), reported with the preparation handoff and its CI run. Do not treat later HEAD changes as covered by an older report.

## Prepared listing

- Title: **[Plugin]: RSS Feed**
- Category: **Productivity**
- Tags: **Bar, Quickshell, Media**
- Reviewable six-section body: [store-submission.md](store-submission.md).

The form was read from `omacom/omarchy-plugin-marketplace` on 22 September 2026; the observed main SHA was `83e08dff5fc9284a2dd11effcedaabd59ed104f7`, and the form blob was `572e3b21e2d92bc97424c54a25789be94e0bfee3`. Compared with the skill's older form, VPN is now an additional tag; this draft uses labels valid in both. Searches by repository name and plugin ID found no matching submission; recheck immediately before opening one.

The checklist is deliberately unchecked pending the owner's confirmation, particularly code/asset rights. Preparation has not created a marketplace issue, tag or GitHub release. The publishing workflow requires approval of the completed body and all five statements before sending it. Marketplace listing also requires maintainer review; successful tests do not confer approval.

## Candidate status and remaining work

- Portable suite and the unmodified Quattro manifest validator pass; results are in `test-results.txt` and CI for the candidate commit.
- The advisory scan has no findings, with process and collected-input capabilities reviewed in [security notes](security.md). It is not a security audit.
- The skill release preflight remains **NOT READY**: its older whitelist rejects Quattro's valid `multiselect` schema when warnings are promoted to errors. The named-skill path lookup also needs the resolved validator location in this environment. This tooling mismatch is recorded rather than bypassed or presented as a pass.
- Tom confirmed the plugin opens and the pre-map floating fix improves its behaviour on his XPS. Update and test this hardened build; record its full plugin SHA and installed Omarchy SHA. Follow the remaining lifecycle checks in [validation](validation.md), especially offline refresh, feed/collection persistence, disable during refresh, Git update, shortcut removal and plugin removal.
- Root `preview.png` contains Tom’s supplied screenshot of the correct RSS Feed plugin. It is unchanged; dimensions, checksum and capture limitations are recorded in [preview provenance](preview.md). No replacement screenshot is required for this preparation.
- After the remaining host evidence is supplied, refresh the source identity, CI and exact submission body. Show that final body to the owner for approval before submission. Tagging/releasing is a separate authorized action and requires the release evidence.

Keep upstream PR #10012 open during this preparation; superseding that PR is a separate action.
