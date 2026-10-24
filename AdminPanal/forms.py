from django import forms

from FeaturesApp.models import Product

class AdminProductForms(forms.ModelForm):

    class Meta:
        model = Product
        fields=['category', 'name', 'description', 'original_price', 'discount', 'image', 'unit', 'stock', 'is_organic' ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-2.5 rounded-xl border border-zinc-300 focus:border-green-900 outline-none focus:ring-1 focus:ring-green-900 transition-all"
            }),

            "category": forms.Select(attrs={
                "class": "w-full px-4 py-2.5 rounded-xl border border-zinc-300 bg-white focus:border-green-900 outline-none focus:ring-1 focus:ring-app-green transtion-all bg-white",
                'empty_label':"Select a category"
            }),

            "original_price": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2.5 rounded-xl border border-zinc-300 focus:border-green-900 outline-none focus:ring-1 focus:ring-app-green transtion-all",
                "step":'0.01',
                'min':'0',
            }),

            "discount": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2.5 rounded-xl border border-zinc-300 focus:border-green-900 outline-none focus:ring-1 focus:ring-app-green transtion-all",
                "step":'0.01',
                'min':'0',
                'max':'100',
            }),

            "unit": forms.TextInput(attrs={
                "class": "w-full px-4 py-2.5 rounded-xl border border-zinc-300 focus:border-green-900 outline-none focus:ring-1 focus:ring-app-green transtion-all",
                'placeholder':"e.g., kg, piece, liter",
            }),

            "stock": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2.5 rounded-xl border border-zinc-300 focus:border-green-900 outline-none focus:ring-1 focus:ring-app-green transtion-all",
                "step":'1',
                'min':'0',
            }),

            "image": forms.FileInput(attrs={
                "class": "w-full px-4 py-2.5 rounded-xl border border-zinc-300 focus:border-green-900 outline-none transition-all file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-orange-400 file:text-white hover:file:bg-orange-600 cursor-pointer"
            }),

            "description": forms.Textarea(attrs={
                "rows": 4,
                "class": "w-full px-4 py-2.5 rounded-xl border border-zinc-300 resize-none focus:border-green-900 outline-none"
            }),

            "is_organic": forms.CheckboxInput(attrs={
                "class": "size-5"
            }),
        }