from django.urls import path
from .views import (
    RegisterView,
    UsersListAPIView,
    ClinicListAPIView,
    CreateClinicAPIView,
    AddClinicUserAPIView,
    ClinicDetailsAPIView,
    DeleteClinicDoctorAPIView,
    GetAllPatientsPerClinicAPIView,
    CreatePatientAPIView,
    EditPatientAPIView,
    PatientDetailsAPIView,
    DeletePatientAPIView,
    LogoutView
)

app_name = "clinic"

urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("users-list", UsersListAPIView.as_view(), name="users"),
    #clinics
    path("clinics", ClinicListAPIView.as_view(), name="clinics"),
    path("clinics/create-clinic", CreateClinicAPIView.as_view(), name="clinic-create"),
    path("clinics/create-user", AddClinicUserAPIView.as_view(), name="clinic-user-create"),
    path("clinics/details/<int:pk>", ClinicDetailsAPIView.as_view(), name="clinic-details"),
    path('clinics/<int:clinic_id>/doctors/<int:pk>/', DeleteClinicDoctorAPIView.as_view(), name='clinic-doctor-delete'),
    #endpoint allowed only for members of that clinic
    path('clinics/<int:clinic_id>/patients/', GetAllPatientsPerClinicAPIView.as_view(), name='clinic-patients-list'),
    #patients endpoints
    path('patients/create', CreatePatientAPIView.as_view(), name='create-patient'),
    path('patients/details/<int:pk>', PatientDetailsAPIView.as_view(), name='edit-patient'),
    path('patients/edit/<int:pk>', EditPatientAPIView.as_view(), name='edit-patient'),
    path('patients/delete/<int:pk>', DeletePatientAPIView.as_view(), name='delete-patient'),
]