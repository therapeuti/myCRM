# Flask CRM API 문서

## 개요
Flask CRM 시스템의 RESTful API 문서입니다.

## 기본 정보
- **Base URL**: `http://localhost:5000`
- **API 버전**: v1
- **Content-Type**: `application/json`
- **인증**: 기본 인증 (admin/admin123)

## 인증 엔드포인트

### 관리자 로그인
관리자 계정으로 로그인합니다.

**POST** `/admin_login`

#### 요청 파라미터
| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| id | string | ✓ | 관리자 ID |
| pw | string | ✓ | 관리자 비밀번호 |

#### 요청 예시
```bash
curl -X POST http://localhost:5000/admin_login \
  -F "id=admin" \
  -F "pw=admin123"
```

#### 응답
- **성공**: 302 Redirect to `/users/`
- **실패**: 302 Redirect to `/?error=invalid_credentials`

---

## 사용자 API

### 사용자 목록 조회
등록된 사용자 목록을 조회합니다.

**GET** `/api/users`

#### 쿼리 파라미터
| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| page | integer | 1 | 페이지 번호 |
| count | integer | 10 | 페이지당 항목 수 |
| orderby | string | id | 정렬 기준 (id, name, age, gender) |
| search | string | - | 검색어 |

#### 응답 예시
```json
{
  "users": [
    {
      "id": "user-uuid-1",
      "name": "김철수",
      "birthdate": "1990-01-15",
      "age": 34,
      "gender": "남성",
      "address": "서울시 강남구",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total_count": 1
}
```

### 사용자 상세 조회
특정 사용자의 상세 정보를 조회합니다.

**GET** `/api/users/{user_id}`

#### 경로 파라미터
| 파라미터 | 타입 | 설명 |
|---------|------|------|
| user_id | string | 사용자 ID |

#### 응답 예시
```json
{
  "user": {
    "id": "user-uuid-1",
    "name": "김철수",
    "birthdate": "1990-01-15",
    "age": 34,
    "gender": "남성",
    "address": "서울시 강남구",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  },
  "order_history": [
    {
      "order_id": "order-uuid-1",
      "ordertime": "2024-01-15T09:30:00",
      "store": "스타벅스 강남점",
      "item": "아메리카노,카페라떼"
    }
  ],
  "store_top5": [
    {
      "store": "스타벅스 강남점",
      "cnt": 5
    }
  ],
  "item_top5": [
    {
      "item": "아메리카노",
      "cnt": 10
    }
  ]
}
```

### 사용자 생성
새로운 사용자를 등록합니다.

**POST** `/api/users`

#### 요청 본문
```json
{
  "name": "김철수",
  "birthdate": "1990-01-15",
  "gender": "남성",
  "address": "서울시 강남구"
}
```

#### 응답
```json
{
  "success": true,
  "message": "사용자가 생성되었습니다.",
  "user_id": "new-user-uuid"
}
```

### 사용자 정보 수정
기존 사용자 정보를 수정합니다.

**PUT** `/api/users/{user_id}`

#### 요청 본문
```json
{
  "name": "김철수",
  "birthdate": "1990-01-15",
  "gender": "남성",
  "address": "서울시 서초구"
}
```

#### 응답
```json
{
  "success": true,
  "message": "사용자 정보가 업데이트되었습니다."
}
```

### 사용자 삭제
사용자를 삭제합니다.

**DELETE** `/api/users/{user_id}`

#### 응답
```json
{
  "success": true,
  "message": "사용자가 삭제되었습니다."
}
```

---

## 스토어 API

### 스토어 목록 조회
등록된 스토어 목록을 조회합니다.

**GET** `/api/stores`

#### 쿼리 파라미터
| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| page | integer | 1 | 페이지 번호 |
| count | integer | 10 | 페이지당 항목 수 |
| orderby | string | id | 정렬 기준 (id, name, type) |

#### 응답 예시
```json
{
  "stores": [
    {
      "id": "store-uuid-1",
      "type": "카페",
      "name": "스타벅스 강남점",
      "address": "서울시 강남구 테헤란로 123",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total_count": 1
}
```

### 스토어 상세 조회
특정 스토어의 상세 정보를 조회합니다.

**GET** `/api/stores/{store_id}`

---

## 주문 API

### 주문 목록 조회
주문 목록을 조회합니다.

**GET** `/api/orders`

