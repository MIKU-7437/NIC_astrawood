from django.contrib import admin
from users.models import User, Profile
from django.utils.html import format_html

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Класс для настройки отображения модели User в административном интерфейсе

    list_display = [
        'email',
        'first_name',
        'last_name',
    ]
    list_filter = [
        'username',
        'email',
    ]
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        # Метод для отображения изображения пользователя в виде тега HTML
        return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.photo.url)
    
    image_tag.short_description = 'Image'
    # Краткое описание для поля image_tag в административном интерфейсе

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Класс для настройки отображения модели Profile в административном интерфейсе
    list_display = ('user', 'phone_number', 'birth_date')
    search_fields = ('user__username', 'phone_number')
    list_filter = ('birth_date',)