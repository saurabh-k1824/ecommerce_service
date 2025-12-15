
from decimal import Decimal

from django.core.management.base import BaseCommand
from categories.models import Category
from products.models import Product


class Command(BaseCommand):
    help = "Seed initial products for all categories"

    def handle(self, *args, **options):
        PRODUCT_DATA = {
            "Mobiles": [
                ("iPhone 14", "Apple smartphone with A15 chip", 69999, 50),
                ("Samsung Galaxy S23", "Samsung flagship smartphone", 74999, 40),
                ("OnePlus 12", "OnePlus flagship device", 64999, 35),
                ("Google Pixel 8", "Pixel phone with AI camera", 71999, 30),
                ("Xiaomi 13 Pro", "High-end Xiaomi smartphone", 59999, 45),
            ],
            "Laptops": [
                ("MacBook Air M2", "Apple M2 ultrabook", 114999, 20),
                ("Dell XPS 13", "Premium Windows ultrabook", 99999, 15),
                ("HP Spectre x360", "Convertible laptop", 104999, 18),
                ("Lenovo ThinkPad X1", "Business-class laptop", 109999, 12),
                ("Asus ZenBook 14", "Lightweight ultrabook", 89999, 25),
            ],
            "Electronics": [
                ("Sony WH-1000XM5", "Noise-cancelling headphones", 29999, 35),
                ("JBL Charge 5", "Portable Bluetooth speaker", 14999, 60),
                ("Amazon Echo Dot", "Smart speaker with Alexa", 4999, 80),
                ("Apple AirPods Pro", "Wireless earbuds with ANC", 24999, 40),
                ("Logitech MX Master 3", "Advanced wireless mouse", 9999, 55),
            ],
            "Home Appliances": [
                ("LG Washing Machine", "Front load washing machine", 35999, 10),
                ("Samsung Refrigerator", "Double door refrigerator", 42999, 8),
                ("Philips Air Fryer", "Healthy air fryer", 12999, 25),
                ("IFB Microwave Oven", "Convection microwave oven", 18999, 12),
                ("Dyson Vacuum Cleaner", "Cordless vacuum cleaner", 49999, 6),
            ],
            "Fashion": [
                ("Nike Running Shoes", "Men running shoes", 7999, 70),
                ("Levi's Jeans", "Slim fit denim jeans", 3999, 90),
                ("Adidas Hoodie", "Comfortable sports hoodie", 4999, 60),
                ("Ray-Ban Sunglasses", "UV-protected sunglasses", 8999, 40),
                ("Puma T-Shirt", "Cotton casual t-shirt", 1999, 100),
            ],
            "Watches": [
                ("Apple Watch Series 9", "Smartwatch with health tracking", 41999, 20),
                ("Samsung Galaxy Watch 6", "Android smartwatch", 36999, 22),
                ("Fossil Gen 6", "Stylish smartwatch", 28999, 18),
                ("Casio G-Shock", "Rugged digital watch", 9999, 50),
                ("Titan Analog Watch", "Classic analog watch", 6999, 65),
            ],
            "Earphones": [
                ("Boat Airdopes 141", "Wireless earbuds", 1499, 120),
                ("Sony WF-1000XM4", "Premium noise-cancelling earbuds", 19999, 30),
                ("Realme Buds Air 5", "Affordable ANC earbuds", 3999, 70),
                ("JBL Tune 230NC", "Bass-focused earbuds", 5999, 55),
                ("Apple EarPods", "Wired earphones", 1999, 80),
            ],
            "Televisions": [
                ("Samsung 55\" Smart TV", "4K UHD Smart TV", 52999, 14),
                ("LG OLED 48\"", "OLED display television", 89999, 7),
                ("Sony Bravia 50\"", "Premium Android TV", 64999, 10),
                ("Mi 43\" Smart TV", "Budget smart television", 32999, 20),
                ("OnePlus 65\" TV", "Large screen smart TV", 74999, 6),
            ],
            "Furniture": [
                ("Wooden Study Table", "Solid wood study table", 15999, 12),
                ("Office Chair", "Ergonomic office chair", 8999, 25),
                ("3-Seater Sofa", "Comfortable fabric sofa", 35999, 5),
                ("Queen Size Bed", "Wooden bed frame", 42999, 4),
                ("Bookshelf", "5-tier wooden bookshelf", 7999, 18),
            ]
        }

        created_count = 0

        for category_name, products in PRODUCT_DATA.items():
            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Category '{category_name}' not found. Skipping.")
                )
                continue

            for name, desc, price, inventory in products:
                Product.objects.create(
                    category=category,
                    name=name,
                    description=desc,
                    price=Decimal(price),
                    inventory=inventory,
                )
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Inserted {created_count} products successfully.")
        )
