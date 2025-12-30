from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('avatar', 'bio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Контактные данные', {'fields': ('email', 'avatar', 'bio')}),
    )
    list_display = ['username', 'email', 'is_staff', 'is_active']