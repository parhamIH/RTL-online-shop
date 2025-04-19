import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from cart.models import Order, Cart

def update_payment_statuses():
    """
    این اسکریپت وضعیت پرداخت سفارش‌ها را به‌روزرسانی می‌کند
    """
    print("به‌روزرسانی وضعیت پرداخت سفارش‌ها...")
    
    # برای هر سفارش
    orders = Order.objects.all()
    updated_count = 0
    
    for order in orders:
        old_status = order.payment_status
        
        # اگر سبد خرید پرداخت شده است
        if order.cart.is_paid:
            order.payment_status = "پرداخت شده"
        else:
            order.payment_status = "در انتظار پرداخت"
        
        if old_status != order.payment_status:
            updated_count += 1
            order.save()
            print(f"سفارش {order.order_number}: {old_status} -> {order.payment_status}")
    
    print(f"تعداد {updated_count} سفارش به‌روزرسانی شد.")

if __name__ == "__main__":
    update_payment_statuses() 