from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterUserSerializer


class CustumUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_seralizer = RegisterUserSerializer(data=request.data)
        if reg_seralizer.is_valid():
            newuser = reg_seralizer.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
