from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from modeltranslation.admin import TranslationAdmin

from .models import Level, Direction, Group, ScheduleUpload, ScheduleGet, Faculty


@admin.register(Level)
class LevelAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'is_active')
    list_display_links = ('id', 'name')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('id', )

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Faculty)
class FacultyAdmin(TranslationAdmin):
    list_display = ('name_uz', 'level', 'is_active')
    list_filter = ('level', 'is_active')
    search_fields = ('name_uz', 'level__name')
    ordering = ('id', )

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Direction)
class DirectionAdmin(TranslationAdmin):
    list_display = ('id', 'name_uz', 'faculty__level', 'is_active')
    list_display_links = ('id', 'name_uz')
    list_filter = ('is_active', 'faculty__level')
    search_fields = ('name',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction', 'course', 'is_active')
    list_filter = ('direction__faculty__level', 'direction', 'course', 'is_active')
    search_fields = ('name', 'direction__name', 'direction__faculty__level')
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

