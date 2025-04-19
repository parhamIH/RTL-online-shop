import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()

from django.db import connection

# Add missing columns to Color table
with connection.cursor() as cursor:
    # Check columns in Color table
    try:
        cursor.execute("SHOW COLUMNS FROM shopApp_color")
        columns = cursor.fetchall()
        print("Columns in shopApp_color table:")
        for column in columns:
            print(column)
    except Exception as e:
        print(f"Error checking columns: {e}")

    # Add hex_code column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE shopApp_color ADD COLUMN hex_code VARCHAR(7) DEFAULT '#FFFFFF'")
        print("Successfully added hex_code column to shopApp_color table")
    except Exception as e:
        print(f"Error adding hex_code column: {e}")

print("Database update completed.") 