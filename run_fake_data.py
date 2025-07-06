 
# -*- coding: utf-8 -*-
"""
Simple script to run fake data generation
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

# Import and run the main function
from generate_fake_data import main

if __name__ == "__main__":
    main()