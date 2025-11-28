# FastAPI CRM 시스템

> Flask에서 FastAPI로 성공적으로 마이그레이션된 CRM 프로젝트

## 🚀 빠른 시작

### 1. 설치 및 실행

```bash
# 프로젝트 디렉토리로 이동
cd CRM_orm_fastapi

# 의존성 설치
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv

# 서버 실행
python main.py

# 또는
uvicorn app.main:app --reload
```

### 2. API 접속

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/api

### 3. 웹 페이지 접속

- **메인 페이지**: http://localhost:8000/
- **사용자 관리**: http://localhost:8000/users
- **매장 관리**: http://localhost:8000/stores
- **주문 관리**: http://localhost:8000/orders
- **상품 관리**: http://localhost:8000/items

---

## 📋 API 엔드포인트 가이드

### Users (사용자)

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/api/users/` | 모든 사용자 조회 |
| `POST` | `/api/users/` | 사용자 생성 |
| `GET` | `/api/users/{user_id}` | 특정 사용자 조회 |
| `PUT` | `/api/users/{user_id}` | 사용자 수정 |
| `DELETE` | `/api/users/{user_id}` | 사용자 삭제 |

**사용자 생성 예시:**
```json
{
  "id": "user001",
  "name": "홍길동",
  "birthdate": "1990-01-01",
  "age": 34,
  "gender": "M",
  "address": "서울시 강남구"
}
```

---

### Stores (매장)

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/api/stores/` | 모든 매장 조회 |
| `POST` | `/api/stores/` | 매장 생성 |
| `GET` | `/api/stores/{store_id}` | 특정 매장 조회 |
| `PUT` | `/api/stores/{store_id}` | 매장 수정 |
| `DELETE` | `/api/stores/{store_id}` | 매장 삭제 |

**매장 생성 예시:**
```json
{
  "id": "store001",
  "type": "카페",
  "name": "커피숍 A",
  "address": "서울시 강남구 테헤란로"
}
```

---

### Items (상품)

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/api/items/` | 모든 상품 조회 |
| `POST` | `/api/items/` | 상품 생성 |
| `GET` | `/api/items/{item_id}` | 특정 상품 조회 |
| `PUT` | `/api/items/{item_id}` | 상품 수정 |
| `DELETE` | `/api/items/{item_id}` | 상품 삭제 |

**상품 생성 예시:**
```json
{
  "id": "item001",
  "type": "음료",
  "name": "아메리카노",
  "price": 3000
}
```

---

### Orders (주문)

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/api/orders/` | 모든 주문 조회 |
| `POST` | `/api/orders/` | 주문 생성 |
| `GET` | `/api/orders/{order_id}` | 특정 주문 조회 |
| `PUT` | `/api/orders/{order_id}` | 주문 수정 |
| `DELETE` | `/api/orders/{order_id}` | 주문 삭제 |

**주문 생성 예시:**
```json
{
  "id": "order001",
  "ordertime": "2024-11-28 10:00:00",
  "store_id": "store001",
  "user_id": "user001"
}
```

---

### Orderitems (주문 상품)

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/api/orderitems/` | 모든 주문-상품 조회 |
| `POST` | `/api/orderitems/` | 주문-상품 생성 |
| `GET` | `/api/orderitems/{orderitem_id}` | 특정 주문-상품 조회 |
| `GET` | `/api/orderitems/order/{order_id}` | 주문의 모든 상품 조회 |
| `DELETE` | `/api/orderitems/{orderitem_id}` | 주문-상품 삭제 |

**주문-상품 생성 예시:**
```json
{
  "id": "oi001",
  "order_id": "order001",
  "item_id": "item001"
}
```

---

## 📁 프로젝트 구조

```
CRM_orm_fastapi/
├── app/
│   ├── core/
│   │   └── config.py              # 환경설정
│   ├── database/
│   │   ├── base.py                # SQLAlchemy Base
│   │   ├── session.py             # DB 세션 관리
│   │   └── models.py              # ORM 모델
│   ├── schemas/
│   │   ├── user.py, store.py, ... # Pydantic 스키마
│   │   └── __init__.py
│   ├── api/
│   │   ├── users/, stores/, ...   # API 라우터
│   │   └── __init__.py
│   ├── static/                    # HTML, CSS, JS
│   └── main.py                    # FastAPI 앱
├── instance/
│   └── mycrm.db                   # SQLite 데이터베이스
├── main.py                        # 실행 진입점
└── .env                           # 환경변수
```

---

## 🔧 기술 스택

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **ORM**: SQLAlchemy 2.0.23
- **Validation**: Pydantic 2.5.0
- **Database**: SQLite

---

## 📚 학습 자료

### 자동 생성된 문서

1. **[FastAPI 마이그레이션 가이드](./FASTAPI_MIGRATION_GUIDE.md)**
   - Flask → FastAPI 변환 과정
   - 각 Phase별 상세 설명

2. **[진행 현황 요약](./PROGRESS_SUMMARY.md)**
   - 완료된 작업
   - 예정된 작업
   - 구현 가이드

3. **[최종 구현 보고서](./FINAL_IMPLEMENTATION_SUMMARY.md)**
   - 전체 구현 내용
   - 통계 및 분석
   - 프로덕션 체크리스트

---

## 🧪 테스트 예시

### cURL로 테스트

```bash
# 사용자 조회
curl http://localhost:8000/api/users/

