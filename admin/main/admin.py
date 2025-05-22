from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, StudentRequest

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'office', 'is_staff')
    list_filter = ('office', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'office')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'telegram_id', 'group', 'course', 'is_registered')
    list_filter = ('is_registered', 'course', 'language')
    search_fields = ('first_name', 'last_name', 'telegram_id')

@admin.register(StudentRequest)
class StudentRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'to_service', 'status', 'office', 'created_at')
    list_filter = ('status', 'office', 'created_at')
    search_fields = ('student__first_name', 'student__last_name', 'to_service')
