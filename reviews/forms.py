from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "title", "comment"]

        widgets = {
            "rating": forms.Select(
                choices=[
                    (5, "★★★★★ - Excellent"),
                    (4, "★★★★ - Good"),
                    (3, "★★★ - Average"),
                    (2, "★★ - Poor"),
                    (1, "★ - Very poor"),
                ]
            ),
            "title": forms.TextInput(attrs={
                "placeholder": "Give your review a title"
            }),
            "comment": forms.Textarea(attrs={
                "placeholder": "Share your experience with this product",
                "rows": 4
            }),
        }

    def clean_comment(self):
        comment = self.cleaned_data["comment"].strip()

        if not comment:
            raise forms.ValidationError(
                "Please write something about the product."
            )

        return comment
