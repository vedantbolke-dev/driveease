-- ============================================================
-- DriveEase Car Rental System - MySQL Database Schema
-- Project: DriveEase Car Rental System
-- Developed by: Vedant Rajendra Bolke & Vishal Rajendra Hapse
-- College: Shri Dnyaneshwar Mahavidyalaya, Newasa
-- Academic Year: 2025-2026
-- ============================================================

-- Step 1: Create the database
CREATE DATABASE IF NOT EXISTS driveease_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE driveease_db;

-- ============================================================
-- Note: Django handles table creation automatically via migrations.
-- The schema below is for reference / documentation purposes.
-- Run: python manage.py migrate  (to auto-create all tables)
-- ============================================================

-- Table: users_customuser (Extended Django User)
-- Fields: id, username, first_name, last_name, email, password,
--         phone_number, address, city, state, pincode,
--         profile_picture, driving_license, is_blocked,
--         is_staff, is_superuser, is_active,
--         date_joined, created_at, updated_at

-- Table: cars_car
-- Fields: id, name, brand, model_year, category, fuel_type,
--         transmission, seating_capacity, mileage, engine_cc,
--         color, price_per_day, description, features,
--         image, is_available, is_featured, location,
--         created_at, updated_at

-- Table: bookings_booking
-- Fields: id, user_id (FK → users_customuser),
--         car_id (FK → cars_car),
--         pickup_date, return_date, pickup_location, drop_location,
--         total_days, price_per_day, total_cost, status,
--         special_requests, admin_notes,
--         created_at, updated_at

-- ============================================================
-- FOREIGN KEY RELATIONSHIPS:
-- bookings_booking.user_id → users_customuser.id (CASCADE DELETE)
-- bookings_booking.car_id  → cars_car.id          (CASCADE DELETE)
-- ============================================================

-- Verify tables after migration:
SHOW TABLES;
