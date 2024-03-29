from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from .serializers import *


class TokenLoginAPIView(ObtainAuthToken):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user).data
        data = {
            'token': token.key,
            'user': user_data
        }
        return Response(data)


class AccountProfileAPIView(RetrieveAPIView):
    serializer_class = AccountAuthUserSerializer

    def get_object(self):
        return self.request.user
