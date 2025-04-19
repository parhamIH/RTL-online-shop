import os
import shutil
import datetime
import subprocess
from pathlib import Path

def create_backup_folders():
    """ساخت پوشه‌های مورد نیاز برای بک‌آپ"""
    # مسیر دسکتاپ کاربر
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    backup_path = os.path.join(desktop_path, 'backup_shahan_shop')
    
    # ساخت پوشه‌های بک‌آپ
    folders = [
        os.path.join(backup_path, 'database'),
        os.path.join(backup_path, 'media'),
        os.path.join(backup_path, 'project')
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f'✅ پوشه {folder} ساخته شد')
    
    return backup_path

def backup_database():
    """تهیه بک‌آپ از دیتابیس"""
    # چک کردن وجود mysqldump
    if not shutil.which('mysqldump'):
        print('⚠️ دستور mysqldump در سیستم یافت نشد. لطفاً MySQL را نصب کنید.')
        print('⚠️ بک‌آپ دیتابیس انجام نشد، اما بقیه فرآیند بک‌آپ ادامه می‌یابد.')
        return True
        
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    backup_file = os.path.join(desktop_path, 'backup_shahan_shop', 'database', f'shahan_shop_{timestamp}.sql')
    
    # تنظیمات دیتابیس
    db_settings = {
        'user': 'root',
        'password': 'parhams',
        'database': 'shahan_shop',
        'host': 'localhost',
    }
    
    # ساخت دستور mysqldump
    mysqldump_cmd = [
        'mysqldump',
        f'--user={db_settings["user"]}',
        f'--password={db_settings["password"]}',
        f'--host={db_settings["host"]}',
        db_settings['database']
    ]
    
    try:
        with open(backup_file, 'w') as f:
            subprocess.run(mysqldump_cmd, stdout=f, check=True)
        print(f'✅ بک‌آپ دیتابیس با موفقیت در {backup_file} ذخیره شد')
    except subprocess.CalledProcessError as e:
        print(f'❌ خطا در تهیه بک‌آپ از دیتابیس: {e}')
        return False
    return True

def backup_media_files():
    """کپی فایل‌های رسانه"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    backup_dir = os.path.join(desktop_path, 'backup_shahan_shop', 'media', f'media_{timestamp}')
    
    try:
        if os.path.exists('uploads'):
            shutil.copytree('uploads', backup_dir)
            print(f'✅ فایل‌های رسانه با موفقیت در {backup_dir} کپی شدند')
        else:
            print('⚠️ پوشه uploads یافت نشد')
    except Exception as e:
        print(f'❌ خطا در کپی فایل‌های رسانه: {e}')
        return False
    return True

def backup_project_files():
    """کپی فایل‌های پروژه"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    backup_dir = os.path.join(desktop_path, 'backup_shahan_shop', 'project', f'project_{timestamp}')
    
    # الگوهای فایل‌هایی که نباید کپی شوند
    exclude_patterns = [
        '.git', '__pycache__', '*.pyc', 'venv',
        'node_modules', '.env', '.idea', '.vscode',
        'backup', 'media', 'static/admin'
    ]
    
    def ignore_patterns(path, names):
        ignored = set()
        for pattern in exclude_patterns:
            for name in names:
                if pattern.startswith('*'):
                    if name.endswith(pattern[1:]):
                        ignored.add(name)
                elif name == pattern:
                    ignored.add(name)
        return ignored
    
    try:
        shutil.copytree('.', backup_dir, ignore=ignore_patterns)
        print(f'✅ فایل‌های پروژه با موفقیت در {backup_dir} کپی شدند')
    except Exception as e:
        print(f'❌ خطا در کپی فایل‌های پروژه: {e}')
        return False
    return True

def create_requirements():
    """به‌روزرسانی فایل requirements.txt"""
    try:
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        backup_path = os.path.join(desktop_path, 'backup_shahan_shop')
        requirements_file = os.path.join(backup_path, 'requirements.txt')
        
        subprocess.run(['pip', 'freeze'], stdout=open(requirements_file, 'w'), check=True)
        print(f'✅ فایل requirements.txt با موفقیت در {requirements_file} به‌روزرسانی شد')
    except Exception as e:
        print(f'❌ خطا در به‌روزرسانی requirements.txt: {e}')
        return False
    return True

def main():
    """تابع اصلی برای اجرای بک‌آپ"""
    print('🔄 شروع فرآیند بک‌آپ...')
    
    # ایجاد پوشه‌های بک‌آپ
    backup_path = create_backup_folders()
    print(f'📂 پوشه بک‌آپ در {backup_path} ایجاد شد')
    
    # بک‌آپ دیتابیس
    if not backup_database():
        print('⚠️ بک‌آپ دیتابیس با خطا مواجه شد')
    
    # بک‌آپ فایل‌های رسانه
    if not backup_media_files():
        print('⚠️ بک‌آپ فایل‌های رسانه با خطا مواجه شد')
    
    # بک‌آپ فایل‌های پروژه
    if not backup_project_files():
        print('⚠️ بک‌آپ فایل‌های پروژه با خطا مواجه شد')
    
    # به‌روزرسانی requirements.txt
    if not create_requirements():
        print('⚠️ به‌روزرسانی requirements.txt با خطا مواجه شد')
    
    print('✅ فرآیند بک‌آپ به پایان رسید')

if __name__ == '__main__':
    main() 