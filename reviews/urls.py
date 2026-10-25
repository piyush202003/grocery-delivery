
from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path(
        "product/<int:product_id>/",
        views.product_reviews,
        name="product"
    ),
    path(
        "product/<int:product_id>/write/",
        views.create_review,
        name="create"
    ),
    path(
        "edit/<int:review_id>/",
        views.edit_review,
        name="edit"
    ),
    path(
        "delete/<int:review_id>/",
        views.delete_review,
        name="delete"
    ),
    path(
        "helpful/<int:review_id>/",
        views.toggle_helpful,
        name="helpful"
    ),
]
