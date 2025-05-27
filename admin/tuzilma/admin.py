from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Level, Direction, Group, ScheduleUpload, ScheduleGet


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_display_links = ('id', 'name')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('id', )

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level', 'is_active')
    list_display_links = ('id', 'name')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction', 'course', 'is_active')
    list_filter = ('direction__level', 'direction', 'course', 'is_active')
    search_fields = ('name', 'direction__name', 'direction__level__name')
    ordering = ('id', )

@admin.register(ScheduleUpload)
class ScheduleUploadAdmin(admin.ModelAdmin):
    list_display = ('direction', 'course', 'created_at')
    list_filter = ('direction', 'course', 'created_at')

@admin.register(ScheduleGet)
class ScheduleGetAdmin(admin.ModelAdmin):
    list_display = ('direction', 'course')
    list_filter = ('direction', 'course')

    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        return super().has_add_permission(request)

