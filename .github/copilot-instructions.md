# Billing System Project - Copilot Instructions

## Project Overview
Django-based billing system for student course registration with automatic bill generation, MySQL database, PDF invoice generation, email notifications, and admin dashboard.

## Tech Stack
- Backend: Django + Django REST Framework
- Database: MySQL
- PDF Generation: ReportLab/WeasyPrint
- Email: Django Email Backend
- Payment: Mock payment gateway (to be integrated with Stripe/PayPal later)

## Key Features
- ✓ Student registration & authentication
- ✓ Course catalog management
- ✓ Online payment processing (mock)
- ✓ Automatic bill generation (PDF)
- ✓ Email notifications
- ✓ Admin dashboard
- ✓ Student portal (view courses/invoices)

## Project Completion Status

- [x] Create project structure and configuration files
- [x] Create database models
- [x] Set up Django REST API
- [x] Create bill generation and PDF module
- [x] Set up email notifications
- [x] Configure admin dashboard
- [ ] Install dependencies
- [ ] Create and run development server
- [ ] Verify all features work correctly

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Update `billing_project/settings.py` with your MySQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'billing_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

### 6. Access Admin Dashboard
Visit: http://localhost:8000/admin

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Student registration
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout

### Courses
- `GET /api/courses/` - List all courses
- `GET /api/courses/{id}/` - Course details

### Enrollments
- `POST /api/enrollments/` - Enroll in course
- `GET /api/enrollments/` - Student's enrollments

### Payments & Bills
- `POST /api/payments/` - Process payment (mock)
- `GET /api/bills/` - Student's bills
- `GET /api/bills/{id}/` - Bill details with PDF download
- `POST /api/bills/{id}/send-email/` - Send bill via email

## Directory Structure
```
billing_project/
├── manage.py
├── requirements.txt
├── .env
├── billing_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── billing_app/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   ├── utils/
│   │   ├── pdf_generator.py
│   │   ├── email_sender.py
│   │   └── payment_gateway.py
│   └── migrations/
└── templates/
    └── emails/
        └── bill.html
```

## Environment Variables (.env)
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=billing_db
DB_USER=root
DB_PASSWORD=your_password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Notes for Development
- The payment gateway is mocked for now - integrate Stripe/PayPal later
- Use Django signals to auto-generate bills when payment is successful
- Bills are generated in PDF format and sent via email
- Students can download bills from their portal
