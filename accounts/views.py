from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserInfoSerializer
from .models import User

# Create your views here.
def login_view(request):
    return render(request, 'accounts/login/login.html')


# Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class UserInfoView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user