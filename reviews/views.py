from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from FeaturesApp.models import Product
from .forms import ReviewForm
from .models import Review, HelpfulVote


def product_reviews(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    reviews = (
        Review.objects.filter(product=product)s
        .select_related("user")
        .annotate(helpful_count=Count("helpful_votes"))
        .order_by("-created_at")
    )

    rating_summary = Review.objects.filter(
        product=product
    ).aggregate(
        average=Avg("rating"),
        total=Count("id")
    )

    distribution = {
        row["rating"]: row["count"]
        for row in Review.objects.filter(product=product)
        .values("rating")
        .annotate(count=Count("id"))
    }

    user_review = None
    voted_review_ids = set()

    if request.user.is_authenticated:
        user_review = Review.objects.filter(
            product=product,
            user=request.user
        ).first()

        voted_review_ids = set(
            HelpfulVote.objects.filter(
                user=request.user,
                review__product=product
            ).values_list("review_id", flat=True)
        )

    return render(request, "reviews/product_reviews.html", {
        "product": product,
        "reviews": reviews,
        "rating_summary": rating_summary,
        "distribution": distribution,
        "user_review": user_review,
        "voted_review_ids": voted_review_ids,
    })


@login_required
def create_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    existing_review = Review.objects.filter(
        product=product,
        user=request.user
    ).first()

    if existing_review:
        messages.info(request, "You have already reviewed this product.")
        return redirect("reviews:edit", review_id=existing_review.pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user

            try:
                review.save()
                messages.success(request, "Your review has been submitted.")
                return redirect("reviews:product", product_id=product.pk)
            except Exception:
                # Handles a concurrent duplicate submission as well.
                if Review.objects.filter(
                    product=product, user=request.user
                ).exists():
                    messages.info(
                        request, "You have already reviewed this product."
                    )
                    return redirect(
                        "reviews:product", product_id=product.pk
                    )
                raise
    else:
        form = ReviewForm()

    return render(request, "reviews/review_form.html", {
        "form": form,
        "product": product,
        "page_title": "Write a review",
    })


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(
        Review, pk=review_id, user=request.user
    )

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated.")
            return redirect(
                "reviews:product", product_id=review.product_id
            )
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/review_form.html", {
        "form": form,
        "product": review.product,
        "review": review,
        "page_title": "Edit your review",
    })


@login_required
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(
        Review, pk=review_id, user=request.user
    )
    product_id = review.product_id
    review.delete()

    messages.success(request, "Your review has been deleted.")
    return redirect("reviews:product", product_id=product_id)


@login_required
@require_POST
def toggle_helpful(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if review.user_id == request.user.id:
        messages.info(request, "You cannot vote on your own review.")
        return redirect("reviews:product", product_id=review.product_id)

    vote, created = HelpfulVote.objects.get_or_create(
        review=review,
        user=request.user
    )

    if not created:
        vote.delete()
        messages.success(request, "Helpful vote removed.")
    else:
        messages.success(request, "Marked as helpful.")

    return redirect("reviews:product", product_id=review.product_id)
