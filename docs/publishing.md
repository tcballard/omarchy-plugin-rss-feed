# Publishing releases

Use a branch and one batched PR for each release. Update `manifest.json`, `CHANGELOG.md`, `docs/releases/vX.Y.Z.md` and the validation evidence together. Record on-device results before authorizing publication.

## Release authority

GitHub Actions only runs the portable checks. Its token has `contents: read`, checkout does not persist credentials, and no workflow creates tags or releases. Merging a version change does not publish it.

The former **Publish release** workflow was removed in response to [marketplace review #8069](https://github.com/omacom/omarchy-plugin-marketplace/issues/8069#issuecomment-5772924216). It gave a mutable hosted runner write access to the repository. An OS label such as `ubuntu-24.04` still receives image updates, and a digest-pinned container would still trust its host. Neither is claimed here as an immutable release environment. See GitHub's [runner image documentation](https://github.com/actions/runner-images#image-releases).

RSS Feed is distributed as Git source, with GitHub-provided source archives and no separately built binaries. Publication is a separately authorized maintainer operation through GitHub's UI or API, bound to an explicit source commit. It does not consume runner-generated release notes, tags or artifacts. CI remains useful test evidence, not an immutable toolchain attestation.

## Publish a reviewed source snapshot

1. Merge the release PR after its checks pass. Record the final main HEAD as a full 40-character commit SHA and confirm **Check reader** passes for that exact commit. Retain the on-device evidence in `docs/validation.md`.
2. Read `manifest.json` and `docs/releases/vX.Y.Z.md` directly at that SHA. Confirm the intended version and obtain authorization for publication. Do not execute repository scripts with release credentials.
3. Through GitHub's Git API, create an annotated `vX.Y.Z` tag whose object is that exact commit SHA, then create its `refs/tags/vX.Y.Z` reference. If the tag already exists, resolve it to its commit and require an exact match; never move or replace it. A mismatched tag requires a new version prepared in another PR.
4. Prepare the release text from the reviewed notes. Pin repository screenshot and validation links to the same SHA and append `Source: <full SHA>`. Recheck that main HEAD still matches the reviewed commit before publication; if it changed, stop and review the new snapshot.
5. Publish through GitHub's UI or Releases API using the existing tag. Do not let release creation implicitly choose a branch tip or create a tag. Leave an existing release unchanged; after an interrupted publication, retry only against the same verified tag and source.
6. Verify the published release URL, version tag and peeled commit SHA. Record the result in the release handoff rather than creating a follow-up commit that immediately changes the marketplace snapshot.

The existing v0.1.0 release was authorized by Tom on 22 September 2026 after all on-device checks passed. Its tag remains at `72b3f47dbf62c2d622132ce75835544638c38b9e`; removing the publishing workflow does not retag or republish that release.

## Marketplace

RSS Feed is [listed in the Omarchy Plugin Store](https://plugins.omarchy.org/plugin.html?id=io.github.tcballard.rss-feed). [Submission #8069](https://github.com/omacom/omarchy-plugin-marketplace/issues/8069) was closed as completed on 22 September 2026 after publication and verification of `48d355253e5e3ce1172366125b3a43dc359ad7d2`. Compatibility and baseline checks cover that exact snapshot, not every newer commit or the entire release history. The earlier `store-submission.md` is a historical draft.

For later changes, follow the marketplace's current update procedure and record the full candidate SHA. Keep local tests, marketplace validation, security disposition and publication evidence bound to their actual commits. This documentation refresh does not extend the earlier verification to a new source snapshot. Never move a published tag or manually remove review labels to imply approval.

The older local release-skill preflight has two documented tooling gaps: supported `multiselect` settings and validator lookup under renamed skill directories. [Build Omarchy Plugins PR #30](https://github.com/tcballard/build-omarchy-plugins/pull/30) prepares fixes for both. Until that update is merged and installed, keep the wrapper failure separate from the passing Quattro and marketplace checks. Do not change the plugin schema or weaken validation to suppress the mismatch.

Keep the original screenshot and its [provenance](preview.md). Follow the [contribution conventions](../CONTRIBUTING.md) for future PRs and README changes. [Upstream PR #10012](https://github.com/omacom/omarchy/pull/10012) is closed as superseded by this plugin.
