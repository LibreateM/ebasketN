# 🛒 eBasketN - E-Commerce Platform

A full-featured Django-based e-commerce application with user authentication, product management, shopping cart, wishlist, and order management.

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

---

## ✨ Features

### User Features
- 👤 User Registration & Authentication
- 🔐 Google OAuth 2.0 Integration
- 📧 Email-based Password Reset
- 👥 User Profile Management
- 🔑 Login/Logout Functionality

### Shopping Features
- 🏷️ Product Catalog with Categories
- 🛒 Shopping Cart Management (Add/Remove Items)
- ❤️ Wishlist Management
- 📦 Product Details & Reviews
- 🔍 Product Search Functionality
- ⭐ Product Ratings & Reviews

### Admin Features
- 📊 Admin Dashboard
- ➕ Add/Edit Products & Categories
- 👥 User Management
- 💬 Contact Messages Management
- 📋 Order Management

### Payment & Checkout
- 💳 Multiple Payment Methods (Card, PayPal, Net Banking, COD)
- 📍 Address Management
- 📝 Order Summary
- 🛍️ Order History & Tracking

### Additional Features
- 📧 Email Notifications via Brevo
- 💾 Cloud Storage with Cloudinary
- 📱 Responsive Design (Bootstrap)
- 🔒 Security Features & CSRF Protection
- 📞 Contact Form with Admin Replies
- ❓ FAQ Section

---

## 🛠️ Tech Stack

### Backend
- **Python 3.x**
- **Django 5.2.8** - Web Framework
- **PostgreSQL** - Database
- **Gunicorn** - WSGI Server

### Frontend
- **HTML5 / CSS3**
- **Bootstrap 5** - UI Framework
- **JavaScript** - Interactivity

### External Services
- **Cloudinary** - Media Storage
- **Google OAuth 2.0** - Authentication
- **Brevo** - Email Service

### Deployment
- **Render** - Cloud Hosting
- **WhiteNoise** - Static Files Serving

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip (Python Package Manager)
- Git

### Local Setup

1. **Clone the Repository**
```bash
git clone https://github.com/LibreateM/ebasketN.git
cd ebasketN
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env File**
```bash
cp .env.example .env
```

5. **Configure Environment Variables** (see [Configuration](#configuration))

6. **Run Migrations**
```bash
python manage.py migrate
```

7. **Create Superuser**
```bash
python manage.py createsuperuser
```

8. **Run Development Server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

---

## ⚙️ Configuration

### Required Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ebasketn_db

# Cloudinary (Media Storage)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Google OAuth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-client-id
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-client-secret

# Brevo Email Service
BREVO_API_KEY=your-brevo-api-key
BREVO_EMAIL_USER=your-email@example.com
```

