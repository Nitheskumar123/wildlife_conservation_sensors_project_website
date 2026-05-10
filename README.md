# Wildlife Conservation Sensors Project Website

![Status](https://img.shields.io/badge/Status-Active%20Development-blue)
![Language](https://img.shields.io/badge/Language-HTML%2059.4%25%20%7C%20Python%2032%25%20%7C%20CSS%208.6%25-brightgreen)
![Framework](https://img.shields.io/badge/Framework-Django%205.0.7-green)
![Database](https://img.shields.io/badge/Database-MySQL-blue)
![License](https://img.shields.io/badge/License-MIT-blue)

A comprehensive web application for wildlife conservation sensor data management, monitoring, and tracking. This platform integrates IoT sensor technology with a full-featured web interface for real-time wildlife monitoring, user management, and payment integration.

## 🌍 Project Overview

The Wildlife Conservation Sensors Project Website is designed to:
- **Monitor Wildlife Habitats** - Track animal movement and environmental conditions using IoT sensors
- **Manage Sensor Data** - Collect and visualize real-time sensor data from conservation sites
- **User Authentication** - Secure user registration with OTP verification via email
- **Payment Processing** - Razorpay integration for donations and subscriptions
- **Dashboard Analytics** - Real-time monitoring of sensor readings and pressure data
- **Animal Tracking** - Track and monitor animal movements in conservation areas

## 🎯 Key Features

### User Management
- ✅ **User Registration & Authentication** - Email-based signup with custom user model
- ✅ **OTP Verification** - Email-based OTP verification for account security
- ✅ **User Profiles** - Complete user profile management with contact information
- ✅ **Password Security** - Django's built-in password validation and hashing
- ✅ **Profile Updates** - Edit user information (email, username, address, location)

### Sensor Data Management
- ✅ **Real-time Sensor Data** - API endpoint for retrieving sensor readings
- ✅ **Pressure Monitoring** - Track pressure sensor data for environmental monitoring
- ✅ **Location Tracking** - GPS coordinates stored for sensor device locations
- ✅ **Data Visualization** - Dashboard with sensor data charts and analytics
- ✅ **CSV Export** - Export sensor data to CSV format for analysis

### Wildlife Tracking
- ✅ **Animal Tracking** - Monitor animal movements and behavior patterns
- ✅ **Device Location Mapping** - Map sensors to physical locations with coordinates
- ✅ **Activity Logs** - Track conservation activities and interventions

### Payment Integration
- ✅ **Razorpay Integration** - Secure payment gateway for donations
- ✅ **Booking System** - Reserve wildlife tours or conservation activities
- ✅ **Transaction Management** - Secure payment processing

### Web Interface
- ✅ **Responsive Design** - Mobile-friendly Bootstrap 5 interface
- ✅ **3D Visualization** - Spline 3D designs for immersive experience
- ✅ **Modern Navigation** - Boxicons for icon library
- ✅ **Beautiful UI/UX** - Custom CSS styling with animations

## 📋 Tech Stack

### Backend
- **Framework**: Django 5.0.7
- **Language**: Python 3.x
- **Database**: MySQL
- **Admin Panel**: Jazzmin (Django admin enhancement)
- **Email**: SMTP via Gmail
- **Payment Gateway**: Razorpay API

### Frontend
- **HTML**: 59.4% of codebase
- **CSS**: 8.6% of codebase (custom + Bootstrap 5)
- **Bootstrap**: Bootstrap 5.2.3 for responsive design
- **Icons**: Boxicons 2.1.4
- **3D Graphics**: Spline Design for interactive 3D

### Features & Libraries
- **Authentication**: Django built-in + custom user model
- **Email**: Django email backend with SMTP
- **Security**: CSRF protection, password validation
- **API**: Django REST API endpoints

## 📁 Project Structure

```
wildlife_conservation_sensors_project_website/
├── manage.py                          # Django management utility
├── requirements.txt                   # Python dependencies
│
├── myapp/                             # Main Django project
│   ├── settings.py                    # Django settings & configuration
│   ├── urls.py                        # Main URL routing
│   ├── wsgi.py                        # WSGI application
│   └── asgi.py                        # ASGI application
│
├── resfinal/                          # Main application
│   ├── models.py                      # Database models
│   │   ├── CustomUser                 # Extended user model with email
│   │   ├── OtpToken                   # OTP management model
│   │   ├── Profile                    # User profile model
│   │   └── DeviceLocation             # Sensor device location tracking
│   │
│   ├── views.py                       # View logic & API handlers
│   │   ├── index()                    # Homepage
│   │   ├── signup()                   # User registration
│   │   ├── verify_email()             # OTP verification
│   │   ├── signin()                   # Login
│   │   ├── logout_page()              # Logout
│   │   ├── profile()                  # User profile view
│   │   ├── update_profile()           # Update profile
│   │   ├── dashboard()                # Sensor data dashboard
│   │   ├── pressure()                 # Pressure data view
│   │   ├── animal()                   # Animal tracking
│   │   ├── about()                    # About page
│   │   ├── contact()                  # Contact page
│   │   └── get_sensor_data()          # API endpoint
│   │
│   ├── urls.py                        # App URL routing
│   ├── forms.py                       # Django forms
│   │   ├── RegisterForm               # User registration form
│   │   ├── UpdateProfileForm          # Profile update form
│   │   └── BookingForm                # Tour/activity booking
│   │
│   ├── static/                        # Static files
│   │   └── resfinal.css               # Custom CSS
│   │
│   └── templates/                     # HTML templates
│       ├── base.html                  # Base template
│       ├── index.html                 # Homepage template
│       ├── navbar.html                # Navigation bar
│       └── [other templates]
│
├── templates/                         # Project-level templates
│   ├── index.html                     # Homepage
│   ├── base.html                      # Base layout
│   ├── navbar.html                    # Header/navigation
│   └── [other pages]
│
├── bin/                               # Binary files
├── csv_outputs/                       # Exported CSV data
└── db/                                # Database files
```

## 🗄️ Database Models

### CustomUser Model
Extended Django user model with email-based authentication:
```python
- email: Unique email field
- username: Username field
- password: Hashed password
- is_active, is_staff, is_superuser: Permission flags
```

### OtpToken Model
Manages OTP verification for user registration:
```python
- user: ForeignKey to CustomUser
- otp_code: 6-digit OTP code
- tp_created_at: Creation timestamp
- otp_expires_at: Expiration timestamp
```

### Profile Model
Extended user profile information:
```python
- user: OneToOneField to CustomUser
- phone: Contact number
- address: Street address
- city: City name
- state: State/Province
- country: Country name
- pincode: Postal code
- created_at: Profile creation date
```

### DeviceLocation Model
Tracks sensor device locations:
```python
- user: ForeignKey to CustomUser
- latitude: GPS latitude coordinate
- longitude: GPS longitude coordinate
- timestamp: Last update time
```

## 📍 API Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|-----------------|
| GET | `/` | Homepage | No |
| GET/POST | `/register` | User registration | No |
| GET/POST | `/verify-email/<username>` | Email OTP verification | No |
| POST | `/resend-otp` | Resend OTP code | Yes |
| GET/POST | `/login` | User login | No |
| GET | `/logout` | User logout | Yes |
| GET | `/profile` | View user profile | Yes |
| POST | `/profile/update` | Update profile | Yes |
| GET | `/about` | About page | No |
| GET | `/dashboard` | Sensor data dashboard | Yes |
| GET | `/pressure` | Pressure data view | Yes |
| GET | `/animal` | Animal tracking view | Yes |
| GET | `/api/sensor-data/` | Get sensor data (API) | Yes |

## 🔧 Configuration

### Django Settings (myapp/settings.py)

**Database Configuration:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'resfinal',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
```

**Email Configuration:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
EMAIL_USE_TLS = True
```

**Razorpay Configuration:**
```python
RAZORPAY_KEY_ID = 'your_razorpay_key_id'
RAZORPAY_KEY_SECRET = 'your_razorpay_secret'
```

**Installed Apps:**
- `jazzmin` - Enhanced Django admin interface
- `django.contrib.admin` - Django admin
- `django.contrib.auth` - Authentication
- `django.contrib.contenttypes` - Content types
- `django.contrib.sessions` - Sessions
- `django.contrib.messages` - Messages framework
- `django.contrib.staticfiles` - Static files
- `resfinal` - Main application

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- Git
- Virtual Environment (recommended)

### Step 1: Clone Repository
```bash
git clone https://github.com/Nitheskumar123/wildlife_conservation_sensors_project_website.git
cd wildlife_conservation_sensors_project_website
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database

**Create MySQL Database:**
```sql
CREATE DATABASE resfinal;
```

**Update settings.py with your credentials:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'resfinal',
        'USER': 'root',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Collect Static Files
```bash
python manage.py collectstatic
```

### Step 8: Configure Email (Gmail)

1. Enable 2-Factor Authentication on Gmail
2. Generate App Password
3. Update in settings.py:
```python
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'  # 16-character password
```

### Step 9: Configure Razorpay

1. Sign up at [Razorpay Dashboard](https://dashboard.razorpay.com)
2. Get your API keys
3. Update in settings.py

### Step 10: Run Development Server
```bash
python manage.py runserver
```

Visit: `http://localhost:8000`

## 📦 Dependencies

Key Python packages (from requirements.txt):
- Django 5.0.7
- mysqlclient - MySQL database driver
- django-jazzmin - Admin interface enhancement
- razorpay - Razorpay payment integration
- python-decouple - Environment variables
- requests - HTTP library
- pillow - Image processing

## 🔐 Security Features

- **Email-based OTP** - Secure two-factor authentication
- **Password Hashing** - Django's PBKDF2 password hashing
- **CSRF Protection** - Cross-site request forgery protection
- **SQL Injection Prevention** - Django ORM prevents SQL injection
- **XSS Protection** - Template auto-escaping
- **Secure Session Management** - HTTP-only cookies

### ⚠️ Security Notes
- Change `SECRET_KEY` before production
- Set `DEBUG = False` in production
- Use environment variables for sensitive data
- Update `ALLOWED_HOSTS` for production domain
- Use HTTPS in production

## 📊 Language Composition

- **HTML**: 59.4% - Frontend templates and structure
- **Python**: 32% - Backend logic and business logic
- **CSS**: 8.6% - Styling and animations

## 🎨 Frontend Technologies

- **Bootstrap 5.2.3** - Responsive CSS framework
- **Boxicons** - Icon library with 2500+ icons
- **Spline Design** - 3D interactive graphics
- **Custom CSS** - Additional styling and animations
- **Django Templates** - Backend template rendering

## 📝 Key Pages

### Public Pages
- **Home** - Animated landing page with Spline 3D forest scene
- **About** - Project information and mission
- **Contact** - Get in touch form
- **Navbar** - Logo "ELYSIAN" with responsive navigation

### Authenticated Pages
- **Dashboard** - Real-time sensor data visualization
- **Pressure View** - Pressure sensor readings and analytics
- **Animal Tracking** - Monitor animal movements and behavior
- **Profile** - View and update user information
- **Update Profile** - Edit contact and location details

## 🚧 Project Status

**Current Phase**: Active Development ✅

**Completed Features:**
- ✅ User authentication system
- ✅ OTP email verification
- ✅ Profile management
- ✅ Database models for sensors and tracking
- ✅ Basic dashboard UI
- ✅ Razorpay payment integration
- ✅ Responsive web design

**In Development:**
- 🔄 Advanced sensor data analytics
- 🔄 Real-time data visualization charts
- 🔄 Animal behavior analysis
- 🔄 Report generation

**Planned Features:**
- 📋 Mobile app for field researchers
- 📋 IoT sensor firmware
- 📋 Machine learning for animal detection
- 📋 Multi-language support
- 📋 Advanced GIS mapping

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 📝 Coding Standards

- Follow PEP 8 for Python code
- Use descriptive variable names
- Add comments for complex logic
- Write docstrings for functions and classes
- Keep functions focused and small

## 🐛 Known Issues

- [ ] Static file paths need optimization for production
- [ ] Email templates need styling enhancement
- [ ] Real-time data updates need WebSocket implementation
- [ ] Mobile responsiveness improvements needed
- [ ] API rate limiting needs implementation

## 📧 Contact & Support

- **Email**: nithes262004@gmail.com
- **WhatsApp**: +91 9025152341
- **GitHub Issues**: [Report Bug](https://github.com/Nitheskumar123/wildlife_conservation_sensors_project_website/issues)

## 📚 Resources & Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Razorpay Integration Guide](https://razorpay.com/docs/)
- [Boxicons](https://boxicons.com/)
- [Spline Design](https://spline.design/)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django Framework community
- Bootstrap for responsive design
- Razorpay for payment integration
- Spline for 3D visualization
- All contributors and supporters

## 📈 Project Statistics

- **Repository Created**: August 6, 2025
- **Latest Update**: August 6, 2025
- **File Size**: ~18.5 MB
- **Language**: HTML (59.4%), Python (32%), CSS (8.6%)
- **Framework**: Django 5.0.7
- **Database**: MySQL

---

**Status**: 🚀 Active Development - Contributing to Wildlife Conservation

For more information, visit the [GitHub Repository](https://github.com/Nitheskumar123/wildlife_conservation_sensors_project_website)
