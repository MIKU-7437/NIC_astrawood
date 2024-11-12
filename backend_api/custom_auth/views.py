from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.encoding import force_str
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    RegisterSerializer, 
    UserSerializer, 
    CustomTokenObtainPairSerializer, 
    ChangePasswordSerializer
)
from users.utils import send_activation_email  # Ensure the path to utils is correct

User = get_user_model()

class RegisterView(views.APIView):
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="User created successfully, please check your email to activate your account",
                examples={"application/json": {"msg": "User created successfully, please check your email to activate your account"}}
            ),
            status.HTTP_400_BAD_REQUEST: "Invalid data"
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # User is created inactive
            user.save()
            send_activation_email(user, request)
            return Response(
                {"msg": "User created successfully, please check your email to activate your account"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('uidb64', openapi.IN_PATH, description="Encoded User ID", type=openapi.TYPE_STRING),
        openapi.Parameter('token', openapi.IN_PATH, description="Token for activation", type=openapi.TYPE_STRING),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response("Account activated successfully"),
        status.HTTP_400_BAD_REQUEST: openapi.Response("Activation link is invalid"),
    }
)
@api_view(['GET'])
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'msg': 'Account activated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': 'Activation link is invalid'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@swagger_auto_schema(
    method='get',
    responses={status.HTTP_200_OK: UserSerializer}
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_detail(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@swagger_auto_schema(
    method='put',
    request_body=UserSerializer,
    responses={
        status.HTTP_200_OK: UserSerializer,
        status.HTTP_400_BAD_REQUEST: "Invalid data"
    }
)
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def user_update(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: "Password changed successfully",
            status.HTTP_400_BAD_REQUEST: "Invalid data"
        }
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            if not check_password(old_password, request.user.password):
                return Response({"old_password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"msg": "Password changed successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
