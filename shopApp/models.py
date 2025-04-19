from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import os
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image  # pillow
from colorfield.fields import ColorField
from model_utils import FieldTracker  # Add this import

# Create your models here.

# image handling
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    unique_id = get_random_string(length=15)
    final_name = f"image-{unique_id}{ext}"
    return f"product-images/{final_name}"

def upload_color_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    unique_id = get_random_string(length=15)
    final_name = f"image-{unique_id}{ext}"
    return f"color-images/{final_name}"

def upload_cat_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    unique_id = get_random_string(length=15)
    final_name = f"image-{unique_id}{ext}"
    return f"categories/{final_name}"

def upload_brand_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    unique_id = get_random_string(length=15)
    final_name = f"image-{unique_id}{ext}"
    return f"brands/{final_name}"
    
def upload_BaseCategory_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    unique_id = get_random_string(length=15)
    final_name = f"image-{unique_id}{ext}"
    return f"color-images/{final_name}"  # change directory name

# مدل جدید برای اسلایدرهای صفحه اصلی
def upload_slider_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    unique_id = get_random_string(length=15)
    final_name = f"slider-{unique_id}{ext}"
    return f"slider-images/{final_name}"

# مدل دسته‌بندی اصلی
class BaseCategorys(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="اسم  --  فارسی --  دسته بندی اصلی")
    en_name = models.CharField(max_length=50, unique=True, verbose_name="اسم- --انگلیسی-- دسته بندی اصلی")
    description = models.TextField(verbose_name="توضیحات دسته بندی اصلی")
    image = models.ImageField(upload_to=upload_BaseCategory_image_path, verbose_name="عکس دسته بندی اصلی", blank=True, null=True)
    brands = models.ManyToManyField('Brand', verbose_name="برند های دسته بندی", related_name='base_categories', blank=True)

    class Meta:
        verbose_name = "دسته بندی  اصلی "
        verbose_name_plural = "دسته بندی های اصلی"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'path') and os.path.isfile(self.image.path):
            img = Image.open(self.image.path)
            output_size = (300,300)
            img.thumbnail(output_size, Image.LANCZOS)
            img.save(self.image.path)

    def __str__(self):
        return self.name

# مدل دسته بندی
class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name="دسته بندی والد", related_name='subcategories')
    base_catgory = models.ForeignKey(BaseCategorys, verbose_name="دسته بندی اصلی", on_delete=models.CASCADE, related_name='categories')
    
    name = models.CharField(max_length=20, unique=True, verbose_name="نام دسته بندی ---فارسی")
    en_name = models.CharField(max_length=20, unique=True, verbose_name="نام دسته بندی ---انگلیسی")
    description = models.TextField(verbose_name="توضیحات دسته بندی")
    image = models.ImageField(upload_to=upload_cat_image_path, verbose_name="عکس دسته بندی", blank=True, null=True)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'path') and os.path.isfile(self.image.path):
            img = Image.open(self.image.path)
            output_size = (300,300)
            img.thumbnail(output_size, Image.LANCZOS)
            img.save(self.image.path)

    def __str__(self):
        return self.name

# مدل برند
class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="نام ---فارسی")
    en_name = models.CharField(max_length=50, unique=True, verbose_name="نام ---انگلیسی")
    logo = models.ImageField(upload_to=upload_brand_image_path, verbose_name="لوگو برند", blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True, verbose_name="دسته بندی")

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برندها"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.logo and hasattr(self.logo, 'path') and os.path.isfile(self.logo.path):
            img = Image.open(self.logo.path)
            output_size = (300,300)
            img.thumbnail(output_size, Image.LANCZOS)
            img.save(self.logo.path)

    def __str__(self):
        return self.en_name

