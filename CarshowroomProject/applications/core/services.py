from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from applications.core import tasks
from applications.core.models import BaseUser
from applications.core.models import BaseUser, CarModel


class CarService:
    def create_car(self, car_data):
        car, created = CarModel.objects.get_or_create(**car_data)
        return car

    def get_car(self, id):
        return CarModel.objects.get(id=id)


class UserService:

    def create_user(self, user_data):
        user = BaseUser(**user_data)
        user.set_password(user.password)
        user.save()
        return user

    def get_user(self, user_id=None, email=None):
        if email:
            return get_object_or_404(BaseUser, email=email)
        if user_id:
            return get_object_or_404(BaseUser, id=user_id)
        else:
            return None

    def get_tokens_for_user(self, user):
        token = RefreshToken.for_user(user)

        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }

    def get_user_from_token(self, token_str):
        try:
            access_token = AccessToken(token_str)
            user_id = access_token['user_id']
            user = BaseUser.objects.get(id=user_id)
        except Exception:
            return None
        return user

    def send_confirm_email(self, user):
        verification_token = self.get_tokens_for_user(user=user)['access']
        verification_link = f'http://localhost:8000/api/user/verify_email/?token={verification_token}'
        subject = 'Подтверждение регистрации'
        message = f'Для завершения регистрации перейдите по ссылке: {verification_link}'
        recipient_list = [user.email]
        tasks.send_email_task.delay(subject=subject, message=message, recipient_list=recipient_list)

    def send_email_for_restore_password(self, user, email):
        token = self.get_tokens_for_user(user=user)['access']
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f'http://localhost:8000/api/reset_password/confirm/{uidb64}/{token}/'
        subject = 'Password Reset'
        message = f'Please click on the link below to reset your password:\n{reset_link}'
        recipient_list = [email]
        tasks.send_email_task.delay(subject=subject, message=message, recipient_list=recipient_list)

    def check_token(self, user, token):
        user_token = self.get_user_from_token(token_str=token)
        if user_token.id == user.id:
            return True
        return False

    def get_user_from_uid(self, uid):
        uid = force_str(urlsafe_base64_decode(uid))
        user = BaseUser.objects.filter(pk=uid).first()
        return user

    def create_uidb64(self, pk):
        return urlsafe_base64_encode(force_bytes(pk))

    def send_email_for_change_email(self, user):
        token = self.get_tokens_for_user(user=user)['access']
        uidb64 = self.create_uidb64(user.pk)
        reset_link = f'http://localhost:8000/api/user/change_email/?uid={uidb64}&token={token}'
        subject = 'Change email'
        message = f'Please click on the link below to change your email:\n{reset_link}'
        recipient_list = [user.email]
        tasks.send_email_task.delay(subject=subject, message=message, recipient_list=recipient_list)
