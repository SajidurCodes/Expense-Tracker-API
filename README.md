# Expense Tracker API 💰

A secure and production-ready **Expense Tracker REST API** built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. The API provides JWT-based authentication, user-specific transaction management, filtering, validation, and automated testing with Pytest.

---

## 🌐 Live Demo

The Expense Tracker API is deployed and available online:

**Live API:** [Click Here](https://expense-tracker-api-32tc.onrender.com/)

**API Documentation:** [Swagger UI](https://expense-tracker-api-32tc.onrender.com/docs)




## 🚀 Features

- 🔐 JWT authentication
- 👤 User registration and login
- 🔒 Password hashing with bcrypt
- 💰 Income and expense management
- ➕ Create transactions
- 📋 Get all personal transactions
- 🔎 Get a transaction by ID
- ✏️ Update transactions
- 🗑️ Delete transactions
- 🔍 Filter transactions by:
  - Transaction type
  - Category
  - Minimum amount
  - Maximum amount
- 👥 User-based transaction ownership
- ✅ Pydantic request validation
- 🗄️ PostgreSQL database with SQLAlchemy ORM
- 🧪 Pytest API testing
- 📖 Interactive Swagger API documentation
- ☁️ Render deployment support

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework and REST API |
| **Python** | Backend programming language |
| **SQLAlchemy** | ORM and database interaction |
| **PostgreSQL** | Relational database |
| **Neon** | Hosted PostgreSQL database |
| **Pydantic** | Data validation |
| **JWT** | Authentication |
| **bcrypt** | Password hashing |
| **Pytest** | Automated testing |
| **Render** | Cloud deployment |

---

## 📁 Project Structure

```text
expense-tracker-api/
│
├── router/
│   ├── __init__.py
│   ├── auth.py
│   └── transactions.py
│
├── test/
│   ├── __init__.py
│   └── test_main.py
│
├── database.py
├── models.py
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/expense-tracker-api.git
cd expense-tracker-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```


---



### User

| Field | Type | Description |
|------|------|-------------|
| `id` | Integer | Primary key |
| `username` | String | Unique username |
| `email` | String | User email |
| `hash_password` | String | Hashed password |

### Transaction

| Field | Type | Description |
|------|------|-------------|
| `id` | Integer | Primary key |
| `title` | String | Transaction title |
| `amount` | Float | Transaction amount |
| `type` | String | `income` or `expense` |
| `category` | String | Transaction category |
| `date` | Date | Transaction date |
| `owner_id` | Integer | ID of the user who owns the transaction |

---

## ▶️ Running the Application

Start the development server with:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---



# 🔑 Authentication

The API uses **JWT Bearer Authentication**.

### Register

```http
POST /auth/register
```

Request:

```json
{
  "username": "sajid",
  "email": "sajid@example.com",
  "password": "123456"
}
```

### Login

```http
POST /auth/login
```

The login endpoint returns:

```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

Use the returned token in protected requests:

```http
Authorization: Bearer YOUR_TOKEN
```

---

# 💳 Transaction API

All transaction endpoints require JWT authentication.

## Create Transaction

```http
POST /transactions
```

Request:

```json
{
  "title": "Lunch",
  "amount": 250,
  "type": "expense",
  "category": "Food",
  "date": "2026-08-26"
}
```

The authenticated user's ID is automatically assigned as `owner_id`.

---

## Get All Transactions

```http
GET /transactions
```

Returns only transactions belonging to the authenticated user.

---

## Get Transaction by ID

```http
GET /transactions/{transaction_id}
```

Example:

```http
GET /transactions/1
```

Users cannot access transactions belonging to other users.

---

## Update Transaction

```http
PUT /transactions/{transaction_id}
```

Example:

```json
{
  "amount": 350,
  "category": "Restaurant"
}
```

Only the fields included in the request are updated.

---

## Delete Transaction

```http
DELETE /transactions/{transaction_id}
```

Example:

```http
DELETE /transactions/1
```

Response:

```json
{
  "message": "Transaction deleted successfully"
}
```

---

# 🔍 Transaction Filtering

Transactions can be filtered using query parameters.

### Filter by type

```http
GET /transactions/filter?type=expense
```

### Filter by category

```http
GET /transactions/filter?category=Food
```

### Filter by amount range

```http
GET /transactions/filter?minimum_amount=100&maximum_amount=5000
```

### Combine filters

```http
GET /transactions/filter?type=expense&category=Food
```

Available query parameters:

| Parameter | Example |
|-----------|---------|
| `type` | `expense` |
| `category` | `Food` |
| `minimum_amount` | `100` |
| `maximum_amount` | `5000` |

---

# ✅ Validation

The API validates incoming request data using **Pydantic**.

Examples:

- Transaction amount must be greater than `0`.
- Transaction type must be either `income` or `expense`.
- Required fields must be provided.
- Update requests allow partial updates.

Invalid requests return appropriate HTTP error responses.

---

# 🧪 Testing

The project includes automated API tests using **Pytest**.

Run all tests:

```bash
pytest
```

The test suite covers:

- Creating a transaction
- Getting all transactions
- Getting a specific transaction
- Updating a transaction
- Deleting a transaction

Expected result:

```text
5 passed
```

Tests use a separate test database so that testing does not modify production PostgreSQL data.

---


# 🔗 API Endpoints

| Method | Endpoint | Authentication | Description |
|--------|----------|----------------|-------------|
| `POST` | `/auth/register` | ❌ | Register a new user |
| `POST` | `/auth/login` | ❌ | Login and receive JWT |
| `POST` | `/transactions` | ✅ | Create transaction |
| `GET` | `/transactions` | ✅ | Get user's transactions |
| `GET` | `/transactions/filter` | ✅ | Filter user's transactions |
| `GET` | `/transactions/{transaction_id}` | ✅ | Get specific transaction |
| `PUT` | `/transactions/{transaction_id}` | ✅ | Update transaction |
| `DELETE` | `/transactions/{transaction_id}` | ✅ | Delete transaction |
| `GET` | `/` | ❌ | API health/root endpoint |

---

