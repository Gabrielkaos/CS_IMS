from django import forms
from .models import Student


class UploadFileForm(forms.Form):
    files = forms.FileField()

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'current_province_code': forms.Select(),
            'current_city_code': forms.Select(),
            'current_barangay_code': forms.Select(),
            'permanent_province_code': forms.Select(),
            'permanent_city_code': forms.Select(),
            'permanent_barangay_code': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        provinces = kwargs.pop('provinces', [])

        super().__init__(*args, **kwargs)
        
        self.fields['date_of_birth'].input_formats = ['%Y-%m-%d']
        province_choices = [('', 'Select Province')] + [(p['code'], p['name']) for p in provinces]
        
        self.fields['current_province_code'].choices = province_choices
        self.fields['permanent_province_code'].choices = province_choices

        # Leave city/barangay blank initially, they’ll be filled by JS
        self.fields['current_city_code'].choices = [('', 'Select City/Municipality')]
        self.fields['current_barangay_code'].choices = [('', 'Select Barangay')]
        self.fields['permanent_city_code'].choices = [('', 'Select City/Municipality')]
        self.fields['permanent_barangay_code'].choices = [('', 'Select Barangay')]

