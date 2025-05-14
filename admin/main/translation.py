from modeltranslation.translator import TranslationOptions, register
from .models import Level, Faculty, Direction, Group

@register(Level)
class LevelTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Faculty)
class FacultyTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Direction)
class DirectionTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Group)
class GroupTranslationOptions(TranslationOptions):
    fields = ('name',)