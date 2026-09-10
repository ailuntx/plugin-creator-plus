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

No implementation, topic, portal steps, credentials, expected answer, or corrective prompt was supplied. The agent selected JSON Change Lens, a JSON comparison plugin, on its own. The first turn passed 30 functional tests, local-install verification, ZIP extraction verification, and all three validators. It stopped before upload after network timeouts and handed off its browser TaskSpace.

The complete follow-up prompts were:

1. “继续完成发布。”
2. “网络问题解决了，继续吧。”

The user restored connectivity between attempts. The same persisted session independently recovered its work, selected the portal's verified publisher identity, rebuilt and revalidated the package, uploaded it, waited for the skill scan, submitted it, and published the approved version. The supervising session did not edit the trial code or operate its publishing page. This was a successful resumed trial, not an uninterrupted single-turn run.

JSON Change Lens 1.0.0 was observed as **Published** at `2026-09-10T14:42:38.334Z`, after a **Passed** skill scan and **Approved** review. [Public installation link](https://chatgpt.com/plugins/plugins_6aa2c00baab481919a952c2da8eeb2a0). The released ZIP SHA-256 is `467160f368e4cf185bbb35cfdbd143b01b8fbb2036767780e8b3cf70c9e3839b`.

The final package and locally installed copy both reproduced the six expected sample changes: two additions, one removal, two value changes, and one type change. All 30 functional tests passed. Public directory installation itself was not tested. See [the portable trial receipt](trial-result.json); detailed test logs remain in the local trial project, outside the release package.

## Plugin Creator Plus publication

Plugin Creator Plus 0.1.0 also passed the platform skill scan and review, and was published. [Public installation link](https://chatgpt.com/plugins/plugins_6aa2a71bc958819187e6ba5fa58ae905). The superseded unpublished draft was deleted after the current version was verified as Published. [Publication receipt](publishing.json).

## Credential integration

AI Know Me doctor succeeded and discovered the existing GitHub service credential by name. Its suppressed-output `run` injected the credential into a reviewed local consumer; only HTTP status and selected nonsecret result fields were persisted. The request failed at the network transport, so this does not establish successful GitHub authentication or publishing. OpenAI portal access used the existing browser login and required no credential retrieval.

The resumed trial identified a configured alternate Clash Verge proxy node and requested confirmation before changing the system VPN/proxy setting through Computer Use. Neither session changed that setting. After the user restored connectivity, the existing GitHub CLI authentication succeeded and the source repository was pushed. Both plugins were published through the existing OpenAI browser login; no publishing token was created or required. A successful credential-injection publishing path was not exercised by this trial.
