# Setup untuk Cron Job (Linux/Mac) atau Task Scheduler (Windows)

## Linux/Mac (menggunakan crontab):

# Jalankan perintah berikut untuk membuka crontab editor:
# crontab -e

# Tambahkan baris berikut untuk menjalankan expire_subscriptions setiap hari jam 00:00:
# 0 0 * * * cd /path/to/your/coursecraft && python manage.py expire_subscriptions

# Atau untuk menjalankan setiap jam:
# 0 * * * * cd /path/to/your/coursecraft && python manage.py expire_subscriptions


## Windows (menggunakan Task Scheduler):

# 1. Buka Task Scheduler (taskschd.msc)
# 2. Klik "Create Basic Task..."
# 3. Masukkan nama: "CourseCraft Expire Subscriptions"
# 4. Pilih "Daily" untuk frekuensi
# 5. Set waktu yang diinginkan (misal: 00:00)
# 6. Pilih "Start a program"
# 7. Program/script: python
# 8. Arguments: manage.py expire_subscriptions
# 9. Start in: C:\Kuliah\Project\coursecraft (path ke folder project)


## Alternatif: Menjalankan manual untuk testing

# Untuk test command secara manual:
# python manage.py expire_subscriptions


## Menggunakan Django APScheduler (Rekomendasi untuk development)

# Install package:
# pip install apscheduler django-apscheduler

# Kemudian tambahkan job di settings.py atau buat management command khusus
