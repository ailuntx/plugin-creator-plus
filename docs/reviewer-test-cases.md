# Reviewer scenarios

These scenarios describe expected behavior for the workflow. They are not claims that every publishing/authentication branch has been executed.

## Positive scenarios

1. Ask to turn a local project into a plugin without publishing. Expected: create/test/install locally and stop at the requested destination.
2. Ask to publish a completed skills-only plugin. Expected: check the distributable folder, create its ZIP, use the signed-in portal, and distinguish scan, review, and published states.
3. Provide a manifest with the directory category `Developer`. Expected: preflight rejects it before upload; the agent uses the documented `Developer Tools` category where appropriate.
4. Ask to update an existing public listing. Expected: prepare the changed version and reuse the existing listing, keeping local cache metadata out of the release.
5. Ask to prepare an MCP-backed plugin for publication. Expected: use the OpenAI Developers submission workflow and the With MCP path, preserving real server capabilities.

## Negative scenarios

1. Ask to summarize meeting notes with no plugin-development request. Expected: this workflow is not selected.
2. Ask only to scaffold a plugin. Expected: no public upload, GitHub publication, credential retrieval, or portal submission is inferred.
3. Include an `.env` file or an external symlink in a plugin directory. Expected: packaging fails and no archive is published until the selected release content is corrected.

Publishing requires an authorized account with a verified identity and platform access. Companion skills are separate installations; API keys do not substitute for portal login.
