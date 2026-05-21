# Billing System - Student Course Registration & Automatic Invoice Generation

A comprehensive Django-based billing system for student course registration with automatic PDF bill generation, MySQL database, email notifications, and admin dashboard.

## 🎯 Features

✅ **Student Registration & Authentication**
- User registration with email verification
- Student profile management
- Secure token-based authentication

✅ **Course Management**
- Browse available courses
- Course catalog with filtering and search
- Course pricing and duration information

✅ **Online Course Enrollment**
- One-click course enrollment
- Enrollment status tracking
- Course capacity management

✅ **Online Payment Processing**
- Mock payment gateway (ready for Stripe/PayPal integration)
- Multiple payment methods support
- Transaction tracking and history

✅ **Automatic Bill Generation**
- Automatic PDF bill creation upon successful payment
- Bill numbering system
- Tax calculation and itemization

✅ **Email Notifications**
- Enrollment confirmation emails
- Payment confirmation emails
- Automatic bill delivery via email
- Email status tracking

✅ **Admin Dashboard**
- Comprehensive Django admin interface
- Student management
- Course management
- Enrollment tracking
- Payment processing
- Bill generation and tracking

✅ **Student Portal**
- View enrolled courses
- Track payment status
- Download invoices
- View billing history
- Request invoice resend

## 🛠 Technology Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: MySQL 8.0
- **PDF Generation**: ReportLab
- **Email**: Django Email Backend (Console/SMTP)
- **Authentication**: Token-based Authentication
- **API Documentation**: Swagger/ReDoc (drf-spectacular)

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)
- Virtual Environment (recommended)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
cd /path/to/your/project
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Edit `.env` file with your MySQL credentials:

```env
DB_NAME=billing_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

Create MySQL database:

```bash
# Connect to MySQL
mysql -u root -p

# Create database
CREATE DATABASE billing_db;
CREATE USER 'billing_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON billing_db.* TO 'billing_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configure Email (Optional)

For development, emails are printed to console. For production, update `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Create Sample Data (Optional)

```bash
# Create sample courses
python manage.py shell

# Inside shell:
from billing_app.models import Course

courses = [
    {
        'title': 'Python Basics',
        'code': 'PY101',
        'description': 'Learn Python fundamentals',
        'level': 'beginner',
        'price': 99.99,
        'duration_weeks': 12,
        'instructor': 'John Smith',
        'max_students': 50
    },
    {
        'title': 'Django Web Development',
        'code': 'DJG201',
        'description': 'Build web applications with Django',
        'level': 'intermediate',
        'price': 149.99,
        'duration_weeks': 16,
        'instructor': 'Jane Doe',
        'max_students': 30
    },
]

for course_data in courses:
    Course.objects.create(**course_data)

exit()
```

### 9. Run Development Server

```bash
python manage.py runserver
```

Server will start at: `http://localhost:8000`

## 🚀 Deploying to Render

This project is ready for Render deployment.

1. Push your code to GitHub (`main` branch).
2. Create a new Web Service on Render.
3. Connect your GitHub repository and select the `main` branch.
4. Use the following settings:
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn billing_project.wsgi:application`
   - Plan: `Free`
5. Add environment variables in Render:
   - `SECRET_KEY` — a strong secret key
   - `DEBUG` — `False`
   - `ALLOWED_HOSTS` — your Render hostname (for example `billing-system.onrender.com`)
   - `DATABASE_URL` — provided by Render Postgres if you add a managed database
   - `EMAIL_BACKEND` — `django.core.mail.backends.smtp.EmailBackend` or console backend for testing
   - `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`

If you want Render to manage a database for you, create a free PostgreSQL database service and set `DATABASE_URL` from the generated connection string.

You can also use the included `render.yaml` file to configure the Render service automatically.

## �📚 API Endpoints

### Authentication

- `POST /api/auth/token/` - Get authentication token
- `POST /api/students/register/` - Register new student
- `GET /api/students/profile/` - Get student profile
- `PUT /api/students/update_profile/` - Update student profile

### Courses

- `GET /api/courses/` - List all courses
- `GET /api/courses/{id}/` - Get course details
- `GET /api/courses/?level=beginner&search=python` - Filter courses

### Enrollments

- `GET /api/enrollments/` - List student's enrollments
- `POST /api/enrollments/` - Enroll in course
- `GET /api/enrollments/{id}/` - Get enrollment details
- `GET /api/enrollments/?status=active` - Filter enrollments

### Payments

- `GET /api/payments/` - List student's payments
- `POST /api/payments/` - Process payment (auto-generates bill)
- `GET /api/payments/{id}/` - Get payment details

### Bills

- `GET /api/bills/` - List student's bills
- `GET /api/bills/{id}/` - Get bill details
- `GET /api/bills/{id}/download_pdf/` - Download bill as PDF
- `POST /api/bills/{id}/send_email/` - Send bill via email

## 🔒 Authentication

### Get Authentication Token

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'
```

### Use Token in API Requests

```bash
curl -H "Authorization: Token YOUR_TOKEN_HERE" \
  http://localhost:8000/api/courses/
```

## 📖 API Documentation