# ادامه مدل‌ها
class BaseColor(models.Model):
    COLOR_PALETTE = [
        ("#FFFFFF", "white"),
        ("#000000", "black"),
        ("#FF0000", "red"),
        ("#008000", "green"),
        ("#0000FF", "blue"),
    ]
    name = models.CharField(max_length=50, verbose_name="نام رنگ", null=True, blank=True)
    color = ColorField(samples=COLOR_PALETTE, default="#FFFFFF", verbose_name="رنگ")
    
    class Meta:
        verbose_name = "رنگ پایه"
        verbose_name_plural = "رنگ های پایه"
        
    def __str__(self):
        return f"{self.name}" if self.name else "بدون نام"
   
class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name= "نام رنگ")
    hex_code = models.CharField(max_length=7, verbose_name= "کد هگز رنگ",help_text=" مثال: #FFFFFF")
    image = models.ImageField(upload_to=upload_color_image_path, verbose_name="تصویر رنگ", blank=True, null=True)
    base_color = models.ForeignKey(BaseColor, on_delete=models.CASCADE, verbose_name="رنگ پایه", related_name="colors", null=True, blank=True)

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ ها"
    
    def __str__(self):
        return self.name

class Size(models.Model):
    SIZE_CHOICES= [
        ("XS","XS"),
        ("S","S"),
        ("M","M"),
        ("L","L"),
        ("XL","XL"),
        ("XXL","XXL"),
        ("3XL","3XL"),
        ("4XL","4XL"),
    ]
    # دسته بندی برای سایزها
    CATEGORY_CHOICES=[
        ("clothing","لباس"),
        ("shoes","کفش"),
        ("accessories","اکسسوری"),
    ]
    size= models.CharField(choices=SIZE_CHOICES, max_length=10, blank= True, null=True, verbose_name="سایز")
    number_size = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="سایز عددی (برای مواردی مثل کفش)")
    size_numrical = models.CharField(max_length=10, verbose_name="سایز عددی نوشتاری")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, blank=True, null=True, verbose_name="دسته بندی")
    
    class Meta:
        verbose_name = "سایز"
        verbose_name_plural = "سایزها"
        ordering = ['number_size']  # چیدمان پیش‌فرض
        
    def __str__(self):
        if self.size:
            return self.size
        elif self.number_size:
            return str(self.number_size)
        else:
            return self.size_numrical or "بدون سایز"

class HomeSlider(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="عنوان اسلاید")
    subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name="زیرعنوان اسلاید")
    image = models.ImageField(upload_to=upload_slider_image_path, verbose_name="تصویر اسلاید", blank=True, null=True)
    link = models.URLField(verbose_name="لینک", blank=True, null=True)
    active = models.BooleanField(default=True, verbose_name="فعال")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    
    class Meta:
        verbose_name = "اسلایدر صفحه اصلی"
        verbose_name_plural = "اسلایدرهای صفحه اصلی"
        ordering = ['order']
        
    def __str__(self):
        return self.title or f"اسلاید {self.id}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'path') and os.path.isfile(self.image.path):
            img = Image.open(self.image.path)
            output_size = (1920, 800)  # مناسب برای اسلایدر عریض
            img = img.resize(output_size, Image.LANCZOS)
            img.save(self.image.path)

# مدل جدید برای بنرهای تبلیغاتی
def upload_banner_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    unique_id = get_random_string(length=15)
    final_name = f"banner-{unique_id}{ext}"
    return f"banner-images/{final_name}"

