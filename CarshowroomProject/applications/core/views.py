from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from . import tasks
from .mixins import SafeDeleteModelMixin
from .serializers import CarSerializer, BaseUserSerializer, RestorePasswordEmailSendSerializer
from .models import CarModel, BaseUser
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, \
    DestroyModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .filters import CarFilter
from .services import UserService


class CarViewSet(GenericViewSet,
                 ListModelMixin,
                 RetrieveModelMixin,
                 UpdateModelMixin,
                 CreateModelMixin,
                 SafeDeleteModelMixin, ):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,
                       SearchFilter,
                       OrderingFilter,
                       )
    filterset_class = CarFilter
    ordering_fields = ('id', 'brand', 'fuel', 'bodys_type', 'model',)
    search_fields = ('id', 'brand', 'fuel', 'body_type', 'model',)


class BaseUserViewSet(GenericViewSet,
                      ListModelMixin,
                      DestroyModelMixin,
                      RetrieveModelMixin):
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer
    permission_classes = (permissions.AllowAny,)
    service = UserService()

    def get_permissions(self):
        if self.action == 'register' or self.action == 'verify_email':
            return [permissions.AllowAny()]
        elif self.action == 'send_confirm_email':
            return [permissions.IsAuthenticated()]
        elif self.action == 'change_email_request':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(detail=False, methods=['POST'])
    def register(self, request: Request):
        password = request.data.get('password')
        hashed_password = make_password(password)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(password=hashed_password, is_confirmed=False)

        user = serializer.instance
        self.service.send_confirm_email(user=user)

        return Response({'detail': 'Verification email sent.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def verify_email(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'detail': 'Token parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)
        user = self.service.get_user_from_token(token_str=token)
        if user:
            user.is_confirmed = True
            user.save()
            return Response({'detail': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        return Response("Error", status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False)
    def send_confirm_email(self, request):
        self.service.send_confirm_email(request.user)
        return Response({'detail': 'Verification email sent.'}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def change_email_request(self, request):
        self.service.send_email_for_change_email(request.user)
        return Response({'detail': 'Email to change email sent.', 'email': request.user.email},
                        status=status.HTTP_200_OK)

    @action(methods=['PUT'], detail=False)
    def change_email(self, request):
        token = request.query_params.get('token')
        uidb64 = request.query_params.get('uid')
        user = self.service.get_user_from_uid(uid=uidb64)
        if user and self.service.check_token(user, token):
            email = request.data.get('email')
            user.email = email
            user.save()
            return Response({'detail': 'Email change successful.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid or expired reset token.'}, status=status.HTTP_400_BAD_REQUEST)


class RestorePasswordEmailSendView(APIView):
    service = UserService()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RestorePasswordEmailSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = BaseUser.objects.filter(email=email).first()
        if user:
            self.service.send_email_for_restore_password(email=email, user=user).delay()
        return Response({'detail': 'Password reset email sent.'}, status=status.HTTP_200_OK)


class RestorePasswordConfirmView(APIView):
    service = UserService()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, uidb64, token):
        user = self.service.get_user_from_uid(uid=uidb64)

        if user and self.service.check_token(user, token):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid or expired reset token.'}, status=status.HTTP_400_BAD_REQUEST)
