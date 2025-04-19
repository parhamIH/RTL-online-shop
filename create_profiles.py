import os
import django
import sys

# تنظیم محیط جنگو
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from django.contrib.auth.models import User
from account.models import Profile

def create_profiles_for_existing_users():
    """ایجاد پروفایل برای کاربران موجود که پروفایل ندارند"""
    users_without_profile = []
    
    for user in User.objects.all():
        try:
            # بررسی وجود پروفایل
            profile = user.profile
            print(f"User {user.username} already has a profile")
        except Profile.DoesNotExist:
            # ایجاد پروفایل جدید
            Profile.objects.create(user=user)
            users_without_profile.append(user.username)
            print(f"Created new profile for user: {user.username}")
    
    if users_without_profile:
        print(f"\nCreated profiles for {len(users_without_profile)} users: {', '.join(users_without_profile)}")
    else:
        print("\nAll users already have profiles")

if __name__ == "__main__":
    create_profiles_for_existing_users() 