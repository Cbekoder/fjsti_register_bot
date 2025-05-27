import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from tuzilma.models import Level, Faculty, Direction, Group


class Command(BaseCommand):
    help = 'Populate Group model with names from a dictionary'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, 'data', 'Guruhlar.xlsx')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        try:
            df = pd.read_excel(file_path, sheet_name=0)

            if df.empty:
                self.stdout.write(self.style.WARNING('No data found in the Excel file.'))
                return

            required_columns = ['Fakultet', 'Daraja', 'Yo\'nalish', 'Kurs', 'Guruh']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                self.stdout.write(self.style.ERROR(f'Missing columns: {missing_columns}'))
                return

            for index, row in df.iterrows():
                self.stdout.write(f"\n=== Processing row {index + 2} ===")

                level_name = row['Daraja']
                if pd.isna(level_name):
                    self.stdout.write(self.style.WARNING(f'Missing Daraja value in row {index + 2}'))
                    continue
                level, created = Level.objects.get_or_create(name=level_name, defaults={'is_active': True})
                self.stdout.write(f"Created/Found Level: {level_name}")

                faculty_name = row['Fakultet']
                if pd.isna(faculty_name):
                    self.stdout.write(self.style.WARNING(f'Missing Fakultet value in row {index + 2}'))
                    continue
                faculty, created = Faculty.objects.get_or_create(
                    name=faculty_name,
                    defaults={'level': level, 'is_active': True}
                )
                self.stdout.write(f"Created/Found Faculty: {faculty_name}")

                direction_name = row['Yo\'nalish']
                if pd.isna(direction_name):
                    self.stdout.write(self.style.WARNING(f'Missing Yo\'nalish value in row {index + 2}'))
                    continue
                direction, created = Direction.objects.get_or_create(
                    name=direction_name,
                    defaults={'faculty': faculty, 'is_active': True}
                )
                self.stdout.write(f"Created/Found Direction: {direction_name}")

                group_name = str(row['Guruh'])
                course = row['Kurs']
                if pd.isna(group_name) or pd.isna(course):
                    self.stdout.write(self.style.WARNING(f'Missing Guruh or Kurs value in row {index + 2}'))
                    continue
                group, created = Group.objects.get_or_create(
                    name=group_name,
                    direction=direction,
                    defaults={'course': course, 'is_active': True}
                )
                self.stdout.write(f"Created/Found Group: {group_name}, Course: {course}")

            self.stdout.write(self.style.SUCCESS('Data processing completed successfully!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing file: {str(e)}'))
