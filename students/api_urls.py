from django.urls import path
from .api_views import StudentListCreateAPI, StudentDetailAPI
from .api_auth_views import LoginAPI, LogoutAPI


urlpatterns = [
    path('login/', LoginAPI.as_view(), name='api_login'),
    path('students/', StudentListCreateAPI.as_view()),
    path('students/<int:pk>/', StudentDetailAPI.as_view()),
    path('logout/', LogoutAPI.as_view(), name='api_logout'),

]
