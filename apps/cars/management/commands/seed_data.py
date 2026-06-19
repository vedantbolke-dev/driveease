"""
DriveEase Car Rental System
Management Command: seed_data
Populates the database with sample cars for demo/testing.

Usage: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.cars.models import Car

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with sample cars and admin user for DriveEase'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding DriveEase database...'))

        # ---- Create superadmin ----
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@driveease.com',
                password='Admin@1234',
                first_name='Admin',
                last_name='DriveEase',
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(self.style.SUCCESS('Admin user created: admin / Admin@1234'))
        else:
            self.stdout.write('Admin user already exists.')

        # ---- Sample cars data ----
        sample_cars = [
            # Hatchback
            {
                'name': 'Swift',
                'brand': 'Maruti Suzuki',
                'model_year': 2023,
                'category': 'hatchback',
                'fuel_type': 'petrol',
                'transmission': 'manual',
                'seating_capacity': 5,
                'mileage': '23 km/l',
                'engine_cc': '1197cc',
                'color': 'Red',
                'price_per_day': 1200,
                'description': (
                    'The Maruti Suzuki Swift is one of India\'s most loved hatchbacks. '
                    'Perfect for city drives with excellent fuel efficiency and a sporty design.'
                ),
                'features': 'AC, Power Steering, Power Windows, ABS, Central Locking, Music System, Rear Parking Sensor',
                'is_available': True,
                'is_featured': True,
                'location': 'Newasa, Maharashtra',
            },
            {
                'name': 'Nexon',
                'brand': 'Tata',
                'model_year': 2023,
                'category': 'hatchback',
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seating_capacity': 5,
                'mileage': '17 km/l',
                'engine_cc': '1199cc',
                'color': 'White',
                'price_per_day': 1800,
                'description': (
                    'The Tata Nexon is a sub-compact SUV/hatchback that offers '
                    'a premium feel with modern safety features and a 5-star safety rating.'
                ),
                'features': 'AC, Touchscreen, Reverse Camera, Sunroof, ABS, 6 Airbags, Cruise Control',
                'is_available': True,
                'is_featured': True,
                'location': 'Newasa, Maharashtra',
            },
            # Sedan
            {
                'name': 'City',
                'brand': 'Honda',
                'model_year': 2023,
                'category': 'sedan',
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seating_capacity': 5,
                'mileage': '18 km/l',
                'engine_cc': '1498cc',
                'color': 'Silver',
                'price_per_day': 2200,
                'description': (
                    'The Honda City is a premium mid-size sedan known for its '
                    'refined driving experience, spacious cabin, and excellent reliability.'
                ),
                'features': 'AC, 8-inch Touchscreen, Android Auto, Apple CarPlay, Lane Watch, ABS, 6 Airbags, Sunroof',
                'is_available': True,
                'is_featured': True,
                'location': 'Newasa, Maharashtra',
            },
            # SUV
            {
                'name': 'Creta',
                'brand': 'Hyundai',
                'model_year': 2024,
                'category': 'suv',
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seating_capacity': 5,
                'mileage': '16 km/l',
                'engine_cc': '1482cc',
                'color': 'Blue',
                'price_per_day': 2800,
                'description': (
                    'The Hyundai Creta is India\'s most popular compact SUV. '
                    'With a bold design, panoramic sunroof, and ADAS features, '
                    'it offers a premium driving experience.'
                ),
                'features': 'Panoramic Sunroof, ADAS, Ventilated Seats, 360 Camera, Wireless Charger, AC, 8 Airbags',
                'is_available': True,
                'is_featured': True,
                'location': 'Newasa, Maharashtra',
            },
            {
                'name': 'Scorpio-N',
                'brand': 'Mahindra',
                'model_year': 2023,
                'category': 'suv',
                'fuel_type': 'diesel',
                'transmission': 'manual',
                'seating_capacity': 7,
                'mileage': '15 km/l',
                'engine_cc': '2184cc',
                'color': 'Black',
                'price_per_day': 3200,
                'description': (
                    'The Mahindra Scorpio-N is a true-blue SUV with powerful road presence, '
                    '7-seater configuration, and off-road capability. Perfect for group trips.'
                ),
                'features': 'AC, 8-inch Infotainment, 4WD, ABS, 6 Airbags, Sunroof, Terrain Modes',
                'is_available': True,
                'is_featured': False,
                'location': 'Newasa, Maharashtra',
            },
            {
                'name': 'Fortuner',
                'brand': 'Toyota',
                'model_year': 2023,
                'category': 'suv',
                'fuel_type': 'diesel',
                'transmission': 'automatic',
                'seating_capacity': 7,
                'mileage': '14 km/l',
                'engine_cc': '2755cc',
                'color': 'White Pearl',
                'price_per_day': 5500,
                'description': (
                    'The Toyota Fortuner is the benchmark SUV in India. '
                    'Known for its legendary reliability, 4WD capability, and '
                    'premium 7-seater comfort for long journeys.'
                ),
                'features': 'AC, 9-inch Touchscreen, 4WD, Crawl Control, 7 Airbags, Sunroof, Ambient Lighting',
                'is_available': True,
                'is_featured': True,
                'location': 'Newasa, Maharashtra',
            },
            {
                'name': 'Thar',
                'brand': 'Mahindra',
                'model_year': 2023,
                'category': 'suv',
                'fuel_type': 'diesel',
                'transmission': 'manual',
                'seating_capacity': 4,
                'mileage': '15 km/l',
                'engine_cc': '2184cc',
                'color': 'Rocky Beige',
                'price_per_day': 3500,
                'description': (
                    'The Mahindra Thar is an iconic 4WD off-roader. '
                    'Perfect for adventure seekers who want to explore rugged terrains '
                    'and experience thrilling drives.'
                ),
                'features': 'AC, 4WD, Soft Top/Hard Top, Rock Mode, Touchscreen, 2 Airbags, Waterproof Interior',
                'is_available': True,
                'is_featured': True,
                'location': 'Newasa, Maharashtra',
            },
            # Luxury
            {
                'name': 'Z4 sDrive',
                'brand': 'BMW',
                'model_year': 2023,
                'category': 'luxury',
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seating_capacity': 2,
                'mileage': '12 km/l',
                'engine_cc': '1998cc',
                'color': 'Misano Blue',
                'price_per_day': 12000,
                'description': (
                    'The BMW Z4 is a premium roadster that combines thrilling performance '
                    'with open-air driving excitement. Perfect for a special occasion or '
                    'unforgettable drive.'
                ),
                'features': 'Retractable Roof, BMW Live Cockpit, Harman Kardon Sound, Sport Mode, Parking Assist, AC',
                'is_available': True,
                'is_featured': True,
                'location': 'Newasa, Maharashtra',
            },
            {
                'name': 'Innova Crysta',
                'brand': 'Toyota',
                'model_year': 2023,
                'category': 'luxury',
                'fuel_type': 'diesel',
                'transmission': 'automatic',
                'seating_capacity': 7,
                'mileage': '15 km/l',
                'engine_cc': '2393cc',
                'color': 'Super White',
                'price_per_day': 4500,
                'description': (
                    'The Toyota Innova Crysta is India\'s most trusted premium MPV. '
                    'With captain seats, premium interiors, and rock-solid reliability, '
                    'it\'s perfect for family trips and corporate travel.'
                ),
                'features': 'Captain Seats, Automatic Climate Control, Touch Infotainment, Rear AC, 7 Airbags, Sunroof',
                'is_available': True,
                'is_featured': True,
                'location': 'Newasa, Maharashtra',
            },
        ]

        # Insert cars if they don't already exist
        created_count = 0
        for car_data in sample_cars:
            car, created = Car.objects.get_or_create(
                name=car_data['name'],
                brand=car_data['brand'],
                defaults=car_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Added: {car.brand} {car.name}')
            else:
                self.stdout.write(f'  - Already exists: {car.brand} {car.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {created_count} new cars added.'
        ))
        self.stdout.write(self.style.SUCCESS(
            '\nAdmin Login:\n  URL: http://127.0.0.1:8000/dashboard/\n'
            '  Username: admin\n  Password: Admin@1234'
        ))
