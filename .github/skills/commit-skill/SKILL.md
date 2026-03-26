---
name: commit-skill
description: 'Strict workflow for Git commits: inspect changes since last commit, generate a Conventional Commits message, show summary, and require explicit user confirmation before commit. Use when user says "커밋 진행", "커밋", "commit", "commit 진행", or asks to save changes with git.'
---

# Commit Skill

Use this skill when the user wants to create a git commit.

## Trigger Intents

- "커밋 진행"
- "커밋해줘"
- "commit this"
- "create commit"
- "save changes with git"

## Mandatory Safety Rule

Never run `git commit` without explicit user approval in the current conversation turn.

## Change Inspection Rule

Do not inspect changes by directly composing ad-hoc git read commands in chat.
Always execute the OS-appropriate inspection script first and base analysis on its output.

- macOS/Linux: `sh .github/skills/commit-skill/scripts/inspect-changes.sh`
- Windows: `cmd /c .github\\skills\\commit-skill\\scripts\\inspect-changes.cmd`

## Workflow

1. Inspect current working tree and changes since last commit by running the OS-appropriate inspection script.
2. Summarize changed files and core intent of the change.
3. Generate a commit message candidate using Conventional Commits style.
4. Present a confirmation message to the user in this form:
   - "다음 내용으로 커밋을 생성합니다: <message>. 진행할까요?"
5. Wait for explicit approval.
6. Only after approval, stage relevant files and execute commit with the approved message.

## Commit Message Generation Rules

- Base analysis on diff since last commit (`HEAD`) including staged and unstaged changes.
- Use a bilingual commit message structure:
   - Main commit subject (first line): English only, format `<type>(<scope>): <subject>`.
   - Detailed body (following lines): Korean bullet points summarizing key changes.
- Allowed types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`.
- Keep subject concise and specific.
- Body bullets should be concrete and file/change oriented.
- If multiple unrelated changes are present, suggest splitting commits.

## Confirmation and Execution Rules

- Approval examples: "진행", "커밋해", "yes", "approve".
- Rejection examples: "취소", "아니오", "cancel", "stop".
- Ambiguous responses: ask a clarification question and do not commit.

## Failure and Edge Cases

- No changes detected: report and stop.
- Commit fails: show error, preserve state, and ask whether to retry with adjusted message.
- Protected branch concerns: warn user before commit if branch appears protected (`main`, `master`, `develop`).
- Inspection script fails: show script error output and stop before commit proposal.

## Output Template

Use this response template before commit execution:

```text
변경 요약:
- <file 1>: <short change>
- <file 2>: <short change>

제안 커밋 메시지:
<type>(<scope>): <english subject>

- <한글 세부 변경사항 1>
- <한글 세부 변경사항 2>

위 메시지로 커밋을 생성할까요?
```
