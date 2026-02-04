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
│           └── output/     # [Output] 완성된 문서
└── 03_Logs/                # 시스템 로그
```

## 기술 스택

- **n8n**: Self-hosted workflow automation (Docker)
- **Python**: docx-mailmerge for Word document generation
- **Platform**: Raspberry Pi (ARM64)
- **Storage**: Local NAS mount

## 빠른 시작

### Raspberry Pi 배포

```bash
# 1. 레포지토리 클론
git clone https://github.com/holee9/abyz-autora.git
cd abyz-autora/docker

# 2. 환경 설정
cp .env.example .env
nano .env  # 비밀번호와 NAS 경로 설정

# 3. 배포 스크립트 실행
chmod +x deploy.sh
./deploy.sh

# 4. n8n 접속
open http://raspberrypi.local:5678
```

### 로컬 개발 환경

```bash
# 1. Python 의존성 설치
pip install -r scripts/requirements.txt

# 2. 병합 스크립트 테스트
python scripts/merge_doc.py --template template.docx --json specs.json --output output.docx

# 3. Docker 컨테이너 시작
docker-compose up -d
```

## 워크플로우 import

n8n UI에서 `workflow/medical-doc-automation.json` 파일을 import하세요.

## 프로젝트 구조

```
abyz-autora/
├── docker/              # Docker 설정
│   ├── docker-compose.yml
│   ├── .env.example
│   └── deploy.sh
├── scripts/             # Python 스크립트
│   ├── merge_doc.py     # 문서 병합 메인
│   └── requirements.txt
├── workflow/            # n8n 워크플로우
│   └── medical-doc-automation.json
├── memory/              # 에러 로그 & 레슨러닝
└── plan-ra-n8n-workflow.md
```

## 프로젝트 상태

- [x] Plan 문서 작성
- [x] GitHub 레포지토리 생성
- [x] 프로젝트 구조 생성
- [x] n8n 워크플로우 설계
- [x] Python 스크립트 개발
- [x] Docker 환경 설정
- [ ] 라즈베리파이 배포 및 테스트
- [ ] 3회 반복 검증/개선

## 라이선스

Copyright © 2026 Abyz-Lab Inc.
