from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Category, Product, Review, Wishlist
from .forms import ReviewForm


def product_list(request, category_slug=None):
    """Display list of products with filtering and search"""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).prefetch_related('reviews')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Sort functionality
    sort = request.GET.get('sort', '-created')
    if sort in ['-created', 'price', '-price', '-rating']:
        if sort == '-rating':
            # Custom sort by average rating (handled in template context)
            pass
        else:
            products = products.order_by(sort)
        
    return render(request, 'products/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query,
        'sort': sort
    })


def product_detail(request, id, slug):
    """Display detailed product information with reviews and ratings"""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    reviews = product.reviews.all()
    review_form = ReviewForm()
    user_review = None
    
    # Check if user already reviewed this product
    if request.user.is_authenticated:
        user_review = product.reviews.filter(user=request.user).first()
    
    # Handle review form submission
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            
            # Update or create review
            Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={'rating': review.rating, 'comment': review.comment}
            )
            messages.success(request, 'Your review has been posted successfully!')
            return redirect('products:product_detail', id=product.id, slug=product.slug)
    
    # Get wishlist status if user is authenticated
    is_in_wishlist = False
    if request.user.is_authenticated:
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        is_in_wishlist = wishlist.is_product_in_wishlist(product)
    
    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'user_review': user_review,
        'is_in_wishlist': is_in_wishlist,
    }
    
    return render(request, 'products/detail.html', context)


@login_required
@require_POST
def add_to_wishlist(request, product_id):
    """Add product to user's wishlist (AJAX endpoint)"""
    try:
        product = get_object_or_404(Product, id=product_id, available=True)
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        
        if wishlist.is_product_in_wishlist(product):
            wishlist.remove_product(product)
            added = False
            message = 'Removed from wishlist'
        else:
            wishlist.add_product(product)
            added = True
            message = 'Added to wishlist'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'added': added, 'message': message})
        
        messages.success(request, message)
        return redirect('products:product_detail', id=product.id, slug=product.slug)
    
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
        messages.error(request, 'Error updating wishlist')
        return redirect('products:product_detail', id=product_id, slug=product.slug)


@login_required
def wishlist_view(request):
    """Display user's wishlist"""
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    
    return render(request, 'products/wishlist.html', {
        'wishlist_products': products,
        'total_items': products.count()
    })

