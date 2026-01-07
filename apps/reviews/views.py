"""
Product review views.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import Review, ReviewVote, ReviewImage
from .forms import ReviewForm
from apps.products.models import Product
from apps.orders.models import Order


@login_required
def create_review_view(request, product_id):
    """
    Create product review (verified buyers only).
    """
    product = get_object_or_404(Product, id=product_id)

    # Check if user purchased this product
    has_purchased = Order.objects.filter(
        user=request.user,
        items__product=product,
        status=Order.STATUS_DELIVERED
    ).exists()

    if not has_purchased:
        messages.error(request, 'You can only review products you have purchased.')
        return redirect('products:detail', slug=product.slug)

    # Check if already reviewed
    if Review.objects.filter(user=request.user, product=product).exists():
        messages.warning(request, 'You have already reviewed this product.')
        return redirect('products:detail', slug=product.slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()

            # Get the order for verification
            order = Order.objects.filter(
                user=request.user,
                items__product=product,
                status=Order.STATUS_DELIVERED
            ).first()
            review.order = order

            review.save()

            # Handle image uploads
            for f in request.FILES.getlist('images'):
                from .models import ReviewImage
                ReviewImage.objects.create(review=review, image=f)

            messages.success(request, 'Thank you for your review!  It will be published after moderation.')
            return redirect('products:detail', slug=product.slug)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'product': product,
    }

    return render(request, 'reviews/create_review.html', context)


@login_required
def vote_review_view(request, review_id):
    """
    Vote on review helpfulness (AJAX).
    """
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        vote_type = request.POST.get('vote_type')

        if vote_type not in ['helpful', 'not_helpful']:
            return JsonResponse({'success': False, 'error': 'Invalid vote type'})

        # Check if already voted
        existing_vote = ReviewVote.objects.filter(review=review, user=request.user).first()

        if existing_vote:
            # Update existing vote
            if existing_vote.vote_type != vote_type:
                # Remove old vote count
                if existing_vote.vote_type == ReviewVote.VOTE_HELPFUL:
                    review.helpful_count -= 1
                else:
                    review.not_helpful_count -= 1

                # Add new vote count
                existing_vote.vote_type = vote_type
                existing_vote.save()

                if vote_type == 'helpful':
                    review.helpful_count += 1
                else:
                    review.not_helpful_count += 1

                review.save()
        else:
            # Create new vote
            ReviewVote.objects.create(
                review=review,
                user=request.user,
                vote_type=vote_type
            )

            if vote_type == 'helpful':
                review.helpful_count += 1
            else:
                review.not_helpful_count += 1

            review.save()

        return JsonResponse({
            'success': True,
            'helpful_count': review.helpful_count,
            'not_helpful_count': review.not_helpful_count,
            'helpful_percentage': review.helpful_percentage
        })

    return JsonResponse({'success': False, 'error': 'Invalid request'})