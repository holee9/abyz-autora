# ERR_20260204_korean_filename

## 메타데이터
- 발생일: 2026-02-04
- 심각도: 🟠 High
- 상태: ✅ 해결됨
- 관련 작업: 한글 파일명 지원 구현

---

## 에러 내용

**문제 설명:**
n8n 워크플로우에서 한글 파일명이 제거되어 파일을 식별할 수 없음

**증상:**
```
입력: "의료기기_인증서_FDA.docx"
출력: "______FDA.docx"  (한글 모두 제거됨)
```

**발생 위치:**
- `workflow/medical-doc-automation.json` - Extract Context 노드

**문제 코드:**
```javascript
// 기존 코드 - 한글 제거
const safeFileName = fileName.replace(/[^a-zA-Z0-9._-]/g, '_');
```

---

## 원인 분석

**근본 원인:**
- 정규식 `[^a-zA-Z0-9._-]`가 ASCII 문자만 허용
- 한글 (U+AC00 ~ U+D7A3)이 제거됨

**영향:**
- 한국 사용자에게 파일명 식별 불가
- Audit Trail에서 파일 추적 어려움

---

## 해결책

**적용한 해결:**

```javascript
// 수정된 코드 - 한글 보존
const safeFileName = fileName
  .replace(/[<>:"/\\|?*\x00-\x1f]/g, '_')  // 파일 시스템 예약어만 제거
  .normalize('NFC');  // Unicode 정규화
```

**Python 스크립트도 동일하게 수정:**
```python
# scripts/merge_doc.py
INVALID_FILENAME_CHARS = r'[<>:"/\\|?*\x00-\x1f]'

def _sanitize_filename(self, filename: str) -> str:
    normalized = unicodedata.normalize('NFC', filename)
    safe = re.sub(INVALID_FILENAME_CHARS, '_', normalized)
    # ...
```

**추가 개선:**
- 다중 인코딩 지원 (UTF-8, EUC-KR, CP949)
- Unicode NFC 정규화로 호환성 문제 해결

**소요 시간:** 30분

---

## 재발 방지

### 1. 파일명 sanitization 규칙
- **제거할 문자:** `< > : " / \ | ? * \x00-\x1f` (파일 시스템 예약어만)
- **보존할 문자:** 한글, 일본어, 중국어 등 모든 Unicode 문자

### 2. 인코딩 처리 순서
1. Unicode NFC 정규화
2. 파일 시스템 예약어 제거
3. 길이 제한 확인 (200바이트)

### 3. 테스트 케이스 추가
```
✅ "의료기기_FDA.docx" → "의료기기_FDA.docx"
✅ "ファイル.docx" → "ファイル.docx"
✅ "file<>name.docx" → "file__name.docx"
```

---

## 관련 파일

- `workflow/medical-doc-automation.json`
- `scripts/merge_doc.py`

---

## 참고

- Unicode 정규화: https://unicode.org/reports/tr15/
- 한글 유니코드: U+AC00 ~ U+D7A3 (가-힣)
- 호환용 한글: U+1100 ~ U+11FF (자모), U+3131 ~ U+318E (옛한글)
