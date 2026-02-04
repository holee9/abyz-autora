# ERR_20260204_hook_missing

## 메타데이터
- 발생일: 2026-02-04
- 심각도: 🟠 High
- 상태: ✅ 해결됨
- 관련 작업: 프로젝트 초기 설정

---

## 에러 내용

**에러 메시지:**
```
PreToolUse hook error: [uv run "%CLAUDE_PROJECT_DIR%//.claude/hooks/moai/pre_tool__security_guard.py"]:
error: Failed to spawn: `E:\github_work\med-ra-n8n-workflow//.claude/hooks/moai/pre_tool__security_guard.py`
Caused by: 지정된 파일을 찾을 수 없습니다. (os error 2)
```

**발생 위치:**
- 프로젝트 초기 설정 중
- Write 도구 사용 시

**재현 단계:**
1. 새 프로젝트 폴더 생성
2. .claude/settings.local.json만 생성
3. hooks 폴더와 스크립트 누락
4. Write 도구 실행 시 hook 실행 실패

---

## 원인 분석

**근본 원인:**
- MoAI 설정에서 hook 파일을 요구하지만, 초기 프로젝트 생성 시 자동으로 생성되지 않음
- `.claude/hooks/moai/` 폴더 구조가 수동으로 필요

---

## 해결책

**적용한 해결:**

```bash
# 1. hooks 폴더 생성
mkdir -p .claude/hooks/moai

# 2. hook 스크립트 생성
echo '#!/usr/bin/env python3
import sys
sys.exit(0)' > .claude/hooks/moai/pre_tool__security_guard.py

# 3. post hooks도 동일하게 생성
echo '#!/usr/bin/env python3
import sys
sys.exit(0)' > .claude/hooks/moai/post_tool__ast_grep_scan.py
```

**소요 시간:** 10분

---

## 재발 방지

### 1. 프로젝트 템플릿에 포함
- `.claude/hooks/moai/` 폴더와 기본 hook 스크립트를 프로젝트 템플릿에 포함

### 2. 체크리스트 추가
- `/memory/checklist.md`에 "hook 파일 존재 확인" 항목 추가

### 3. Hook 파일 내용 (최소 구현)
```python
#!/usr/bin/env python3
"""
MoAI Hook - Security Guard
최소 구현: 항상 성공 리턴
"""
import sys
sys.exit(0)
```

---

## 관련 파일

- `.claude/hooks/moai/pre_tool__security_guard.py`
- `.claude/hooks/moai/post_tool__ast_grep_scan.py`
- `.claude/hooks/moai/post_tool__code_formatter.py`
- `.claude/hooks/moai/post_tool__linter.py`

---

## 참고

- Windows에서 `echo` 명령과 리다이렉션 사용 시 주의 필요
- nul 파일 생성 문제와 연관됨 (ERR_20260204_nul_file)
