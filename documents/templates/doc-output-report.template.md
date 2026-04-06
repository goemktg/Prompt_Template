# Documentation Output Report Template

**목적:** 문서 생성 작업에 대한 구조화된 완료 리포트.  
**사용 주체:** 작업 완료 시 `@doc-writer`가 사용.

---

## 템플릿

```markdown
# 문서 생성 완료 ✅

**프로젝트 (Project):** [Project Name]  
**작성일 (Date):** [ISO8601]  
**문서 ID (Documentation ID):** [doc_id]

## 생성된 파일 목록 (Files Generated)

| 파일 명 (File) | 타입 (Type) | 섹션 수 | 단어 수 | 예상 독해 시간 | 상태 (Status) |
|------|------|----------|-------|-----------|--------|
| README.md | Overview | 9 | 1,500 | 6 min | ✅ |
| API_REFERENCE.md | Reference | 25 | 3,200 | 12 min | ✅ |

## 문서 커버리지 지표 (Coverage Metrics)

- **문서화된 함수 비율:** 100%
- **문서화된 클래스 비율:** 100%
- **제공된 예제 비율:** 95%
- **설치 지침 포함 여부:** ✅ 완료
- **자주 발생하는 오류 정리 여부:** ✅ 확인
- **배포 준비 여부:** ✅ 확인

## 품질 체크리스트 (Quality Checklist)

- ✅ 맞춤법 및 문법 검토 완료
- ✅ 코드 예제 테스트 완료 (문법적으로 유효함)
- ✅ 모든 링크 검증 완료
- ✅ 전반적으로 일관된 어조 유지
- ✅ 컨벤션에 맞게 포맷 준수
- ✅ 예제가 예상된 출력을 보여주도록 구성

## 리뷰 검증 기록 (Review Validation Evidence)

| 필드 | 값 |
|-------|-------|
| **리뷰 결과 (Verdict)** | [APPROVED / CONDITIONAL / REJECTED / BLOCKED] |
| **리뷰된 파일 목록** | [file1.md, file2.md, ...] |
| **리뷰 시도 횟수** | [1-3] |
| **남은 미해결 이슈** | [0 or list] |
| **블로킹 이슈** | [none or list] |

## 개선 권장 사항 (Recommendations)

1. [Suggestion 1] — 커버리지 확장을 위해
2. [Suggestion 2] — 고급 사용자를 위해

---

**세션 ID (Session ID):** [timestamp]
```

---

## 성공 완료 기준 필드

| 필드 | 필수 여부 | 완료 기준 |
| ----- | -------- | ------------------- |
| Review Verdict | ✅ | `APPROVED` 또는 비차단 `CONDITIONAL` 이어야 함 |
| Reviewed Files | ✅ | 생성되거나 편집된 모든 파일이 기재되어야 함 |
| Review Attempts | ✅ | 최대 3회; 초과 시 에스컬레이션 |
| Open Issues | ✅ | `APPROVED`일 때는 0; `CONDITIONAL`일 때는 비차단 에러만 허용 |
| Blocking Issues | ✅ | 작업 완료를 위해선 비어 있어야 함 |
