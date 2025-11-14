from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'nickname', 'gender', 'phone', 'email', 'birth_date')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'nickname', 'gender', 'phone', 'email', 'birth_date', 'is_staff', 'is_active', 'is_superuser')

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'name', 'nickname', 'email', 'gender', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'gender')
    search_fields = ('username', 'name', 'nickname', 'email', 'phone')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('개인 정보', {'fields': ('name', 'nickname', 'gender', 'phone', 'email', 'birth_date')}),
        ('권한', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'nickname', 'gender', 'phone', 'email', 'birth_date', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
