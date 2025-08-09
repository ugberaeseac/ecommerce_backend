# E-commerce Backend

This project is a Django REST Framework-based backend for an e-commerce platform, featuring product management, cart, and order handling with authentication and role-based access.

---

## ERD (Entity Relationship Diagram)
![ERD](https://i.postimg.cc/BbGYnRtz/ERdiagram-ecommerce-backend.png)

---

## Technologies Used
- Python 3.10+
- Django 4.x
- Django REST Framework
- PostgreSQL
- Render (deployment)
- JWT Authentication (SimpleJWT)
- drf-spectacular (Swagger/OpenAPI Documentation)
- unittest for testing

---

## Features Implemented
- User authentication & registration
- Product listing, retrieval, creation, update, and deletion
- Product search, filtering, sorting and ordering.
- Category management
- Cart operations (add, remove, list items, checkout)
- Order creation and listing
- Role-based access for admin and regular users
- API documentation with Swagger and Postman collection
- Unit tests for core functionalities

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- PostgreSQL
- pipenv / virtualenv (recommended)

### Steps
```bash
# Clone repository
git clone https://github.com/ugberaeseac/ecommerce_backend.git
cd ecommerce_backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  


# Install dependencies
pip install -r requirements.txt


# Create .env file and configure environment variables
touch .env

DJANGO_SECRET_KEY="<your secret key>"

DB_HOST="<your database host>"
DB_USER="<your database user>"
DB_PASS="<your database password>"
DB_NAME="<your database name>"
DB_PORT="<your database port>"

ALLOWED_HOSTS="Your allowed hosts seperated by whitespace" # "127.0.0.1 localhost"


# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## Implemented API Endpoints

### Authentication
**Register**
```http
POST /api/auth/signup/
```
Request:
```json
{
  "username": "devCharles",
  "email": "devcharles@demo.com",
  "password": "pass1234"
}
```
Response:
```json
{
  "id": 1,
  "username": "devCharles",
  "email": "devcharles@demo.com"
}
```

**Login**
```http
POST /api/auth/login/
```
Request:
```json
{
  "email": "devcharles@demo.com",
  "password": "pass1234"
}
```
Response:
```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

---

### Products
**List Products**
```http
GET /api/products/
```

**Retrieve Product**
```http
GET /api/products/{product_id}/
```

**Create Product** *(Admin only)*
```http
POST /api/products/
```

---

### Cart
**View My Cart**
```http
GET /api/cart/my-cart/
```

**Add Item to Cart**
```http
POST /api/cart/items/
```
Request:
```json
{
  "product": "product-uuid",
  "quantity": 2
}
```

---

### Orders
**List My Orders**
```http
GET /api/orders/
```

**Retrieve Order**
```http
GET /api/orders/{order_id}/
```

---

## API Documentation
- **Swagger UI**: [https://ecommerce-backend-ga7o.onrender.com/api/schema/swagger-ui/](https://ecommerce-backend-ga7o.onrender.com/api/schema/swagger-ui/)
- **ReDoc**: [https://ecommerce-backend-ga7o.onrender.com/api/schema/redoc/](https://ecommerce-backend-ga7o.onrender.com/api/schema/redoc/)
- **Postman Collection**: [postman](postman)

---

## Assumptions & Design Decisions
- All authenticated users can create carts; one cart per user at a time.
- Products must belong to a category.
- Orders are created from the authenticated user’s cart upon checkout.
- Quantity in cart items must be greater than 0.

---

## Future Improvements
- Payment gateway integration (Stripe/PayPal).
- Inventory management with stock tracking.
- Email notifications on order status updates.
- Improved error handling and validation messages.

---
