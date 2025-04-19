from django.contrib import admin
from .models import *
from django.utils.html import format_html


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1


class GalleryAdmin(admin.ModelAdmin):
    list_display = ["product", 'image_preview']
    list_display_links = ("product",)
    list_filter = ("product",)
    ordering = ("product",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "بدون تصویر"
    image_preview.short_description = 'پیش‌نمایش تصویر'

    fieldsets = (
        ("محصول / عکس", {"fields": ("product", "image")}),
    )


class SizeAdmin(admin.ModelAdmin):
    list_display = ('size', 'size_numrical', 'category')
    search_fields = ('size', 'size_numrical')
    list_filter = ('category',)
    fieldsets = (
        ("اطلاعات سایز", {
            'fields': ('size', 'number_size', 'size_numrical', 'category')
        }),
    )


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    list_display = ("product", "user", "created_at", "text_preview", "rating", "is_approved")
    list_display_links = ("product",)
    list_filter = ("product", "is_approved", "rating", "created_at")
    ordering = ("product", "created_at")
    list_editable = ("is_approved",)
    
    def text_preview(self, obj):
        if len(obj.text) > 50:
            return f"{obj.text[:50]}..."
        return obj.text
    text_preview.short_description = 'متن نظر'

    fieldsets = (
        ("محصول / کاربر", {"fields": ("product", "user")}),
        ("نظر / امتیاز", {"fields": ("text", "rating", "is_approved")}),
        ("زمان ثبت", {"fields": ("created_at",)}),
    )


class BaseCategorysAdmin(admin.ModelAdmin):
    list_display = ("name", "en_name", "get_brands", "image_preview")
    list_filter = ("en_name", "name")
    ordering = ("name",)
    search_fields = ("name", "en_name")
    list_editable = ("en_name",)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "بدون تصویر"
    image_preview.short_description = 'تصویر'
    
    fieldsets = (
        ("نام ها", {'fields': ("en_name", "name")}),
        ("توضیحات دسته بندی", {"fields": ('description',)}),
        ("عکس دسته بندی", {"fields": ('image',)}),
    )
    list_select_related = True

    def get_brands(self, obj):
        return ", ".join([str(brand) for brand in obj.brands.all()])
    get_brands.short_description = 'برندها'


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ("parent", "base_catgory", "name")
    ordering = ("parent",)
    list_display = ("parent", "name", "en_name", "base_catgory", "image_preview")
    search_fields = ("name", "en_name")
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "بدون تصویر"
    image_preview.short_description = 'تصویر'

    fieldsets = (
        ("دسته بندی/دستته بندی اصلی ", {"fields": ('parent', "base_catgory")}),
        ("نام ها", {'fields': ("en_name", "name")}),
        ("توضیحات دسته بندی", {"fields": ('description',)}),
        ("عکس", {"fields": ("image",)}),
    )


class BrandAdmin(admin.ModelAdmin):
    list_filter = ("category", "name")
    ordering = ("en_name",)
    list_editable = ("name",)
    list_display = ("en_name", "name", "logo_preview")
    list_display_links = ("en_name",)
    search_fields = ('name', 'en_name')
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="80" />', obj.logo.url)
        return "بدون لوگو"
    logo_preview.short_description = 'لوگو'
    
    fieldsets = (
        ("دسته بندی", {"fields": ('category',)}),
        ("نام ها", {'fields': ("en_name", "name")}),
        ("لوگو برند", {"fields": ('logo',)}),
    )


class BaseColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_preview')
    search_fields = ('name',)
    
    def color_preview(self, obj):
        return format_html('<div style="background-color: {}; width: 30px; height: 30px; border-radius: 50%;"></div>', obj.color)
    color_preview.short_description = 'رنگ'
    
    fieldsets = (
        (None, {
            'fields': ('name', 'color')
        }),
    )


class ColorAdmin(admin.ModelAdmin):
    list_filter = ("base_color",)
    list_display = ("name", "hex_code", "hex_preview", "base_color", "image_preview")
    list_editable = ("hex_code",)
    list_display_links = ("name",)
    search_fields = ("name", "hex_code")
    
    def hex_preview(self, obj):
        return format_html('<div style="background-color: {}; width: 30px; height: 30px; border: 1px solid #ccc;"></div>', obj.hex_code)
    hex_preview.short_description = 'پیش‌نمایش'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "بدون تصویر"
    image_preview.short_description = 'تصویر'
    
    fieldsets = (
        ("رنگ", {"fields": ("name", "hex_code", "base_color")}),
        ("تصویر", {"fields": ("image",)}),
    )


class ProductPackageInline(admin.TabularInline):
    model = ProductPackage
    extra = 1
    fields = ('size', 'brand', 'color', 'quantity', 'price', 'discount', 'is_active_discount', 'is_active_package', 'final_price')
    readonly_fields = ('final_price',)


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPackageInline, GalleryInline]
    
    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'دسته‌بندی‌ها'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" />', obj.image.url)
        return "بدون تصویر"
    image_preview.short_description = 'تصویر'

    readonly_fields = ("id", 'created_date', 'updated_date')
    search_fields = ["name", "description"]
    list_filter = ('is_active', "categories", "created_date")
    ordering = ("-created_date", "is_active")

    list_display = ("id", "name", "is_active", "get_categories", "created_date", "updated_date", "image_preview")

    list_editable = ("is_active",)
    list_display_links = ("name",)
    
    fieldsets = (
        ("نام محصول / توضیحات محصول / موجود", {"fields": ("name", "description", "is_active")}),
        ("دسته بندی", {"fields": ("categories",)}),
        ("تصویر محصول", {"fields": ("image",)}),
        ("زمان", {"fields": ("created_date", "updated_date")}),
    )


