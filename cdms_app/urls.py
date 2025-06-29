from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    #this is used as login, in real-world scenario i would create login page
    #and then return token with all the data i need (data like role, full name, clinic etc.)
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", include('clinic.urls', namespace="clinic"))
]
