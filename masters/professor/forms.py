from django import forms
from phonenumber_field.formfields import PhoneNumberField
from professor.models import Professor, ProfessorFields, MasterRequest


class ProfessorForm(forms.ModelForm):


    class Meta:
        model  = Professor
        fields = ['first_name', 'last_name', 'username', 'n_code', 'email', 'phone', 'gender']


    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name.isdigit():
            raise forms.ValidationError('نوع ورودی نامعتبر')
        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name.isdigit():
            raise forms.ValidationError('نوع ورودی نامعتبر')
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) != 10:
            raise forms.ValidationError('شماره دانشجویی ۱۰ رقم است!')
        if not username.isdigit():
            raise forms.ValidationError('شماره دانشجویی عدد است!')
        return username

    def clean_n_code(self):
        n_code = self.cleaned_data.get('n_code')
        if len(n_code) != 10:
            raise forms.ValidationError('کدملی ۱۰ رقم است!')
        if not n_code.isdigit():
            raise forms.ValidationError('کدملی عدد است!')
        return n_code


class PFForm(forms.ModelForm):
    class Meta:
        model  = ProfessorFields
        fields = ['grade', 'last_university']

class MRForm(forms.ModelForm):
    class Meta:
        model  = MasterRequest
        fields = ['type_1', 'type_2']

    def clean_type_1(self):
        type_1 = self.cleaned_data.get('type_1')
        # if not type_1.isdigit():
        #     raise forms.ValidationError('لطفا عدد وارد کنید')
        if type_1 > 15:
            raise forms.ValidationError('بیشتر از حد مجاز')
        return type_1



    def clean_type_2(self):
        type_2 = self.cleaned_data.get('type_2')
        # if not type_2.isdigit():
        #     raise forms.ValidationError('لطفا عدد وارد کنید')
        if type_2 > 15:
            raise forms.ValidationError('بیشتر از حد مجاز')
        return type_2

# class StudentForm(forms.ModelForm):

#     # GENDER = (
#     #     ('female', 'مونث'),
#     #     ('male', 'مذکر'),
#     #     ('none', 'سایر'),
#     # )

#     # first_name = forms.CharField(label='نام', max_length=30, required=True)
#     # last_name  = forms.CharField(label='نام خانوادگی', max_length=30, required=True)
#     # username   = forms.CharField(label='نام کاربری(کد دانشجویی، کد پرسنلی)', max_length=30, required=False)
#     # n_code     = forms.CharField(label='کد ملی', required=True)
#     # email      = forms.EmailField(label='ایمیل', required=True)
#     # phone      = PhoneNumberField(required=True, required=True)
#     # college    = forms.CharField(max_length=20, required=True)
#     # item_type  = forms.CharField(max_length=10, required=True)
#     # gender     = forms.ChoiceField(choices=GENDER, required=True)


#     class Meta:
#         model  = Student
#         fields = ['first_name', 'last_name', 'username', 'n_code', 'email', 'phone', 'college', 'item_type', 'gender']
#         # fields = "__all__"

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if len(username) != 10:
#             raise forms.ValidationError('شماره دانشجویی ۱۰ رقم است!')
#         if not username.isdigit():
#             raise forms.ValidationError('شماره دانشجویی عدد است!')
#         return username

#     def clean_n_code(self):
#         n_code = self.cleaned_data.get('n_code')
#         if len(n_code) != 10:
#             raise forms.ValidationError('کدملی ۱۰ رقم است!')
#         if not n_code.isdigit():
#             raise forms.ValidationError('کدملی عدد است!')
#         return n_code


# class SFForm(forms.Form):
#     class Meta:
#         model  = StudentFields
#         fields = ['is_daily', 'last_university']


# class UserUpdateForm(UserForm):
#     about_me = RichTextFormField(max_length=700)

#     def __init__(self, *args, **kwargs):
#         super(UserUpdateForm, self).__init__(*args, **kwargs)
#         self.fields['email'].disabled = True
#         # self.fields.pop('password')

#     class Meta(UserForm.Meta):
#         fields = ['about_me', 'first_name', 'last_name', 'username', 'email', 'gender']

# class AvatarUpdateForm(forms.ModelForm):
#     class Meta:
#         model  = AvatarModel
#         fields = ['avatar']


# class ResetPasswordForm(forms.Form):
#     password       = forms.CharField(widget=forms.PasswordInput())
#     password_check = forms.CharField(widget=forms.PasswordInput())


#     def clean(self):
#         cleaned_data   = super().clean()
#         password       = cleaned_data.get('password')
#         password_check = cleaned_data.get('password_check')

#         if len(password) < 8:
#             raise forms.ValidationError('حداقل ۸ کاراکتر لازمه...')


#         if password != password_check:
#             raise forms.ValidationError('گذرواژه ها با هم همخوان نیست...')


#         # check for digit
#         if not any(char.isdigit() for char in password):
#             raise forms.ValidationError(('حداقل ۱ عدد باید داشته باشه...'))

#         # check for letter
#         if not any(char.isalpha() for char in password):
#             raise forms.ValidationError(('...حداقل ۱ حرف باید داشته باشه'))

#         return password

        


# class GetEmailForm(forms.Form):
#     email = forms.EmailField(required=True)