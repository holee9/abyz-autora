# Errors - 에러 로그

이 폴더에는 프로젝트 진행 중 발생한 모든 에러와 해결책이 기록됩니다.

## 에러 목록

| 파일 | 제목 | 날짜 | 심각도 | 상태 |
|------|------|------|--------|------|
| ERR_20260204_hook_missing.md | Hook 파일 누락 | 2026-02-04 | 🟠 High | ✅ |
| ERR_20260204_nul_file.md | Windows nul 파일 생성 | 2026-02-04 | 🟡 Medium | ✅ |
| ERR_20260204_korean_filename.md | 한글 파일명 제거 문제 | 2026-02-04 | 🟠 High | ✅ |
| ERR_20260204_command_injection.md | Command Injection 취약점 | 2026-02-04 | 🔴 Critical | ✅ |

## 빠른 검색

```bash
# 에러 검색
grep -r "키워드" memory/errors/

# 최근 에러 확인
ls -lt memory/errors/ | head -10

# 미해결 에러 확인
grep -l "상태:.*보류\|상태:.*미해결" memory/errors/*.md
```

## 에러 작성 가이드

새 에러 기록 시 다음 템플릿을 사용하세요:

```markdown
# ERR_YYYYMMDD_간단_제목

## 메타데이터
- 발생일: YYYY-MM-DD
- 심각도: [🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low]
- 상태: [✅ 해결됨 / ⏳ 진행중 / ⏸️ 보류]
- 관련 작업: 작업명

## 에러 내용
**에러 메시지:** ...
**발생 위치:** ...
**재현 단계:** ...

## 원인 분석
**근본 원인:** ...

## 해결책
**적용한 해결:** ...
**소요 시간:** ...

## 재발 방지
...

## 관련 파일
...
```
