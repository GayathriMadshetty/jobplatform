from django import forms
from .models import Job, Profile, Application
class JobForm(forms.ModelForm):
    class Meta: model = Job; fields = ["title","company","location","job_type","remote","salary","skills","description"]
class ProfileForm(forms.ModelForm):
    class Meta: model = Profile; fields = ["headline","resume_text","skills"]
class ApplyForm(forms.ModelForm):
    class Meta: model = Application; fields = ["cover_note"]
