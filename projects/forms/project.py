from django import forms

from projects.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name",)
        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }
