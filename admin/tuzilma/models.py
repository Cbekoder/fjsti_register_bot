from django.db import models
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from django.conf import settings
from main.services import get_text


class Level(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nomi")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi")

    class Meta:
        verbose_name = "Ta'lim darajasi "
        verbose_name_plural = "Ta'lim darajalari "

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=100, verbose_name="Fakultet nomi")
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Daraja")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi")

    class Meta:
        verbose_name = "Fakultet "
        verbose_name_plural = "Fakultetlar "

    def __str__(self):
        return self.name


class Direction(models.Model):
    name = models.CharField(max_length=100, verbose_name="Yo‘nalish nomi")
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Fakultet")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi")

    class Meta:
        verbose_name = "Ta'lim yo'nalishi "
        verbose_name_plural = "Ta'lim yo'nalishlari "

    def __str__(self):
        return f"{self.name} | {self.faculty.level.name if self.faculty else 'N/A'}"


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name="Guruh nomi")
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Yo‘nalish")
    course = models.SmallIntegerField(default=1, verbose_name="Kurs")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi")

    class Meta:
        verbose_name = "Guruh "
        verbose_name_plural = "Guruhlar "

    def __str__(self):
        return self.name


class ScheduleUpload(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Yo‘nalish")
    course = models.SmallIntegerField(verbose_name="Kurs")
    file = models.FileField(upload_to='schedules/', verbose_name="Fayl")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuklangan vaqt")

    class Meta:
        verbose_name = "Jadval Yuklash"
        verbose_name_plural = "Jadvallar "
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.SCHEDULES_STORAGE_PATH = Path(settings.BASE_DIR).parent / "files/schedules"
        self.SCHEDULES_STORAGE_PATH.mkdir(parents=True, exist_ok=True)

        custom_storage = FileSystemStorage(location=self.SCHEDULES_STORAGE_PATH)

        if self.file:
            file_name = f"{self.direction.name}_{self.course}_jadval.xlsx"

            if custom_storage.exists(file_name):
                custom_storage.delete(file_name)

            new_path = custom_storage.save(file_name, self.file)
            self.file.name = new_path

        super().save(*args, **kwargs)

    @property
    def file_path(self):
        if self.file:
            SCHEDULES_STORAGE_PATH = Path(settings.BASE_DIR).parent / "files/schedules"
            return SCHEDULES_STORAGE_PATH / self.file.name
        return None


class ScheduleGet(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Yo‘nalish")
    course = models.SmallIntegerField(verbose_name="Kurs")

    class Meta:
        verbose_name = "Jadval shabloni"
        verbose_name_plural = "Jadval shabloni"