class ProductPackageAdmin(admin.ModelAdmin): 
    list_display = ('product', 'size', 'brand', 'color', 'quantity', 'price', 'discount', 'final_price', 'is_active_discount', "is_active_package", "sold_count")
    search_fields = ('product__name', 'brand__name', 'color__name')
    list_filter = ('product', 'size', 'brand', 'is_active_discount', "is_active_package")
    ordering = ('product', 'size', "is_active_package")
    list_editable = ('is_active_discount', 'is_active_package', 'price', 'discount')
    readonly_fields = ('final_price', 'views_count', 'sold_count')
    
    fieldsets = (
        ("محصول و ویژگی‌ها", {
            'fields': ('product', 'size', 'brand', 'color')
        }),
        ("موجودی و وزن", {
            'fields': ('quantity', 'weight')
        }),
        ("قیمت‌گذاری", {
            'fields': ('price', 'discount', 'is_active_discount', 'final_price')
        }),
        ("وضعیت", {
            'fields': ('is_active_package',)
        }),
        ("آمار", {
            'fields': ('sold_count', 'views_count', 'rating')
        }),
    )


class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'order', 'image_preview')
    list_filter = ('active',)
    list_editable = ('active', 'order')
    search_fields = ('title', 'subtitle')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "بدون تصویر"
    image_preview.short_description = 'تصویر'
    
    fieldsets = (
        ("عنوان و زیرعنوان", {
            'fields': ('title', 'subtitle')
        }),
        ("تصویر", {
            'fields': ('image',)
        }),
        ("لینک و وضعیت", {
            'fields': ('link', 'active', 'order')
        }),
    )


class PromotionalBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'size', 'active', 'order', 'image_preview')
    list_filter = ('active', 'position', 'size')
    list_editable = ('active', 'order', 'position', 'size')
    search_fields = ('title',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "بدون تصویر"
    image_preview.short_description = 'تصویر'
    
    fieldsets = (
        ("عنوان", {
            'fields': ('title',)
        }),
        ("تصویر", {
            'fields': ('image',)
        }),
        ("موقعیت و اندازه", {
            'fields': ('position', 'size')
        }),
        ("لینک و وضعیت", {
            'fields': ('link', 'active', 'order')
        }),
    )


class FeaturedBrandAdmin(admin.ModelAdmin):
    list_display = ('brand', 'active', 'order', 'logo_preview')
    list_filter = ('active', 'brand')
    list_editable = ('active', 'order')
    
    def logo_preview(self, obj):
        if obj.brand.logo:
            return format_html('<img src="{}" width="80" />', obj.brand.logo.url)
        return "بدون لوگو"
    logo_preview.short_description = 'لوگو'


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'email', 'phone')
    
    fieldsets = (
        ('اطلاعات اصلی سایت', {
            'fields': ('site_name', 'site_url', 'logo', 'favicon')
        }),
        ('اطلاعات تماس', {
            'fields': ('email', 'phone', 'address')
        }),
        ('شبکه‌های اجتماعی', {
            'fields': ('instagram', 'telegram', 'twitter', 'linkedin')
        }),
        ('متن‌های سایت', {
            'fields': ('footer_text', 'about_text')
        }),
        ('تنظیمات سئو', {
            'fields': ('seo_keywords', 'seo_description')
        }),
        ('تنظیمات فروشگاه', {
            'fields': ('shipping_cost', 'free_shipping_threshold', 'tax_percentage')
        }),
    )


class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'active', 'updated_at')
    list_filter = ('active', 'updated_at')
    list_editable = ('active',)
    search_fields = ('title', 'content', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'content', 'active')
        }),
        ('تنظیمات سئو', {
            'classes': ('collapse',),
            'fields': ('seo_title', 'seo_keywords', 'seo_description')
        }),
    )


# Register your models here.
admin.site.register(ProductPackage, ProductPackageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(BaseColor, BaseColorAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(BaseCategorys, BaseCategorysAdmin)
admin.site.register(HomeSlider, HomeSliderAdmin)
admin.site.register(PromotionalBanner, PromotionalBannerAdmin)
admin.site.register(FeaturedBrand, FeaturedBrandAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(StaticPage, StaticPageAdmin)