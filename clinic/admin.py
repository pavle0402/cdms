from django.contrib import admin
from .models import Clinic, User, Patient

admin.site.register(Clinic)
admin.site.register(Patient)
admin.site.register(User)