from rest_framework import serializers
from .models import Patient, User, Clinic
from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueValidator

class CustomAPIException(APIException):
    status_code = 422

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', "last_name", 'email', "clinic", "role"]
        extra_kwargs = {"password": {"write_only": True}}
    

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        
        if not request or not request.user.is_authenticated or not request.user.is_superuser:
            self.fields.pop('clinic', None)
            self.fields.pop('role', None)

class UsersGetAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


#clinic serializers
class ClinicsGetAllSerializer(serializers.ModelSerializer):
    doctors = serializers.SerializerMethodField()
    admins = serializers.SerializerMethodField()
    
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'description', 'address', 'phone', 'email', 'doctors', 'admins']

    def get_doctors(self, obj):
        doctors = obj.users.filter(role=User.Role.DOCTOR)
        return BaseUserSerializer(doctors, many=True).data

    def get_admins(self, obj):
        admins = obj.users.filter(role=User.Role.CLINIC_ADMIN)
        return BaseUserSerializer(admins, many=True).data

class ClinicCreateUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Clinic.objects.all(), message="Clinic with this name already exists.")]
    )
    email = serializers.CharField(
        validators=[UniqueValidator(queryset=Clinic.objects.all(), message="Clinic with this email already exists.")]
    )

    class Meta:
        model = Clinic
        fields = ["name", "description", "address", "phone", "email"]
    

class AddClinicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'role', 'clinic']
        extra_kwargs = {"password": {"write_only": True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        
        if request and request.user.is_authenticated:
            user = request.user
            if user.is_clinic_admin:
                self.fields['clinic'].queryset = Clinic.objects.filter(id=user.clinic.id)
                self.fields['clinic'].initial = user.clinic.id
                
                self.fields['role'].choices = [
                    (User.Role.DOCTOR, 'Doctor'),
                    (User.Role.CLINIC_ADMIN, 'Clinic Admin'),
                ]

    def validate(self, data):
        request = self.context.get('request')
        user = request.user if request else None
        
        if not user or not user.is_authenticated:
                raise CustomAPIException({"message":"Authentication required"})
        
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        validated_data['clinic'] = user.clinic

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    


class ClinicsDetailSerializer(serializers.ModelSerializer):
    doctors = serializers.SerializerMethodField()
    admins = serializers.SerializerMethodField()
    
    class Meta:
        model = Clinic
        fields = ['name', 'description', 'address', 'phone', 'email', 'doctors', 'admins']


    def get_doctors(self, obj):
        doctors = obj.users.filter(role=User.Role.DOCTOR)
        return BaseUserSerializer(doctors, many=True).data

    def get_admins(self, obj):
        admins = obj.users.filter(role=User.Role.CLINIC_ADMIN)
        return BaseUserSerializer(admins, many=True).data



#patient serializers

class ClinicPatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    permission_classes = []

    class Meta:
        model = Patient
        fields = [
            'id', 'full_name', 'gender', 'age', 'phone', 'doctor_name',
        ]

    def get_age(self, obj):
        return obj.age
    
    def get_doctor_name(self, obj):
        return obj.doctor.first_name + obj.doctor.last_name
    

class AddEditPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['full_name', 'gender', 'age', 'phone', 'date_of_birth', 'address', 'doctor', 'ssn']

    def validate(self, data):
        request = self.context.get("request")
        user = request.user 

        if user.role != User.Role.DOCTOR:
            raise CustomAPIException({"message":"Only doctors can add/edit patients."})
        
        return data
    
class PatientDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"