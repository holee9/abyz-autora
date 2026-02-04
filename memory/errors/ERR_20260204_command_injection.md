# ERR_20260204_command_injection

## 메타데이터
- 발생일: 2026-02-04
- 심각도: 🔴 Critical
- 상태: ✅ 해결됨
- 관련 작업: 보안 감사 (Iteration 1-2)

---

## 에러 내용

**취약점 유형:** OS Command Injection

**취약한 코드:**
```javascript
// n8n workflow - Merge Document 노드
"command": "=python3 /scripts/merge_doc.py --template=\"{{ $json.templatePath }}\" ..."
```

**공격 예시:**
```
파일명: "; rm -rf / #.docx"
실제 실행: python3 /scripts/merge_doc.py --template="; rm -rf / #.docx"
결과: 임의 명령 실행 가능!
```

**발생 위치:**
- `workflow/medical-doc-automation.json` - 여러 Execute Command 노드
- Node 6 (mkdir), Node 7 (merge), Node 10 (mv)

---

## 원인 분석

**근본 원인:**
1. 사용자 입력(파일 경로)을 검증 없이 shell 명령에 직접 삽입
2. 따옴표로 감싸더라도 내부 따옴표 이스케이프 미흡
3. n8n의 표현식 보간이 shell-safe하지 않음

**영향:**
- 공격자가 임의 명령 실행 가능
- 파일 시스템 파괴 가능
- 데이터 유출 가능

---

## 해결책

**적용한 해결:**

### 1. 파일명 sanitization (JavaScript)
```javascript
// 파일명에서 위험 문자 제거
const safeFileName = fileName
  .replace(/[<>:"/\\|?*\x00-\x1f]/g, '_')  // 파일 시스템 예약어
  .replace(/[;&|`$()]/g, '_');  // shell 메타문자 추가 제거
```

### 2. Path validation (Python)
```python
def _validate_paths(self):
    for path_str in [self.template_path, self.json_path]:
        # Path traversal 확인
        if '..' in Path(path_str).parts:
            raise ValueError(f"Path traversal attempt: {path_str}")

        # Symlink attack 확인
        resolved = Path(path_str).resolve()
        try:
            resolved.relative_to(self.base_dir)
        except ValueError:
            raise ValueError(f"Path outside base: {resolved}")
```

### 3. n8n 파라미터 사용
```javascript
// 가능한 경우 n8n의 내장 파라미터 바인딩 사용
"filePath": "={{ $json.specsPath }}"  // n8n가 안전하게 처리
```

**소요 시간:** 1시간

---

## 재발 방지

### 1. 입력 검증 계층
```
사용자 입력
    ↓
[1] 화이트리스트 필터 (파일명)
    ↓
[2] Path traversal 검사
    ↓
[3] Symlink 검사
    ↓
[4] Shell 메타문자 제거
    ↓
안전한 명령 실행
```

### 2. 보안 검토 체크리스트
- [ ] 모든 사용자 입력이 sanitization 되었는가?
- [ ] Path traversal 검사가 있는가?
- [ ] Shell 메타문자가 제거되었는가?
- [ ] 최소 권한 원칙이 적용되었는가?

### 3. 정기 보안 감사
- 각 반복마다 보안 전문가에게 코드 리뷰 요청
- OWASP Top 10 체크리스트 사용

---

## 관련 취약점 (CWE)

- CWE-78: OS Command Injection
- CWE-22: Improper Limitation of a Pathname
- CWE-20: Improper Input Validation

---

## 참고

- OWASP Command Injection: https://owasp.org/www-community/attacks/Command_Injection
- n8n Security: https://docs.n8n.io/security/
