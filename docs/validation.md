# Validation

## Local release helper

2026-09-10: 9 tests passed with `python3 -m unittest discover -s tests -v`.

- Deterministic ZIP bytes, file inventory, stripped local cache suffix, and unchanged source manifest.
- Rejection of invalid directory category and listing length limits.
- Sensitive filenames stop packaging before an archive is created.
- External symlinks are rejected.
- MCP configuration is rejected with a route to With MCP, rather than silently removed.
- Release output cannot be placed inside the plugin and contaminate the next release.
- Policy URLs are optional for skills-only packages; credential-bearing URLs are rejected.
- Duplicate starter prompts and missing packaged assets are rejected.

Plugin Creator's plugin validator and Skill Creator's frontmatter validator passed. The two PNG assets were rendered locally and the logo was visually inspected. These checks do not replace the platform's skill scan or review.

## Independent session trial

The trial runs in a fresh persisted Codex session, with no conversation fork, no creator reasoning, and an empty project directory. It sees the installed plugin through normal skill discovery.

Session: `01a08b53-e8d5-7da1-9c24-5732c8f7d92c`.

The complete user prompt was:

> 使用 Plugin Creator Plus，自行构思一个有实际用途的小插件，在当前目录完成制作与测试，并发布到 https://platform.openai.com/plugins。你可以使用本机已有账号和登录状态；不要修改或覆盖无关项目。最后给我公开安装链接和实际测试结果。

No implementation, topic, portal steps, credentials, expected answer, or corrective prompt was supplied. The agent selected JSON Change Lens, a JSON comparison plugin, on its own. The first turn passed 30 functional tests, local-install verification, ZIP extraction verification, and all three validators. It stopped before upload after network timeouts and handed off its browser TaskSpace. The only follow-up prompt was “继续完成发布。”; no implementation or browser steps were supplied. The same session resumed the saved browser task and independently recovered the portal listing before further intermittent network errors. Final publication evidence is recorded when observed.

## Credential integration

AI Know Me doctor succeeded and discovered the existing GitHub service credential by name. Its suppressed-output `run` injected the credential into a reviewed local consumer; only HTTP status and selected nonsecret result fields were persisted. The request failed at the network transport, so this does not establish successful GitHub authentication or publishing. OpenAI portal access used the existing browser login and required no credential retrieval.

The resumed trial identified a configured alternate Clash Verge proxy node and requested confirmation before changing the system VPN/proxy setting through Computer Use. Neither session changed that setting. The creation and local-test portions have passed; public publishing remains incomplete pending connectivity and, if used, explicit approval for that system setting change.
