import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from tuzilma.models import Level, Faculty, Direction, Group


# Removed googletrans import as per the requirement


class Command(BaseCommand):
    help = 'Populate models by strictly reading data and translations from XLSX columns.'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, 'data', 'Guruhlar.xlsx')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        try:
            df = pd.read_excel(file_path, sheet_name=0)

            # Normalize column names by stripping whitespace from beginning/end
            df.columns = df.columns.str.strip()

            if df.empty:
                self.stdout.write(self.style.WARNING('No data found in the Excel file.'))
                return

            # Map Excel column names to more generic names used in the code
            # These are based on the image provided
            col_mapping = {
                'Fakultet_uz': 'Fakultet',
                'Fakultet_en': 'Fakultet_en',
                'Fakultet_ru': 'Fakultet_ru',
                'Daraja_uz': 'Daraja',
                'Daraja_en': 'Daraja_en',
                'Daraja_ru': 'Daraja_ru',
                'Yo\'nalish_uz': 'Yo\'nalish',
                'Yo\'nalish_en': 'Yonalish_en',
                'Yo\'nalish_ru': 'Yonalish_ru',
                'Kurs': 'Kurs',
                'Guruh': 'Guruh',
            }

            df.rename(
                columns={excel_col: code_col for excel_col, code_col in col_mapping.items() if excel_col in df.columns},
                inplace=True)

            core_required_columns = ['Fakultet', 'Daraja', 'Yo\'nalish', 'Kurs', 'Guruh']
            missing_core_columns = [col for col in core_required_columns if col not in df.columns]
            if missing_core_columns:
                self.stdout.write(self.style.ERROR(f'Missing core columns: {missing_core_columns}'))
                return

            for index, row in df.iterrows():
                self.stdout.write(f"\n=== Processing row {index + 2} ===")

                level_name = row['Daraja']
                if pd.isna(level_name):
                    self.stdout.write(self.style.WARNING(f'Missing Daraja value in row {index + 2}'))
                    continue

                defaults = {'is_active': True}
                level, created = Level.objects.get_or_create(name=level_name, defaults=defaults)
                self.stdout.write(
                    f"Level: {level_name} (EN: {level.name_en if level.name_en else 'N/A'}, RU: {level.name_ru if level.name_ru else 'N/A'})")

                faculty_name = row['Fakultet']
                if pd.isna(faculty_name):
                    self.stdout.write(self.style.WARNING(f'Missing Fakultet value in row {index + 2}'))
                    continue

                faculty_name_en = row['Fakultet_en'] if 'Fakultet_en' in df.columns and pd.notna(
                    row['Fakultet_en']) else None
                faculty_name_ru = row['Fakultet_ru'] if 'Fakultet_ru' in df.columns and pd.notna(
                    row['Fakultet_ru']) else None

                defaults = {'level': level, 'is_active': True}
                if faculty_name_en:
                    defaults['name_en'] = faculty_name_en
                if faculty_name_ru:
                    defaults['name_ru'] = faculty_name_ru

                faculty, created = Faculty.objects.get_or_create(
                    name=faculty_name,
                    defaults=defaults
                )

                if not created:
                    updated = False
                    if faculty_name_en and faculty.name_en != faculty_name_en:
                        faculty.name_en = faculty_name_en
                        updated = True
                    if faculty_name_ru and faculty.name_ru != faculty_name_ru:
                        faculty.name_ru = faculty_name_ru
                        updated = True
                    if updated:
                        faculty.save(update_fields=['name_en', 'name_ru'])

                self.stdout.write(
                    f"Faculty: {faculty_name} (EN: {faculty.name_en if faculty.name_en else 'N/A'}, RU: {faculty.name_ru if faculty.name_ru else 'N/A'})")

                direction_name = row['Yo\'nalish']
                if pd.isna(direction_name):
                    self.stdout.write(self.style.WARNING(f'Missing Yo\'nalish value in row {index + 2}'))
                    continue

                direction_name_en = row['Yonalish_en'] if 'Yonalish_en' in df.columns and pd.notna(
                    row['Yonalish_en']) else None
                direction_name_ru = row['Yonalish_ru'] if 'Yonalish_ru' in df.columns and pd.notna(
                    row['Yonalish_ru']) else None

                defaults = {'is_active': True}
                if direction_name_en:
                    defaults['name_en'] = direction_name_en
                if direction_name_ru:
                    defaults['name_ru'] = direction_name_ru

                direction, created = Direction.objects.get_or_create(
                    name=direction_name,
                    faculty=faculty,
                    defaults=defaults
                )

                if not created:
                    updated = False
                    if direction_name_en and direction.name_en != direction_name_en:
                        direction.name_en = direction_name_en
                        updated = True
                    if direction_name_ru and direction.name_ru != direction_name_ru:
                        direction.name_ru = direction_name_ru
                        updated = True
                    if updated:
                        direction.save(update_fields=['name_en', 'name_ru'])

                self.stdout.write(
                    f"Direction: {direction_name} (EN: {direction.name_en if direction.name_en else 'N/A'}, RU: {direction.name_ru if direction.name_ru else 'N/A'})")

                group_name = str(row['Guruh'])
                course = row['Kurs']
                if pd.isna(group_name) or pd.isna(course):
                    self.stdout.write(self.style.WARNING(f'Missing Guruh or Kurs value in row {index + 2}'))
                    continue

                group, created = Group.objects.get_or_create(
                    name=group_name,
                    direction=direction,
                    course=course,
                    defaults={'is_active': True}
                )
                self.stdout.write(f"Group: {group_name}, Course: {course}")

            self.stdout.write(self.style.SUCCESS('Data processing completed! (No automatic translation used)'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing file: {str(e)}'))