# 삼성 갤럭시워치 수면 데이터 분석 솔루션

이 프로젝트는 삼성 갤럭시워치4 클래식과 갤럭시 스마트폰의 수면 데이터를 활용하여 개인 맞춤형 수면 분석 솔루션을 제공합니다. Health Connect API를 통해 삼성 헬스 데이터에 접근하고, 웹 기반 대시보드를 통해 최적의 수면 시간과 패턴을 분석하여 보여줍니다.

## 주요 기능

- 최적 수면 시간 및 입면/기상 시간 분석
- 수면 단계별(깊은 수면, 얕은 수면, REM 등) 분석
- 수면 효율성 및 패턴 분석
- 활동량, 스트레스 지수 등 수면에 영향을 미치는 요소 분석
- 수면과 다른 건강 지표 간의 상관관계 분석
- 사용자 피드백 시스템 (수면 만족도 및 기상 시 컨디션 평가)
- 직관적인 데이터 시각화 대시보드

## 프로젝트 구조

```
sleep_analysis_project/
├── src/
│   ├── frontend/            # 프론트엔드 (React)
│   │   └── dashboard/       # 대시보드 애플리케이션
│   ├── backend/             # 백엔드 (Flask)
│   │   └── api/             # API 서버
│   └── data_analysis/       # 데이터 분석 모듈 (Python)
│       └── src/             # 분석 알고리즘 및 Health Connect 클라이언트
├── design_document.md       # 설계 문서
├── development_plan.md      # 개발 계획
├── feasibility_analysis.md  # 타당성 분석
└── README.md                # 이 파일
```

## 설치 및 실행 방법 (윈도우 환경)

### 필수 요구사항

- [Node.js](https://nodejs.org/) (v14 이상)
- [Python](https://www.python.org/downloads/) (v3.8 이상)
- [Git](https://git-scm.com/downloads) (선택사항: GitHub에 올리기 위함)

### 1. 프로젝트 다운로드 및 압축 해제

1. 제공된 ZIP 파일을 다운로드합니다.
2. 원하는 위치에 압축을 해제합니다. (예: `C:\Projects\sleep_analysis_project`)

### 2. 백엔드 설정 및 실행

1. 명령 프롬프트(CMD)를 실행합니다. 시작 메뉴에서 "cmd"를 검색하여 실행할 수 있습니다.
2. 백엔드 디렉토리로 이동합니다:
   ```
   cd C:\Projects\sleep_analysis_project\src\backend\api
   ```
3. 가상 환경을 생성합니다:
   ```
   python -m venv venv
   ```
4. 가상 환경을 활성화합니다:
   ```
   venv\Scripts\activate
   ```
5. 필요한 패키지를 설치합니다:
   ```
   pip install flask flask-cors pyjwt pandas numpy
   ```
6. 백엔드 서버를 실행합니다: (sleep_analysis_project\src\backend\api\src 에서)
   ```
   cd src
   python main.py
   ```
7. 서버가 성공적으로 실행되면 다음과 같은 메시지가 표시됩니다:
   ```
   * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
   ```

### 3. 프론트엔드 설정 및 실행

1. 새 명령 프롬프트(CMD) 창을 엽니다.
2. 프론트엔드 디렉토리로 이동합니다:
   ```
   cd C:\Projects\sleep_analysis_project\src\frontend\dashboard
   ```
3. 필요한 패키지를 설치합니다:
   ```
   npm install
   ```
   (이 과정은 몇 분 정도 소요될 수 있습니다)
4. 프론트엔드 개발 서버를 실행합니다:
   ```
   npm start
   ```
5. 자동으로 기본 웹 브라우저가 열리고 `http://localhost:3000`에서 애플리케이션이 실행됩니다.

### 4. 애플리케이션 사용하기

1. 웹 브라우저에서 `http://localhost:3000`으로 접속합니다.
2. 테스트 계정으로 로그인합니다:
   - 이메일: `test@example.com`
   - 비밀번호: `password123`
3. 대시보드에서 수면 데이터 분석 결과를 확인합니다.

## GitHub에 프로젝트 올리기

1. [GitHub](https://github.com/) 계정을 생성합니다 (아직 없는 경우).
2. GitHub 웹사이트에서 새 저장소(repository)를 생성합니다:
   - GitHub에 로그인 후 오른쪽 상단의 "+" 아이콘을 클릭하고 "New repository"를 선택합니다.
   - 저장소 이름을 입력합니다 (예: "sleep-analysis-project").
   - "Create repository" 버튼을 클릭합니다.
3. GitHub Desktop을 사용하여 프로젝트를 업로드합니다:
   - [GitHub Desktop](https://desktop.github.com/)을 다운로드하고 설치합니다.
   - GitHub 계정으로 로그인합니다.
   - "File" > "Add local repository"를 클릭합니다.
   - 프로젝트 폴더를 선택합니다 (예: `C:\Projects\sleep_analysis_project`).
   - "Add repository" 버튼을 클릭합니다.
   - "Publish repository" 버튼을 클릭하고 생성한 저장소를 선택합니다.
   - "Publish repository" 버튼을 다시 클릭하여 업로드를 완료합니다.

## 문제 해결

### 백엔드 서버가 실행되지 않는 경우
- Python이 올바르게 설치되었는지 확인합니다.
- 가상 환경이 활성화되었는지 확인합니다 (명령 프롬프트 앞에 `(venv)`가 표시되어야 함).
- 필요한 모든 패키지가 설치되었는지 확인합니다.

### 프론트엔드가 실행되지 않는 경우
- Node.js가 올바르게 설치되었는지 확인합니다.
- 모든 npm 패키지가 설치되었는지 확인합니다.
- 백엔드 서버가 실행 중인지 확인합니다.

### 로그인이 작동하지 않는 경우
- 백엔드 서버가 실행 중인지 확인합니다.
- 테스트 계정 정보가 올바른지 확인합니다.

## 기술 스택

- **프론트엔드**: React.js, TypeScript, Tailwind CSS
- **백엔드**: Flask (Python), RESTful API
- **데이터 분석**: Python (NumPy, Pandas)
- **데이터 접근**: Health Connect API
- **인증**: JWT 기반 사용자 인증

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.

## 연락처

문제가 발생하거나 질문이 있는 경우 GitHub 이슈를 통해 문의해 주세요.
