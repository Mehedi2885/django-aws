from .models import Student
from django import forms


class StudentForm(forms.ModelForm):

    def clean_marks(self):
        input_marks = self.cleaned_data['marks']
        if input_marks < 35:
            raise forms.ValidationError('Marks should be >= 35')
        return input_marks

    class Meta:
        model = Student
        fields = '__all__'
