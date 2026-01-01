from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer
from .api_permissions import IsAdmin, IsAdminOrStaff, ReadOnlyForAll


# LIST + CREATE
class StudentListCreateAPI(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), ReadOnlyForAll()]
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminOrStaff()]
        return []


# RETRIEVE + UPDATE + DELETE
class StudentDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), ReadOnlyForAll()]
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated(), IsAdminOrStaff()]
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdmin()]
        return []
