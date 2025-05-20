# 수면 데이터 분석 대시보드 - 백엔드

이 디렉토리는 삼성 갤럭시워치 수면 데이터 분석 솔루션의 백엔드 코드를 포함합니다.

## 기술 스택

- Node.js: 서버 런타임
- Express.js: 웹 프레임워크
- SQLite: 로컬 데이터베이스 (초기 MVP)
- JWT: 인증 시스템
- RESTful API: 프론트엔드 통신

## 주요 기능

- Health Connect API 연동 인터페이스
- 수면 데이터 수집 및 저장
- 사용자 인증 및 권한 관리
- 데이터 분석 결과 제공 API

## 개발 시작하기

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm run dev

# 프로덕션 서버 실행
npm start
```

## 디렉토리 구조

```
backend/
├── src/             # 소스 코드
│   ├── controllers/ # API 컨트롤러
│   ├── models/      # 데이터 모델
│   ├── routes/      # API 라우트
│   ├── services/    # 비즈니스 로직
│   ├── utils/       # 유틸리티 함수
│   └── middleware/  # 미들웨어
├── config/          # 설정 파일
└── tests/           # 테스트 코드
```