class PromotionalBanner(models.Model):
    POSITION_CHOICES = [
        ('top', 'بالای صفحه'),
        ('middle', 'وسط صفحه'),
        ('bottom', 'پایین صفحه'),
    ]
    
    SIZE_CHOICES = [
        ('full', 'تمام عرض'),
        ('half', 'نیم عرض'),
        ('third', 'یک سوم'),
    ]
    
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="عنوان بنر")
    image = models.ImageField(upload_to=upload_banner_image_path, verbose_name="تصویر بنر", blank=True, null=True)
    link = models.URLField(verbose_name="لینک", blank=True, null=True)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, default='middle', verbose_name="موقعیت در صفحه")
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='full', verbose_name="اندازه بنر")
    active = models.BooleanField(default=True, verbose_name="فعال")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    
    class Meta:
        verbose_name = "بنر تبلیغاتی"
        verbose_name_plural = "بنرهای تبلیغاتی"
        ordering = ['position', 'order']
        
    def __str__(self):
        return self.title or f"بنر {self.id}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'path') and os.path.isfile(self.image.path):
            img = Image.open(self.image.path)
            # تنظیم اندازه بر اساس نوع بنر
            if self.size == 'full':
                output_size = (1200, 300)
            elif self.size == 'half':
                output_size = (600, 300)
            else:  # third
                output_size = (400, 300)
            img = img.resize(output_size, Image.LANCZOS)
            img.save(self.image.path)

# مدل برای نمایش ویژه برندها در صفحه اصلی
class FeaturedBrand(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="برند")
    active = models.BooleanField(default=True, verbose_name="فعال")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    
    class Meta:
        verbose_name = "برند ویژه"
        verbose_name_plural = "برندهای ویژه"
        ordering = ['order']
        
    def __str__(self):
        return f"{self.brand.name}"

# مدل محصول
class Product(models.Model):
    name = models.CharField(max_length=150, unique= True, verbose_name="نام محصول")
    description = models.TextField(verbose_name="توضیحات")
    is_active = models.BooleanField(default=False, verbose_name="موجود")
    categories = models.ManyToManyField('Category', verbose_name="دسته بندی")
# _________________________________________________*price*_____________________________________________________
    
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="زمان اضافه شدن")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="آخرین تغییر")
    image = models.ImageField(upload_to='uploads/', verbose_name="عکس", blank=True, null=True)  # مسیر بارگذاری تصویر را تنظیم کنید

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return f"نام محصول: {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # باز کردن تصویر
        if self.image and hasattr(self.image, 'path') and os.path.isfile(self.image.path):
            img = Image.open(self.image.path)
            # تنظیم ابعاد جدید
            output_size = (800, 800)
            # تغییر اندازه تصویر به ابعاد مشخص
            img = img.resize(output_size, Image.LANCZOS)  # استفاده از LANCZOS برای کیفیت بهتر
            # ذخیره تصویر با ابعاد جدید
            img.save(self.image.path)

class ProductPackage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_packages')
    # ____________________________________________________*product attributes *___________________________________________
    size = models.ForeignKey(Size, on_delete=models.CASCADE, default=None,blank=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name="برند")
    color = models.ForeignKey(Color,verbose_name="رنگ", blank= True, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=0, verbose_name="تعداد" , blank= False)
    weight = models.PositiveIntegerField(verbose_name="وزن به گرم" , default= 0 , blank= True)

    is_active_package=models.BooleanField(default=False ,  verbose_name=" موجود ؟" , )

    created_date = models.DateTimeField(auto_now_add=True)
    
    # _________________________________________________*price*_____________________________________________________
    price = models.BigIntegerField(null=False, verbose_name="قیمت برای این ویژگی ها")
    final_price = models.BigIntegerField(default= 0 , verbose_name= "  قیمت نهایی با این ویژگی ها ",editable=False)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], null=True, blank=True ,default=0, verbose_name="درصد تخفیف")
    is_active_discount = models.BooleanField(default=False, verbose_name="اعمال تخفیف")
    
    # آمار فروش
    sold_count = models.PositiveIntegerField(default=0, verbose_name="تعداد فروش")
    views_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="امتیاز")

    # Add field tracker to track changes
    tracker = FieldTracker(fields=['is_active_package'])

    class Meta:
        verbose_name = " ویژگی های محصول"
        verbose_name_plural = " ویژگی های محصولات"

    def __str__(self):
        return f"{self.product.id} - {self.product.name} - {self.size.size} - {self.quantity} - {self.weight} - "


    @property
    def discounted_price(self):
        return (self.price * self.discount) / 100
    
    def save(self, *args, **kwargs):
        # محاسبه قیمت نهایی با توجه به تخفیف
        if self.is_active_discount and self.discount > 0:
            self.final_price = self.price - int((self.price * self.discount) / 100)
        else:
            self.final_price = self.price
            
        super().save(*args, **kwargs)

