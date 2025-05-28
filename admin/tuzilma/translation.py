from .models import Level, Faculty, Direction
from modeltranslation.translator import TranslationOptions, register

@register(Level)
class LevelTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Faculty)
class FacultyTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Direction)
class DirectionTranslationOptions(TranslationOptions):
    fields = ('name',)