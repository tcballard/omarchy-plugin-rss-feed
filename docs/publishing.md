# Publishing and releases

The repository is [tcballard/omarchy-plugin-rss-feed](https://github.com/tcballard/omarchy-plugin-rss-feed). GitHub Actions runs the portable checks on each push and pull request.

The manifest identifies the v0.1.0 candidate. Before tagging a release, pass CI and complete the XPS installation, shortcut, migration and removal checks in [validation](validation.md). Portable checks do not establish live shell behaviour.

Keep upstream PR #10012 open until the independent plugin is tested on-device. Then supersede it with the repository link and migration instructions.
