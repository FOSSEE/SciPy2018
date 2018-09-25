from django.db import models
from django.contrib.auth.models import User

from social.apps.django_app.default.models import UserSocialAuth
from Scipy2018 import settings
from django.core.validators import RegexValidator
import os
from datetime import datetime

position_choices = (
    ("student", "Student"),
    ("faculty", "Faculty"),
    ("industry_people", "Industry People"),
)

gender = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
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

attending_job_fair = (
    ("Yes", 1),
    ("No", 0),
)

req_accomodation = (
    ("Yes", 1),
    ("No", 0),
)

t_shirt_size = (
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("XXL", "XXL"),
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

want_tshirt = (
    ("No", "No"),
    ("Yes", "Yes"),
)

reg_purpose = (
    ("scipy-2018", 1),
)


def get_document_dir(instance, filename):
    # ename, eext = instance.user.email.split("@")
    fname, fext = os.path.splitext(filename)
    # print "----------------->",instance.user
    return '%s/attachment/%s/%s.%s' % (instance.user, instance.proposal_type, fname+'_'+str(instance.user), fext)


class Proposal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    name_of_author1 = models.CharField(max_length=200, default='None')
    name_of_author2 = models.CharField(max_length=200, default='None')   
    about_the_authors = models.TextField(max_length=500)
    email = models.CharField(max_length=128)
    phone = models.CharField(max_length=20)
    title = models.CharField(max_length=250)
    abstract = models.TextField(max_length=700)
    prerequisite = models.CharField(max_length=750)
    duration = models.CharField(max_length=100)
    attachment = models.FileField(upload_to=get_document_dir)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, default='Pending', editable=True)
    proposal_type = models.CharField(max_length=100)
    tags = models.CharField(max_length=250)
    open_to_share = models.CharField(max_length=2, default=1)
    terms_and_conditions = models.BooleanField(default= 'True')


class Ratings(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    rating = models.CharField(max_length=700)


class Comments(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    comment = models.CharField(max_length=700)
    # rate = models.CharField(max_length =100)

# profile module


class Profile(models.Model):
    """Profile for users"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=32, blank=True, choices=title)
    institute = models.CharField(max_length=150)
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(
                    regex=r'^.{10}$', message=(
                        "Phone number must be entered \
                                in the format: '9999999999'.\
                                Up to 10 digits allowed.")
                    )], null=False)
    position = models.CharField(max_length=32, choices=position_choices,
                                default='student',
                                help_text='Selected catagoery ID shold be required')
    how_did_you_hear_about_us = models.CharField(
        max_length=255, blank=True, choices=source)
    is_email_verified = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=255, blank=True, null=True)
    key_expiry_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return u"id: {0}| {1} {2} | {3} ".format(
            self.user.id,
            self.user.first_name,
            self.user.last_name,
            self.user.email
        )

# payment details


class PaymentDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='null')
    # "regular/late registration"
    ticket_type = models.CharField(
        max_length=32, blank=True, choices=attendee_type_choices)
    attendee_type = models.CharField(
        max_length=32, blank=True, choices=attendee_type_choices)
    ticket_price = models.CharField(max_length=20, default=0)
    first_name = models.CharField(max_length=50, default="null")
    last_name = models.CharField(max_length=50, default="null")
    email = models.CharField(max_length=100, default="null")
    gender = models.CharField(max_length=32, blank=True, choices=gender)
    phone_number = models.CharField(max_length=10, default="0000000000")
    full_address = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=20, blank=True)
    pincode = models.CharField(max_length=6, blank=True)
    institute = models.CharField(max_length=150, default="null")
    gstin = models.CharField(max_length=15, null=True)
    jobfair = models.CharField(
        max_length=32, blank=True, choices=attending_job_fair, default="No") 
    req_tshirt = models.CharField(
        max_length=32, blank=True, choices=want_tshirt, default="No")
    tshirt_size = models.CharField(
        max_length=32, blank=True, choices=t_shirt_size, default="None")
    tshirt_price = models.CharField(max_length=20, default=0)
    accomodation = models.CharField(
        max_length=32, blank=True, choices=req_accomodation, default="No")
    amount = models.CharField(max_length=20, default=0)
    purpose = models.CharField(max_length=32, blank=True, choices=reg_purpose, default = "null")
    status = models.PositiveIntegerField(blank=True,default = 0)
    confirm = models.CharField(max_length=1, null=False, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


class PaymentTransactionDetails(models.Model):
    paymentdetail = models.ForeignKey(
        PaymentDetails, blank=False, null=False, on_delete=models.PROTECT)
    requestType = models.CharField(max_length=2)
    userId = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.PROTECT)
    amount = models.CharField(max_length=20)
    reqId = models.CharField(max_length=50)
    transId = models.CharField(max_length=100)
    refNo = models.CharField(max_length=50)
    provId = models.CharField(max_length=50)
    status = models.CharField(max_length=2)
    msg = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
