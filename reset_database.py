import os
import django
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()

from django.db import connection
from django.conf import settings

def reset_database():
    # این تابع کل دیتابیس را پاک می‌کند و مجدد می‌سازد
    
    # هشدار به کاربر
    confirmation = input("این عمل تمام داده‌های دیتابیس را پاک می‌کند. آیا مطمئن هستید؟ (y/n): ")
    if confirmation.lower() != 'y':
        print("عملیات لغو شد.")
        return

    # اتصال به دیتابیس
    with connection.cursor() as cursor:
        # نام دیتابیس فعلی را دریافت می‌کنیم
        db_name = settings.DATABASES['default']['NAME']
        
        # لیست تمام جداول را دریافت می‌کنیم
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"در حال حذف {len(tables)} جدول از دیتابیس {db_name}...")
        
        # غیرفعال کردن بررسی کلیدهای خارجی
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # حذف تمام جداول
        for table in tables:
            table_name = table[0]
            print(f"در حال حذف جدول: {table_name}")
            cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        
        # فعال‌سازی مجدد بررسی کلیدهای خارجی
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        print("تمام جداول با موفقیت حذف شدند.")
    
    print("در حال اجرای مایگریشن‌ها برای ساخت مجدد ساختار دیتابیس...")
    
    # اجرای مایگریشن‌ها
    from django.core.management import call_command
    call_command('migrate')
    
    print("دیتابیس با موفقیت بازسازی شد.")
    return True

if __name__ == "__main__":
    reset_database() 