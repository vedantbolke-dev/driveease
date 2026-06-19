# DriveEase Car Rental System

**Final Year Project** | B.Sc. Computer Science
**Developed by:** Vedant Rajendra Bolke & Vishal Rajendra Hapse
**College:** Shri Dnyaneshwar Mahavidyalaya, Newasa
**Academic Year:** 2025–2026
**Guide:** Prof. Jagtap S. G

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.x, Django 4.2 |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Database | MySQL |
| Charts | Chart.js |
| Icons | Bootstrap Icons |
| Config | python-decouple (.env) |

---

## Project Structure

```
driveease/               ← project root (run manage.py from here)
├── manage.py
├── .env.example         ← copy to .env and fill in credentials
├── requirements.txt
├── README.md
├── driveease/           ← Django settings package
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                ← all application code lives here
│   ├── users/           ← custom user model, auth, profile
│   ├── cars/            ← car listings, search, seed data
│   ├── bookings/        ← booking creation, cancellation
│   └── dashboard/       ← admin analytics dashboard
├── templates/           ← HTML templates
├── static/              ← CSS, JS, images
└── media/               ← user-uploaded files
```

---

## Project Setup Instructions

### Step 1: Prerequisites

Make sure you have installed:
- Python 3.10 or higher
- MySQL Server (XAMPP or standalone)
- pip (Python package manager)

---

### Step 2: Extract the Project

```bash
cd driveease
```

---

### Step 3: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

---

### Step 4: Install Requirements

```bash
pip install -r requirements.txt
```

> **Windows note:** If `mysqlclient` fails to build, either:
> - Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/), OR
> - Replace `mysqlclient` with `PyMySQL` in requirements.txt and add to settings.py:
>   ```python
>   import pymysql; pymysql.install_as_MySQLdb()
>   ```

---

### Step 5: Configure Environment Variables

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env` and set your MySQL password:
```
DB_NAME=driveease_db
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=3306
```

---

### Step 6: Create MySQL Database

Open MySQL / phpMyAdmin and run:
```sql
CREATE DATABASE driveease_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

### Step 7: Run Django Migrations

```bash
python manage.py makemigrations users cars bookings
python manage.py migrate
```

---

### Step 8: Seed Sample Data

```bash
python manage.py seed_data
```

This creates:
- ✅ 9 sample cars (all categories)
- ✅ Admin user: `admin` / `Admin@1234`

---

### Step 9: Run the Development Server

```bash
python manage.py runserver
```

Open in browser: **http://127.0.0.1:8000**

---

## Admin Access

After running `python manage.py seed_data`, an admin account is created automatically.
Use the admin dashboard at `/dashboard/` or Django admin at `/admin/`.

---

## Project Pages

| Page | URL |
|------|-----|
| Home | / |
| Car Listing | /cars/ |
| Car Detail | /cars/\<id\>/ |
| Register | /users/register/ |
| Login | /users/login/ |
| User Dashboard | /users/dashboard/ |
| Admin Dashboard | /dashboard/ |
| About Us | /about/ |
| Contact | /contact/ |

---

## Features

### User Features
- Register, Login, Logout
- Browse cars with filters (category, price, fuel type, transmission)
- View full car details and specifications
- Book a car (pick & return date with auto cost calculation)
- Booking date-overlap prevention (no double-booking)
- Booking status tracking
- Cancel pending/confirmed bookings
- Profile management with driving license field

### Admin Features
- Analytics dashboard with Chart.js (revenue, bookings, popular cars)
- Add / Edit / Delete cars with image upload
- Mark cars as featured (shown on homepage)
- Manage booking status (Approve / Reject / Complete)
- Block / Unblock / Delete users
- Revenue analytics (last 6 months)

---

## Copyright

© 2026 DriveEase Car Rental System. All rights reserved.
Developed by Vedant Rajendra Bolke & Vishal Rajendra Hapse
B.Sc. Computer Science | Shri Dnyaneshwar Mahavidyalaya, Newasa
