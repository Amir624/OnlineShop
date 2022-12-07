from django.contrib import admin
from .models import *

admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Variant)
admin.site.register(ProductGallery)
admin.site.register(Comment)
admin.site.register(CountViews)


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }


class ProductVariant(admin.TabularInline):
    model = Variant
    extra = 2

#
# class ProductGallery(admin.TabularInline):
#     models = ProductGallery
#

@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('title', 'total_price', 'discount', 'stock', 'available',)
    prepopulated_fields = {
        'slug': ('title',)
    }

    list_editable = ('stock',)

    inlines = [ProductVariant,  ]
