from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.utils.translation import gettext_lazy as _

class Seeker_SignUp_Form(UserCreationForm):
    password1 = forms.CharField(required=True,label="Password",widget=forms.PasswordInput(attrs={'class':"mb-0 form-control",
                'placeholder':'Enter Password'}))
    password2 = forms.CharField(required=True,label="Confirm Password",widget=forms.PasswordInput(attrs={'class':"mb-0 form-control",'placeholder':'Enter Password Again'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
                        'class':"mb-0 form-control",
                       'placeholder':'Enter Your Email'
                    }))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        widgets = {
            'username' : forms.TextInput(attrs={
                'class':"mb-0 form-control",
                'placeholder':'Enter Your Username'
            }),
        }


class Seeker_Verify_Email_Form(forms.Form):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
        'placeholder' : "Enter your Email",
        'class' : "form-control"
    }))


class Seeker_ForgotPassword_Form(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control',}))
    class Meta:
        model = User
        fields = ['email']


class Seeker_OtpVerify_Form(forms.Form):
     otp = forms.CharField(required=True, error_messages={'required':'Please enter OTP'} ,max_length=6, widget=forms.TextInput(
        attrs={'class': 'form-control'}))


class Seeker_Login_Form(AuthenticationForm):
    username = forms.CharField(required=True,label="Username",widget=forms.TextInput(attrs={'class':"form-control"}))
    password = forms.CharField(required=True,label="Password",widget=forms.PasswordInput(attrs={'class':"form-control"}))
    class Meta:
        model = User
        Fields = ['username','password']


class Seeker_UserForm(forms.ModelForm):
    username = forms.CharField(max_length=50,disabled=True,widget=forms.TextInput(
        attrs={
            'class' : 'form-control',
        }
    ))
    email = forms.EmailField(max_length=50,disabled=True,widget=forms.EmailInput(
        attrs={
            'class' : 'form-control',
        }
    ))
    class Meta:
        model = User
        fields = ['username','email']


class Seeker_ProfileForm(forms.ModelForm):
    class Meta:
        model = Seeker_Profile_Model
        fields =  ['avatar', 'fname', 'lname', 'tel', 'gender', 'age', 'address', 'area']

        widgets = {
            'avatar': forms.FileInput(attrs={
                'class':'form-control'
            }),
            'fname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'First Name'
            }),
            'lname': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Last Name'
            }),
            'area': forms.Select(attrs={
                'class':'wide form-control',
                'placeholder':'Area'
            }),
            'gender' : forms.Select(attrs={
                'class':'wide form-control',
            }),
            'age' : forms.NumberInput(attrs={
                'class':'form-control',
            }),
            'tel' : forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Phone Number',
            }),
            'address' : forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Address',
                'rows': 4, 'cols': 60
            }),
        }

class Resume_Form(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume']
        widgets = {
            'resume':forms.FileInput(attrs={
                'class':'wide form-control'
            }),
        }


class Headline_Form(forms.ModelForm):
    class Meta:
        model = Headline
        fields = ['headline']
        widgets = {
            'headline':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Headline',
                'rows': 4, 'cols': 80
            }),
        }


class Summary_Form(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ['summary']
        widgets = {
            'summary':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Summary',
                'rows': 4, 'cols': 80
            }),
        }


class Education_Form(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['user']
        widgets = {
            'education': forms.Select(attrs={
                'class': 'wide form-select'
            }),
            'course': forms.Select(attrs={
                'class': 'wide form-select'
            }),
            'specialization': forms.Select(attrs={
                'class': 'wide form-select'
            }),
            'university': forms.Select(attrs={
                'class': 'wide form-select'
            }),
            'course_type': forms.RadioSelect(attrs={
            }),
            'passing_year': forms.Select(attrs={
                'class': 'wide form-select'
            })
        }


class Project_Form(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter Project Title',
                'class': 'form-control'
            }),
            'start_month': forms.Select(attrs={
                'class': 'wide form-select'
            }),
            'start_year': forms.Select(attrs={
                'class': 'wide form-select'
            }),
            'end_month': forms.Select(attrs={
                'class': 'wide form-select'
            }),
            'end_year': forms.Select(attrs={
                'class': 'wide form-select'
            }),
            'url': forms.URLInput(attrs={
                'placeholder': 'Enter Project Url',
                'class': 'wide form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            })
        }


class Certificate_Form(forms.ModelForm):
    class Meta:
        model = Certificate
        exclude = ['user']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: Front-End Web Development',
                'class': 'form-control'
            }),
            'issuing_org': forms.TextInput(attrs={
                'placeholder': 'Ex: Coursera',
                'class': 'wide form-control'
            }),
            'issue_month': forms.Select(attrs={
                'class': 'wide form-control'
            }),
            'issue_year': forms.Select(attrs={
                'class': 'wide form-control'
            }),
            'expiry_month': forms.Select(attrs={
                'class': 'wide form-control'
            }),
            'expiry_year': forms.Select(attrs={
                'class': 'wide form-control'
            }),
            'credential_id': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'credential_url': forms.URLInput(attrs={
                'class': 'form-control'
            })
        }


class Social_Form(forms.ModelForm):
    class Meta:
        model = Social
        exclude = ['user']
        widgets = {
            'profile_name': forms.TextInput(attrs={
                'placeholder': 'Online Profile Name',
                'class': 'form-control'
            }),
            'profile_url': forms.URLInput(attrs={
                'placeholder': 'Enter Profile Url',
                'class': 'form-control'
            }),
            'profile_des': forms.Textarea(attrs={
                'placeholder': 'Enter Profile Description',
                'class': 'form-control',
                'rows': 4
            })
        }

class Skill_Form(forms.ModelForm):
    class Meta:
        model = Skills
        exclude = ['user']
        widgets = {
            'skill': forms.TextInput(attrs={
                'placeholder': 'Enter your Skills',
                'class': 'form-control'
            }),
        }

class ApplyJobForm(forms.ModelForm):
    name = forms.CharField(max_length=50, label=_("Full Name"), required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=50, label=_("Email"), required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=10, label=_("Phone"), required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    resume = forms.FileField(label=_("Resume"), required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))


    class Meta:
        model = ApplyJob
        fields = ['name', 'email', 'phone', 'resume']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = _("Enter your full name")
        self.fields['email'].widget.attrs['placeholder'] = _("Enter your email address")
        self.fields['phone'].widget.attrs['placeholder'] = _("Enter your phone number")
        self.fields['resume'].widget.attrs['accept'] = ".pdf,.doc,.docx,.rtf"

    def clean_resume(self):
        resume = self.cleaned_data['resume']
        if resume:
            content_type = resume.content_type.split('/')[0]
            if content_type != 'application':
                raise forms.ValidationError(_("Invalid file type. Please upload a PDF, DOC, DOCX or RTF file."))
        return resume

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label,
            })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('.com'):
            raise forms.ValidationError('Please enter a valid email address.')
        return email
