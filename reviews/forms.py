from django import forms
from matplotlib.pyplot import cla
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
                ], attrs={
                    "class": "w-full px-4 py-2.5 text-sm rounded-xl border border-zinc-300 focus:border-green-900 outline-non"
                }
            ),
            "title": forms.TextInput(attrs={
                "placeholder": "Give your review a title",
                "class" : 'w-full px-4 py-2.5 text-sm rounded-xl border border-zinc-300 focus:border-green-900 outline-non'
            }),
            "comment": forms.Textarea(attrs={
                "placeholder": "Share your experience with this product",
                "rows": 4,
                "class": "w-full px-4 py-2.5 text-sm rounded-xl border border-zinc-300 focus:border-green-900 outline-non"
            }),
        }

    def clean_comment(self):
        comment = self.cleaned_data["comment"].strip()

        if not comment:
            raise forms.ValidationError(
                "Please write something about the product."
            )

        return comment
