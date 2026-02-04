# ERR_20260204_nul_file

## 메타데이터
- 발생일: 2026-02-04
- 심각도: 🟡 Medium
- 상태: ✅ 해결됨
- 관련 작업: Git 커밋 중

---

## 에러 내용

**에러 메시지:**
```
error: short read while indexing nul
error: nul: failed to insert into database
error: unable to index file 'nul'
fatal: adding files failed
```

**발생 위치:**
- Git add 실행 중

**재현 단계:**
1. Windows bash에서 echo와 리다이렉션 사용
2. 실수로 `echo "content" > nul` 실행 (Windows 예약어)
3. Git add로 인식 실패

---

## 원인 분석

**근본 원인:**
- Windows에서 `nul`은 예약된 장치 이름 (Linux의 /dev/null과 유사)
- bash echo 리다이렉션 사용 시 파일 대신 장치로 인식
- Git이 이를 정상 파일로 인식하지 못함

**발생한 위치:**
```bash
# 문제가 된 명령 (hooks 폴더 생성 중)
echo '#!/usr/bin/env python3
import sys
sys.exit(0)' > ".claude/hooks/moai/pre_tool__security_guard.py"
```

---

## 해결책

**적용한 해결:**

```bash
# 1. 생성된 nul 파일 삭제
rm -f ./nul
rm -f ./scripts/nul

# 2. 파일을 안전하게 생성하는 방법
# 방법 A: Write 도구 사용 (권장)
# 방법 B: cat heredoc 사용
cat > file.py << 'EOF'
#!/usr/bin/env python3
import sys
sys.exit(0)
EOF

# 방법 C: printf 사용
printf '#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n' > file.py
```

**소요 시간:** 5분

---

## 재발 방지

### 1. Windows 예약어 목록 숙지
```
nul, con, prn, aux, com1-9, lpt1-9
```

### 2. 파일 생성 모범 사례
- **권장:** Write 도구 또는 cat heredoc 사용
- **비권장:** echo + 리다이렉션 (다중 라인 시)

### 3. 체크리스트 추가
- Git add 전 `git status`로 예약어 파일 확인

---

## 관련 에러

- ERR_20260204_hook_missing - 같은 원인으로 발생

---

## 참고

Windows와 Linux 경로 구분자 차이로 인해 다른 문제도 발생할 수 있음:
- Windows: 백슬래시 (`\`)
- Linux: 슬래시 (`/`)
- 해결: `path.replace(/\\/g, '/')` 정규화 사용
