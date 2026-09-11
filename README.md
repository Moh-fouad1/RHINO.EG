# RHINO.EG

A full-stack e-commerce web application built with **Django**, developed as a university project.

RHINO.EG is an online store designed around customizable products, allowing users to browse products, customize orders, upload their own designs, manage a shopping cart, apply promotional codes, and place orders through a complete checkout workflow.

## Features

### Product Catalog

* Browse products by category
* Product search
* Product detail pages
* Featured products
* Latest products
* Product availability management
* Product ratings and reviews
* Related products

### Custom Designs

Users can upload their own designs and customize their order by selecting:

* Paper size: A5, A4, or A3
* Framed or frameless options
* Additional notes

Uploaded designs are automatically connected to the user's cart and order.

### Shopping Cart

* Add products to cart
* Update quantities
* Remove products
* Support for custom-designed products
* Automatic subtotal and total calculation
* Promotional/discount code support

### Promo Codes

The system supports:

* Percentage discounts
* Fixed-amount discounts
* Minimum order requirements
* Maximum usage limits
* Activation/deactivation
* Start and expiration dates
* Automatic discount calculation

### Orders

Users can:

* Complete checkout
* Provide shipping information
* Place orders
* Receive a unique order number
* View individual order details
* Track the order status

Order statuses include:

`Pending → Confirmed → Processing → Shipped → Delivered`

###  User Accounts

* User registration
* Login/logout
* Authenticated checkout
* User-specific carts
* User-specific orders
* Custom design ownership

###  Reviews

Authenticated users can submit product reviews with:

* 1–5 star ratings
* Written comments
* Review approval workflow

##  Tech Stack

**Backend**

* Python
* Django 5.2.5

**Database**

* SQLite for development
* PostgreSQL support for deployment

**Frontend**

* Django Templates
* HTML
* CSS
* JavaScript

**Other Technologies**

* Pillow
* django-widget-tweaks
* Gunicorn
* dj-database-url
* psycopg2

## Project Structure

```text
RHINO.EG/
│
├── cart/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── shop/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── templatetags/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── rhino_eg/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
├── static/
├── media/
├── create_sample_data.py
├── manage.py
├── requirements.txt
└── PAYMENT_SYSTEM_GUIDE.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Moh-fouad1/RHINO.EG.git
cd RHINO.EG
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an admin account

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

##  Sample Data

The project includes:

```text
create_sample_data.py
```

which can be used to populate the application with sample data for development and testing.

## Payment System

The current checkout implementation provides the foundation for order processing and payment-method selection.

Currently implemented:

* Order creation
* Shipping information
* Cart processing
* Promo codes
* Order tracking
* Payment-method selection UI

The payment methods are currently implemented as a development/demo workflow rather than production payment-gateway integrations.

For production deployment, payment gateways such as Paymob, PayTabs, or another appropriate provider would need to be integrated.

See:

```text
PAYMENT_SYSTEM_GUIDE.md
```

for details about the current implementation and planned payment integration.

##  Security

For production deployment, make sure to:

* Use environment variables for secrets
* Disable Django `DEBUG`
* Configure `ALLOWED_HOSTS`
* Use HTTPS
* Protect payment information
* Configure secure database credentials
* Configure proper media/static file handling
* Never store credit-card information directly

##  What I Learned

This project provided practical experience with:

* Django project architecture
* Django models and relationships
* CRUD operations
* Authentication and authorization
* Django forms
* File uploads
* Shopping cart architecture
* Order management
* Promotional pricing logic
* Database design
* Template rendering
* Static and media files
* PostgreSQL configuration
* Production deployment concepts

## Author

**Mohamed Fouad**

GitHub:
https://github.com/Moh-fouad1

---

## License

RHINO.EG is a proprietary project developed for the RHINO.EG startup.

The source code is publicly available for portfolio and demonstration purposes. Commercial use, redistribution, or modification of the project without permission is not permitted.
