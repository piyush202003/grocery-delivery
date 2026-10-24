from django import forms

from accounts.models import Address


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['label', 'address', 'city', 'state', 'zip', 'is_default', 'lat', 'lng']

        widgets = {
            'label' : forms.TextInput(attrs={
                'class' : "w-full px-4 py-2.5 text-sm rounded-xl border border-zinc-300 focus:border-green-900 outline-none",
                'placeholder' : "Home, Work, etc.", 
            }),
            'address' : forms.TextInput(attrs={
                'class' : "w-full px-4 py-2.5 text-sm rounded-xl border border-zinc-300 focus:border-green-900 outline-none",
            }),
            'city' : forms.TextInput(attrs={
                'placeholder' : "Mumbai, Pune, etc.",
                'class' : "w-full px-4 py-2.5 text-sm rounded-xl border border-zinc-300 focus:border-green-900 outline-none",
            }),
            'state' : forms.TextInput(attrs={
                'placeholder' : "Maharashtra, Delhi, etc.",
                'class' : "w-full px-4 py-2.5 text-sm rounded-xl border border-zinc-300 focus:border-green-900 outline-none",
            }),
            'zip' : forms.TextInput(attrs={
                'placeholder' : "6-Digit code of city", 
                'class' : "w-full px-4 py-2.5 text-sm rounded-xl border border-zinc-300 focus:border-green-900 outline-none",
                'maxlength': 6,
            }),
            'is_default' : forms.CheckboxInput(attrs={
                'class' : 'size-5 rounded border-zinc-300 text-green-900 focus:ring-green-900 cursor-pointer',
            }),
            'lat' : forms.HiddenInput(),
            'lng' : forms.HiddenInput(),
        }