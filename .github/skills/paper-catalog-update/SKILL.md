---
name: paper-catalog-update
description: 'Monthly prompt engineering paper catalog update with scoring rules and safe add/retire operations. Triggers: update paper catalog, refresh paper DB, paper database update.'
---

# paper-catalog-update

## Usage

Invocation name: `paper-catalog-update`

Use this skill when updating the prompt engineering paper catalog in:
- documents/reference/papers/prompt-engineering-papers.md
- documents/reference/papers/categories/*.md

Typical triggers:
- `(today - Last_Updated) > 30 days`
- User explicitly asks for paper DB/catalog update
- Prompt-plan-master is invoked and database freshness must be checked

## Responsibility

This skill owns catalog update procedure only:
- Scope: stale-check, category selection, search, scoring, add/retire, metadata update
- Out of scope: prompt generation, prompt optimization, model choice recommendations

## Inputs

- `today` date
- `Last Updated` value from master index
- Optional: target categories requested by user

## Required Tools

| Tool | Purpose | Fallback |
|------|---------|----------|
| `context7/*` | Library/framework doc lookup | Skip if unavailable; note in report |
| Web search (if available) | arXiv, Semantic Scholar, ACL Anthology queries | Manual user search; tag `[TOOL LIMITED]` |
| `read` / `search` | Read existing catalog files | Required; no fallback |
| `memory/*` | Store update decisions | Required; no fallback |
| `edit` / `replace_string_in_file` | Write updated catalog files | Required; no fallback |

If web search tools are unavailable, this skill MUST:

1. Report `[TOOL LIMITED]` in the output summary.
2. Limit updates to papers the user provides directly.
3. Not fabricate citation metadata.

## Protocol

1. Check freshness
- Read `Last Updated` from `documents/reference/papers/prompt-engineering-papers.md`.
- If within 30 days and no explicit update request, skip update and report "fresh".

2. Select target categories
- If user specified categories, use them.
- Otherwise prioritize: lowest current count first, then oldest category update date.

3. Collect candidates
- Search authoritative sources (arXiv, Semantic Scholar, ACL Anthology).
- Prefer papers published since the last update date.

4. Score candidates
- Use the rubric from the master index:
  - novelty: 1-100
  - impact: 1-100
  - score = round((novelty + impact) / 2)

5. Apply add/retire policy
- If category count < 100: add candidates with score >= 50.
- If category count >= 100: add only if score is above current minimum.
- Retire lowest-scoring entries until count returns to 100.
- Never retire score >= 80 papers automatically.

6. Update metadata
- Update category current counts in the master index.
- Update `Last Updated` in modified files.
- Keep tag/category format unchanged.

7. Report summary
- Return updated categories, added count, retired count, skipped reason (if any), and unresolved uncertainties.

## Output Contract

Every run MUST return a structured report with these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `freshness_decision` | `"update"` \| `"skip"` | ✅ | Whether update was needed |
| `skip_reason` | string | if skip | Why update was skipped |
| `affected_files` | string[] | ✅ | Paths of modified files |
| `added` | number | ✅ | Papers added |
| `retired` | number | ✅ | Papers retired |
| `categories_touched` | string[] | ✅ | Category names updated |
| `count_changes` | {category: before → after} | ✅ | Per-category count delta |
| `risk_notes` | string[] | ✅ | Each entry: one specific concern (e.g., "arXiv unreachable — 3 candidates scored from abstract only") |
| `tool_limitations` | string[] | if any | Tools unavailable during execution |

## Guardrails

- Preserve existing markdown schema and table structure.
- Do not modify unrelated documents.
- If source confidence is low, prefer skip with explicit note over speculative additions.

## Failure Handling & Escalation

| Condition | Action |
|-----------|--------|
| All external sources unreachable | Tag `[TOOL LIMITED]`. Skip steps 3–4. Report with `added: 0` and `risk_notes: ["No external sources reachable"]`. Return to caller. |
| Category file schema broken (parse error) | Tag `[EXECUTION BLOCKED]`. Do NOT write to the file. Report broken file path. Escalate to user for manual fix. |
| Scoring ambiguity (novelty/impact uncertain for >50% of candidates) | Proceed but flag each ambiguous entry in `risk_notes`. Do not auto-retire if confidence is low. |
| Catalog count exceeds 100 after add but retire policy cannot select a victim (all ≥80) | Skip retirement. Report count overflow in `risk_notes`. Escalate to user for manual curation. |
