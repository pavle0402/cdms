from rest_framework.permissions import BasePermission

class IsClinicAdmin(BasePermission):
    """
    Permission that allows only clinic admins to access the view.
    Optionally checks if they're admin of a specific clinic.
    """
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and request.user.is_clinic_admin):
            return False
            
        if hasattr(view, 'clinic_id'):
            return request.user.clinic_id == view.clinic_id
            
        return True
    
class IsPatientDoctorOrClinicAdmin(BasePermission):
    """
    Permission that allows only the patient's doctor or clinic admin to access patient data.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_doctor or request.user.is_clinic_admin)
    


class IsUserPartOfClinic(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser:
            return True
            
        clinic_id = view.kwargs.get('pk')
        
        try:
            clinic_id = int(clinic_id)
        except (TypeError, ValueError):
            print("exception block")
            return False
            
        if request.user.clinic_id is None:
            return False
        
        return (
            request.user.clinic_id == clinic_id or
            (request.user.is_clinic_admin and request.user.clinic_id == clinic_id)
        )
    


class IsClinicStaff(BasePermission):
    """
    Permission that allows only doctors and clinic admins
    from the specified clinic to access patient data.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        if not (request.user.is_doctor or request.user.is_clinic_admin):
            return False
            
        clinic_id = view.kwargs.get('clinic_id')
        if not clinic_id:
            return False
            
        return request.user.clinic_id == int(clinic_id)