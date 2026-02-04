# [Project] Abyz-AutoRA: 로컬 NAS 기반 의료기기 인증 자동화 시스템

**Version:** Final (Deep Sync Verified)
**Date:** 2026-02-04
**Author:** Abyz-Lab AI Partner

## 1. 개요 (Overview)
본 프로젝트는 로컬 NAS(Synology 등)와 Self-hosted n8n을 연동하여, 의료기기 인증에 필요한 기술문서 작성을 자동화하는 시스템 구축을 목표로 합니다. 보안을 위해 외부 클라우드 의존도를 제거하고, 데이터 무결성 및 예외 처리 로직을 강화했습니다.

## 2. 제품 요구사항 (PRD)

### 2.1 핵심 기능
1.  **Zero-Touch Trigger:** 사용자가 NAS의 `requests` 폴더에 양식 파일을 넣으면 자동으로 감지하여 작업 시작.
2.  **Context-Aware Mapping:** 파일 경로를 분석하여 제품(Product)과 모델(Model)을 스스로 식별하고, 적합한 `specs.json`을 로드.
3.  **Cross-Border Templating:** 단일 스펙 데이터로 국가별(FDA, CE, MFDS) 상이한 양식을 자동 처리.
4.  **Audit Trail:** GMP/ISO 13485 규정 준수를 위해 생성 이력(Timestamp, User, File)을 로그로 기록.

### 2.2 기술적 제약 사항 (Non-Functional Req)
* **Local Execution:** 모든 데이터 처리는 로컬 네트워크(Docker Container) 내부에서 완결.
* **Fail-Safe:** 필수 데이터 누락 시 오작동을 방지하고 `_Error` 폴더로 격리 조치.

## 3. 기술 명세 (Technical Spec)

### 3.1 폴더 구조 (Standardized Architecture)
NAS 마운트 경로: `/data/medical-auth/`

```text
/data/medical-auth/
├── 01_Templates/           # [Read-Only] 국가별 원본 양식 (예: FDA_510k_v2.docx)
├── 02_Projects/
│   └── [ProductName]/      # 예: X-ray_Detector
│       └── [ModelName]/    # 예: DX-2026
│           ├── specs.json  # [Master Data] 모델 사양서 (Single Source of Truth)
│           ├── assets/     # [Images] 도면, 그래프, 시험성적서 등
│           ├── requests/   # [Input] 사용자가 빈 양식을 넣는 곳
│           └── output/     # [Output] 완성된 문서가 저장되는 곳
└── 03_Logs/                # 시스템 로그 (CSV/Txt)

3.2 데이터 스키마 (specs.json)
JSON
{
  "model_info": {
    "model_id": "DX-2026",
    "trade_name": "Abyz-Ray Pro",
    "classification": "Class IIb"
  },
  "tech_specs": {
    "resolution": "3072 x 3072",
    "pixel_pitch": "140 um",
    "input_voltage": "DC 24V"
  },
  "manufacturer": {
    "name": "Abyz-Lab Inc.",
    "address": "Suwon-si, Gyeonggi-do, Korea"
  }
}
3.3 워크플로우 로직 (Step-by-Step)
Trigger: Local File Trigger가 **/requests/*.docx 생성 감지.

Path Parsing: 정규식(Regex)으로 파일 경로에서 ProductName, ModelName 변수 추출.

Data Validation: specs.json 존재 여부 및 필수 필드 값 검증.

Content Merging: Word 템플릿의 {{tag}}를 JSON 데이터로 치환 (Python Script or Word Node).

Archiving: 결과물을 output 폴더에 [YYMMDD]_[Type]_[Model]_Completed.docx로 저장.

4. 품질 보증 (QA Checklist)
[ ] 폴더명 변경(Renaming) 시에도 경로 추적이 가능한가? (Regex 유연성)

[ ] specs.json 파일이 손상되었을 때 워크플로우가 멈추고 알림을 보내는가?

[ ] 한글 파일명 및 특수문자가 포함된 경로도 에러 없이 처리되는가?


---

### 파일 2: Claude Code 입력용 프롬프트 (영문)
* **파일명:** `Claude_Code_Prompt_n8n_Workflow.md`
* **용도:** Claude Code(또는 AI 코딩 도구)에게 입력하여 **실제 n8n JSON 코드**를 생성하게 하는 설계도

```markdown
# Prompt: Generate n8n Workflow for Medical Doc Automation

## Role & Objective
You are an expert n8n workflow developer specializing in local automation (Self-hosted) and file system operations. 
Your task is to generate a robust **n8n Workflow JSON** based on the specifications below. The system runs on Docker with a mounted NAS volume.

## Project Scope
Automate the filling of medical device certification documents (.docx) by merging them with product specification data (.json) stored in a structured local file system.

## Environment Configuration
1.  **Platform:** n8n (Self-hosted, Docker)
2.  **Mount Point:** `/data/medical-auth/` (Mapped to local NAS)
3.  **Key Nodes:** `Local File Trigger`, `Read Binary File`, `Code` (JavaScript), `Execute Command` (for Python docx-mailmerge), `Write Binary File`.

## Detailed Logic & Requirements

### Step 1: Trigger (Monitoring)
* **Node:** `Local File Trigger`
* **Path:** `/data/medical-auth/02_Projects/**/requests/*.docx`
* **Event:** On file created.
* **Output:** Must pass the full binary data and file path.

### Step 2: Context Extraction (The Brain)
* **Node:** `Code` (JavaScript)
* **Logic:**
    * Input: `filePath` from Step 1.
    * Regex Action: Extract `ProductName` and `ModelName` from path `.../02_Projects/{ProductName}/{ModelName}/requests/...`.
    * Path Construction: Define path to Master Data -> `/data/medical-auth/02_Projects/{ProductName}/{ModelName}/specs.json`.
    * Context Action: Identify 'Target Country' from filename (e.g., "FDA" -> "US", "MDR" -> "EU").

### Step 3: Data Retrieval & Validation
* **Node:** `Read Binary File` (Read `specs.json`).
* **Node:** `Code` (Validation): Check if JSON parses correctly and contains required keys (`model_id`, `manufacturer`). If not, throw Error.

### Step 4: Document Generation (Merging)
* **Constraint:** Since n8n native Word nodes can be limited in local/offline environments, use `Execute Command` to run a Python script.
* **Python Logic (Conceptual):**
    ```python
    from mailmerge import MailMerge
    # Load template and json data
    # Merge fields: template.merge(**data)
    # Save to output path
    ```
* *Note for Workflow:* Please construct the `Execute Command` node to run a script like `python3 /scripts/merge_doc.py --template {path} --data {json_path}`.

### Step 5: Output & Cleanup
* **Node:** `Write Binary File` (if not handled by Python).
* **Path:** `/data/medical-auth/02_Projects/{ProductName}/{ModelName}/output/`
* **Naming:** `{YYYYMMDD}_{TargetCountry}_{OriginalName}_Completed.docx`

## Output Format
Provide the **complete n8n Workflow JSON code** that can be directly pasted into the n8n UI. Include comments in the `Code` nodes explaining the Regex logic.