class Gallery(models.Model):

    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="محصول")

    image = models.ImageField(upload_to=upload_image_path,verbose_name="عکس", blank=True, null=True)

    class Meta :
        verbose_name ="عکس"
        verbose_name_plural = "گالری"
    
    def __str__(self):
        return f"{self.product}"
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'path') and os.path.isfile(self.image.path):
            img = Image.open(self.image.path)
            output_size = (800, 800)
            img = img.resize(output_size, Image.LANCZOS)
            img.save(self.image.path)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name="پاسخ به")
    text = models.TextField(verbose_name="متن نظر")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="امتیاز")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده")
    
    # Add field tracker to track changes
    tracker = FieldTracker()

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}★"

# مدل تنظیمات کلی سایت
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, verbose_name="نام سایت")
    site_url = models.URLField(verbose_name="آدرس سایت")
    logo = models.ImageField(upload_to='settings/', verbose_name="لوگوی سایت", blank=True, null=True)
    favicon = models.ImageField(upload_to='settings/', verbose_name="فاوآیکون سایت", blank=True, null=True)
    
    # اطلاعات تماس
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="آدرس")
    
    # شبکه‌های اجتماعی
    instagram = models.URLField(blank=True, null=True, verbose_name="اینستاگرام")
    telegram = models.URLField(blank=True, null=True, verbose_name="تلگرام")
    twitter = models.URLField(blank=True, null=True, verbose_name="توییتر")
    linkedin = models.URLField(blank=True, null=True, verbose_name="لینکدین")
    
    # متن‌های سایت
    footer_text = models.TextField(verbose_name="متن فوتر")
    about_text = models.TextField(verbose_name="درباره ما")
    
    # تنظیمات سئو
    seo_keywords = models.TextField(verbose_name="کلمات کلیدی سئو", blank=True, null=True)
    seo_description = models.TextField(verbose_name="توضیحات سئو", blank=True, null=True)
    
    # تنظیمات فروشگاه
    shipping_cost = models.PositiveIntegerField(default=0, verbose_name="هزینه ارسال")
    free_shipping_threshold = models.PositiveIntegerField(default=0, verbose_name="حداقل خرید برای ارسال رایگان")
    tax_percentage = models.FloatField(default=9.0, verbose_name="درصد مالیات")
    
    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"
        
    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.logo and hasattr(self.logo, 'path') and os.path.isfile(self.logo.path):
            img = Image.open(self.logo.path)
            output_size = (300, 100)
            img.thumbnail(output_size, Image.LANCZOS)
            img.save(self.logo.path)
            
        if self.favicon and hasattr(self.favicon, 'path') and os.path.isfile(self.favicon.path):
            img = Image.open(self.favicon.path)
            output_size = (32, 32)
            img = img.resize(output_size, Image.LANCZOS)
            img.save(self.favicon.path)

# مدل صفحات استاتیک (مانند قوانین و مقررات، درباره ما)
class StaticPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان صفحه")
    slug = models.SlugField(unique=True, verbose_name="نامک")
    content = models.TextField(verbose_name="محتوای صفحه")
    active = models.BooleanField(default=True, verbose_name="فعال")
    
    # تنظیمات سئو
    seo_title = models.CharField(max_length=200, blank=True, null=True, verbose_name="عنوان سئو")
    seo_keywords = models.TextField(blank=True, null=True, verbose_name="کلمات کلیدی سئو")
    seo_description = models.TextField(blank=True, null=True, verbose_name="توضیحات سئو")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "صفحه استاتیک"
        verbose_name_plural = "صفحات استاتیک"
        
    def __str__(self):
        return self.title


    


