from django.urls import path
from .views import RegisterView, LoginView, user_detail, user_update, ChangePasswordView, activate_user

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth-login'),
    path('user/', user_detail, name='auth-user-detail'),
    path('user/update/', user_update, name='auth-user-update'),
    path('user/change-password/', ChangePasswordView.as_view(), name='auth-change-password'),
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('activate/<uidb64>/<token>/', activate_user, name='activate'),
]
