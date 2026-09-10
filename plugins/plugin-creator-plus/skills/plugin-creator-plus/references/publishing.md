# Public directory release

Use the current official [submission guide](https://developers.openai.com/plugins/deploy/submission), [error reference](https://developers.openai.com/plugins/deploy/submission-errors), and [package guide](https://developers.openai.com/plugins/build/plugins). This workflow was checked on 2026-09-10. Recheck relevant rules on a new release; the live form varies by plugin type.

## Prepare before opening the form

Keep public version, package, metadata, and test evidence in the project. Public policy/support pages should describe the actual plugin and its publisher. For skills-only ZIPs these URLs are optional under the current error reference; remote MCP submissions require them. Do not invent a website, legal identity, test result, or privacy guarantee. A GitHub repository or policy page may be published when that is part of the user's authorized public release; never upload the whole working directory by default.

Use a new base version for an update. Reuse the existing listing rather than creating another plugin with the same purpose. Keep local cachebuster suffixes out of public releases. The package helper reports an immutable upload digest so the receipt can identify what was actually sent.

## Account and credentials

Read ego-browser's current skill and use its supported API. Open https://platform.openai.com/plugins in the goal's TaskSpace and inspect it. Existing login normally needs no credential lookup. Check the active organization and verified publishing identity. Use the organization selected by the user; if multiple plausible accounts exist and context cannot resolve them, prepare everything else while asking which account to use.

When authentication is needed, read AI Know Me, run its `doctor`, then discover relevant entry **names** with `search`/`list`. Use its `run --env … -- <trusted consumer>` to inject into a reviewed process that actually consumes those variables. For ego-browser login, the consumer can read environment variables in Node and supply them to observed login fields; never put credential values in command literals or return them through browser snapshots/logs. AI Know Me suppresses child output, so write only a deliberately selected, nonsecret outcome separately if needed. Read the target script before injecting. Never read the YAML into context, try unrelated password variants, extract browser session tokens, or package credentials.

Authentication and verified publisher access are different requirements. MFA, CAPTCHA, identity verification, protected permission prompts, or an explicit browser handoff may need the user. Use ego-browser's handoff mechanism and explain the exact action; do not work around a tool denial. No public directory publishing token/API is documented in the sources above. If OpenAI adds one, verify its official documentation and prefer the supported interface.

## Submit and wait

1. Inspect existing listings/recorded receipt. For a new listing choose Create plugin, then **Skills only** or **With MCP** according to the implementation.
2. Upload the final ZIP or configure the production MCP server. Complete only tabs that actually exist. With MCP may include domain verification, tool scan, and reviewer access. Skills-only can expose just Info, Prompts, Skills, and Submit.
3. Verify the imported fields and identity. Fill missing fields from prepared metadata. Review actual policy attestations against the implementation; do not attest to unperformed tests or unavailable rights. Apply straightforward validation fixes and recheck the resulting package.
4. For a corrected upload, use the portal's re-upload button and file chooser. Reassigning an unchanged path to the same file input may not trigger another upload. Inspect the displayed version and validation result afterward.
5. Wait for each skill scan to pass. The official error reference allows scans to take up to two hours. Use bounded condition waits and resume the same draft; keep the user informed without frequent full-page dumps or duplicate submissions. A long scan does not imply failure. Do other useful work while waiting when available.
6. Submit when the form is ready, observe the review state, and continue to Publish once approved within the existing publication request. An approval alone is not a published listing. If review is still pending, record that status and explain that publication remains unfinished.
7. Verify **Published** for the intended version and save its directory link and evidence. Finish ego-browser's TaskSpace once, following its normal completion rules.

Use snapshots and semantic selectors grounded in observed UI. Reuse stable selectors when batching fields; snapshot refs expire after mutations. Prefer one concise final observation over repeated checks on multiple pages. Do not scrape private publish endpoints or persist cookies as a replacement for browser authentication.
