from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import *
from seeker.models import ScheduleMeeting
from django.utils.translation import gettext_lazy as _


class Provider_SignUp_Form(UserCreationForm):
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


class Provider_Verify_Email_Form(forms.Form):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
        'placeholder' : "Enter your Email",
        'class' : "form-control"
    }))


class Provider_ForgotPassword_Form(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control',}))
    class Meta:
        model = User
        fields = ['email']


class Provider_OtpVerify_Form(forms.Form):
     otp = forms.CharField(required=True, error_messages={'required':'Please enter OTP'} ,max_length=6, widget=forms.TextInput(
        attrs={'class': 'form-control'}))


class Provider_Login_Form(AuthenticationForm):
    username = forms.CharField(required=True,label="Username",widget=forms.TextInput(attrs={'class':"form-control"}))
    password = forms.CharField(required=True,label="Password",widget=forms.PasswordInput(attrs={'class':"form-control"}))
    class Meta:
        model = User
        Fields = ['username','password']


class Provider_UserForm(forms.ModelForm):
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


class Provider_ProfileForm(forms.ModelForm):
    class Meta:
        model = Provider_Profile_Model
        fields = ['avatar', 'fname', 'lname', 'tel', 'gender', 'age', 'address', 'area', 'c_name', 'c_email', 'c_website', 'c_descrip']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class':'profile_img img-fluid form-control',
                'label': 'Profile Image',
            }),
            'fname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'First Name',
                'label': 'First Name',
            }),
            'lname': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Last Name',
                'label': 'Last Name',
            }),
            'area': forms.Select(attrs={
                'class':'wide form-control',
                'placeholder':'Area',
                'label': 'Area',
            }),
            'gender' : forms.Select(attrs={
                'class':'wide form-control',
                'label': 'Gender',
            }),
            'age' : forms.NumberInput(attrs={
                'class':'form-control',
                'label': 'Age',
            }),
            'tel' : forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Phone Number',
                'label': 'Phone Number',
            }),
            'address' : forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Address',
                'rows': 4, 'cols': 60,
                'label': 'Address',
            }),
            'c_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name',
                'label': 'Company Name',
            }),
            'c_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Email',
                'label': 'Company Email',
            }),
            'c_website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Website',
                'label': 'Company Website',
            }),
            'c_descrip': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Company Description',
                'rows': 4, 'cols': 60,
                'label': 'Company Description',
            }),
        }
        labels = {
            'avatar': 'Profile Picture',
            'fname': 'First Name',
            'lname': 'Last Name',
            'tel': 'Phone Number',
            'gender': 'Gender',
            'age': 'Age',
            'address': 'Address',
            'area': 'Area',
            'c_name': 'Company Name',
            'c_email': 'Company Email',
            'c_website': 'Company Website',
            'c_descrip': 'Company Description',
        }

class PostJobForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True, label_suffix="", label="Job title", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter job title',
    }))
    description = forms.CharField(required=True, label_suffix="",label="Job description", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter job description',
        'rows': 5
    }))
    category = forms.ModelChoiceField(queryset=JobCategory.objects.all(), empty_label="Select category", required=True,label_suffix="", label="Job category", widget=forms.Select(attrs={
        'class': 'wide form-control',
    }))
    location = forms.ModelChoiceField(queryset=city_data.objects.all(), empty_label="Select location", required=True,label_suffix="", label="Job location", widget=forms.Select(attrs={
        'class': 'wide form-control',
    }))
    salary_min = forms.IntegerField(min_value=0, required=False,label_suffix="", label="Minimum salary", widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter minimum salary',
    }))
    salary_max = forms.IntegerField(min_value=0, required=False, label_suffix="",label="Maximum salary", widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter maximum salary',
    }))
    experience_years = forms.DecimalField(max_digits=4, decimal_places=1, min_value=0, required=False, label_suffix="",label="Experience (in years)", widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter experience in years',
    }))
    skills_required = forms.CharField(required=True, label_suffix="", label="Required Skills", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Skills which are required',
    }))
    class Meta:
        model = PostJob
        fields = ['title', 'description', 'category', 'location', 'salary_min', 'salary_max', 'experience_years','skills_required']
        labels = {
            'title': 'Job Title',
            'description': 'Job Description',
            'category': 'Job Category',
            'location': 'Job Location',
            'salary_min': 'Minimum Salary',
            'salary_max': 'Maximum Salary',
            'experience_years': 'Experience (in years)',
            'skills_required' : 'Requiered Skills'
        }

class ScheduleMeetingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control datepicker'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time','class': 'form-control timepicker'}))
    location = forms.CharField(max_length=300, label=_("Location"), required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)

    class Meta:
        model = ScheduleMeeting
        fields = ['date', 'time', 'location', 'notes']

    def __init__(self, *args, **kwargs):
        company_profile = kwargs.pop('company_profile')
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['placeholder'] = _("Select a date")
        self.fields['time'].widget.attrs['placeholder'] = _("Select a time")
        self.fields['location'].widget.attrs['placeholder'] = _("Enter the location of the meeting")
        self.fields['location'].initial = company_profile.address + ' , ' + str(company_profile.area)