# RTL-online-shop
this is a Django online shop web application RLT

# Project Setup Guide

## English

### Prerequisites

- Python 3.x installed on your system.

### Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Create a virtual environment:**
    It's recommended to use a virtual environment to manage project dependencies.

    -   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install dependencies:**
    Install the required packages using the `freeze.txt` file:
    ```bash
    pip install -r freeze.txt
    ```

4.  **Run the application:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```


---

## فارسی

### پیش‌نیازها

-   پایتون نسخه ۳ یا بالاتر روی سیستم شما نصب باشد.

### دستورالعمل‌های راه‌اندازی

۱.  **کلون کردن ریپازیتوری:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```
    *(به جای `<your-repository-url>` آدرس ریپازیتوری خود و به جای `<your-repository-directory>` نام پوشه پروژه خود را قرار دهید)*

۲.  **ایجاد محیط مجازی (virtual environment):**
    پیشنهاد می‌شود برای مدیریت وابستگی‌های پروژه از یک محیط مجازی استفاده کنید.

    -   در ویندوز:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    -   در مک‌او‌اس/لینوکس:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *پس از فعال‌سازی محیط مجازی، نام `(venv)` در ابتدای خط فرمان شما نمایش داده می‌شود.*

۳.  **نصب وابستگی‌ها:**
    بسته‌های مورد نیاز پروژه را با استفاده از فایل `freeze.txt` نصب کنید:
    ```bash
    pip install -r freeze.txt
    ```

۴.  **اجرای برنامه:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```
