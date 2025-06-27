from django.conf import settings 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, TelegramUserSerializer
from .models import TelegramUser


# Public endpoint 
class PublicDataView(APIView):
    """
    An endpoint that is accessible to everyone.
    """
    permission_classes = [] # No permissions required
    authentication_classes = [] # No authentication required

    def get(self, request, *args, **kwargs):
        return Response({"message": "This is a public endpoint. Anyone can see this!"})


# Protected endpoint 
class ProtectedDataView(APIView):
    """
    An endpoint only accessible to authenticated users.
    Requires a valid token in the 'Authorization: Token <your_token>' header.
    """
    permission_classes = [IsAuthenticated] # Only authenticated users can access

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response({
            "message": "You are authenticated! Only you can see this.",
            "user_data": serializer.data
        })
    
# API for the bot
class CreateTelegramUserView(APIView):
    """
    An endpoint to create a new telegram user.
    This will be called by our separate bot script.
    We will secure it with a simple secret key.
    """
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        # Simple secret key authentication
        secret = request.headers.get("X-Bot-Secret")
        # The 'settings' object is now correctly imported and available
        if not secret or secret != settings.TELEGRAM_BOT_API_SECRET:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TelegramUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)