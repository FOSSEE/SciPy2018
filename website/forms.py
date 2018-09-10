from django import forms

from django.forms import ModelForm, widgets

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MinValueValidator, \
    RegexValidator, URLValidator
from captcha.fields import ReCaptchaField
from string import punctuation, digits
try:
    from string import letters
except ImportError:
    from string import ascii_letters as letters

from website.models import Proposal, PaymentDetails
from website.send_mails import generate_activation_key
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from website.models import (
    Profile, User
)

UNAME_CHARS = letters + "._" + digits
PWD_CHARS = letters + punctuation + digits

MY_CHOICES = (
    ('Beginner', 'Beginner'),
    ('Advanced', 'Advanced'),
)

ws_duration = (
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
)
abs_duration = (
    ('15', '15'),
    ('30', '30'),
)

t_shirt_size = (
    ("None", "Select size"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("XXL", "XXL"),
)

gender = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)

MY_CHOICES = (
    ('Beginner', 'Beginner'),
    ('Advanced', 'Advanced'),
)
rating = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
)

CHOICES = [('Yes', 'Yes'),
           ('No', 'No')]

accomodation_choice = (
    ('Yes', 'Yes'),
    ('No', 'No')
)

attending_job_fair = (
    ("No", "No"),
    ("Yes", "Yes"),
)

want_tshirt = (
    ("No", "No"),
    ("Yes", "Yes"),
)

attendee_type_choices = (
    ("Student-750", "Student (Rs 750)"),
    ("Faculty-1000", "Faculty (Rs 1,000)"),
    ("Industry participant-2000", "Industry participant (Rs 2,000)"),
)

ticket_type = (

    ("Regular registration", "Regular registration"),
    ("Late registration", "Late registration")

)

source = (
    ("Poster", "Poster"),
    ("FOSSEE website", "FOSSEE website"),
    ("Google", "Google"),
    ("Social Media", "Social Media"),
    ("From other College", "From other College"),
)

title = (
    ("Mr", "Mr."),
    ("Miss", "Ms."),
    ("Professor", "Prof."),
    ("Doctor", "Dr."),
)
states = (
    ("",    "Select your State"),
    ("Andhra Pradesh",    "Andhra Pradesh"),
    ("Arunachal Pradesh",    "Arunachal Pradesh"),
    ("Assam",    "Assam"),
    ("Bihar",    "Bihar"),
    ("Chhattisgarh",    "Chhattisgarh"),
    ("Goa",    "Goa"),
    ("Gujarat",    "Gujarat"),
    ("Haryana",    "Haryana"),
    ("Himachal Prades",    "Himachal Pradesh"),
    ("Jammu and Kashmir",    "Jammu and Kashmir"),
    ("Jharkhand",    "Jharkhand"),
    ("Karnataka",    "Karnataka"),
    ("Kerala",    "Kerala"),
    ("Madhya Pradesh",    "Madhya Pradesh"),
    ("Maharashtra",    "Maharashtra"),
    ("Manipur",    "Manipur"),
    ("Meghalaya",    "Meghalaya"),
    ("Mizoram",    "Mizoram"),
    ("Nagaland",    "Nagaland"),
    ("Odisha",    "Odisha"),
    ("Punjab",    "Punjab"),
    ("Rajasthan",    "Rajasthan"),
    ("Sikkim",    "Sikkim"),
    ("Tamil Nadu",    "Tamil Nadu"),
    ("Telangana",    "Telangana"),
    ("Tripura",    "Tripura"),
    ("Uttarakhand",    "Uttarakhand"),
    ("Uttar Pradesh",    "Uttar Pradesh"),
    ("West Bengal",    "West Bengal"),
    ("Andaman and Nicobar Islands",    "Andaman and Nicobar Islands"),
    ("Chandigarh",    "Chandigarh"),
    ("Dadra and Nagar Haveli",    "Dadra and Nagar Haveli"),
    ("Daman and Diu",    "Daman and Diu"),
    ("Delhi",    "Delhi"),
    ("Lakshadweep",    "Lakshadweep"),
    ("Puducherry",    "Puducherry")
)


