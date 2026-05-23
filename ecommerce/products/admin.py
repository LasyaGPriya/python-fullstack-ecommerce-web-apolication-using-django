from django.contrib import admin
from .models import Category, Product, Review, Wishlist

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created', 'updated']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created', 'comment_preview']
    list_filter = ['created', 'rating']
    readonly_fields = ['user', 'created']
    
    def comment_preview(self, obj):
        """Show preview of comment"""
        if obj.comment:
            return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
        return '(No comment)'
    comment_preview.short_description = 'Comment'

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_count', 'created', 'updated']
    readonly_fields = ['created', 'updated']
    
    def product_count(self, obj):
        """Show count of products in wishlist"""
        return obj.products.count()
    product_count.short_description = 'Products in Wishlist'

