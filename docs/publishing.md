# Release preparation and Plugin Store status

## v0.1.0

The manifest already declares **0.1.0**. This PR prepares that version; it does not create a tag or publish a release. The base is `b786eb40fc137ba89983573e854dbf30371e18c5`. Runtime code is unchanged from the hardened submission at `aa476b512763188387d638f45cac165176fe61e0`; later main-branch commits change only the README.

[Release notes](releases/v0.1.0.md) include Tom's supplied screenshot, the product story, features and install/update commands. [Preview provenance](preview.md) records the original image and its limitations. A replacement screenshot is not required.

Use branches and batched PRs for changes from this point forward. [Contributing](../CONTRIBUTING.md) records the workflow and README conventions.

## Marketplace evidence

Tom submitted [#8069](https://github.com/omacom/omarchy-plugin-marketplace/issues/8069). The earlier `store-submission.md` is a historical preparation draft; the issue is the authoritative submitted body. Do not open a duplicate.

At `aa476b512763188387d638f45cac165176fe61e0`:

- [Quattro compatibility passed](https://github.com/omacom/omarchy-plugin-marketplace/issues/8069#issuecomment-5772200422), including the manifest, README, licence and root preview.
- [The automated security baseline passed](https://github.com/omacom/omarchy-plugin-marketplace/issues/8069#issuecomment-5772200710), with no findings or action requested. It is not a security audit or listing approval.

Those reports identify that exact snapshot, not newer README or release-preparation commits. After the release PR merges, provide its final full SHA on the existing submission for fresh review. The GitHub App currently cannot write to the marketplace repository; Tom submitted the issue himself.

## Before publishing

- [ ] Merge the batched release PR after its CI passes.
- [ ] Record the full merged commit and its CI run; the release tag must identify that source.
- [ ] Complete the remaining host checks in [validation](validation.md), recording plugin/Omarchy revisions. Tom's XPS opening/floating feedback and supplied screenshot are already recorded.
- [ ] Rerun the portable suite and official validation for the final source. Record the local preflight's known schema/tooling mismatch separately from the upstream result.
- [ ] Make release-note evidence links immutable at the final merged SHA; publish only claims supported by the recorded results.
- [ ] After release authorization, create the annotated `v0.1.0` tag and GitHub release using the prepared notes. Do not move an existing tag.
- [ ] If attaching separately built archives, produce their checksums and source/release manifests from that exact tag, and verify downloaded assets before publication. No release archives have been uploaded during preparation.
- [ ] Update the existing marketplace request with the final SHA; do not imply prior baseline results cover it.

No final release SHA can be fixed until merge. The preparation PR's head identifies the candidate tested by its CI.

## Local preflight limitation

The older release-skill validator promotes its unsupported `multiselect` warning to an error and reports **NOT READY**. Quattro's unmodified validator and the actual marketplace compatibility check accept the setting. The skill's named-package lookup also requires the resolved validator path in this environment. These tooling limitations are recorded, not hidden or described as passes. Actual host lifecycle checks remain a separate release requirement.

Keep upstream PR #10012 open during preparation; superseding it is a separate action.
