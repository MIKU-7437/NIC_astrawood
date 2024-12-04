from django.urls import path
from . import views
from .views import UserProfileView, UserAvatarView,CurrentUserView

urlpatterns = [
    path('list/', views.AllUsersView.as_view(), name='account-list'),  # Список пользователей, если это ещё актуально
    # path('', views.UserDetailView.as_view(), name='account-detail'),  # Детали аккаунта пользователя
    path('profile/', UserProfileView.as_view(), name='user-profile'), # Эта строка кода определяет шаблон URL для доступа к странице профиля пользователя в Django web
    path('<int:user_id>/avatar/', UserAvatarView.as_view(), name='user-avatar-by-id'),
    path('users/me/', CurrentUserView.as_view(), name='current_user'),
]
