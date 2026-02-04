# Project Context - Abyz-AutoRA

**최종 업데이트:** 2026-02-04

## 프로젝트 개요

**이름:** Abyz-AutoRA (로컬 NAS 기반 의료기기 인증 자동화 시스템)

**목표:** n8n + Docker + Python으로 의료기기 인증 문서 자동 생성

**레포지토리:** https://github.com/holee9/abyz-autora

---

## 현재 상태

| 구성 요소 | 상태 | 비고 |
|----------|------|------|
| Plan 문서 | ✅ 완료 | plan-ra-n8n-workflow.md |
| 프로젝트 구조 | ✅ 완료 | docker/, scripts/, workflow/, memory/ |
| n8n 워크플로우 | ✅ 완료 | medical-doc-automation.json (v3) |
| Python 스크립트 | ✅ 완료 | merge_doc.py (보안 강화 완료) |
| Docker 설정 | ✅ 완료 | docker-compose.yml (ARM64) |
| 보안 검토 | ✅ 완료 | 3회 반복 검증 완료 |
| 한글 지원 | ✅ 완료 | EUC-KR/CP949 인코딩 지원 |
| 라즈베리파이 배포 | ⏳ 대기중 | 실제 장비에서 테스트 필요 |

---

## 기술 스택

- **워크플로우:** n8n v1.64.1
- **언어:** Python 3
- **문서 처리:** docx-mailmerge
- **플랫폼:** Raspberry Pi 4/5 (ARM64)
- **스토리지:** 로컬 NAS 마운트

---

## 보안 강화 사항

- 파일명 sanitization (Command injection 방지)
- Path traversal 검출
- 파일 크기 제한 (10MB)
- 한글 파일명 보존 (Unicode NFC)
- 다중 인코딩 지원

---

## 다음 작업 (NEXT TASKS)

1. 라즈베리파이 실제 배포 테스트
2. 실제 의료기기 문서 템플릿으로 검증
3. 성능 테스트 (대용량 파일 처리)

---

## 중요 경로

```bash
# NAS 마운트 포인트
/data/medical-auth/

# 프로젝트 루트
E:/github_work/med-ra-n8n-workflow/

# Docker 컨테이너 실행 위치
docker/

# n8n 워크플로우
workflow/medical-doc-automation.json

# Python 병합 스크립트
scripts/merge_doc.py
```

---

## 환경 변수 (필수 설정값)

```bash
N8N_PASSWORD=changeme          # 필수 변경
ENCRYPTION_KEY=32_char_hex     # 필수 생성
NAS_PATH=/mnt/medical-auth     # NAS 경로
```

---

## Git 상태

```bash
# 브랜치: master
# 원격: origin (https://github.com/holee9/abyz-autora.git)
# 마지막 커밋: a6a78d0 "feat: Security hardening and Korean support"
```

---

## 완료된 반복 (COMPLETED ITERATIONS)

| 반복 | 날짜 | 주요 내용 |
|------|------|----------|
| 1 | 2026-02-04 | 초기 구현, 기본 보안 |
| 2 | 2026-02-04 | Command injection fix |
| 3 | 2026-02-04 | 한글 지원, symlink 방지 |
