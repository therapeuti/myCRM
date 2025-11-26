# Flask CRM 시스템

ORM을 활용한 고객 관계 관리(CRM) 시스템입니다.

## 📋 주요 기능

- **사용자 관리**: 고객 정보 등록, 조회, 수정, 삭제
- **스토어 관리**: 매장 정보 관리
- **주문 관리**: 주문 내역 추적 및 관리
- **아이템 관리**: 상품 정보 관리
- **키오스크 모드**: 고객 셀프 서비스
- **관리자 대시보드**: 통계 및 관리 기능

## 🚀 개선된 주요 사항

### 보안 강화
- ✅ 환경변수 기반 시크릿 키 관리
- ✅ 적절한 인증 로직 구현
- ✅ 비밀번호 로깅 제거
- ✅ 전역 에러 핸들링

### 코드 품질
- ✅ 데이터베이스 모델 개선 (적절한 타입, 제약조건)
- ✅ 관계(Relationship) 정의
- ✅ 중복 코드 제거
- ✅ Import 최적화
- ✅ 중앙화된 로깅 시스템

### 개발 환경
- ✅ 환경별 설정 관리
- ✅ 데이터베이스 마이그레이션 스크립트
- ✅ 단위 테스트 코드
- ✅ API 문서화
- ✅ 애플리케이션 팩토리 패턴

## 🛠️ 기술 스택

- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Testing**: pytest
- **Logging**: Python logging module

## 📦 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 설정
```bash
# .env 파일 생성 (.env.example 참고)
cp .env.example .env

# 환경변수 설정
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password
```

### 3. 데이터베이스 초기화
```bash
# 데이터베이스 생성 및 마이그레이션
python migrations/init_db.py

# 샘플 데이터 생성 (선택사항)
python migrations/seed_data.py
```

### 4. 애플리케이션 실행
```bash
# 개발 모드
python run.py

# 또는 직접 실행
python app.py
```

### 5. 애플리케이션 접속
- **URL**: http://localhost:5000
- **관리자 로그인**: 설정한 ADMIN_USERNAME/ADMIN_PASSWORD 사용

## 🧪 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/test_models.py

# 커버리지와 함께 실행
pytest --cov=.
```

## 📁 프로젝트 구조

```
CRM_orm_claude_code_refactoring/
├── app.py                 # 메인 애플리케이션
├── run.py                 # 실행 스크립트
├── config.py              # 설정 관리
├── requirements.txt       # 의존성 목록
├── .env.example          # 환경변수 예시
├── README.md             # 프로젝트 문서
├── API_DOCUMENTATION.md  # API 문서
│
├── database/             # 데이터베이스 관련
│   ├── models.py         # ORM 모델
│   ├── users_db.py       # 사용자 DB 함수
│   ├── stores_db.py      # 스토어 DB 함수
│   ├── orders_db.py      # 주문 DB 함수
│   ├── items_db.py       # 아이템 DB 함수
│   └── kiosk_db.py       # 키오스크 DB 함수
│
├── routes/               # 라우트 모듈
│   ├── api.py            # API 라우트
│   ├── users.py          # 사용자 라우트
│   ├── stores.py         # 스토어 라우트
│   ├── orders.py         # 주문 라우트
│   ├── items.py          # 아이템 라우트
│   └── kiosk.py          # 키오스크 라우트
│
├── static/               # 정적 파일
│   ├── css/              # 스타일시트
│   ├── js/               # JavaScript
│   └── *.html            # HTML 템플릿
│
├── utils/                # 유틸리티
│   └── logger.py         # 로깅 설정
│
├── migrations/           # 데이터베이스 마이그레이션
│   ├── init_db.py        # 초기화 스크립트
│   └── seed_data.py      # 샘플 데이터
│
├── tests/                # 테스트 코드
│   ├── conftest.py       # 테스트 설정
│   ├── test_models.py    # 모델 테스트
│   ├── test_users_db.py  # 사용자 DB 테스트
│   └── test_app.py       # 애플리케이션 테스트
│
└── logs/                 # 로그 파일 (자동 생성)
    ├── crm.log           # 일반 로그
    └── error.log         # 에러 로그
```

## 🔧 환경 설정

### 개발 환경
```bash
export FLASK_ENV=development
```

### 운영 환경
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
```

### 테스트 환경
```bash
export FLASK_ENV=testing
```

## 📚 API 문서

자세한 API 문서는 [API_DOCUMENTATION.md](API_DOCUMENTATION.md)를 참고하세요.

### 주요 엔드포인트

- `POST /admin_login` - 관리자 로그인
- `GET /api/users` - 사용자 목록 조회
- `POST /api/users` - 사용자 생성
- `GET /api/stores` - 스토어 목록 조회
- `GET /api/orders` - 주문 목록 조회
- `GET /api/items` - 아이템 목록 조회

## 🐛 문제 해결

### 데이터베이스 오류
```bash
# 데이터베이스 재초기화
rm mycrm.db
python migrations/init_db.py
```

### 로그 확인
```bash
# 실시간 로그 확인
tail -f logs/crm.log

# 에러 로그 확인
tail -f logs/error.log
```

## 🔐 보안 고려사항

1. **시크릿 키**: 운영 환경에서는 반드시 강력한 시크릿 키 사용
2. **관리자 계정**: 기본 계정 정보 변경 필수
3. **데이터베이스**: 운영 환경에서는 SQLite 대신 PostgreSQL/MySQL 권장
4. **HTTPS**: 운영 환경에서는 HTTPS 사용 필수
5. **로그 관리**: 민감한 정보 로깅 금지

## 📈 성능 최적화

1. **데이터베이스 인덱스**: 자주 조회되는 필드에 인덱스 추가
2. **쿼리 최적화**: N+1 쿼리 문제 해결
3. **캐싱**: Redis 등을 활용한 캐싱 구현
4. **페이지네이션**: 대량 데이터 조회 시 페이지네이션 적용

## 🤝 기여하기

1. 이 저장소를 Fork 합니다
2. 새 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 Push 합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 있습니다.

## 📞 연락처

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 생성해 주세요.