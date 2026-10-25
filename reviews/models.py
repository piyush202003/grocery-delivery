from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from FeaturesApp.models import Product


class Review(models.Model):
    product = models.ForeignKey(
        Product,  # Change "products" to your app label
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="product_reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    title = models.CharField(max_length=150, blank=True)
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "user"],
                name="unique_product_review_per_user"
            )
        ]

    def __str__(self):
        return f"{self.product} - {self.rating}/5 by {self.user}"


class HelpfulVote(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="helpful_votes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_votes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["review", "user"],
                name="unique_helpful_vote_per_user"
            )
        ]

    def __str__(self):
        return f"{self.user} found review {self.review_id} helpful"
