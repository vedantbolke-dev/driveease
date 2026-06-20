# 🌐 Deploying DriveEase to PythonAnywhere (Free Plan)

This guide provides step-by-step instructions to deploy the **DriveEase Car Rental Management System** onto [PythonAnywhere](https://www.pythonanywhere.com/) using the completely free Beginner tier.

---

## 🛠️ Step-by-Step Deployment Guide

### Step 1: Clone the Project and Set Up the Virtual Environment

1. Log in to your [PythonAnywhere Dashboard](https://www.pythonanywhere.com/user-dashboard/).
2. Go to the **Consoles** tab and start a new **Bash Console**.
3. Clone your repository:
   ```bash
   git clone https://github.com/vedantbolke-dev/driveease.git
   cd driveease
   ```
4. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
5. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

### Step 2: Create the Environment File (`.env`)

1. While inside the `driveease/` directory in the Bash Console, run:
   ```bash
   nano .env
   ```
2. Paste the following configuration (replace `YOUR_USERNAME` with your actual PythonAnywhere username):
   ```env
   # Security Key (Keep this secret)
   SECRET_KEY=f_vlg2ucm=yoys22wy0*a0x6o6ucu4+24s8dmba9kfjjhfl)55

   # Production Safety
   DEBUG=False

   # Database Settings (Using free SQLite database for free tier)
   USE_SQLITE=True
   ```
3. Press `CTRL+O`, then `Enter` to save, and `CTRL+X` to exit nano.

---

### Step 3: Run Migrations and Prepare Data

1. Run the database migrations to set up the SQLite database:
   ```bash
   python manage.py migrate
   ```
2. Collect static files for production styling:
   ```bash
   python manage.py collectstatic --noinput
   ```
3. Seed the database with default cars and an admin user:
   ```bash
   python manage.py seed_data
   ```

---

### Step 4: Configure the Web App

1. Go back to your PythonAnywhere Dashboard and click the **Web** tab.
2. Click **Add a new web app**.
3. Choose **Manual configuration** (do not select Django here; manual config gives complete control).
4. Choose **Python 3.10** as the version.
5. Once created, configure the following fields on the Web tab page:

#### 📂 Code Configuration
* **Source code**: `/home/YOUR_USERNAME/driveease`
* **Working directory**: `/home/YOUR_USERNAME/driveease`

#### 🐍 Virtualenv Configuration
* **Virtualenv**: `/home/YOUR_USERNAME/driveease/venv`

---

### Step 5: Edit the WSGI Configuration File

1. On the **Web** tab under **Code**, click the link next to **WSGI configuration file**.
2. Delete everything in the editor and paste the following:
   ```python
   import os
   import sys

   # Add project directory to sys.path
   path = '/home/YOUR_USERNAME/driveease'
   if path not in sys.path:
       sys.path.append(path)

   # Set settings module
   os.environ['DJANGO_SETTINGS_MODULE'] = 'driveease.settings'

   # Load WSGI application
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
3. Replace `YOUR_USERNAME` with your actual PythonAnywhere username (e.g. `vedantbolke123`).
4. Click **Save** in the top right.

---

### Step 6: Configure Static & Media Paths

1. Go back to the **Web** tab.
2. Scroll down to the **Static files** section.
3. Add the following two paths:

| URL | Directory |
|---|---|
| `/static/` | `/home/YOUR_USERNAME/driveease/staticfiles` |
| `/media/` | `/home/YOUR_USERNAME/driveease/media` |

*(Replace `YOUR_USERNAME` with your actual username, e.g. `vedantbolke123`).*

---

### Step 7: Reload and Test!

1. Scroll to the top of the **Web** tab and click **Reload yourwebpage.pythonanywhere.com**.
2. Visit `https://yourusername.pythonanywhere.com` in your browser.
3. Log in to the Admin Panel:
   * **URL**: `https://yourusername.pythonanywhere.com/dashboard/`
   * **Username**: `admin`
   * **Password**: `Admin@1234`
