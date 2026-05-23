from django.core.management.base import BaseCommand
from django.db import IntegrityError
from products.models import Category, Product, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with dummy categories, products, and reviews'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')

        try:
            # Categories - safely create with get_or_create
            cat_electronics, created = Category.objects.get_or_create(
                slug='electronics',
                defaults={'name': 'Electronics'}
            )
            if created:
                self.stdout.write(self.style.SUCCESS('✓ Created category: Electronics'))
            else:
                self.stdout.write(self.style.WARNING('✓ Category Electronics already exists (skipped)'))

            cat_clothing, created = Category.objects.get_or_create(
                slug='clothing',
                defaults={'name': 'Clothing'}
            )
            if created:
                self.stdout.write(self.style.SUCCESS('✓ Created category: Clothing'))
            else:
                self.stdout.write(self.style.WARNING('✓ Category Clothing already exists (skipped)'))

            cat_books, created = Category.objects.get_or_create(
                slug='books',
                defaults={'name': 'Books'}
            )
            if created:
                self.stdout.write(self.style.SUCCESS('✓ Created category: Books'))
            else:
                self.stdout.write(self.style.WARNING('✓ Category Books already exists (skipped)'))

            # Products
            products = [
                {
                    'category': cat_electronics,
                    'name': 'Smartphone X',
                    'slug': 'smartphone-x',
                    'description': 'Latest smartphone with amazing features and camera.',
                    'price': 699.99,
                    'stock': 50
                },
                {
                    'category': cat_electronics,
                    'name': 'Wireless Headphones',
                    'slug': 'wireless-headphones',
                    'description': 'Noise-cancelling wireless headphones with 20h battery life.',
                    'price': 199.99,
                    'stock': 100
                },
                {
                    'category': cat_clothing,
                    'name': 'Cotton T-Shirt',
                    'slug': 'cotton-t-shirt',
                    'description': 'Comfortable 100% cotton t-shirt.',
                    'price': 19.99,
                    'stock': 200
                },
                {
                    'category': cat_clothing,
                    'name': 'Denim Jeans',
                    'slug': 'denim-jeans',
                    'description': 'Classic blue denim jeans.',
                    'price': 49.99,
                    'stock': 150
                },
                {
                    'category': cat_books,
                    'name': 'Django for Beginners',
                    'slug': 'django-for-beginners',
                    'description': 'Learn to build web applications with Django.',
                    'price': 39.99,
                    'stock': 75
                },
                {
                    'category': cat_books,
                    'name': 'Python Crash Course',
                    'slug': 'python-crash-course',
                    'description': 'A hands-on, project-based introduction to programming.',
                    'price': 29.99,
                    'stock': 120
                }
            ]

            created_count = 0
            skipped_count = 0
            products_list = []

            for p_data in products:
                try:
                    product, created = Product.objects.get_or_create(
                        slug=p_data['slug'],
                        defaults=p_data
                    )
                    products_list.append(product)
                    if created:
                        created_count += 1
                        self.stdout.write(self.style.SUCCESS(f'✓ Created product: {p_data["name"]}'))
                    else:
                        skipped_count += 1
                        self.stdout.write(self.style.WARNING(f'✓ Product "{p_data["name"]}" already exists (skipped)'))
                except IntegrityError as e:
                    self.stdout.write(self.style.WARNING(f'⚠ Skipped "{p_data["name"]}": {str(e)[:50]}'))
                    skipped_count += 1

            # Create sample users for reviews
            sample_users = []
            user_data = [
                {'username': 'john_doe', 'email': 'john@example.com'},
                {'username': 'jane_smith', 'email': 'jane@example.com'},
                {'username': 'mike_johnson', 'email': 'mike@example.com'},
                {'username': 'sarah_williams', 'email': 'sarah@example.com'},
            ]
            
            for user_info in user_data:
                user, created = User.objects.get_or_create(
                    username=user_info['username'],
                    defaults={'email': user_info['email']}
                )
                sample_users.append(user)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Created sample user: {user_info["username"]}'))

            # Add sample reviews to products
            reviews_data = [
                {'product_idx': 0, 'user_idx': 0, 'rating': 5, 'comment': 'Amazing smartphone! Best camera I have ever seen.'},
                {'product_idx': 0, 'user_idx': 1, 'rating': 4, 'comment': 'Great phone but a bit expensive.'},
                {'product_idx': 0, 'user_idx': 2, 'rating': 5, 'comment': 'Worth every penny. Highly recommended!'},
                {'product_idx': 0, 'user_idx': 3, 'rating': 4, 'comment': 'Good performance, battery life could be better.'},
                
                {'product_idx': 1, 'user_idx': 0, 'rating': 5, 'comment': 'Perfect sound quality with noise cancellation.'},
                {'product_idx': 1, 'user_idx': 1, 'rating': 4, 'comment': 'Comfortable to wear for long periods.'},
                {'product_idx': 1, 'user_idx': 2, 'rating': 5, 'comment': 'Best headphones in this price range!'},
                
                {'product_idx': 2, 'user_idx': 0, 'rating': 5, 'comment': 'Very soft and comfortable cotton material.'},
                {'product_idx': 2, 'user_idx': 1, 'rating': 4, 'comment': 'Good quality but sizing runs a bit small.'},
                {'product_idx': 2, 'user_idx': 3, 'rating': 5, 'comment': 'Love the fit and feel. Great value!'},
                
                {'product_idx': 3, 'user_idx': 0, 'rating': 5, 'comment': 'Perfect fit and excellent quality denim.'},
                {'product_idx': 3, 'user_idx': 2, 'rating': 4, 'comment': 'Classic style, very durable.'},
                {'product_idx': 3, 'user_idx': 3, 'rating': 5, 'comment': 'Best jeans I own. Highly recommend!'},
                
                {'product_idx': 4, 'user_idx': 0, 'rating': 5, 'comment': 'Great resource for learning Django. Clear and concise.'},
                {'product_idx': 4, 'user_idx': 1, 'rating': 4, 'comment': 'Very helpful but could use more advanced examples.'},
                
                {'product_idx': 5, 'user_idx': 2, 'rating': 5, 'comment': 'Excellent hands-on introduction to Python!'},
                {'product_idx': 5, 'user_idx': 3, 'rating': 5, 'comment': 'Perfect for beginners. Highly engaging content.'},
            ]
            
            review_count = 0
            for review_data in reviews_data:
                try:
                    if review_data['product_idx'] < len(products_list):
                        product = products_list[review_data['product_idx']]
                        user = sample_users[review_data['user_idx']]
                        
                        review, created = Review.objects.get_or_create(
                            product=product,
                            user=user,
                            defaults={
                                'rating': review_data['rating'],
                                'comment': review_data['comment']
                            }
                        )
                        if created:
                            review_count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠ Could not create review: {str(e)[:50]}'))
            
            if review_count > 0:
                self.stdout.write(self.style.SUCCESS(f'✓ Added {review_count} sample reviews'))

            self.stdout.write(self.style.SUCCESS(f'\n✅ Done! Created Products: {created_count}, Skipped: {skipped_count}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
            self.stdout.write(self.style.ERROR('Your existing products are safe - no data was deleted.'))
