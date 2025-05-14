from django.db import models

class Level(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Direction(models.Model):
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name="directions")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Group(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, blank=True, related_name="groups")
    course = models.SmallIntegerField(default=1)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=200, unique=True, null=True, blank=True)
    language = models.CharField(max_length=2, default='uz')
    is_registered = models.BooleanField(default=False)
    level = models.CharField(max_length=200, null=True, blank=True)
    faculty = models.CharField(max_length=200, null=True, blank=True)
    direction = models.CharField(max_length=200, null=True, blank=True)
    course = models.SmallIntegerField(default=1, null=True, blank=True)
    group = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''} {self.middle_name or ''}".strip()

    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''} {self.middle_name or ''}".strip()