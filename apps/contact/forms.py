from django import forms

from .models import ContactSubmission

INPUT_CLASSES = (
    "mt-1 block w-full rounded-md border border-neutral-300 px-3 py-2 text-sm "
    "shadow-sm focus:border-neutral-500 focus:outline-none focus:ring-1 "
    "focus:ring-neutral-500"
)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASSES}),
            "phone": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "message": forms.Textarea(attrs={"class": INPUT_CLASSES, "rows": 5}),
        }
