from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.contrib.auth.models import User
from django.utils.timezone import now


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Создание пользователя без указания имени пользователя
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Создание суперпользователя без указания имени пользователя
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    
    is_active = models.BooleanField(default=False)
    
    email = models.EmailField(
        verbose_name='Почта',
        max_length=256,
        unique=True,
        blank=False
    )
    first_name = models.CharField(
        max_length=50, 
        blank=False
    )
    last_name = models.CharField(
        max_length=50,
        blank=False
    )
    username = models.CharField(
        max_length=256
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата обновления',
        auto_now=True,
    )
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=False
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=50,
        blank=False
    )
    region = models.CharField(
        verbose_name='Область',
        max_length=50,
        blank=False
    )
    address = models.TextField(
        verbose_name='Адрес',
        blank=False
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=15,
        unique=True,
        blank=False
    )
    
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to='customer_photos/',
        null=True,
        blank=True,
        default='customer_photos/default-profile-picture.jpg'
    )
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'city', 'region', 'address', 'phone']


    def __str__(self):
        return self.email

def user_avatar_path(instance, filename):
    # Задает путь к файлу аватара: media/avatars/user_<id>/<filename>
    return f'avatars/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"