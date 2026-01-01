from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # current user's token delete
        request.user.auth_token.delete()
        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # current user's token delete
        request.user.auth_token.delete()
        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )
