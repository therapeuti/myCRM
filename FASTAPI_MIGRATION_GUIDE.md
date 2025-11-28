# FastAPI CRM 마이그레이션 가이드

> Flask 기반 CRM을 FastAPI로 리팩토링하는 과정을 단계별로 기록합니다.

---

## 📋 목차

1. [Phase 1: 기초 인프라 설정](#phase-1-기초-인프라-설정)
2. [Phase 2: API 스키마 정의](#phase-2-api-스키마-정의)
3. [Phase 3: API 엔드포인트 구현](#phase-3-api-엔드포인트-구현)
4. [Phase 4: 최종 통합](#phase-4-최종-통합)

---

## Phase 1: 기초 인프라 설정

### 목표
- FastAPI 설정 관리 (`config.py`)
- SQLAlchemy 데이터베이스 설정
- 의존성 주입 패턴 적용

### 완료된 작업

#### 1.1 설정 파일 생성 (`app/core/config.py`)

**파일 위치**: `CRM_orm_fastapi/app/core/config.py`

**역할**:
- 환경별 설정 관리 (개발/테스트/운영)
- 데이터베이스 URI 설정
- 로깅 설정
- API 버전 관리

**주요 설정**:
```python
DATABASE_URL = f"sqlite:///{BASE_DIR}/instance/mycrm.db"
LOG_LEVEL = "DEBUG"
API_V1_PREFIX = "/api/v1"
CORS_ORIGINS = ["*"]
```

**특징**:
- Pydantic `BaseSettings`를 사용한 환경변수 관리
- `.env` 파일 지원
- 싱글톤 패턴으로 설정 객체 관리

---

#### 1.2 데이터베이스 기본 설정

##### `app/database/base.py`
- **목적**: SQLAlchemy Base 클래스 정의
- **내용**: `Base = declarative_base()`
- **사용**: 모든 ORM 모델이 상속받는 기본 클래스

##### `app/database/session.py`
- **목적**: 데이터베이스 엔진과 세션 관리
- **내용**:
  - `engine`: SQLAlchemy 엔진 (SQLite)
  - `SessionLocal`: 세션 팩토리
  - `get_db()`: 의존성 주입용 함수

**의존성 주입 패턴**:
```python
# FastAPI 라우터에서 사용
@app.get("/api/users")
async def get_users(db: Session = Depends(get_db)):
    # db를 사용하여 데이터베이스 쿼리
    return db.query(User).all()
```

---

#### 1.3 ORM 모델 변환

**변경 사항**: Flask-SQLAlchemy → SQLAlchemy 2.0

| 항목 | 이전 (Flask) | 현재 (FastAPI) |
|------|-------------|--------------|
| **Base 클래스** | `db.Model` | `Base` (declarative) |
| **Column 정의** | `db.Column()` | `Column()` |
| **외래키** | `db.ForeignKey()` | `ForeignKey()` |
| **임포트** | `from flask_sqlalchemy import SQLAlchemy` | `from sqlalchemy import Column, String, ...` |

**변환된 모델 예시**:
```python
# 이전 (Flask)
class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

# 현재 (FastAPI)
class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    name = Column(String)
```

**모델 목록** (변환 완료):
- ✅ User
- ✅ Store
- ✅ Order
- ✅ Item
- ✅ Orderitem

---

### 파일 구조

```
CRM_orm_fastapi/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              ✅ 생성됨
│   └── database/
│       ├── __init__.py
│       ├── base.py                ✅ 생성됨
│       ├── session.py             ✅ 생성됨
│       ├── models.py              ✅ 변환됨
│       ├── users_db.py
│       ├── stores_db.py
│       ├── items_db.py
│       ├── orders_db.py
│       └── orderitems_db.py
├── main.py
└── instance/
    └── mycrm.db                   (자동 생성됨)
```

---

### 다음 단계

→ **Phase 2: API 스키마 정의** (Pydantic 모델)

---

## Phase 2: API 스키마 정의

### 목표
- Pydantic 스키마 작성 (요청/응답 검증)
- 타입 힌팅을 통한 자동 문서화

### ✅ 완료된 작업

#### 2.1 스키마 파일 생성

**파일 위치**: `app/schemas/`

**생성된 파일들**:

| 파일 | 설명 | 스키마 클래스 |
|------|------|------------|
| `user.py` | 사용자 스키마 | UserCreate, UserUpdate, UserResponse |
| `store.py` | 매장 스키마 | StoreCreate, StoreUpdate, StoreResponse |
| `item.py` | 상품 스키마 | ItemCreate, ItemUpdate, ItemResponse |
| `order.py` | 주문 스키마 | OrderCreate, OrderUpdate, OrderResponse |
| `orderitem.py` | 주문-상품 스키마 | OrderitemCreate, OrderitemResponse |
| `__init__.py` | 스키마 통합 | 모든 클래스 export |

#### 2.2 스키마 설계 패턴

**사용자 예시**:
```python
# app/schemas/user.py

class UserBase(BaseModel):
    """기본 정보 (공통)"""
    name: str
    age: int

class UserCreate(UserBase):
    """생성 요청"""
    id: str

class UserUpdate(BaseModel):
    """수정 요청 (모든 필드 선택사항)"""
    name: Optional[str] = None
    age: Optional[int] = None

class UserResponse(UserBase):
    """응답/조회"""
    id: str
    class Config:
        from_attributes = True  # ORM 모델 자동 변환
```

#### 2.3 주요 특징

- **계층적 상속**: `Base` → `Create`, `Update`, `Response`
- **타입 검증**: Pydantic이 자동으로 입력값 검증
- **자동 직렬화**: ORM 모델 → JSON 직렬화
- **API 문서 생성**: FastAPI가 자동으로 Swagger 문서 생성

**From_attributes**:
```python
from_attributes = True  # SQLAlchemy ORM → Pydantic 모델 자동 변환
```

#### 2.4 사용 예시

```python
# API 라우터에서 사용
from fastapi import FastAPI
from app.schemas import UserCreate, UserResponse

@app.post("/api/v1/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # user: UserCreate (자동 검증됨)
    # 응답: UserResponse (JSON으로 변환됨)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    return new_user
```

---

## Phase 3: API 엔드포인트 구현

### 목표
- 각 리소스별 CRUD API 엔드포인트 작성
- FastAPI 라우터 통합

### ✅ 진행 상황: Users API 완성

#### 3.1 Users API 구현

**구조**:
```
api/users/
├── __init__.py       # 라우터 통합
├── users.py          # ✅ CRUD 함수
└── user_info.py      # ✅ API 엔드포인트
```

#### 3.2 CRUD 함수 (`users.py`)

```python
def get_user(db: Session, user_id: str) -> User:
    """특정 사용자 조회"""

def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    """모든 사용자 조회 (페이지네이션)"""

def create_user(db: Session, user: UserCreate) -> User:
    """새 사용자 생성"""

def update_user(db: Session, user_id: str, user_update: UserUpdate) -> User:
    """사용자 정보 수정"""

def delete_user(db: Session, user_id: str) -> bool:
    """사용자 삭제"""
```

#### 3.3 라우터 엔드포인트 (`user_info.py`)

| 메서드 | 경로 | 설명 | 상태 |
|--------|------|------|------|
| `GET` | `/` | 모든 사용자 조회 (페이지네이션) | ✅ 완성 |
| `GET` | `/{user_id}` | 특정 사용자 조회 | ✅ 완성 |
| `POST` | `/` | 새 사용자 생성 | ✅ 완성 |
| `PUT` | `/{user_id}` | 사용자 정보 수정 | ✅ 완성 |
| `DELETE` | `/{user_id}` | 사용자 삭제 | ✅ 완성 |

**API 엔드포인트**:
```
GET    /api/users/              # 사용자 목록
POST   /api/users/              # 사용자 생성
GET    /api/users/{user_id}     # 특정 사용자 조회
PUT    /api/users/{user_id}     # 사용자 수정
DELETE /api/users/{user_id}     # 사용자 삭제
```

#### 3.4 주요 기능

- **자동 검증**: Pydantic으로 요청 데이터 자동 검증
- **에러 처리**: HTTPException으로 404, 400 에러 반환
- **응답 모델**: response_model로 자동 직렬화
- **문서화**: Docstring으로 Swagger 자동 생성

#### 3.5 구현 패턴

```python
@router.get('/{user_id}', response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)  # 의존성 주입
):
    """API 문서에 나타날 설명"""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user
```

### 구현 예정

**다음 단계** (동일한 패턴으로 구현):
- Stores API
- Items API
- Orders API
- Orderitems API

---

## Phase 4: 최종 통합

### 목표
- 모든 라우터를 `main.py`에 등록
- HTML 페이지 서빙과 API를 통합
- 미들웨어 설정 (CORS, 로깅 등)

### 구현 예정

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, stores, items, orders, orderitems

app = FastAPI()

# 미들웨어
app.add_middleware(CORSMiddleware, ...)

# API 라우터 등록
app.include_router(users.router, prefix="/api/v1/users")
app.include_router(stores.router, prefix="/api/v1/stores")
# ...

# HTML 라우팅
@app.get("/{path:path}")
async def serve_html(path: str):
    # HTML 파일 서빙
```

---

## 🛠️ 개발 중 참고사항

### 데이터베이스 초기화
```python
from app.database.base import Base
from app.database.session import engine

# 테이블 생성
Base.metadata.create_all(bind=engine)
```

### 의존성 주입
```python
from fastapi import Depends
from app.database.session import get_db

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

### 환경 설정 사용
```python
from app.core.config import settings

print(settings.DATABASE_URL)
print(settings.DEBUG)
```

---

## 📊 진행 상황

| Phase | 상태 | 설명 |
|-------|------|------|
| Phase 1 | ✅ 완료 | 설정 및 데이터베이스 초기화 |
| Phase 2 | ⏳ 예정 | Pydantic 스키마 작성 |
| Phase 3 | ⏳ 예정 | API 엔드포인트 구현 |
| Phase 4 | ⏳ 예정 | 최종 통합 및 문서화 |

---

## 📝 참고 링크

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org/)
- [Pydantic 문서](https://docs.pydantic.dev/)

