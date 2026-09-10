---
name: plugin-creator-plus
description: Create, test, package, and publish ChatGPT and Codex plugins from a project or an idea. Coordinates Plugin Creator, OpenAI Developers submission preparation, AI Know Me credentials when needed, and ego-browser for the OpenAI publishing portal. Use for plugin creation, updates, or public directory releases.
---

# Plugin Creator Plus

Take the user's plugin from its current state to the requested destination. Respond in their language. This is an independent workflow plugin, not an OpenAI product. It needs a local terminal; browser publication also needs ego-browser. It uses separately installed skills without copying them or bundling credentials.

## Route the work

Resolve companion skills from the current session's skill catalog and read the actual SKILL.md when needed; never pin a user's home directory or a cache version. If an installed companion is missing from the catalog, inspect the configured skill/plugin directories for that named skill. Do not silently claim that dependencies are bundled or installed.

| Need | Companion |
| --- | --- |
| Scaffold, manifest, personal marketplace, local install/update | Built-in `plugin-creator` |
| Author or improve the skill itself | Built-in `skill-creator`, when available |
| Current OpenAI requirements | `openai-docs` and official developer documentation |
| MCP app implementation and submission JSON | OpenAI Developers: `build-chatgpt-app`, `chatgpt-app-submission` |
| Stored service or website credentials | `ai-know-me` |
| Signed-in publishing portal | `ego-browser` |

If a required capability is unavailable, report its name and continue independent preparation. Installing this plugin alone does not install its companions. For a skills-only plugin, do not introduce MCP or API-key setup just to use the OpenAI Developers bundle.

## Create and prove the plugin

- Use the current project or the location requested by the user. Choose a focused, useful idea when they delegate the concept. Scaffold with Plugin Creator; maintain its normal local marketplace and reinstall flow.
- Build the actual capability and exercise representative inputs. Check meaningful behavior and failure handling for bundled scripts. A manifest check alone is not a functional test. When the user requests an independent trial, use a fresh session with only the task and plugin reference; keep the creator's intended solution and work history out of that session.
- Prepare accurate display text, prompts, assets, and publisher metadata. Public publisher identity comes from the verified account or user-provided facts, not a previous project's author. Do not present this plugin or a generated plugin as official OpenAI software.
- For MCP plugins, use the OpenAI Developers submission skill on the real implementation and generate its submission JSON. For skills-only plugins, use observed input/output cases; do not invent MCP action names or force an MCP form onto a skills-only submission.
- Run Plugin Creator's plugin validator and Skill Creator's skill validator. Before directory release, also run the bundled preflight below. Local ingestion and public listing have different limits.

## Package a skills-only release

Resolve the helper relative to this SKILL.md:

```bash
python3 scripts/release.py check /absolute/plugin-root
python3 scripts/release.py package /absolute/plugin-root --out /absolute/project/dist
```

The helper reads the `.codex-plugin/plugin.json` layout created by Plugin Creator. It checks common directory blockers and builds a ZIP from the plugin root only. It strips only the local `+codex.…` version suffix in the archive, leaves source untouched, rejects symlinks and sensitive filenames, and reports the exact files and SHA-256. Inspect this inventory before uploading; automated checks cannot prove that every file is appropriate to publish. Keep credentials, execution logs, project-only tests, and publishing receipts outside the plugin directory.

This helper intentionally packages skills-only releases. If the plugin has MCP/apps configuration, follow **With MCP** in the portal; do not delete working capabilities to make a ZIP pass. Portal rules are authoritative and may change: fix demonstrated mismatches, not unrelated source.

## Publish when requested

Creation/local installation and public publication are different destinations. A user request to publish authorizes completing that release in the specified account; retain that authorization through scan waits and routine fixes. Do not ask again merely because the next action is Submit or Publish. If publication has not been requested, deliver the prepared result without making it public.

Read [the portal workflow](references/publishing.md) for public releases. Use the existing signed-in browser session first. AI Know Me supplies an existing credential only when the task actually needs one; storing a secret is not permission to use it elsewhere. Do not create an OpenAI API key for portal publishing or treat the Skills API as a directory publishing endpoint.

Success requires the portal to show the requested version as **Published** and provide its directory link. Record nonsecret evidence in a project-level `docs/publishing.json`: package SHA-256, version, plugin/submission IDs and URLs, last observed status, observation time, and directory URL when present. Draft, scan passed, submitted, approved, and published are distinct states. On interruption, reopen the recorded draft and inspect it before retrying; do not create duplicate listings.

Report the result, real tests, local installation link, and public directory link. State any remaining scan or user action accurately. Never describe an unfinished release or a trial that received repair instructions as an independent successful publication.
