# Python Recruitment Test


---

## **User Management**
This module should handle user registration, authentication, and profile management.

### **Endpoints**

#### **User Registration**
**Request:**
```http
POST /api/register
```
**Request Body Example:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response Example:**
```json
{
    "message": "User registered successfully",
    "user_id": 1
}
```

#### **User Login**
**Request:**
```http
POST /api/login
```
**Request Body Example:**
```json
{
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response Example:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

#### **Get User Profile**
**Request:**
```http
GET /api/profile
Authorization: Bearer <JWT Token>
```
**Response Example:**
```json
{
    "user_id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2025-03-12T08:30:00"
}
```

---

## **Financial Transactions**
This module should handle secure transactions, balance management, and transaction history.

### **Endpoints**

#### **Create a Transaction**
**Request:**
```http
POST /api/transactions
Authorization: Bearer <JWT Token>
```
**Request Body Example:**
```json
{
    "amount": 100.50,
    "currency": "USD",
    "transaction_type": "deposit",
    "recipient_id": 2
}
```

**Response Example:**
```json
{
    "transaction_id": 42,
    "status": "success"
}
```

#### **Get Transaction History**
**Request:**
```http
GET /api/transactions
Authorization: Bearer <JWT Token>
```

**Response Example:**
```json
[
    {
        "transaction_id": 42,
        "amount": 100.50,
        "currency": "USD",
        "transaction_type": "deposit",
        "recipient_id": 2,
        "timestamp": "2025-03-12T10:15:30"
    },
    {
        "transaction_id": 43,
        "amount": -50.00,
        "currency": "USD",
        "transaction_type": "withdrawal",
        "recipient_id": null,
        "timestamp": "2025-03-12T11:00:00"
    }
]
```

#### **Get User Balance**
**Request:**
```http
GET /api/balance
Authorization: Bearer <JWT Token>
```

**Response Example:**
```json
{
    "user_id": 1,
    "balance": 250.75,
    "currency": "USD"
}
```

---