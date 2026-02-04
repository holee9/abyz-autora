# Abyz-AutoRA: 로컬 NAS 기반 의료기기 인증 자동화 시스템

## 개요

로컬 NAS(Synology 등)와 Self-hosted n8n을 연동하여, 의료기기 인증에 필요한 기술문서 작성을 자동화하는 시스템입니다. 보안을 위해 외부 클라우드 의존도를 제거하고, 데이터 무결성 및 예외 처리 로직을 강화했습니다.

## 주요 기능

| 기능 | 설명 |
|------|------|
| **Zero-Touch Trigger** | NAS의 `requests` 폴더에 양식 파일을 넣으면 자동 감지 |
| **Context-Aware Mapping** | 파일 경로를 분석하여 제품(Product)과 모델(Model) 자동 식별 |
| **Cross-Border Templating** | 단일 스펙 데이터로 국가별(FDA, CE, MFDS) 양식 자동 처리 |
| **Audit Trail** | GMP/ISO 13485 규정 준용 로그 기록 |
| **Korean Support** | 한글 파일명 및 EUC-KR/CP949 인코딩 지원 |

## 시스템 구조

```
/data/medical-auth/
├── 01_Templates/           # 국가별 원본 양식
├── 02_Projects/
│   └── [ProductName]/
│       └── [ModelName]/
│           ├── specs.json  # 모델 사양서 (Single Source of Truth)
│           ├── assets/     # 도면, 그래프, 시험성적서
│           ├── requests/   # [Input] 빈 양식 넣는 곳
│           ├── output/     # [Output] 완성된 문서
│           └── _Error/     # 에러 발생 파일 격리
└── 03_Logs/                # 시스템 로그 (audit.log, errors.log)
```

## 기술 스택

| 구성 | 기술 |
|------|------|
| **워크플로우 엔진** | n8n v1.64.1 (Docker) |
| **문서 생성** | Python 3 + docx-mailmerge |
| **플랫폼** | Raspberry Pi 4/5 (ARM64) |
| **스토리지** | 로컬 NAS 마운트 |
| **보안** | no-new-privileges, resource limits |

## 보안 강화

- 파일명 sanitization (Command injection 방지)
- Path traversal 검출
- 파일 크기 제한 (10MB)
- 한글 파일명 보존 (Unicode NFC 정규화)
- 다중 인코딩 지원 (UTF-8, EUC-KR, CP949)

## 빠른 시작

### Raspberry Pi 배포

```bash
# 1. 레포지토리 클론
git clone https://github.com/holee9/abyz-autora.git
cd abyz-autora/docker

# 2. 환경 설정 (.env 파일은 git에서 제외됨)
cp .env.example .env
nano .env  # 필수: 비밀번호, ENCRYPTION_KEY, NAS_PATH 변경

# 3. 암호화 키 생성
openssl rand -hex 32  # .env의 ENCRYPTION_KEY에 값 입력

# 4. 배포 스크립트 실행
chmod +x deploy.sh
./deploy.sh

# 5. n8n 접속
# 브라우저에서 http://raspberrypi.local:5678 접속
```

### 로컬 개발 환경

```bash
# 1. Python 의존성 설치
pip install -r scripts/requirements.txt

# 2. 병합 스크립트 테스트
python scripts/merge_doc.py \
  --template template.docx \
  --json specs.json \
  --output output.docx
```

## 워크플로우 import

n8n UI에서 `workflow/medical-doc-automation.json` 파일을 import하세요.

## 프로젝트 구조

```
abyz-autora/
├── docker/              # Docker 설정
│   ├── docker-compose.yml
│   ├── .env.example     # 환경변수 템플릿 (.env는 gitignore)
│   └── deploy.sh        # 자동 배포 스크립트
├── scripts/             # Python 스크립트
│   ├── merge_doc.py     # 문서 병합 메인
│   ├── requirements.txt
│   └── setup_folder_structure.sh
├── workflow/            # n8n 워크플로우
│   └── medical-doc-automation.json
├── memory/              # 에러 로그 & 레슨러닝
│   └── log.md           # 개발 중 발견된 이슈 기록
└── README.md
```

## 환경 변수 (.env 필수 설정)

```bash
# 보안: 반드시 변경하세요
N8N_PASSWORD=your_secure_password
ENCRYPTION_KEY=32_character_hex_key_from_openssl

# NAS 설정
NAS_PATH=/mnt/medical-auth  # 실제 NAS 마운트 경로
```

## 프로젝트 상태

- [x] Plan 문서 작성
- [x] GitHub 레포지토리 생성
- [x] 프로젝트 구조 생성
- [x] n8n 워크플로우 설계
- [x] Python 스크립트 개발
- [x] Docker 환경 설정
- [x] 보안 강화 (3회 반복 검증 완료)
- [x] 한글 파일명 지원
- [ ] 라즈베리파이 실제 배포 테스트

## 라이선스

Copyright © 2026 Abyz-Lab Inc.