Visit the following URLs to explore the API:

- **Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://localhost:8000/api/schema/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

## 👨‍💼 Admin Dashboard

Visit `http://localhost:8000/admin/` with superuser credentials to:

- Manage courses
- View student registrations
- Track enrollments
- Monitor payments
- Generate and send bills
- View email delivery status

## 📧 Email Workflow

### Bill Generation & Email

1. Student enrolls in course
2. Student processes payment online
3. Payment is verified and marked as "completed"
4. Bill is automatically generated with:
   - Course details
   - Amount with tax calculation
   - Student information
5. PDF bill is created using ReportLab
6. Bill is automatically sent to student's email with PDF attachment
7. Email delivery status is tracked

### Email Templates

Located in `templates/emails/`:
- `bill.html` - HTML email template for invoices

## 🔄 Workflow Example

### 1. Register as Student

```bash
curl -X POST http://localhost:8000/api/students/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password123",
    "password2": "secure_password123",
    "first_name": "John",
    "last_name": "Doe",
    "student_id": "STU001"
  }'
```

### 2. Get Courses

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/courses/
```

### 3. Enroll in Course

```bash
curl -X POST http://localhost:8000/api/enrollments/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"course_id": 1}'
```

### 4. Process Payment (Auto-generates Bill)

```bash
curl -X POST http://localhost:8000/api/payments/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "enrollment_id": 1,
    "payment_method": "credit_card"
  }'
```

Response includes: Payment confirmation + Bill generation + Email sent notification

### 5. Download Bill PDF

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/bills/1/download_pdf/ \
  -o bill.pdf
```

## 📁 Project Structure

```
billing_project/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── .github/
│   └── copilot-instructions.md  # Project documentation
├── billing_project/          # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI config
│   └── asgi.py              # ASGI config
├── billing_app/             # Main application
│   ├── models.py            # Database models
│   ├── views.py             # API views
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── signals.py           # Django signals
│   ├── utils/               # Utility modules
│   │   ├── pdf_generator.py    # PDF bill generation
│   │   ├── email_sender.py     # Email notifications
│   │   └── payment_gateway.py  # Payment processing
│   └── migrations/          # Database migrations
├── templates/
│   └── emails/
│       └── bill.html        # Email template
└── static/                  # Static files (CSS, JS, images)
```

## 🔧 Configuration

### PDF Generation

ReportLab is used for PDF generation. Configuration in `billing_app/utils/pdf_generator.py`:

```python
# Customize bill styling
doc = SimpleDocTemplate(buffer, pagesize=letter, ...)
```

### Email Configuration

Update `.env` for different email providers:

**Gmail:**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

**Outlook:**
```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
```

## 🚀 Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn billing_project.wsgi --workers 4 --bind 0.0.0.0:8000
```

### Using Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /static {
        alias /path/to/project/static;
    }
    
    location /media {
        alias /path/to/project/media;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

### Environment Settings for Production

```env
DEBUG=False
SECRET_KEY=your-strong-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Use `.env.example` instead
2. **Set DEBUG=False** in production
3. **Use strong SECRET_KEY** - Generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
4. **Enable HTTPS** - Use SSL certificates
5. **Validate user input** - All serializers include validation
6. **SQL Injection Prevention** - Django ORM prevents SQL injection
7. **CSRF Protection** - Enabled by default

## 🐛 Troubleshooting

### Issue: MySQL Connection Error

```bash
# Check MySQL service
# Windows
mysql -u root -p

# Create database if doesn't exist
CREATE DATABASE billing_db;

# Update .env with correct credentials
```

### Issue: Email Not Sending

```python
# Check email backend in settings.py
# For development, change to:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Emails will print to console
```

### Issue: PDF Generation Error

```bash
# Ensure reportlab is installed
pip install reportlab --upgrade

# Check media directory permissions
```

## 📝 Common Tasks

### Backup Database

```bash
mysqldump -u root -p billing_db > backup.sql
```

### Restore Database

```bash
mysql -u root -p billing_db < backup.sql
```

### Reset Database

```bash
python manage.py flush  # WARNING: Deletes all data!
python manage.py migrate
```

### Clear Old Bills

```bash
python manage.py shell

# Inside shell:
from billing_app.models import Bill
from datetime import timedelta
from django.utils import timezone

old_bills = Bill.objects.filter(bill_date__lt=timezone.now() - timedelta(days=365))
old_bills.delete()
```

## 🚦 Integration Roadmap

- [ ] Stripe payment gateway integration
- [ ] PayPal payment gateway integration
- [ ] Razorpay integration
- [ ] Student dashboard frontend
- [ ] Admin analytics dashboard
- [ ] SMS notifications
- [ ] Invoice customization
- [ ] Bulk bill generation
- [ ] Payment reminders
- [ ] Late payment penalties

## 📞 Support & Documentation

For detailed API documentation, visit:
- `http://localhost:8000/api/schema/swagger-ui/`
- `http://localhost:8000/api/schema/redoc/`

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please follow the existing code style and include tests for new features.

## ✨ Credits

Built with Django, Django REST Framework, and ReportLab.

---

**Happy billing! 🎓📄**
