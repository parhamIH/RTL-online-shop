from django.urls import path
from .views import *


urlpatterns = [
    path("products", products_list),
    path('product/<pk>/<name>', product_detail),
    path ("categories/<en_name>", category_products),    
    path("get-package-info/<int:package_id>/", get_package_info, name='get_package_info'),
    path("page/<slug:slug>/", static_page, name='static_page'),
]
    