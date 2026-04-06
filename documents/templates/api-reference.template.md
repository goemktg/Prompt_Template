# API Reference Template

**목적:** 모든 공개 API에 대한 포괄적이고 검색 가능한 레퍼런스.  
**대상 위치:** `docs/API.md` 또는 `API_REFERENCE.md`

---

## 항목 템플릿 (함수/클래스당)

```markdown
### FunctionName(param1, param2) → ReturnType

이 기능이 수행하는 작업에 대한 간단한 한 문장 설명.

**매개변수 (Parameters):**
- `param1` (Type): 설명. 기본값: `value`. 제약 조건: [있는 경우]
- `param2` (Type): 설명. 기본값: `value`. 제약 조건: [있는 경우]

**반환값 (Returns):**
- Type: 반환값에 대한 설명

**예외 (Raises):**
- `ExceptionType`: 이 예외가 발생하는 경우

**예제 (Examples):**

\`\`\`[language]
# 기본 예제
[code]

# 출력:
[expected output]
\`\`\`

**관련 항목 (Related):**
- `OtherFunction()` — 유사한 기능
- `AnotherClass.method()` — 관련 작업

---
```

---

## 문서 구조

1. **목차 (Table of Contents)** — 각 API 섹션으로의 링크
2. **클래스/객체 (Classes/Objects)** — 각각 다음을 포함:
   - 생성자 시그니처
   - 프로퍼티/속성
   - 메서드
   - 사용 예제
3. **함수 (Functions)** — 각각 다음을 포함:
   - 타입이 포함된 시그니처
   - 설명
   - 매개변수 (제약 조건 포함)
   - 반환값
   - 예외
   - 하나 이상의 예제
   - 관련 함수
4. **상수/열거형 (Constants/Enums)** — 해당하는 경우
5. **타입 정의 (Type Definitions)** — 해당하는 경우

---

## 품질 표준

- 모든 시그니처에 대해 일관된 포맷 사용
- 타입 힌트 포함 (Python: `def func(x: int) -> str`)
- 가상이 아닌 실제 예제 출력 표시
- 관련 API 간의 링크 제공
- 일반적인 오류 및 피하는 방법 강조
