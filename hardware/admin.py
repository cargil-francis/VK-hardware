from django.contrib import admin
from .models import Category, Product, Cart,Order,Userdetails

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category_image', 'gst_tax','is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title", )}



class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'product_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'category', 'short_description')
    prepopulated_fields = {"slug": ("title", )}

   




admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Userdetails)