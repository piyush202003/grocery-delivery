from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from FeaturesApp.models import Product
from reviews.forms import ReviewForm
from reviews.models import Review

def get_rating_breakdown(ratings):
    counts = [0, 0, 0, 0, 0]

    for rating in ratings:
        if rating is not None and 1 <= rating <= 5:
            counts[rating - 1] += 1

    return counts[::-1]

@login_required
def create_review(request, product_id):
    product = Product.objects.filter(pk=product_id).first()
    if not product:
        messages.error(request, 'Product did not found')
        return redirect('ProductPage', pdid=product_id)

    existing_review = Review.objects.filter(
        product=product,
        user=request.user
    ).first()
    if existing_review:
        messages.info(request, 'You have already reviewed this product.')
        return edit_review(request, review_id=existing_review.pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user

            try:
                review.save()
                messages.success(request, 'Your review has been submitted.')
                return redirect('ProductPage', pdid=product.pk)
            except Exception:
                if Review.objects.filter(
                    product=product, user=request.user
                ).exists():
                    messages.info(request, 'You have already reviewed this product.')
                    return redirect('ProductPage', pdid=product.pk)
                raise
    else:
        form = ReviewForm()

    context={
        'form':form
    }
    return context

@login_required
def edit_review(request, review_id):
    try:
        review = Review.objects.filter(user=request.user, pk=review_id).first()
    except Exception:
        messages.error(request, 'Did not found review to edit.')
        return redirect('ProductPage', pdid=review.product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated.')
            return redirect('ProductPage', pdid=review.product_id)
    else:
        form = ReviewForm(instance=review)

    context = {
        'form':form,
        'review_id':review_id
    }
    return context

