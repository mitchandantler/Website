from django import forms


class MenuImportForm(forms.Form):
    csv_file = forms.FileField(label="Menu CSV file")
