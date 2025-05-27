from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from .services import Telegram, get_text

OFFICE_CHOICES = (
    ('back_office', 'Back Office'),
    ('front_office', 'Front Office'),
)


class User(AbstractUser):
    first_name = None
    last_name = None

    office = models.CharField(max_length=50, choices=OFFICE_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "Admin "
        verbose_name_plural = "Adminlar "

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() if self.first_name and self.last_name else self.username



class Student(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=2, default='uz')
    is_registered = models.BooleanField(default=False)
    level = models.CharField(max_length=200, null=True, blank=True)
    level_key = models.CharField(max_length=200, null=True, blank=True)
    faculty = models.CharField(max_length=200, null=True, blank=True)
    faculty_key = models.CharField(max_length=200, null=True, blank=True)
    direction = models.CharField(max_length=200, null=True, blank=True)
    direction_key = models.CharField(max_length=200, null=True, blank=True)
    course = models.SmallIntegerField(default=1, null=True, blank=True)
    group = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = "Talaba "
        verbose_name_plural = "Talabalar "

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''} {self.middle_name or ''}".strip()

    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''} {self.middle_name or ''}".strip()


STATUS_CHOICES = (
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('rejected', 'Rejected'),
)

SERVICES_LIST = {
    "recover_password": "Hemis parolini tiklash",
    "changing_personal_data": "Shaxsiy ma’lumotlarni o’zgartirish",
    "study_information": "Universitetda o‘qiyotganligi to‘g‘risidagi ma’lumotnoma olish",
    "rating_record": "Reyting qaydnomasini olish",
    "attendance": "Talabaning darslardan qoldirgan soatlari (Davomat)",
    "graduation_paper": "Bitiruv qog'ozini olish",

    "diplom_request": "Diplom ilovasiga so'rov",
    "contract_info": "Kontrakt to'lovi haqida ma'lumot",
    "transcript_paper": "Transkript qog’ozini olish",
    "gpa_request": "GPA balini olish",
    "rental_contract": "Ijara shartnoma uchun ariza",

    "illness-inform": "Kasallik haqida ma’lumot",
    "custom-question": "Qo'shimcha savol va takliflar",

}

back_office_services = ["changing_personal_data", "attendance", "graduation_paper", "diplom_request"]


class StudentRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    to_service = models.CharField(max_length=200)
    service_slug = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)

    status = models.CharField(max_length=50, default="new", choices=STATUS_CHOICES)
    office = models.CharField(max_length=50, choices=OFFICE_CHOICES, default="front_office")

    response = models.TextField(null=True, blank=True)
    response_file = models.FileField(upload_to='files/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "So'rovlar "
        verbose_name = "So'rov "
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student} - {self.to_service}"

    def save(self, *args, **kwargs):
        with transaction.atomic():

            self.to_service = SERVICES_LIST.get(self.service_slug)

            if self.to_service in back_office_services:
                self.office = "back_office"

            super().save(*args, **kwargs)
            if self.status in ('completed', 'rejected'):
                if self.status == 'completed':
                    status_text = get_text(self.student.language, 'request-success')
                elif self.status == 'rejected':
                    status_text = get_text(self.student.language, 'request-reject')
                response_text = f"{get_text(self.student.language, 'request-number')} {self.id:05d}\n{status_text}\n\n{self.response}"

                Telegram.send_message(self.student.telegram_id, response_text)

                if self.response_file:
                    Telegram.send_file(self.student.telegram_id, self.response_file.path)
                    print(self.response_file.path)