### Cloudinary Setup
1. Create account at [Cloudinary](https://cloudinary.com/)
2. Get your Cloud Name, API Key, and API Secret
3. Add to environment variables

### Google OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 Client ID
3. Add authorized redirect URIs
4. Set credentials in environment variables

### Brevo Email Setup
1. Create account at [Brevo](https://www.brevo.com/)
2. Generate API Key
3. Add to environment variables

---

## 🚀 Usage

### User Registration
1. Visit `/registration/`
2. Fill in user details
3. Verify email

### Browsing Products
1. Go to `/category/` to view all categories
2. Click on category to see products
3. View product details at `/product/<id>/`

### Shopping
1. Click "Add to Cart" on product page
2. Manage cart at `/cart/`
3. Proceed to checkout from cart

### Checkout Process
1. Add/select address at `/address/`
2. Select payment method at `/payment_method/`
3. Review order at `/order_summary/`
4. Place order at `/place-order/`

### Admin Panel
1. Visit `/admin/` 
2. Login with superuser credentials
3. Manage products, categories, users, and orders

---

## 📱 API Endpoints

### Authentication
- `POST /auth/login/` - User login (Google OAuth)
- `POST /logout/` - User logout
- `POST /forgot-password/` - Password reset request
- `POST /reset-password/<token>/` - Confirm password reset

### Products
- `GET /category/` - List all categories
- `GET /product/<id>/` - Product details
- `GET /products/<category_id>/` - Products by category
- `GET /search/` - Search products

### Cart
- `GET /cart/` - View cart
- `POST /add-to-cart/<product_id>/` - Add to cart
- `POST /remove-from-cart/<item_id>/` - Remove from cart

### Wishlist
- `POST /add-wishlist/<product_id>/` - Add to wishlist
- `POST /remove-wishlist/<product_id>/` - Remove from wishlist
- `GET /wish/` - View wishlist

### Orders
- `GET /order_summary/` - Order summary
- `POST /place-order/` - Place order
- `GET /dashboard/` - User dashboard

### Admin
- `GET /dashboard/` - Admin dashboard
- `POST /dashboard/productform/` - Add product
- `POST /dashboard/categoryform/` - Add category
- `GET /dashboard/users/` - Manage users
- `GET /dashboard/contacts/` - View contact messages

---

## 🌐 Deployment on Render

### Prerequisites
- GitHub account
- Render account
- PostgreSQL database (Render or external)
- Cloudinary account

### Steps

1. **Push to GitHub**
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

2. **Connect to Render**
- Go to [Render Dashboard](https://dashboard.render.com/)
- Click "New +" → "Web Service"
- Connect GitHub repository

3. **Configure Build Settings**
- Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
- Start Command: `gunicorn ebasket.wsgi:application`

4. **Set Environment Variables**
In Render Dashboard → Environment:
```
DEBUG=False
DATABASE_URL=your-postgres-url
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=...
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=...
BREVO_API_KEY=...
BREVO_EMAIL_USER=...
SECRET_KEY=generate-random-key
```

5. **Deploy**
- Click "Create Web Service"
- Render will automatically deploy

### Post-Deployment
- Run migrations (if needed)
- Create superuser via Render Shell
- Test all features

---

## 📁 Project Structure

```
ebasketN/
├── ebasket/              # Main project settings
│   ├── settings.py       # Django configuration
│   ├── urls.py           # URL routing
│   ├── wsgi.py           # WSGI configuration
│   └── brevo_backend.py  # Email backend
│
├── eapp/                 # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── urls.py           # App URL routing
│   ├── forms.py          # Django forms
│   └── admin.py          # Admin configuration
│
├── templates/            # HTML templates
│   ├── base.html
│   ├── subpages/         # Individual page templates
│   └── ...
│
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
│
├── requirements.txt      # Python dependencies
├── manage.py             # Django management
├── Dockerfile            # Container configuration
└── README.md             # This file
```

---

## 📊 Database Models

### User Model
- Extends Django User model
- Related to Address, PaymentMethod, Order, Cart, Wish

### Product Model
- name, price, description
- category (ForeignKey to Category)
- image (stored in Cloudinary)
- created, modified timestamps

### Category Model
- name
- image
- created, modified timestamps

### Order Model
- user, total_price, payment_method
- related OrderItems
- created timestamp

### Cart Model
- user, product, quantity
- total_price (computed property)

### Wish Model
- user, product (unique together)
- created_at timestamp

### Address Model
- user, name, email, phone
- address fields
- created, modified timestamps

---

## 🔒 Security Features

- ✅ CSRF Protection enabled
- ✅ Password hashing with Django
- ✅ SQL Injection prevention
- ✅ XSS Protection
- ✅ Secure session management
- ✅ OAuth 2.0 for Google authentication
- ✅ Environment variables for secrets
- ✅ HTTPS in production

---

## 🐛 Troubleshooting

### Images Not Showing
- Verify Cloudinary credentials in environment variables
- Check if media files are uploaded to Cloudinary
- Ensure `DEFAULT_FILE_STORAGE` is set to Cloudinary

### Database Connection Error
- Check `DATABASE_URL` format
- Verify PostgreSQL server is running
- Run migrations: `python manage.py migrate`

### 404 Errors on Static Files
- Run: `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` and `STATIC_URL` settings

### Email Not Sending
- Verify Brevo API key
- Check sender email address
- Test in development with print statements

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push to branch: `git push origin feature/YourFeature`
5. Submit a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📞 Support

For issues, feature requests, or questions:
- Create an issue on GitHub
- Contact: [Your Contact Info]

---

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Framework
- Cloudinary for media hosting
- Google for OAuth
- Brevo for email services

---

**Happy Shopping! 🛍️**

*Last Updated: 2026-04-25*
