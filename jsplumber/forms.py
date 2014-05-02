from django import forms
from jsplumber.models import PlumbElement

#from django.contrib.admin.widgets import AdminDateWidget
#from django.utils.translation import ugettext_lazy as _


class EditElementForm(forms.ModelForm):

    class Meta:
        model = PlumbElement
        exclude = ['id', 'created', 'modified']
