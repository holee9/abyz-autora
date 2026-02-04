# Memory Rules - 작업 규칙

## 원칙 (PRINCIPLES)

1. **작업 시작 전 필수 확인**: 모든 작업 시작 전 `/memory/` 폴더를 확인해야 함
2. **실즉시 기록**: 작업 중 발생한 실수/실패/에러는 즉시 기록해야 함
3. **작업 지시 저장**: 새로운 작업은 `/memory/tasks/`에 먼저 기록 후 시작
4. **갑작스러운 종료 대비**: 모든 상태를 문서화하여 중단 후 속개 가능하게 함

---

## 작업 시작 전 체크리스트 (PRE-WORK CHECKLIST)

모든 작업 시작 전 반드시 다음을 확인:

```
[ ] /memory/errors/ - 이전 에러 확인 (재발 방지)
[ ] /memory/tasks/ - 진행 중인 작업 확인
[ ] /memory/rules.md - 이 규칙 확인
[ ] /memory/context.md - 프로젝트 현재 맥락 확인
```

---

## 작업 지시 프로세스 (TASK WORKFLOW)

### 1. 새 작업 시작 시

```bash
# 1. /memory/tasks/에 작업 파일 생성
touch /memory/tasks/TASK_YYYYMMDD_이름.md

# 2. 작업 파일 양식에 맞춰 작성
# - 목적
# - 선행 조건
# - 예상 소요 시간
# - 관련 파일

# 3. 작업 시작

# 4. 완료 시 상태 업데이트
```

### 2. 작업 파일 양식

```markdown
# TASK_YYYYMMDD_이름.md

## 메타데이터
- 생성일: YYYY-MM-DD
- 상태: [진행중/완료/보류/중단]
- 담당: Claude

## 목적
(작업 목표)

## 선행 조건
- [ ] 조건1
- [ ] 조건2

## 작업 내용
(단계별 작업 내용)

## 관련 파일
- 파일1
- 파일2

## 로그
(작업 진행 중 중요 이벤트 기록)
```

---

## 에러 기록 프로세스 (ERROR LOGGING)

### 1. 에러 발생 시 즉시 기록

```markdown
### [YYYY-MM-DD HH:MM] 에러 제목

**발생 위치:** 파일:줄번호 또는 작업 단계

**에러 내용:**
- 에러 메시지: ...
- 재현 단계: ...

**원인 분석:**
- 근본 원인: ...

**해결책:**
- 적용한 해결: ...
- 소요 시간: ...

**재발 방지:**
- 코드 변경: ...
- 프로세스 변경: ...
- 체크리스트 추가: ...

**관련 작업:**
- TASK_YYYYMMDD_이름.md
```

### 2. 에러 분류

| 심각도 | 라벨 | 대응 시간 |
|--------|------|----------|
| Critical | 🔴 | 즉시 |
| High | 🟠 | 1시간 이내 |
| Medium | 🟡 | 당일 |
| Low | 🟢 | 다음 작업 시 |

---

## 작업 중단 시 복구 절차 (RESUME PROCEDURE)

### 갑작스러운 종료 후 복구

1. 최근 작업 확인: `/memory/tasks/`에서 가장 최근 파일 확인
2. 에러 확인: `/memory/errors/`에서 미해결 에러 확인
3. 컨텍스트 복구: `/memory/context.md`로 현재 상태 파악
4. 작업 속개: 중단 지점부터 재개

---

## 문서 구조 (FOLDER STRUCTURE)

```
/memory/
├── rules.md              # 이 규칙 파일
├── context.md            # 프로젝트 현재 맥락
├── checklist.md          # 작업 체크리스트
├── tasks/                # 작업 지시 저장소
│   ├── TASK_20260204_project_setup.md
│   ├── TASK_20260204_workflow_design.md
│   └── template.md       # 작업 템플릿
├── errors/               # 에러 로그
│   ├── ERR_20260204_hook_missing.md
│   └── ERR_20260204_nul_file.md
└── log.md                # 종합 로그
```

---

## 강제 규칙 (MANDATORY RULES)

1. **NO WORK WITHOUT MEMORY CHECK**: 작업 시작 전 /memory/ 확인 없이 작업 금지
2. **ERROR FIRST**: 에러 발생 시 해결책 찾기 전 다른 작업 금지
3. **CONTEXT UPDATE**: 작업 완료 시 context.md 업데이트
4. **TASK CLOSURE**: 작업 완료/중단 시 tasks/ 파일에 상태 명시
