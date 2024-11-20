from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'city', 'region', 'address', 'photo']
        read_only_fields = ['email']
        ref_name = 'CustomAuthUserSerializer'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_conf = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password_conf', 'phone', 'city', 'region', 'address']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_conf']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_conf')
        user = User.objects.create_user(**validated_data)
        return user

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['name'] = user.get_full_name()
#         return token


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Получаем данные из базового класса
        data = super().validate(attrs)

        # Получаем пользователя
        user = self.user

        # Проверяем, что пользователь активирован
        if not user.is_active:
            raise serializers.ValidationError("Аккаунт не активирован. Проверьте свою почту для активации аккаунта.")

        return data
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        ref_name = 'CustomAuthChangePasswordSerializer'  # Уникальное имя ссылки