from django.forms import ModelForm
from db.models import *

class SubmitRequest(ModelForm):
    class Meta:
        model = TutorRequest
