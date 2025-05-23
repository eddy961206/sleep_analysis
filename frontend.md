# 수면 데이터 분석 대시보드 - 프론트엔드

이 디렉토리는 삼성 갤럭시워치 수면 데이터 분석 솔루션의 프론트엔드 코드를 포함합니다.

## 기술 스택

- React.js: UI 컴포넌트 및 애플리케이션 구조
- Redux: 상태 관리
- D3.js/Chart.js: 데이터 시각화
- Tailwind CSS: 스타일링 및 반응형 디자인
- PWA 지원: 오프라인 기능 및 모바일 최적화

## 주요 기능

- 수면 데이터 시각화 대시보드
- 수면 패턴 분석 결과 표시
- 사용자 피드백 입력 인터페이스
- 설정 및 데이터 관리 기능

## 개발 시작하기

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm start

# 프로덕션 빌드
npm run build
```

## 디렉토리 구조

```
frontend/
├── public/          # 정적 파일
├── src/             # 소스 코드
│   ├── components/  # UI 컴포넌트
│   ├── pages/       # 페이지 컴포넌트
│   ├── hooks/       # 커스텀 훅
│   ├── store/       # Redux 스토어
│   ├── api/         # API 클라이언트
│   ├── utils/       # 유틸리티 함수
│   └── styles/      # 스타일 파일
└── tests/           # 테스트 코드
```
