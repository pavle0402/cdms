from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


class Clinic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_independent_doctor = models.BooleanField(default=True)
    
    class Meta:
        db_table = "clinics"

    def __str__(self):
        return self.name 
    
class User(AbstractUser):
    class Role(models.TextChoices):
        CLINIC_ADMIN = 'clinic_admin', 'Clinic Admin'
        DOCTOR = 'doctor', 'Doctor'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.DOCTOR,
        blank=False,
        null=False
    )
    clinic = models.ForeignKey(
        'Clinic',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        help_text="Clinic the user belongs to (not required for solo doctors)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_clinic_admin(self):
        return self.role == self.Role.CLINIC_ADMIN
    
    @property
    def is_doctor(self):
        return self.role == self.Role.DOCTOR
    
    @property
    def is_solo_doctor(self):
        return self.role == self.Role.DOCTOR and self.clinic is None

class Patient(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'


    doctor = models.ForeignKey('User', on_delete=models.CASCADE, related_name='patients')
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, null=False, blank=False)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ssn = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = "patients"

    def __str__(self):
        return self.full_name
    
    @property
    def age(self):
        return date.today().year - self.date_of_birth.year
    
