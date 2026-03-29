---
name: paper-catalog-update
description: 'Maintain the prompt engineering paper catalog with a monthly update protocol, scoring rules, and safe add-retire operations.'
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
- Prompt-master is invoked and database freshness must be checked

## Responsibility

This skill owns catalog update procedure only:
- Scope: stale-check, category selection, search, scoring, add/retire, metadata update
- Out of scope: prompt generation, prompt optimization, model choice recommendations

## Inputs

- `today` date
- `Last Updated` value from master index
- Optional: target categories requested by user

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

Every run must include:
- freshness decision (update or skip)
- affected files list
- numeric delta (added/retired/count changes)
- risk notes (source confidence or scoring ambiguity)

## Guardrails

- Preserve existing markdown schema and table structure.
- Do not modify unrelated documents.
- If source confidence is low, prefer skip with explicit note over speculative additions.
