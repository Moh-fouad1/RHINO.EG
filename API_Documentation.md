# RHINO.EG API Documentation


**Base URL:** `http://localhost:8000/api/v1/`

## Authentication
The API uses JWT for authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## Endpoints

#### Register User
- **URL:** `POST /api/v1/auth/register/`
- **Description:** Register a new user account

#### Login
- **URL:** `POST /api/v1/auth/login/`
- **Description:** Authenticate user and get JWT tokens

#### Refresh Token
- **URL:** `POST /api/v1/auth/refresh/`
- **Description:** Get new access token using refresh token

#### Verify Token
- **URL:** `POST /api/v1/auth/verify/`
- **Description:** Verify if a token is valid


### Categories

#### List Categories
- **URL:** `GET /api/v1/categories/`
- **Description:** Get all active categories

#### Get Category
- **URL:** `GET /api/v1/categories/{id}/`
- **Description:** Get specific category details

#### Get Category Products
- **URL:** `GET /api/v1/categories/{id}/products/`
- **Description:** Get all products in a specific category

### Products

#### List Products
- **URL:** `GET /api/v1/products/`
- **Description:** Get all active products
- **Query Parameters:**
  - `category`: Filter by category ID
  - `framed`: Filter by framed (true/false)
  - `size`: Filter by size (A5, A4, A3)
  - `featured`: Filter featured products (true/false)
  - `in_stock`: Filter by stock availability (true/false)
  - `search`: Search in name, description, category name
  - `ordering`: Order by name, base_price, rating, created_at, sales_count
 


#### Get Product
- **URL:** `GET /api/v1/products/{id}/`
- **Description:** Get specific product details

#### Featured Products
- **URL:** `GET /api/v1/products/featured/`
- **Description:** Get all featured products

#### Search Products
- **URL:** `GET /api/v1/products/search/?q={query}`
- **Description:** Search products by name, description, or category

#### Add Product to Cart
- **URL:** `POST /api/v1/products/{id}/add_to_cart/`
- **Description:** Add a product to user's cart

### Custom Designs

#### List Custom Designs
- **URL:** `GET /api/v1/custom-designs/`
- **Description:** Get user's custom designs
- **Authentication:** Required

#### Create Custom Design
- **URL:** `POST /api/v1/custom-designs/`
- **Description:** Upload a new custom design
- **Authentication:** Required


#### Add Custom Design to Cart
- **URL:** `POST /api/v1/custom-designs/{id}/add_to_cart/`
- **Description:** Add a custom design to cart

### Reviews

#### List Reviews
- **URL:** `GET /api/v1/reviews/`
- **Description:** Get all approved reviews
- **Query Parameters:**
  - `product`: Filter by product ID
  - `rating`: Filter by rating (1-5)
  - `ordering`: Order by created_at, rating

#### Create Review
- **URL:** `POST /api/v1/reviews/`
- **Description:** Create a new review
- **Authentication:** Required

### Orders

#### List Orders
- **URL:** `GET /api/v1/orders/`
- **Description:** Get user's orders
- **Authentication:** Required
- **Query Parameters:**
  - `status`: Filter by status
  - `ordering`: Order by created_at, total_amount

#### Cancel Order
- **URL:** `POST /api/v1/orders/{id}/cancel/`
- **Description:** Cancel an order (if status is pending or confirmed)

### Promo Codes

#### List Promo Codes
- **URL:** `GET /api/v1/promo-codes/`
- **Description:** Get all active promo codes
- **Authentication:** Required
- **Query Parameters:**
  - `search`: Search in code and description

#### Validate Promo Code
- **URL:** `POST /api/v1/promo-codes/validate/`
- **Description:** Validate a promo code
- **Authentication:** Required
### Cart

#### Get Cart
- **URL:** `GET /api/v1/cart/`
- **Description:** Get user's cart
- **Authentication:** Required

#### Apply Promo Code
- **URL:** `POST /api/v1/cart/apply_promo/`
- **Description:** Apply a promo code to cart
- **Authentication:** Required


#### Checkout
- **URL:** `POST /api/v1/cart/checkout/`
- **Description:** Checkout cart and create order
- **Authentication:** Required

### Cart Items

#### List Cart Items
- **URL:** `GET /api/v1/cart-items/`
- **Description:** Get user's cart items
- **Authentication:** Required

#### Add Cart Item
- **URL:** `POST /api/v1/cart-items/`
- **Description:** Add item to cart
- **Authentication:** Required

#### Update Cart Item Quantity
- **URL:** `POST /api/v1/cart-items/{id}/update_quantity/`
- **Description:** Update cart item quantity
- **Authentication:** Required

## Error Responses

### 400 Bad Request
```json
{
  "error": "Error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

