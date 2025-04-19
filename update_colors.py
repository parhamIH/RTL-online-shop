import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from shopApp.models import BaseColor, Color

def update_colors():
    # به‌روزرسانی BaseColor
    colors = BaseColor.objects.all()
    color_data = [
        {'name': 'سفید', 'color': '#FFFFFF'},
        {'name': 'سیاه', 'color': '#000000'},
        {'name': 'قرمز', 'color': '#FF0000'},
        {'name': 'سبز', 'color': '#008000'},
        {'name': 'آبی', 'color': '#0000FF'},
    ]
    
    for i, color in enumerate(colors):
        data = color_data[i % len(color_data)]
        color.name = data['name']
        color.color = data['color']
        color.save()
        print(f'Updated BaseColor {i+1} with name: {color.name}, color: {color.color}')
    
    print(f'Total BaseColors updated: {len(colors)}')
    
    # به‌روزرسانی Color
    colors = Color.objects.all()
    color_data = [
        {'name': 'جگری', 'hex_code': '#A52A2A'},
        {'name': 'زرد قناری', 'hex_code': '#FFFF00'},
        {'name': 'سفید', 'hex_code': '#FFFFFF'},
        {'name': 'مشکی', 'hex_code': '#000000'},
        {'name': 'آبی', 'hex_code': '#0000FF'},
    ]
    
    for i, color in enumerate(colors):
        if i < len(color_data):
            data = color_data[i]
            # فقط hex_code را تغییر می‌دهیم و نام را دست نمی‌زنیم
            color.hex_code = data['hex_code']
            color.save()
            print(f'Updated Color {i+1} with name: {color.name}, hex_code: {color.hex_code}')
    
    print(f'Total Colors updated: {len(colors)}')

if __name__ == '__main__':
    update_colors() 