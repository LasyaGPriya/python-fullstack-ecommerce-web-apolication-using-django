from django.db import models
from django.conf import settings
from django.db.models import Avg

class Category(models.Model):
    """Product category model"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model with ratings and reviews support"""
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    stock = models.PositiveIntegerField(default=10)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_average_rating(self):
        """Calculate average rating from all reviews"""
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

    def get_review_count(self):
        """Get total number of reviews"""
        return self.reviews.count()

    def get_rating_percentage(self, stars):
        """Get percentage of reviews with specific star rating"""
        total = self.reviews.count()
        if total == 0:
            return 0
        count = self.reviews.filter(rating=stars).count()
        return (count / total) * 100


class Review(models.Model):
    """Review model for product ratings and feedback"""
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        unique_together = ('product', 'user')  # One review per user per product

    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'


class Wishlist(models.Model):
    """Wishlist model for saving favorite products"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='wishlist', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlist_items', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Wishlist for {self.user.username}'

    def add_product(self, product):
        """Add product to wishlist"""
        self.products.add(product)

    def remove_product(self, product):
        """Remove product from wishlist"""
        self.products.remove(product)

    def is_product_in_wishlist(self, product):
        """Check if product is in wishlist"""
        return self.products.filter(id=product.id).exists()