#### 쿼리 파라미터
| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| page | integer | 1 | 페이지 번호 |
| count | integer | 10 | 페이지당 항목 수 |
| user_id | string | - | 특정 사용자의 주문만 조회 |
| store_id | string | - | 특정 스토어의 주문만 조회 |

#### 응답 예시
```json
{
  "orders": [
    {
      "id": "order-uuid-1",
      "ordertime": "2024-01-15T09:30:00",
      "store_id": "store-uuid-1",
      "user_id": "user-uuid-1",
      "created_at": "2024-01-15T09:30:00"
    }
  ],
  "total_count": 1
}
```

### 주문 생성
새로운 주문을 생성합니다.

**POST** `/api/orders`

#### 요청 본문
```json
{
  "store_id": "store-uuid-1",
  "user_id": "user-uuid-1",
  "items": [
    {
      "item_id": "item-uuid-1",
      "quantity": 2
    },
    {
      "item_id": "item-uuid-2",
      "quantity": 1
    }
  ]
}
```

---

## 아이템 API

### 아이템 목록 조회
등록된 아이템 목록을 조회합니다.

**GET** `/api/items`

#### 쿼리 파라미터
| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| page | integer | 1 | 페이지 번호 |
| count | integer | 10 | 페이지당 항목 수 |
| type | string | - | 아이템 타입 필터 |

#### 응답 예시
```json
{
  "items": [
    {
      "id": "item-uuid-1",
      "type": "음료",
      "name": "아메리카노",
      "price": 4500,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total_count": 1
}
```

---

## 키오스크 API

### 스토어 타입 조회
키오스크에서 사용할 스토어 타입을 조회합니다.

**GET** `/api/kiosk/store-types`

#### 응답 예시
```json
{
  "store_types": ["카페", "패스트푸드", "베이커리"]
}
```

---

## 에러 응답

### 일반적인 에러 형식
```json
{
  "success": false,
  "error": "error_code",
  "message": "에러 메시지"
}
```

### HTTP 상태 코드
- **200 OK**: 요청 성공
- **201 Created**: 리소스 생성 성공
- **400 Bad Request**: 잘못된 요청
- **401 Unauthorized**: 인증 필요
- **403 Forbidden**: 권한 없음
- **404 Not Found**: 리소스를 찾을 수 없음
- **500 Internal Server Error**: 서버 내부 오류

---

## 사용 예시

### 사용자 생성 및 주문 과정
```bash
# 1. 사용자 생성
curl -X POST http://localhost:5000/signup \
  -F "name=김철수" \
  -F "birthdate=1990-01-15" \
  -F "gender=남성" \
  -F "address=서울시 강남구"

# 2. 스토어 목록 조회
curl -X GET http://localhost:5000/api/stores

# 3. 아이템 목록 조회
curl -X GET http://localhost:5000/api/items

# 4. 주문 생성
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "store-uuid-1",
    "user_id": "user-uuid-1",
    "items": [
      {"item_id": "item-uuid-1", "quantity": 2}
    ]
  }'
```

---

## 데이터 모델

### User (사용자)
```typescript
interface User {
  id: string;          // UUID
  name: string;        // 이름
  birthdate: string;   // 생년월일 (YYYY-MM-DD)
  age: number;         // 나이
  gender: string;      // 성별
  address?: string;    // 주소 (선택사항)
  created_at: string;  // 생성일시 (ISO 8601)
  updated_at: string;  // 수정일시 (ISO 8601)
}
```

### Store (스토어)
```typescript
interface Store {
  id: string;          // UUID
  type: string;        // 스토어 타입
  name: string;        // 스토어 이름
  address: string;     // 주소
  created_at: string;  // 생성일시
  updated_at: string;  // 수정일시
}
```

### Item (아이템)
```typescript
interface Item {
  id: string;          // UUID
  type: string;        // 아이템 타입
  name: string;        // 아이템 이름
  price: number;       // 가격
  created_at: string;  // 생성일시
  updated_at: string;  // 수정일시
}
```

### Order (주문)
```typescript
interface Order {
  id: string;          // UUID
  ordertime: string;   // 주문일시 (ISO 8601)
  store_id: string;    // 스토어 ID
  user_id: string;     // 사용자 ID
  created_at: string;  // 생성일시
}
```

### OrderItem (주문 아이템)
```typescript
interface OrderItem {
  id: string;          // UUID
  order_id: string;    // 주문 ID
  item_id: string;     // 아이템 ID
  quantity: number;    // 수량
  created_at: string;  // 생성일시
}
```