# modal proposal form for cfp
class ProposalForm(forms.ModelForm):

    about_me = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About Me'}),
                               required=True,
                               error_messages={
                                   'required': 'About me field required.'},
                               )
    attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                 label='Please upload relevant documents (if any)',
                                 required=False,)
    phone = forms.CharField(min_length=10, max_length=12, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}), required=False, validators=[RegexValidator(regex='^[0-9-_+.]*$', message='Enter a Valid Phone Number',)],
                            # error_messages = {'required':'Title field required.'},
                            )
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
                            required=True,
                            error_messages={
                                'required': 'Title field required.'},
                            )
    abstract = forms.CharField(min_length=300,  widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Abstract', 'onkeyup': 'countChar(this)'}),
                               required=True,
                               label='Abstract (Min. 300 char.)',
                               error_messages={
                                   'required': 'Abstract field required.'},
                               )
    proposal_type = forms.CharField(
        widget=forms.HiddenInput(), label='', initial='ABSTRACT', required=False)

    duration = forms.ChoiceField(
        choices=abs_duration, label='Duration (Mins.)')

    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags'}),
                           required=False,
                           )
    open_to_share = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=True,
                                      label='I am agree to publish my content',)

    class Meta:
        model = Proposal
        exclude = ('user', 'email', 'prerequisite', 'status', 'rate')

    def clean_attachment(self):
        import os
        cleaned_data = self.cleaned_data
        attachment = cleaned_data.get('attachment', None)
        if attachment:
            ext = os.path.splitext(attachment.name)[1]
            valid_extensions = ['.pdf']
            if not ext in valid_extensions:
                raise forms.ValidationError(
                    u'File not supported!  Only .pdf file is accepted')
            if attachment.size > (5*1024*1024):
                raise forms.ValidationError('File size exceeds 5MB')
        return attachment


# modal workshop form for cfw
class WorkshopForm(forms.ModelForm):
    about_me = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About Me'}),
                               required=True,
                               error_messages={
                                   'required': 'About Me field required.'},
                               )
    attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                 label='Please upload relevant documents (if any)',
                                 required=False,)
    phone = forms.CharField(min_length=10, max_length=12, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}), required=False, validators=[RegexValidator(regex='^[0-9-_+.]*$', message='Enter a Valid Phone Number',)],
                            )
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
                            required=True,
                            error_messages={
                                'required': 'Title field required.'},
                            )
    abstract = forms.CharField(min_length=300, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Desciption', 'onkeyup': 'countChar(this)'}),
                               required=True,
                               label='Description (Min. 300 char.)',)

    prerequisite = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Prerequisite'}),
                                   label='Prerequisites',
                                   required=False,
                                   )
    proposal_type = forms.CharField(
        widget=forms.HiddenInput(), label='', required=False, initial='WORKSHOP')

    duration = forms.ChoiceField(choices=ws_duration, label='Duration (Hrs.)')

    tags = forms.ChoiceField(choices=MY_CHOICES, label='Level')
    open_to_share = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=True,
                                      label='I am agree to publish my content',)

    class Meta:
        model = Proposal
        exclude = ('user', 'email', 'status', 'rate')

    def clean_attachment(self):
        import os
        cleaned_data = self.cleaned_data
        attachment = cleaned_data.get('attachment', None)
        if attachment:
            ext = os.path.splitext(attachment.name)[1]
            valid_extensions = ['.pdf', ]
            if not ext in valid_extensions:
                raise forms.ValidationError(
                    u'File not supported! Only .pdf file is accepted')
            if attachment.size > (5*1024*1024):
                raise forms.ValidationError('File size exceeds 5MB')
        return attachment


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1',
                  'password2')
        first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                                     label='First Name'
                                     )
        last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                                    label='Last Name'
                                    )
        email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                                 required=True,
                                 error_messages={
                                     'required': 'Email field required.'},
                                 label='Email'
                                 )
        username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                                   required=True,
                                   error_messages={
                                       'required': 'Username field required.'},
                                   label='Username'
                                   )
        password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                                    required=True,
                                    error_messages={
                                        'required': 'Password field required.'},
                                    label='Password'
                                    )
        password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
                                    required=True,
                                    error_messages={
                                        'required': 'Password Confirm field required.'},
                                    label='Re-enter Password'
                                    )

        def clean_first_name(self):
            return self.cleaned_data["first_name"].title()

        def clean_email(self):
            return self.cleaned_data["email"].lower()

        def clean_last_name(self):
            return self.cleaned_data["last_name"].title()


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-inline', 'placeholder': 'Username'}),
        label='User Name'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-inline', 'placeholder': 'Password'}),
        label='Password'
    )


