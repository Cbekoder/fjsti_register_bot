from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Level, Faculty, Direction, Group, Student
from modeltranslation.admin import TranslationAdmin

@admin.register(Level)
class LevelAdmin(TranslationAdmin):
    list_display = ('id', 'name')
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

@admin.register(Faculty)
class FacultyAdmin(TranslationAdmin):
    list_display = ('id', 'name')
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

@admin.register(Direction)
class DirectionAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'faculty')
    search_fields = ('name',)
    list_filter = ('faculty',)

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
class GroupAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'direction')
    search_fields = ('name',)
    list_filter = ('direction',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = ('id', 'telegram_id', 'full_name', 'level', 'faculty', 'direction', 'course', 'group')
    list_display_links = ('id', 'telegram_id', 'full_name')
    search_fields = ('full_name',)
    list_filter = ('level', 'faculty', 'direction', 'course', 'group')