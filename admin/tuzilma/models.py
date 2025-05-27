from django.db import models
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from django.conf import settings
from main.services import get_text

LEVEL_NAME_CHOICES = (
    ("Bakalavr", "Bakalavr"),
    ("Magistr", "Magistr"),
    ("Ordinatura", "Ordinatura"),
)

DIRECTION_NAME_CHOICES = (
    ("Biotibbiyot muhandisligi", "Biotibbiyot muhandisligi"),
    ("Oliy hamshiralik ishi", "Oliy hamshiralik ishi"),
    ("Tibbiy profilaktika ishi", "Tibbiy profilaktika ishi"),
    ("Davolash ishi", "Davolash ishi"),
    ("Farmatsiya", "Farmatsiya"),
    ("Pediatriya ishi", "Pediatriya ishi"),
    ("Stomatologiya", "Stomatologiya"),
    ("Fundamental tibbiyot", "Fundamental tibbiyot"),
    ("Xalq tabobati", "Xalq tabobati"),
    ("Akusherlik", "Akusherlik"),
    ("Endokrinologiya", "Endokrinologiya"),
    ("Gigiena", "Gigiena"),
    ("Kardiologiya", "Kardiologiya"),
    ("Laboratoria ishi", "Laboratoria ishi"),
    ("Morfologiya", "Morfologiya"),
    ("Otorinolaringologiya", "Otorinolaringologiya"),
    ("Patologik anatomiya", "Patologik anatomiya"),
    ("Rentgent texnikasi va texnologiyasi", "Rentgent texnikasi va texnologiyasi"),
    ("Sog‘liqni saqlashni boshqarish va jamoat sog‘lig‘ini saqlash", "Sog‘liqni saqlashni boshqarish va jamoat sog‘lig‘ini saqlash"),
    ("Terapiya", "Terapiya"),
    ("Tibbiy-biologik apparatlar, tizimlar va majmualar", "Tibbiy-biologik apparatlar, tizimlar va majmualar"),
    ("Umumiy onkologiya", "Umumiy onkologiya"),
    ("Urologiya", "Urologiya"),
    ("Xirurgiya", "Xirurgiya"),
    ("Akusherlik va ginekologiya", "Akusherlik va ginekologiya"),
    ("Allergologiya va klinik immunologiya", "Allergologiya va klinik immunologiya"),
    ("Anesteziologiya va reanimatologiya", "Anesteziologiya va reanimatologiya"),
    ("Bolalar anesteziologiya va reanimatologiyasi", "Bolalar anesteziologiya va reanimatologiyasi"),
    ("Bolalar kardiorevmatalogiyasi", "Bolalar kardiorevmatalogiyasi"),
    ("Bolalar nefrologiyasi", "Bolalar nefrologiyasi"),
    ("Bolalar nevrologiyasi", "Bolalar nevrologiyasi"),
    ("Bolalar va o‘smir qizlar ginekologiyasi", "Bolalar va o‘smir qizlar ginekologiyasi"),
    ("Bolalar xirurgiyasi", "Bolalar xirurgiyasi"),
    ("Dermatovenerologiya", "Dermatovenerologiya"),
    ("Epidemiologiya", "Epidemiologiya"),
    ("Ftiziatriya", "Ftiziatriya"),
    ("Gemotologiya va transfuziologiya", "Gemotologiya va transfuziologiya"),
    ("Ichki kasalliklar terapiya", "Ichki kasalliklar terapiya"),
    ("Kommunal gigiena", "Kommunal gigiena"),
    ("Mehnat gigienasi", "Mehnat gigienasi"),
    ("Narkologiya", "Narkologiya"),
    ("Nefrologiya", "Nefrologiya"),
    ("Nefrologiya gtmodializ bilan", "Nefrologiya gtmodializ bilan"),
    ("Neonatologiya", "Neonatologiya"),
    ("Nevrologiya", "Nevrologiya"),
    ("Neyroxirurgiya", "Neyroxirurgiya"),
    ("Nutritsiologiya", "Nutritsiologiya"),
    ("Oftalmologiya", "Oftalmologiya"),
    ("Psixiatriya", "Psixiatriya"),
    ("Pulmonologiya", "Pulmonologiya"),
    ("Revmatologiya", "Revmatologiya"),
    ("Terapevtik stomatologiya", "Terapevtik stomatologiya"),
    ("Tibbiy psixologiya", "Tibbiy psixologiya"),
    ("Tibbiy radiologiya", "Tibbiy radiologiya"),
    ("Travmatologiya va ortopediya", "Travmatologiya va ortopediya"),
    ("Yuqumli kasalliklar", "Yuqumli kasalliklar"),
    ("Yuz jag‘ jarroxligi", "Yuz jag‘ jarroxligi"),
)

class Level(models.Model):
    name = models.CharField(max_length=100, choices=LEVEL_NAME_CHOICES, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Ta'lim darajasi "
        verbose_name_plural = "Ta'lim darajalari "

    def __str__(self):
        return self.name

class Direction(models.Model):
    name = models.CharField(max_length=100, choices=DIRECTION_NAME_CHOICES, unique=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Ta'lim yo'nalishi "
        verbose_name_plural = "Ta'lim yo'nalishlari "

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    course = models.SmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Guruh "
        verbose_name_plural = "Guruhlar "

    def __str__(self):
        return self.name



class ScheduleUpload(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, blank=False)
    course = models.SmallIntegerField()
    file = models.FileField(upload_to='schedules/')
    created_at = models.DateTimeField(auto_now_add=True)

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

                # Save the new file with the specified name
            new_path = custom_storage.save(file_name, self.file)
            self.file.name = new_path

        super().save(*args, **kwargs)

    @property
    def file_path(self):
        """
        Return the absolute path to the file.
        """
        if self.file:
            SCHEDULES_STORAGE_PATH = Path(settings.BASE_DIR).parent / "files/schedules"
            return SCHEDULES_STORAGE_PATH / self.file.name
        return None  #


class ScheduleGet(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, blank=False)
    course = models.SmallIntegerField()

    class Meta:
        verbose_name = "Jadval shabloni"
        verbose_name_plural = "Jadval shabloni"
