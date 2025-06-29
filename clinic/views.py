from rest_framework import generics, permissions, status,views
from rest_framework.response import Response
from .models import Clinic, User, Patient 
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
                        BaseUserSerializer,
                        UsersGetAllSerializer,
                        ClinicsGetAllSerializer,
                        ClinicCreateUpdateSerializer,
                        AddClinicUserSerializer,
                        ClinicsDetailSerializer,
                        ClinicPatientSerializer,
                        AddEditPatientSerializer,
                        PatientDetailsSerializer
                        )
from .permissions import IsUserPartOfClinic, IsClinicAdmin, IsClinicStaff
from rest_framework.exceptions import APIException
from .filters import PatientFilter

class CustomAPIException(APIException):
    status_code = 422

lookup_field = "pk"

#AUTH VIEWS
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = BaseUserSerializer


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class LogoutView(views.APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            print(token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print("exception")
            return CustomAPIException({"message":f"Exception occured: {e}."})
        
class UsersListAPIView(generics.ListAPIView):
    serializer_class = UsersGetAllSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

#clinic views

#list of all clinics and their data that only superadmin can access.
class ClinicListAPIView(generics.ListAPIView):
    queryset = Clinic.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ClinicsGetAllSerializer

class CreateClinicAPIView(generics.CreateAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

class UpdateClinicAPIView(generics.UpdateAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

class ClinicDetailsAPIView(generics.RetrieveAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicsDetailSerializer
    lookup_field = lookup_field
    permission_classes = [IsUserPartOfClinic]

class AddClinicUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AddClinicUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
#delete whole clinic
class DeleteClinicAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    lookup_field = lookup_field
    queryset = Clinic.objects.all()
    serializer_class = ClinicsGetAllSerializer


#endpoint for clinic admins to delete user from THEIR clinic
class DeleteClinicDoctorAPIView(generics.DestroyAPIView):
    queryset = User.objects.filter(role=User.Role.DOCTOR)
    permission_classes = [IsClinicAdmin]
    
    def get_clinic_id(self):
        doctor = self.get_object()
        return doctor.clinic_id if doctor.clinic else None
    
    def check_permissions(self, request):
        super().check_permissions(request)
        
        doctor = self.get_object()
        if request.user.clinic != doctor.clinic:
            self.permission_denied(
                request,
                message="You can only delete doctors from your own clinic",
                code=status.HTTP_403_FORBIDDEN
            )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if request.user.clinic != instance.clinic:
            return CustomAPIException({"message": "You can only delete doctors from your own clinic"})
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    


#patients endpoints

class GetAllPatientsPerClinicAPIView(generics.ListAPIView):
    model = Patient.objects.all()
    serializer_class = ClinicPatientSerializer
    permission_classes = [IsClinicStaff]
    filterset_class = PatientFilter

    def get_queryset(self):
        clinic_id = self.kwargs['clinic_id']
        return Patient.objects.filter(
            doctor__clinic_id=clinic_id
        ).select_related('doctor')

class CreatePatientAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    model = Patient.objects.all()
    serializer_class = AddEditPatientSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class PatientDetailsAPIView(generics.RetrieveAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = lookup_field

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        if user != obj.doctor:
            raise CustomAPIException({"message":"Only patient's doctor can access their information!"})
        
class EditPatientAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    model = Patient.objects.all()
    serializer_class = AddEditPatientSerializer
    lookup_field = lookup_field

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class DeletePatientAPIView(generics.DestroyAPIView):
    permission_classes = [IsClinicStaff]
    model = Patient.objects.all()
    serializer_class = ClinicPatientSerializer
    lookup_field = lookup_field