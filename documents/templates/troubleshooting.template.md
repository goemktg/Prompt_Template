# Troubleshooting Template

**목적:** 문제를 신속하게 해결하고, 향후 문제를 방지함.  
**대상 위치:** `TROUBLESHOOTING.md` 또는 `docs/faq.md`

---

## 항목 템플릿 (이슈당)

```markdown
## [Error Message 또는 Problem Title]

**증상 (Symptoms):**
- 증상 현상
- 발생하는 일

**근본 원인 (Root Cause):**
[Why this occurs]

**해결책 (Solution):**

옵션 1: [빠른 해결책]
\`\`\`bash
[command]
\`\`\`

옵션 2: [대안 해결책]
\`\`\`bash
[command]
\`\`\`

**예방 (Prevention):**
- [향후 이를 방지하는 방법]
- [베스트 프랙티스]

**관련 이슈 (Related Issues):**
- [Similar problem and solution]

---
```

---

## 문서 구조

1. **빠른 답변 FAQ (Quick Answer FAQ)** (가장 많이 묻는 질문 3-5가지)
2. **설치 오류 (Installation Errors)** (OS별 그룹화)
3. **런타임 오류 (Runtime Errors)** (증상별 그룹화)
4. **성능 문제 (Performance Issues)**
5. **통합 문제 (Integration Problems)** (해당하는 경우)
6. **디버깅 가이드 (Debugging Guide)** (버그 리포트를 위해 정보를 수집하는 방법)

---

## 품질 표준

- 오류 메시지를 그대로 제목으로 사용 (로그에서 복사-붙여넣기가 가능하도록 유지)
- 여러 가지의 해결책이 있다면 모두 제시
- 문제가 발생한 이유(WHY)를 교육적으로 설명
- 사전 예방을 돕는 예방 팁 제공
- 더 깊은 이해를 위해 API_REFERENCE.md 링크 제공
