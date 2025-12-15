# users/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import User
from categories.models import Category
from products.models import Product
from django.contrib.auth.hashers import make_password



class Command(BaseCommand):
    help = "Seed initial users, categories, and products"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Seeding initial data...")

        """
        USERS
        """
        admin, created = User.objects.get_or_create(
            email="admin@gmail.com",
            contact_number = "9876543211",
            first_name = "Admin",
            last_name = "K",
            defaults={
                "role": "ADMIN",
                "password": make_password("Qwerty@12345"),
            },
        )
        

        user, created = User.objects.get_or_create(
            email="user@gmail.com",
            first_name = "Customer",
            last_name = "K",
            contact_number = "9876543210",
            defaults={
                "role": "USER",
                "password": make_password("Qwerty@12345"),
            },
        )
        
        user, created = User.objects.get_or_create(
            email="user2@gmail.com",
            first_name = "Customer",
            last_name = "K",
            contact_number = "9876543212",
            defaults={
                "role": "USER",
                "password": make_password("Qwerty@12345"),
            },
        )
        """
        CATEGORIES
        """
        categories_data = [
            ("Mobiles", "Smartphones and accessories"),
            ("Laptops", "Laptops and notebooks"),
            ("Electronics", "Electronic devices"),
        ]

        category_map = {}

        for name, desc in categories_data:
            category, _ = Category.objects.get_or_create(
                name=name,
                defaults={"description": desc},
            )
            category_map[name] = category

        """
        PRODUCTS
        """
        products_data = [
            ("iPhone 14", 69999, 20, "Mobiles"),
            ("Samsung Galaxy S23", 74999, 15, "Mobiles"),
            ("MacBook Air", 119999, 10, "Laptops"),
            ("Dell XPS", 129999, 8, "Laptops"),
        ]

        for name, price, inventory, category_name in products_data:
            Product.objects.get_or_create(
                name=name,
                category=category_map[category_name],
                defaults={
                    "price": price,
                    "inventory": inventory,
                    "description": f"{name} description",
                },
            )

        self.stdout.write(self.style.SUCCESS("Seed data created successfully"))