class UserRegistrationForm(forms.Form):
    """A Class to create new form for User's Registration.
    It has the various fields and functions required to register
    a new user to the system"""
    required_css_class = 'required'
    errorlist_css_class = 'errorlist'
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter user name'}), max_length=32, help_text='''Letters, digits,
                               period and underscore only.''',)
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter valid email id'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        max_length=32, widget=forms.PasswordInput())
    title = forms.ChoiceField(choices=title)
    first_name = forms.CharField(max_length=32, label='First name', widget=forms.TextInput(
        attrs={'placeholder': 'Enter first name'}))
    last_name = forms.CharField(max_length=32, label='Last name', widget=forms.TextInput(
        attrs={'placeholder': 'Enter last name'},))
    phone_number = forms.RegexField(regex=r'^.{10}$',
                                    error_messages={'invalid': "Phone number must be entered \
                                                  in the format: '9999999999'.\
                                                 Up to 10 digits allowed."}, label='Phone/Mobile', widget=forms.TextInput(attrs={'placeholder': 'Enter valid contact number'},))
    institute = forms.CharField(max_length=128,
                                help_text='Please write full name of your Institute/Organization/Company', label='Institute/Organization/Company', widget=forms.TextInput(attrs={'placeholder': 'Enter name of your Institute/Organization/Company', 'size': '50'},))
    # department = forms.ChoiceField(help_text='Department you work/study',
    #             choices=department_choices)
    #location = forms.CharField(max_length=255, help_text="Place/City")
    #state = forms.ChoiceField(choices=states)
    how_did_you_hear_about_us = forms.ChoiceField(
        choices=source, label='How did you hear about us?')

    def clean_username(self):
        u_name = self.cleaned_data["username"]
        if u_name.strip(UNAME_CHARS):
            msg = "Only letters, digits, period  are"\
                  " allowed in username"
            raise forms.ValidationError(msg)
        try:
            User.objects.get(username__exact=u_name)
            raise forms.ValidationError("Username already exists.")
        except User.DoesNotExist:
            return u_name

    def clean_password(self):
        pwd = self.cleaned_data['password']
        if pwd.strip(PWD_CHARS):
            raise forms.ValidationError("Only letters, digits and punctuation\
                                        are allowed in password")
        return pwd

    def clean_confirm_password(self):
        c_pwd = self.cleaned_data['confirm_password']
        pwd = self.data['password']
        if c_pwd != pwd:
            raise forms.ValidationError("Passwords do not match")

        return c_pwd

    def clean_email(self):
        user_email = self.cleaned_data['email']
        if User.objects.filter(email=user_email).exists():
            raise forms.ValidationError("This email already exists")
        return user_email

    def save(self):
        u_name = self.cleaned_data["username"]
        u_name = u_name.lower()
        pwd = self.cleaned_data["password"]
        email = self.cleaned_data["email"]
        new_user = User.objects.create_user(u_name, email, pwd)
        new_user.first_name = self.cleaned_data["first_name"]
        new_user.last_name = self.cleaned_data["last_name"]
        new_user.save()

        cleaned_data = self.cleaned_data
        new_profile = Profile(user=new_user)
        new_profile.institute = cleaned_data["institute"]
        #new_profile.department = cleaned_data["department"]
        #new_profile.position = cleaned_data["position"]
        new_profile.phone_number = cleaned_data["phone_number"]
        #new_profile.location = cleaned_data["location"]
        new_profile.title = cleaned_data["title"]
        #new_profile.state = cleaned_data["state"]
        new_profile.how_did_you_hear_about_us = cleaned_data["how_did_you_hear_about_us"]
        new_profile.activation_key = generate_activation_key(new_user.username)
        new_profile.key_expiry_time = timezone.now() + \
            timezone.timedelta(days=1)
        new_profile.save()
        key = Profile.objects.get(user=new_user).activation_key
        return u_name, pwd, key


class PaymentDetailsForm(forms.Form):
    """A Class to create new form for User's ticket booking.
    It has the various fields and functions required to ticket booking system"""
    ticket_type = forms.CharField(widget=forms.TextInput(
        attrs={'size': '50', 'Readonly': True}),
        label='Registration Type')
    attendee_type = forms.ChoiceField(widget=forms.RadioSelect(),
                                      choices=attendee_type_choices, required=True)
    ticket_price = forms.CharField(widget=forms.TextInput(
        attrs={'size': '5', 'Readonly': True}),
        label='Ticket price')

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First Name',
               'size': '50', 'Readonly': True}),
        label='First Name')

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last Name',
               'size': '50', 'Readonly': True}),
        label='Last Name')



    email = forms.EmailField(max_length=100, widget=forms.TextInput(
        attrs={'size': '50',
                       'placeholder': 'Enter valid email id', 'Readonly': True}))
    gender = forms.ChoiceField(choices=gender)

    phone_number = forms.RegexField(regex=r'^.{10}$',
                                    error_messages={
                                        'invalid': "Phone number must be entered \
                    in the format: '9999999999'.\
                    Up to 10 digits allowed."},
                                    label='Phone/Mobile',
                                    widget=forms.TextInput(
                                        attrs={'placeholder': 'Enter valid contact number',
                                               }))


    full_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50,
                                     'placeholder': 'Enter your full address'}),
        required=True,
        error_messages={
            'required': 'Address is required.'},
    )

    city = forms.CharField(max_length=100,
                           help_text='Please enter your city', label='City',
                           widget=forms.TextInput(attrs={'placeholder': 'Enter  your City',
                                                         'size': '50'}))

    state = forms.ChoiceField(choices=states)

    pincode = forms.CharField(max_length=6,
                              help_text='Please enter your pincode',
                              label='Pincode', widget=forms.TextInput(
                                  attrs={'placeholder': 'Pincode', 'size': '6'}))


    institute = forms.CharField(max_length=128,
                                help_text='Please write full name of your Institute/ \
                Organization/ Company', label='Institute/Organization/Company',
                                widget=forms.TextInput(attrs={'placeholder': 'Enter name of '
                                                              'your Institute/Organization/Company', 'size': '50'}))


    gstin = forms.CharField(max_length=15, required=False,
                            help_text='Please enter your GSTIN',
                            label='GSTIN',
                            widget=forms.TextInput(
                                attrs={'placeholder': 'GSTIN (Optional)', 'size': '15'}))


    job_fair = forms.ChoiceField(choices=attending_job_fair)
    req_tshirt = forms.ChoiceField(choices=want_tshirt)
    tshirt_size = forms.ChoiceField(choices=t_shirt_size, required=False)
    tshirt_price = forms.CharField(widget=forms.TextInput(
        attrs={'size': '5', 'Readonly': True}),
        label='Tshirt price')

    accomodation = forms.ChoiceField(choices=accomodation_choice, required=True)

    total_amount = forms.CharField(max_length=15, required=False,
                             label='Price',
                             widget=forms.TextInput(
                                 attrs={'Readonly': 'True', 'size': '15'}))
