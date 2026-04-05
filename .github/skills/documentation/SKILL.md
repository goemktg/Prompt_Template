---
name: documentation
description: 'Create and maintain project documents (drafts, final, reference) with strict language and path policy. Triggers: write doc, create documentation, document this, publish report.'
---

# documentation

## Usage

Use this skill when a task requires creating or updating project documents, notes, reports, references, or publication-ready markdown outputs.

## Responsibility

This skill owns documentation authoring workflow only:

- Scope: planning, drafting, polishing, and publishing docs.
- Out of scope: code implementation, runtime debugging, package management.

## Project Policy

- Operational assets must be written in English.
- Content under documents/ must be written in Korean.
- Keep one task narrative in one document; avoid duplicated sources of truth.

## Canonical Paths

Use these paths consistently:

- documents/drafts/: in-progress structured drafts
- documents/final/: reviewed, stable deliverables
- documents/reference/: durable technical or research reference
- temp/: temporary raw notes, extraction outputs, disposable artifacts

## Protocol

0. Language Gate (Required First Step)
- Check target path against language zone rules:
  - `documents/**/*` → prose in **Korean**
  - All other paths → prose in **English**
- Code blocks, identifiers, and commands: always **English** in both zones.
- If zone mismatch in existing file: flag and fix before proceeding.

1. Classify request
- Decide doc type: draft, final report, or reference.
- Decide target audience and required depth.

2. Place file correctly
- Start in documents/drafts/ unless the user explicitly asks for final output.
- Move or rewrite to documents/final/ after review-ready quality is reached.
- Store evergreen material in documents/reference/.

3. Write with policy compliance
- Enforce zone language from Step 0:
  - `documents/` files: prose in **Korean**.
  - Other files: prose in **English**.
- Code blocks, identifiers, commands: always **English**.
- Keep headings stable and searchable.
- **Mismatch handling**: If existing content violates zone rules, fix language before adding new content.

**Examples (Quick Reference)**:

| File | ✅ Correct | ❌ Wrong |
|---|---|---|
| `documents/final/report.md` | `## 결론` | `## Conclusion` |
| `documents/drafts/plan.md` | `실행 명령: \`pytest\`` | `Run: \`pytest\`` |
| `README.md` (repo root) | `## Installation` | `## 설치 방법` |
| `.github/agents/*.agent.md` | `## Mission` | `## 미션` |

4. Quality pass
- Remove ambiguity and repeated statements.
- Verify internal links and section consistency.
- Ensure markdown linting passes.

5. Invoke `@doc-reviewer` for validation (MANDATORY — Single-Driver Model)
- After saving documentation files, invoke `@doc-reviewer` with the list of created/edited files.
- Wait for verdict: `APPROVED`, `CONDITIONAL`, or `REJECTED`.
- **Single-Driver Constraint**: `@doc-reviewer` returns structured issues only. It does **NOT** invoke `@doc-writer`. The skill driver or `@doc-writer` owns fix responsibility.
- **If `REJECTED` or `CONDITIONAL` with blocking issues**:
  - Skill driver or `@doc-writer` fixes the reported issues directly.
  - Skill driver or `@doc-writer` re-invokes `@doc-reviewer` for re-review.
  - Repeat until `APPROVED` or `CONDITIONAL` (non-blocking only).
- **Retry cap**: Maximum 3 review cycles. If still rejected after 3 attempts, escalate to user with `[REVIEW ESCALATION]` tag.
- **If reviewer call fails**: Retry once. If still failing, mark as `[REVIEW BLOCKED]` and surface to user.

6. Publication handoff
- Summarize what changed and where.
- Note unresolved questions and next updates.

## Output Contract

Each delivery should include:

- Target file path
- Purpose in one sentence
- Key sections added or updated
- Risks or assumptions, if any
- **Review evidence** (REQUIRED):
  - `review_verdict`: `APPROVED` | `CONDITIONAL` | `REJECTED` | `BLOCKED`
  - `reviewed_files`: list of files reviewed
  - `review_attempts`: number of review cycles (1-3)
  - `open_issues_count`: remaining issues (must be 0 for `APPROVED`)

**Task is NOT complete** unless `review_verdict` is `APPROVED` or `CONDITIONAL` (with non-blocking issues only).

## Minimal Template

Use this skeleton when structure is unclear:

```markdown
# 제목

## 목적

## 배경

## 핵심 내용

## 검증 또는 근거

## 결론

## 후속 작업
```
