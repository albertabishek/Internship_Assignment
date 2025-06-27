from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

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