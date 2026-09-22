# Publishing releases

Use a branch and one batched PR for each release. Update `manifest.json`, `CHANGELOG.md`, `docs/releases/vX.Y.Z.md` and the validation evidence together. Record on-device results before authorizing publication.

Merging a version change to main triggers **Publish release**. The workflow runs the full portable suite, checks that its source is still main HEAD, creates an annotated version tag, and publishes the corresponding notes. It pins screenshot and validation links to the tagged commit. It never moves an existing tag. A manual workflow run can retry an interrupted publication at the same source.

The initial v0.1.0 publication also runs when this workflow is introduced. Tom explicitly authorized that release on 22 September 2026 after confirming all on-device checks passed. The final source identity is the publication workflow's merged commit and annotated tag. GitHub provides source archives; no separately built binaries are distributed.

## Marketplace

The existing submission is [#8069](https://github.com/omacom/omarchy-plugin-marketplace/issues/8069). Quattro compatibility and the automated security baseline passed for `aa476b512763188387d638f45cac165176fe61e0`. They are exact-snapshot checks, not approval or a security audit. Newer commits require fresh review on the same issue. The earlier store-submission.md is a historical draft.

The older local release-skill preflight rejects the supported multiselect setting; both Quattro's validator and marketplace validation accept it. Keep that tooling mismatch distinct from actual plugin failures. No schema change is needed to suppress it.

Keep the original screenshot and its [provenance](preview.md). Follow the [contribution conventions](../CONTRIBUTING.md) for future PRs and README changes. Superseding upstream PR #10012 is a separate action.
