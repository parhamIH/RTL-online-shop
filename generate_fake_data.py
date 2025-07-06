#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to generate fake data for the RTL Online Shop models
"""

import os
import sys
import django
from django.core.files.base import ContentFile
from django.utils.text import slugify
from PIL import Image
import io
import random
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from django.contrib.auth.models import User
from shopApp.models import *
from faker import Faker

# Initialize Faker with Persian locale
fake = Faker(['fa_IR'])

def create_fake_image(width=300, height=300, color=None):
    """Create a fake image for testing"""
    if color is None:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    img = Image.new('RGB', (width, height), color)
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return ContentFile(img_io.getvalue(), name=f'fake_image_{random.randint(1000, 9999)}.jpg')

def generate_base_categories():
    """Generate fake base categories"""
    print("Generating Base Categories...")
    
    base_categories_data = [
        {"name": "الکترونیک", "en_name": "electronics", "description": "محصولات الکترونیکی و دیجیتال"},
        {"name": "پوشاک", "en_name": "clothing", "description": "لباس و پوشاک مردانه و زنانه"},
        {"name": "کفش", "en_name": "shoes", "description": "کفش و صندل برای همه سنین"},
        {"name": "لوازم خانگی", "en_name": "home_appliances", "description": "لوازم خانگی و آشپزخانه"},
    ]
    
    base_categories = []
    for data in base_categories_data:
        base_category = BaseCategorys.objects.create(
            name=data["name"],
            en_name=data["en_name"],
            description=data["description"],
            image=create_fake_image()
        )
        base_categories.append(base_category)
        print(f"Created Base Category: {base_category.name}")
    
    return base_categories

def generate_categories(base_categories):
    """Generate fake categories"""
    print("Generating Categories...")
    
    categories_data = {
        "electronics": [
            {"name": "گوشی موبایل", "en_name": "mobile_phones"},
            {"name": "لپ تاپ", "en_name": "laptops"},
            {"name": "هدفون", "en_name": "headphones"},
        ],
        "clothing": [
            {"name": "پیراهن مردانه", "en_name": "mens_shirts"},
            {"name": "شلوار مردانه", "en_name": "mens_pants"},
        ],
        "shoes": [
            {"name": "کفش ورزشی", "en_name": "sports_shoes"},
            {"name": "کفش رسمی", "en_name": "formal_shoes"},
        ],
        "home_appliances": [
            {"name": "یخچال", "en_name": "refrigerators"},
            {"name": "ماشین لباسشویی", "en_name": "washing_machines"},
        ],
    }
    
    categories = []
    for base_cat in base_categories:
        if base_cat.en_name in categories_data:
            for cat_data in categories_data[base_cat.en_name]:
                category = Category.objects.create(
                    name=cat_data["name"],
                    en_name=cat_data["en_name"],
                    description=fake.text(max_nb_chars=200),
                    base_catgory=base_cat,
                    image=create_fake_image()
                )
                categories.append(category)
                print(f"Created Category: {category.name} under {base_cat.name}")
    
    return categories

def generate_brands():
    """Generate fake brands"""
    print("Generating Brands...")
    
    brands_data = [
        {"name": "سامسونگ", "en_name": "samsung"},
        {"name": "اپل", "en_name": "apple"},
        {"name": "شیائومی", "en_name": "xiaomi"},
        {"name": "نایک", "en_name": "nike"},
        {"name": "آدیداس", "en_name": "adidas"},
    ]
    
    brands = []
    for data in brands_data:
        brand = Brand.objects.create(
            name=data["name"],
            en_name=data["en_name"],
            logo=create_fake_image(200, 100)
        )
        brands.append(brand)
        print(f"Created Brand: {brand.name}")
    
    return brands

def generate_colors():
    """Generate fake colors"""
    print("Generating Colors...")
    
    colors_data = [
        {"name": "قرمز", "hex_code": "#FF0000"},
        {"name": "آبی", "hex_code": "#0000FF"},
        {"name": "سبز", "hex_code": "#00FF00"},
        {"name": "مشکی", "hex_code": "#000000"},
        {"name": "سفید", "hex_code": "#FFFFFF"},
    ]
    
    # Create base colors first
    base_colors = []
    for i in range(3):
        base_color = BaseColor.objects.create(
            name=f"رنگ پایه {i+1}",
            color=colors_data[i]["hex_code"]
        )
        base_colors.append(base_color)
    
    colors = []
    for data in colors_data:
        color = Color.objects.create(
            name=data["name"],
            hex_code=data["hex_code"],
            base_color=random.choice(base_colors),
            image=create_fake_image(100, 100, tuple(int(data["hex_code"][i:i+2], 16) for i in (1, 3, 5)))
        )
        colors.append(color)
        print(f"Created Color: {color.name}")
    
    return colors

def generate_sizes():
    """Generate fake sizes"""
    print("Generating Sizes...")
    
    sizes_data = [
        {"size": "S", "size_numrical": "کوچک", "category": "clothing"},
        {"size": "M", "size_numrical": "متوسط", "category": "clothing"},
        {"size": "L", "size_numrical": "بزرگ", "category": "clothing"},
        {"number_size": 40, "size_numrical": "40", "category": "shoes"},
        {"number_size": 41, "size_numrical": "41", "category": "shoes"},
        {"number_size": 42, "size_numrical": "42", "category": "shoes"},
    ]
    
    sizes = []
    for data in sizes_data:
        size = Size.objects.create(**data)
        sizes.append(size)
        print(f"Created Size: {size}")
    
    return sizes

def generate_specifications(categories):
    """Generate fake specifications"""
    print("Generating Specifications...")
    
    spec_templates = {
        "mobile_phones": [
            {"name": "حافظه داخلی", "data_type": "int", "unit": "GB", "is_main": True},
            {"name": "رم", "data_type": "int", "unit": "GB", "is_main": True},
            {"name": "اندازه صفحه نمایش", "data_type": "decimal", "unit": "اینچ", "is_main": True},
        ],
        "laptops": [
            {"name": "پردازنده", "data_type": "str", "unit": None, "is_main": True},
            {"name": "رم", "data_type": "int", "unit": "GB", "is_main": True},
            {"name": "هارد دیسک", "data_type": "int", "unit": "GB", "is_main": True},
        ],
        "sports_shoes": [
            {"name": "سایز", "data_type": "int", "unit": None, "is_main": True},
            {"name": "وزن", "data_type": "decimal", "unit": "گرم", "is_main": False},
        ],
    }
    
    specifications = []
    for category in categories:
        if category.en_name in spec_templates:
            for spec_data in spec_templates[category.en_name]:
                spec = Specification.objects.create(
                    name=spec_data["name"],
                    data_type=spec_data["data_type"],
                    unit=spec_data["unit"],
                    is_main=spec_data["is_main"],
                    category=category
                )
                specifications.append(spec)
                print(f"Created Specification: {spec.name} for {category.name}")
    
    return specifications

def generate_products(categories, brands, colors, sizes, specifications):
    """Generate fake products"""
    print("Generating Products...")
    
    products = []
    for i in range(20):  # Generate 20 products
        category = random.choice(categories)
        
        if "mobile" in category.en_name:
            product_name = f"گوشی {random.choice(['سامسونگ', 'اپل', 'شیائومی'])} مدل {fake.word()}"
        elif "laptop" in category.en_name:
            product_name = f"لپ تاپ {random.choice(['لنوو', 'سونی'])} مدل {fake.word()}"
        else:
            product_name = f"{category.name} {fake.word()} مدل {fake.word()}"
        
        product = Product.objects.create(
            name=product_name,
            description=fake.text(max_nb_chars=300),
            is_active=random.choice([True, True, False]),
            image=create_fake_image(400, 400)
        )
        
        product.categories.add(category)
        products.append(product)
        print(f"Created Product: {product.name}")
    
    return products

def generate_product_packages(products, brands, colors, sizes):
    """Generate fake product packages"""
    print("Generating Product Packages...")
    
    packages = []
    for product in products:
        num_packages = random.randint(1, 3)
        
        for i in range(num_packages):
            price = random.randint(100000, 50000000)
            discount = random.choice([0, 0, 5, 10, 15])
            
            package = ProductPackage.objects.create(
                product=product,
                size=random.choice(sizes),  # Always provide a size
                brand=random.choice(brands) if random.choice([True, False]) else None,
                color=random.choice(colors),
                quantity=random.randint(0, 50),
                weight=random.randint(100, 2000),
                is_active_package=random.choice([True, True, False]),
                price=price,
                discount=discount,
                is_active_discount=discount > 0,
                sold_count=random.randint(0, 20),
                views_count=random.randint(0, 500),
                rating=round(random.uniform(1, 5), 1)
            )
            packages.append(package)
            print(f"Created Package for {product.name}")
    
    return packages

def generate_product_specifications(products, specifications):
    """Generate fake product specifications"""
    print("Generating Product Specifications...")
    
    for product in products:
        product_specs = []
        for category in product.categories.all():
            category_specs = Specification.objects.filter(category=category)
            product_specs.extend(category_specs)
        
        product_specs = list(set(product_specs))
        
        if len(product_specs) >= 2:
            count = random.randint(2, len(product_specs))
        elif len(product_specs) == 1:
            count = 1
        else:
            count = 0

        for spec in product_specs[:count]:
            if spec.data_type == 'int':
                if 'حافظه' in spec.name or 'رم' in spec.name:
                    value = random.choice([4, 8, 16, 32, 64, 128])
                else:
                    value = random.randint(1, 100)
                int_value = value
                decimal_value = None
                str_value = None
                bool_value = None
            elif spec.data_type == 'decimal':
                value = round(random.uniform(5.0, 17.0), 1)
                int_value = None
                decimal_value = value
                str_value = None
                bool_value = None
            elif spec.data_type == 'str':
                if 'پردازنده' in spec.name:
                    value = random.choice(['Intel i5', 'Intel i7', 'AMD Ryzen 5'])
                else:
                    value = fake.word()
                int_value = None
                decimal_value = None
                str_value = value
                bool_value = None
            
            ProductSpecification.objects.create(
                product=product,
                specification=spec,
                int_value=int_value,
                decimal_value=decimal_value,
                str_value=str_value,
                bool_value=bool_value,
                is_main=spec.is_main
            )
            print(f"Created Product Specification: {spec.name} = {value} for {product.name}")

def main():
    """Main function to generate all fake data"""
    print("🚀 Starting fake data generation...")
    
    # Clear existing data first
    print("🗑️ Clearing existing data...")
    ProductSpecification.objects.all().delete()
    Specification.objects.all().delete()
    Gallery.objects.all().delete()
    Comment.objects.all().delete()
    ProductPackage.objects.all().delete()
    Product.objects.all().delete()
    Size.objects.all().delete()
    Color.objects.all().delete()
    BaseColor.objects.all().delete()
    Brand.objects.all().delete()
    Category.objects.all().delete()
    BaseCategorys.objects.all().delete()
    HomeSlider.objects.all().delete()
    PromotionalBanner.objects.all().delete()
    FeaturedBrand.objects.all().delete()
    print("✅ Existing data cleared successfully!")
    
    try:
        base_categories = generate_base_categories()
        categories = generate_categories(base_categories)
        brands = generate_brands()
        colors = generate_colors()
        sizes = generate_sizes()
        specifications = generate_specifications(categories)
        products = generate_products(categories, brands, colors, sizes, specifications)
        packages = generate_product_packages(products, brands, colors, sizes)
        generate_product_specifications(products, specifications)
        
        print("\n✅ Fake data generation completed successfully!")
        print(f"📊 Generated:")
        print(f"   - {BaseCategorys.objects.count()} Base Categories")
        print(f"   - {Category.objects.count()} Categories")
        print(f"   - {Brand.objects.count()} Brands")
        print(f"   - {Color.objects.count()} Colors")
        print(f"   - {Size.objects.count()} Sizes")
        print(f"   - {Specification.objects.count()} Specifications")
        print(f"   - {Product.objects.count()} Products")
        print(f"   - {ProductPackage.objects.count()} Product Packages")
        print(f"   - {ProductSpecification.objects.count()} Product Specifications")
        
    except Exception as e:
        print(f"❌ Error during data generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()