# Open Questions

## virality-and-citations - 2026-03-30

- [ ] PyPI package name: is `paper-manager` available on PyPI, or do we need an alternative like `arxiv-paper-manager`? -- Determines the install command and branding
- [ ] Should the citation-based descendants use Claude to synthesize a narrative (richer but slower), or just format citation data directly into markdown (faster, no extra Claude call)? -- Affects both UX quality and processing time
- [ ] For the Semantic Scholar API, should we require an optional API key for higher rate limits (1 req/sec unauthenticated vs 10 req/sec with key)? -- Matters for batch processing of many papers
- [ ] README demo GIF: should this show the full analysis (which takes 60-90s) or a pre-recorded/sped-up version? -- Affects authenticity vs. attention span
- [ ] English language support: should this be a separate template file (`default_en.md`) or a parameterized single template? -- Affects maintenance burden
- [ ] License: the project currently has no LICENSE file. MIT is recommended for virality. Confirm before publishing to PyPI. -- Required for PyPI and signals openness
- [ ] Should `paper-manager cite --update` re-run the full Claude analysis or only patch the Descendants subsection? -- Full re-analysis is expensive; patching is faster but technically harder
- [ ] The `rich` library adds a dependency. Is the current `typer[all]` dependency sufficient (it bundles rich), or do we need to add it explicitly? -- `typer[all]` already includes `rich`, so this may be a non-issue
