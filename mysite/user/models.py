from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

BLOOD_GROUP = [
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("O+", "O+"),
    ("O-", "O-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
]

DOCUMENT_CHOICES = [
    ("NIC", "National Identity Card"),
    ("Passport", "Passport"),
    ("CItitzenShip Number", "CitizenShip Number"),

]

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is Required!")
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("SuperUser Must have super_user = True")
        
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=254, null=True, blank=True)
    middle_name = models.CharField(max_length=254, null=True, blank=True)
    last_name = models.CharField(max_length=254, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True, help_text= "Please Enter your Date of Birth in the following format : 'Year-Month-Day'")
    gender = models.CharField(max_length=1, choices=[("M", "Male"),("F", "Female")])
    blood_group = models.CharField(max_length=3, null=True, blank=True, choices=BLOOD_GROUP)
    identity_document_type = models.CharField(max_length=32, choices=DOCUMENT_CHOICES)
    identity_document_number = models.CharField(max_length=255)
    photo = models.ImageField(null= True, upload_to="profileImages/")
    date_joined = models.DateTimeField(default = timezone.now)
    last_updated = models.DateTimeField(auto_now= True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default= False)
    is_superuser = models.BooleanField(default= False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"
    
    objects = UserManager()
