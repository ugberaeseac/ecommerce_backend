from django.core.management.base import BaseCommand
from apps.products.models import Category, Product
from decimal import Decimal
import random
import uuid

class Command(BaseCommand):
    help = "Seed the database with real African categories and products"

    def handle(self, *args, **kwargs):
        # Clear old data
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Category: name -> description (optional, for clarity)
        categories = {
            "African Fashion": "Traditional and modern African wear including Ankara, Dashiki, and Kente.",
            "Agricultural Produce": "Organic farm produce from across African regions.",
            "Art & Crafts": "Handmade African crafts, masks, carvings, and beads.",
            "Beauty & Skincare": "Natural African skin and hair products like shea butter and black soap.",
            "Herbal Medicine": "Natural remedies, roots, and herbs used in traditional African medicine.",
            "African Cuisine": "Staple food items like yam flour, palm oil, dried fish, and suya spice.",
            "Home Decor": "Cultural home items like raffia mats, sculptures, and wooden utensils.",
            "Electronics": "Locally assembled electronics and gadgets.",
            "Books & Literature": "African novels, history books, and educational content.",
            "Footwear": "Leather sandals, slippers, and shoes made by African cobblers.",
            "Textiles & Fabrics": "Handwoven African textiles like Aso Oke and Kitenge.",
            "African Jewelry": "Beads, bracelets, and bangles made from local materials.",
            "Toys & Games": "Traditional African toys, board games, and puzzles.",
            "Furniture": "Locally made furniture using indigenous wood.",
            "Music & Instruments": "Drums, shekeres, kalimbas, and African musical CDs.",
            "Livestock & Poultry": "Goats, chickens, and livestock-related products.",
            "Construction Materials": "Cement, roofing sheets, and locally made bricks.",
            "Local Beverages": "Zobo, palm wine, kunu, and other African drinks.",
            "Mobile Accessories": "Affordable accessories for mobile phones.",
            "Handbags & Accessories": "African handbags, purses, and fashion items."
        }

        created_categories = {}

        for name, desc in categories.items():
            category = Category.objects.create(name=name)
            created_categories[name] = category

        # Products per category
        products = [
            ("Ankara Gown", "African Fashion", "Beautifully tailored Ankara gown suitable for events.", 7500),
            ("Yam Tubers", "Agricultural Produce", "Freshly harvested tubers of yam from Benue.", 3500),
            ("Shea Butter 500ml", "Beauty & Skincare", "Raw unrefined shea butter from Ghana.", 1200),
            ("Dried Catfish (1kg)", "African Cuisine", "Well-dried catfish for soups and sauces.", 4500),
            ("Ayo Game Set", "Toys & Games", "Traditional Yoruba board game made from quality wood.", 3000),
            ("Leather Sandals", "Footwear", "Handmade leather sandals from Aba.", 5500),
            ("Black Soap Bar", "Beauty & Skincare", "Organic African black soap for skin care.", 1000),
            ("Kente Fabric", "Textiles & Fabrics", "Traditional handwoven fabric from Ghana.", 8000),
            ("Zobo Drink (1L)", "Local Beverages", "Healthy hibiscus drink spiced with ginger and pineapple.", 700),
            ("Palm Oil 5L", "African Cuisine", "Red palm oil freshly extracted from local farms.", 2500),
            ("Djembe Drum", "Music & Instruments", "Hand-carved djembe with authentic skin head.", 15000),
            ("Beaded Necklace Set", "African Jewelry", "Handcrafted colorful bead set from Nigeria.", 3500),
            ("Efo Riro Seasoning", "African Cuisine", "Blend of local spices for rich vegetable soup.", 1000),
            ("African Carving (Mask)", "Art & Crafts", "Wooden mask representing cultural heritage.", 6000),
            ("Solar Lantern", "Electronics", "Rechargeable solar lantern with phone charging support.", 8000),
            ("Leather Handbag", "Handbags & Accessories", "Elegant African-designed leather handbag.", 6500),
            ("Palm Wine (2L)", "Local Beverages", "Freshly tapped palm wine from Eastern Nigeria.", 900),
            ("Aso Oke Cap", "Textiles & Fabrics", "Handwoven traditional cap for special occasions.", 2500),
            ("African History Book", "Books & Literature", "A deep dive into African kingdoms and empires.", 4500),
            ("Goat (1 year)", "Livestock & Poultry", "Healthy male goat ready for rearing or meat.", 28000)
        ]

        for name, category_name, description, price in products:
            Product.objects.create(
                name=name,
                description=description,
                price=Decimal(price),
                stock=random.randint(0, 15),
                category=created_categories[category_name]
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded 20 categories and multiple African products."))
