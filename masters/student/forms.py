from django import forms
from professor.models import Professor, ProfessorFields
from phonenumber_field.formfields import PhoneNumberField
from system.models import Group, Orientation, User
from student.models import Dissertation, DissertationReport, AchievementReport
from django.core.exceptions import ValidationError
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


# from ckeditor.fields import RichTextFormField

class DissertationForm(forms.ModelForm):
    class Meta:
        model  = Dissertation
        fields = ['title', 'description', 'docfile']

    # def __init__(self, *args, **kwargs):
    #     super(DissertationForm, self).__init__(*args, **kwargs)
    #     self.fields['jury_date'] = JalaliDateField(# date format is  "yyyy-mm-dd"
    #         widget=AdminJalaliDateWidget # optional, to use default datepicker
    #     )

        # you can added a "class" to this field for use your datepicker!
        # self.fields['date'].widget.attrs.update({'class': 'jalali_date-date'})


class DRForm(forms.ModelForm):
    class Meta:
        model  = DissertationReport
        fields = ['title', 'summary', 'problems', 'proceedings',]

