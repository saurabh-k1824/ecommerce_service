# E-commerce REST API
*(Django REST Framework | OAuth 2.0 Concepts)*
Note: For testing purpose pushed the .env and .sqlite3 file in github

---

## 1. Overview

This project is a production-style E-commerce REST API built using Django REST Framework, implementing OAuth 2.0 concepts with JWT, scope-based authorization, and strict business rules.

The system models a real-world marketplace with two clearly defined user roles:

User Roles
Role	Description
ADMIN (Seller)	Manages categories, products, users, and order status
USER (Customer / Buyer)	Browses products and creates/manages own orders

Important Business Rule
Admins (Sellers) cannot create orders.
Only Normal Users (Customers) are allowed to place orders.

The API manages:
- Authentication & Users
- Categories
- Products
- Orders

### Key Features
- OAuth 2.0 concepts using JWT (access & refresh tokens)
- Scope-based authorization
- Role-based access control (Admin vs User)
- Strict business rules
- Pagination & filtering
- Prometheus-compatible metrics
- Clean separation of concerns
- Comprehensive API tests using APITestCase

---

## 2. Tech Stack

- Python 
- Django 
- Django REST Framework
- JWT (OAuth 2.0 concepts with scopes)
- Postgres 
- Prometheus Python Client
- Swagger / OpenAPI
- Django Test Framework (APITestCase)

---

## 3. Project Structure

ecommerce_service/

├── auth_service/

├── users/

├── categories/

├── products/

├── orders/

├── ecommerce_service/

│ ├── common/

│ ├── middleware/

│ ├── metrics.py

│ ├── settings.py

│ └── urls.py



### Architecture Principles
- **Models** → database schema
- **Serializers** → validation
- **Services** → business logic
- **Views / ViewSets** → API layer
- **Middleware** → authentication & metrics

### Initial Seed Data (For Testing)

During project setup, seed data is automatically inserted into the database to make testing easier.

Seeded Users
Role	Email	Password
Admin (Seller)	user@admin.com	Qwerty@12345
User (Customer)	user@gmail.com	Qwerty@12345
User (Customer)	user2@gmail.com	Qwerty@12345
Seeded Data Includes

3 Users (1 Admin, 2 Normal Users)

Multiple Categories

Multiple Products linked to categories
---

## 4. Setup Instructions

### 4.1 Clone Repository
git clone <repository-url>
cd ecommerce_service

### 4.2 Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activat

### 4.3 Install Dependencies
pip install -r requirements.txt

### 4.4 Run Migrations
python manage.py migrate

### 4.5 Create Admin User
python manage.py createsuperuser

### 4.6 Start Server
python manage.py runserver

## 5. Authentication & Authorization
### 5.1 Authentication

JWT-based authentication

OAuth 2.0 concepts:

Access token

Refresh token

Scopes

### 5.2 Roles

ADMIN – Full access (cannot create orders)

USER – Can manage only own orders


### 6. Sample OAuth 2.0 Credentials (Testing)
## Admin User
{
  "email": "user@admin.com",
  "password": "Qwerty@12345"
}

## Normal User
{
  "email": "user@gmail.com",
  "password": "Qwerty@12345"
}

## 7. Authentication APIs
### Login
POST /api/auth/login/

### Authorization Header
Authorization: Bearer <access_token>


## 8. Scope-Based Authorization

| Scope            | Description                |
| ---------------- | -------------------------- |
| categories:read  | View categories            |
| categories:write | Manage categories          |
| products:read    | View products              |
| products:write   | Manage products            |
| orders:read      | View orders                |
| orders:write     | Create / cancel own orders |
| orders:admin     | Admin order status updates |
| users:read       | View users                 |
| users:write      | Manage users               |


## 9. API Endpoints
### 9.1 Categories
| Method | Endpoint                              |
| ------ | ------------------------------------- |
| GET    | `/api/categories/`                    |
| POST   | `/api/categories/`                    |
| PATCH  | `/api/categories/{id}/`               |
| DELETE | `/api/categories/{id}/` (soft delete) |
| DELETE | `/api/categories/{id}/hard-delete/`   |

### 9.2 

| Method | Endpoint                            |
| ------ | ----------------------------------- |
| GET    | `/api/products/`                    |
| POST   | `/api/products/`                    |
| PATCH  | `/api/products/{id}/`               |
| DELETE | `/api/products/{id}/` (soft delete) |
| DELETE | `/api/products/{id}/hard-delete/`   |

#### Filtering:
GET /api/products/?category=<category_id>


### 9.3 Orders
| Method | Endpoint                         |
| ------ | -------------------------------- |
| GET    | `/api/orders/`                   |
| POST   | `/api/orders/`                   |
| POST   | `/api/orders/{id}/cancel/`       |
| POST   | `/api/orders/{id}/admin-status/` |

Rules
- Admins cannot create orders
- Users can access only their own orders
- Inventory is validated and updated atomically
- Strict order status transitions enforced

## 10. Pagination & Filtering

### Pagination is mandatory:

GET /api/orders/?page=1&limit=10


### Optional filters:

GET /api/orders/?page=1&limit=10&status=SHIPPED

GET /api/orders/?page=1&limit=10&start_date=2025-01-01&end_date=2025-01-31
