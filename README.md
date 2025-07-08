<h1 align="center">🛡️ Online Grooming Detection System</h1>
<p align="center">
  아동·청소년을 위한 온라인 그루밍 탐지 및 분석 시스템  
</p>

## 🔍 프로젝트 정보

- **프로젝트명**: Online Grooming Detection
- **진행 기간**: 2025.05 ~ 2025.07
- **주요 내용**: 온라인 그루밍 대화 탐지 모델 + GPT 기반 위험 분석
- **주요 기술**: `Huggingface Transformers`, `RoBERTa`, `PyTorch`, `WandB`, `GPT-4o API`

---

## 🔗 배포 주소

- 서비스 데모 (클릭): 👉 [https://online-grooming-detection.com](https://)
- hugging face 모델 배포 : 

---
## 👨‍👩‍👧‍👦 팀 소개

| 이름 | 소속 | 역할 | GitHub |
|------|------|------|--------|
| 강준규 | 동의대학교 물리치료학과 | 팀장, 프로젝트 기획 및 총괄, 탐지 모델 설계 | [@jade-kang](https://github.com/jade-kang) |
| 임성훈 | 동의대학교 컴퓨터소프트웨어학과 | 시스템 개발, 데이터 엔지니어링 | |
| 노성민 | 동의대학교 응용소프트웨어학과 | 데이터 엔지니어링, 탐지 모델 설계 | [@minnnnnnnnnnn](https://github.com/minnnnnnnnnnn) |
| 정석호 | 동의대학교 응용소프트웨어학과 | 프로젝트 기획, 탐지 모델 설계 | [@seokho22](https://github.com/seokho22) |
| 허원준 | 동의대학교 산업빅데이터학과 | 데이터 엔지니어링, 보고서 및 포스터 작성 |  |

---
## 🧠 프로젝트 소개

> 본 프로젝트는 **디지털 성범죄의 전 단계인 온라인 그루밍**을 조기에 탐지하고,  
> **GPT 기반 해석 분석으로 위험 상황을 구조적으로 판단**할 수 있는 시스템입니다.  
> 실제 온라인 채팅 데이터를 활용해 인공지능이 대화 흐름과 문맥을 학습하도록 설계하였고,  
> 위험 발화를 감지했을 때, 그 이유와 맥락을 사람이 이해할 수 있도록 보고서 형태로 제공합니다.  
> 향후 실시간 플랫폼 연동을 통해 **채팅 서비스 내 조기 경고**로도 확장할 수 있는 기반을 마련했습니다.

---
## 기술 스택 
### Environment
<img src="https://img.shields.io/badge/googlecolab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white"> <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 

### Development
<img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">

### Communication 
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"> <img src="https://img.shields.io/badge/notion-000000?style=for-the-badge&logo=notion&logoColor=white">

---

## 🚀 시작 가이드

---

### ⚙️ 설치 및 실행

```bash
# 1. Clone the repository
git clone https://github.com/your-org/online-grooming-detection.git
cd online-grooming-detection

# 2. 가상환경 생성 (선택)
python -m venv venv
source venv/bin/activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 환경 변수 설정 (필요 시)
export WANDB_API_KEY=your_key_here

# 5. 학습 시작
python train.py

--- 
