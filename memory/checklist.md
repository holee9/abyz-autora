# Pre-Work Checklist - 작업 시작 전 체크리스트

모든 작업 시작 전 반드시 이 체크리스트를 완료하세요.

---

## 1. Memory 확인 (MEMORY CHECK)

- [ ] `/memory/errors/` - 이전 에러 확인 (재발 방지)
- [ ] `/memory/tasks/` - 진행 중인 작업 확인
- [ ] `/memory/context.md` - 프로젝트 현재 상태 확인
- [ ] `/memory/rules.md` - 규칙 확인

---

## 2. 환경 확인 (ENVIRONMENT CHECK)

- [ ] 작업 디렉토리: `E:/github_work/med-ra-n8n-workflow`
- [ ] Git 상태: 깨끗한지 확인 (`git status`)
- [ ] Docker: 필요 시 실행 중인지 확인

---

## 3. 이전 작업 상태 (PREVIOUS WORK STATUS)

- [ ] 마지막 작업 완료 여부 확인
- [ ] 미완료 작업이 있다면 우선순위 결정

---

## 4. 새 작업 시작 시 (NEW WORK)

- [ ] `/memory/tasks/`에 작업 파일 생성
- [ ] 작업 목적과 범위 명시
- [ ] 예상 소요 시간 산정
- [ ] 관련 파일 목록 작성

---

## 5. 에러 발생 시 (ON ERROR)

- [ ] `/memory/errors/`에 즉시 기록
- [ ] 근본 원인 분석
- [ ] 해결책 문서화
- [ ] 재발 방지 조치 기록

---

## 6. 작업 완료 시 (ON COMPLETE)

- [ ] 작업 파일 상태를 "완료"로 변경
- [ ] `/memory/context.md` 업데이트 (필요 시)
- [ ] Git 커밋 (변경 사항 있을 시)
- [ ] 다음 작업 계획 기록

---

## 자주 발생하는 에러 (COMMON ERRERS - FROM /memory/errors/)

| 에러 | 해결책 | 참고 |
|------|--------|------|
| Hook 파일 누락 | `echo '#!/usr/bin/env python3' > .claude/hooks/moai/pre_tool__security_guard.py` | ERR_20260204_hook_missing |
| nul 파일 생성 (Windows) | bash echo 리다이렉션 사용 시 주의 | ERR_20260204_nul_file |
| 한글 파일명 깨짐 | Unicode NFC 정규화 사용 | merge_doc.py 참조 |

---

## 빠른 참조 (QUICK REFERENCE)

```bash
# 에러 기록 생성
echo "### [$(date +%Y%m%d)] 에러 제목" >> memory/errors/ERR_$(date +%Y%m%d).md

# 작업 파일 생성
cp memory/tasks/template.md memory/tasks/TASK_$(date +%Y%m%d).md

# Git 상태 확인
git status

# 컨텍스트 확인
cat memory/context.md
```
