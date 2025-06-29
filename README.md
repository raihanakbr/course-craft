# CourseCraft 🎓

**Modern Online Learning Platform with Integrated Payment Gateway**

![CourseCraft Logo](https://img.shields.io/badge/CourseCraft-Learning%20Platform-blue?style=for-the-badge&logo=graduation-cap)

## 🌐 Live Demo
**Website:** [http://34.124.154.40/](http://34.124.154.40/)

---

## 📖 About CourseCraft

CourseCraft adalah platform pembelajaran online modern yang memungkinkan pengguna untuk mengakses kursus premium dengan sistem pembayaran terintegrasi. Platform ini dibangun dengan Django dan menggunakan Xendit sebagai payment gateway untuk memproses pembayaran subscription.

### ✨ Key Features

- 🎥 **Video Streaming** - Sistem streaming video yang smooth dengan progress tracking
- 💳 **Payment Gateway** - Integrasi Xendit untuk berbagai metode pembayaran Indonesia
- 👤 **User Management** - Sistem registrasi, login, dan profile management
- 📊 **Progress Tracking** - Melacak progress pembelajaran user per video
- 🔒 **Premium Content** - Sistem subscription untuk akses konten premium
- 💰 **Flexible Pricing** - Multiple subscription plans (1, 3, 6 bulan)

---

## 💳 Payment Gateway Integration

### Xendit Payment Gateway
CourseCraft menggunakan **Xendit** sebagai payment gateway utama untuk memproses pembayaran subscription di Indonesia.

#### Supported Payment Methods:
- **Virtual Account**: BCA, BNI, BRI, Mandiri, Permata
- **E-Wallet**: OVO, DANA, GoPay, LinkAja, ShopeePay
- **QR Code**: QRIS
- **Retail Outlet**: Indomaret, Alfamart

#### Payment Flow:
1. **Package Selection** - User memilih paket subscription
2. **Payment Method** - User memilih metode pembayaran yang diinginkan
3. **Xendit Processing** - Request dikirim ke Xendit API
4. **Payment Instructions** - User mendapat instruksi pembayaran (VA number, QR code, dll)
5. **Webhook Notification** - Xendit mengirim notifikasi status pembayaran
6. **Subscription Activation** - Sistem mengaktifkan subscription user otomatis

#### Subscription Plans:
```
📦 Paket 1 Bulan
   ├── Harga: Rp 125,000 (diskon 58% dari Rp 300,000)
   ├── Durasi: 30 hari
   └── Features: Akses semua kursus, sertifikat, live session

📦 Paket 3 Bulan (Most Popular)
   ├── Harga: Rp 375,000 (diskon 58% dari Rp 900,000)
   ├── Durasi: 90 hari
   └── Features: Semua fitur + priority support + early access

📦 Paket 6 Bulan
   ├── Harga: Rp 750,000 (diskon 58% dari Rp 1,800,000)
   ├── Durasi: 180 hari
   └── Features: Semua fitur + career mentor + job placement
```

#### Environment Configuration:
```bash
# .env file
XENDIT_SECRET_KEY=xnd_development_xxxxx
XENDIT_PUBLIC_KEY=xnd_public_development_xxxxx
WEBHOOK_VERIFICATION_TOKEN=your_webhook_token
```

---

## 🛠 Technology Stack

### Backend
- **Framework**: Django 5.2.3
- **Database**: SQLite (Development), PostgreSQL (Production Ready)
- **Authentication**: Django's built-in auth system
- **Payment**: Xendit Payment Gateway

### Frontend
- **CSS Framework**: Bootstrap 5.3 + Custom CSS
- **Icons**: Font Awesome 6.0
- **JavaScript**: Vanilla JS for interactivity
- **Video Player**: HTML5 native video player

### Infrastructure
- **Deployment**: Google Cloud Platform (GCP)
- **Web Server**: Django development server
- **Static Files**: Local storage
- **Media Files**: Local storage

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- pip
- Git

### Local Development Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd coursecraft
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install django python-dotenv
   ```

4. **Environment Configuration**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Add your Xendit credentials
   XENDIT_SECRET_KEY=your_xendit_secret_key
   XENDIT_PUBLIC_KEY=your_xendit_public_key
   WEBHOOK_VERIFICATION_TOKEN=your_webhook_token
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py setup_payment_data
   python manage.py populate_courses
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

### Production Deployment

1. **Server Setup**
   ```bash
   # For production on port 80
   sudo python manage.py runserver 0.0.0.0:80
   
   # Or on port 8000 (if port is open)
   python manage.py runserver 0.0.0.0:8000
   ```

2. **Django Settings for Production**
   ```python
   # settings.py
   DEBUG = False
   ALLOWED_HOSTS = ['34.124.154.40', 'your-domain.com']
   ```

---

## 📁 Project Structure

```
coursecraft/
├── coursecraft/           # Django project settings
│   ├── settings.py       # Main configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI configuration
├── main/                 # Main app
│   ├── models.py        # Course, Video, UserProgress models
│   ├── views.py         # Course and video views
│   ├── forms.py         # Custom user forms
│   └── management/      # Django commands
├── payment/              # Payment app
│   ├── models.py        # Subscription, Payment models
│   ├── views.py         # Payment processing views
│   └── management/      # Payment setup commands
├── templates/            # HTML templates
│   ├── main/            # Course templates
│   └── payment/         # Payment templates
├── media/               # User uploaded files
├── .env                 # Environment variables
└── requirements.txt     # Dependencies
```

---

## 🔧 Management Commands

CourseCraft includes several Django management commands for easy setup:

```bash
# Setup payment plans and methods
python manage.py setup_payment_data

# Populate sample courses and videos
python manage.py populate_courses

# Check and expire subscriptions (for cron jobs)
python manage.py expire_subscriptions
```

---

## 🎯 Key Features Breakdown

### 1. Course Management System
- **Course Categories**: Organize courses by subject
- **Video Lessons**: Upload and stream video content
- **Progress Tracking**: Track user completion per video
- **Preview Videos**: Allow free preview of selected videos

### 2. User Authentication & Profiles
- **Custom Registration Form**: Extended user registration
- **Profile Management**: User can update personal information
- **Subscription Status**: Display current subscription details

### 3. Payment Integration
- **Xendit Integration**: Complete payment gateway integration
- **Multiple Payment Methods**: Support for Indonesian payment methods
- **Webhook Handling**: Automatic subscription activation
- **Payment History**: Track all user payments

### 4. Subscription Management
- **Flexible Plans**: Multiple subscription durations
- **Auto Expiration**: Automatic subscription expiry handling
- **Access Control**: Premium content access based on subscription

---

## 🔐 Security Features

- **Environment Variables**: Sensitive data stored in .env
- **CSRF Protection**: Django's built-in CSRF protection
- **Authentication Required**: Protected routes for premium content
- **Payment Security**: Webhook verification for payment callbacks

---

## 📱 Responsive Design

CourseCraft is fully responsive and optimized for:
- 📱 **Mobile Devices** (320px+)
- 📟 **Tablets** (768px+)
- 💻 **Desktop** (1024px+)
- 🖥 **Large Screens** (1400px+)

---

## 🔄 Git Workflow

This project follows conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `chore:` - Maintenance tasks
- `docs:` - Documentation updates

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📞 Support

For technical support or questions:
- **Website**: [http://34.124.154.40/](http://34.124.154.40/)
- **Documentation**: This README
- **Issues**: Create GitHub issue for bugs

---

## 📄 License

This project is proprietary and confidential. All rights reserved.

---

## 🏆 Acknowledgments

- **Django** - Web framework
- **Xendit** - Payment gateway
- **Bootstrap** - CSS framework
- **Font Awesome** - Icons
- **Google Cloud Platform** - Hosting

---

**Made with ❤️ by Muhammad Raihan Akbar**