# 사용자 생성
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "user001",
    "name": "홍길동",
    "birthdate": "1990-01-01",
    "age": 34,
    "gender": "M",
    "address": "서울"
  }'

# 특정 사용자 조회
curl http://localhost:8000/api/users/user001

# 사용자 수정
curl -X PUT http://localhost:8000/api/users/user001 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "김길동"
  }'

# 사용자 삭제
curl -X DELETE http://localhost:8000/api/users/user001
```

### Python으로 테스트

```python
import requests

BASE_URL = "http://localhost:8000/api"

# 사용자 생성
response = requests.post(f"{BASE_URL}/users/", json={
    "id": "user001",
    "name": "홍길동",
    "birthdate": "1990-01-01",
    "age": 34,
    "gender": "M",
    "address": "서울"
})
print(response.json())

# 사용자 조회
response = requests.get(f"{BASE_URL}/users/user001")
print(response.json())
```

---

## 🔒 환경설정

### .env 파일 생성

```env
# 데이터베이스
DATABASE_URL=sqlite:///./instance/mycrm.db

# 앱 설정
DEBUG=True
LOG_LEVEL=DEBUG
APP_NAME=CRM API
```

---

## 📈 마이그레이션 결과

### Flask vs FastAPI

| 항목 | Flask | FastAPI |
|------|-------|---------|
| **API 문서** | 수동 | 자동 (Swagger) |
| **데이터 검증** | 수동 | Pydantic 자동 |
| **성능** | 동기식 | 비동기식 |
| **타입 안전성** | 낮음 | 높음 |
| **개발 생산성** | 중간 | 높음 |

---

## ✅ 완성도 체크리스트

- ✅ 기초 인프라 설정
- ✅ API 스키마 정의
- ✅ 모든 엔드포인트 구현
- ✅ 데이터 검증
- ✅ 에러 처리
- ✅ CORS 설정
- ✅ 자동 문서화
- ✅ 정적 파일 서빙
- ⏳ 인증/권한 (향후 추가)
- ⏳ 테스트 코드 (향후 추가)
- ⏳ 배포 (향후 추가)

---

## 🚨 문제 해결

### 서버가 실행되지 않음

```bash
# 의존성 확인
pip list | grep fastapi

# 포트 확인
netstat -tlnp | grep 8000

# 재설치
pip install --upgrade fastapi uvicorn
```

### 404 에러

- 경로 확인: `/api/users/` (O), `/api/users` (X)
- HTTP 메서드 확인: GET, POST, PUT, DELETE
- Swagger UI에서 확인: http://localhost:8000/docs

### 데이터베이스 오류

```bash
# 데이터베이스 재초기화
rm -rf instance/mycrm.db
python main.py
```

---

## 💡 팁

1. **Swagger UI 활용**
   - http://localhost:8000/docs에서 API 테스트
   - "Try it out" 버튼으로 직접 테스트 가능

2. **ReDoc 활용**
   - http://localhost:8000/redoc에서 API 문서 보기
   - 더 깔끔한 UI

3. **페이지네이션**
   - `skip`, `limit` 파라미터로 페이지네이션
   - 예: `/api/users/?skip=0&limit=10`

4. **에러 메시지**
   - 자동으로 한국어 에러 메시지 반환
   - API 문서에서 확인 가능

---

## 📞 연락처 및 지원

프로젝트에 대한 질문이나 버그 리포트는 다음 문서를 참조하세요:
- [마이그레이션 가이드](./FASTAPI_MIGRATION_GUIDE.md)
- [최종 구현 보고서](./FINAL_IMPLEMENTATION_SUMMARY.md)

---

## 📜 라이선스

이 프로젝트는 자유롭게 사용, 수정, 배포할 수 있습니다.

---

**Happy Coding! 🚀**

