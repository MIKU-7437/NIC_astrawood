from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.AllUsersView.as_view(), name='account-list'),  # Список пользователей, если это ещё актуально
    path('', views.UserDetailView.as_view(), name='account-detail'),  # Детали аккаунта пользователя
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),  # Смена пароля
]
