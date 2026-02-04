# Memory - 프로젝트 기억 저장소

이 폴더는 프로젝트의 모든 맥락, 규칙, 에러, 작업을 저장하여 **갑작스러운 종료 후에도 작업을 속개할 수 있도록** 합니다.

## 📁 폴더 구조

```
memory/
├── README.md              # 이 파일
├── rules.md               # 작업 규칙 (필독!)
├── context.md             # 프로젝트 현재 맥락
├── checklist.md           # 작업 시작 전 체크리스트
├── log.md                 # 종합 로그
├── tasks/                 # 작업 지시 저장소
│   ├── README.md
│   └── template.md        # 작업 템플릿
└── errors/                # 에러 로그
    ├── README.md
    └── ERR_YYYYMMDD_*.md  # 에러 기록
```

## 🚀 작업 시작 전 (MANDATORY)

**모든 작업 시작 전 반드시 다음을 확인하세요:**

1. **체크리스트 실행**: `memory/checklist.md`의 모든 항목 확인
2. **에러 확인**: `memory/errors/`에서 재발 방지 확인
3. **컨텍스트 확인**: `memory/context.md`로 현재 상태 파악
4. **규칙 확인**: `memory/rules.md`의 규칙 준수

## 📝 문서 작성 가이드

### 새 작업 시작 시
```bash
cp memory/tasks/template.md memory/tasks/TASK_YYYYMMDD_이름.md
```

### 새 에러 기록 시
`memory/errors/ERR_YYYYMMDD_제목.md` 생성

## 🔥 빠른 참조

| 항목 | 파일 | 용도 |
|------|------|------|
| 규칙 | rules.md | 작업 규칙 |
| 체크리스트 | checklist.md | 작업 전 확인 |
| 컨텍스트 | context.md | 현재 프로젝트 상태 |
| 작업 템플릿 | tasks/template.md | 새 작업 생성 |
| 에러 | errors/ | 에러/해결책 |

## ⚠️ 핵심 규칙

1. **NO WORK WITHOUT MEMORY CHECK** - /memory/ 확인 없이 작업 금지
2. **ERROR FIRST** - 에러 발생 시 즉시 기록
3. **CONTEXT UPDATE** - 상태 변경 시 context.md 업데이트
