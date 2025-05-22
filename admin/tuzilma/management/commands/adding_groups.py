from django.core.management.base import BaseCommand
from tuzilma.models import Group, Direction


class Command(BaseCommand):
    help = 'Populate Group model with names from a dictionary'

    def handle(self, *args, **options):
        json_data = {
            "direction_1": {
                "1": ["BM-1124", "BM-1224"],
                "2": ["BM-1523"],
                "3": ["BM-1622", "BM-1722"],
                "4": ["BM-1321", "BM-1421"]
            },
            "direction_2": {
                "1": ["P-5024", "P-5124", "P-5224", "P-5324", "P-5424", "P-5524", "P-5624", "P-5724", "P-5824",
                      "P-5924", "P-5024A", "P-5824 A"],
                "2": ["P-5023", "P-5123", "P-5223", "P-5323", "P-5423", "P-5523", "P-5623", "P-5723"],
                "3": ["PI-5022", "PI-5122", "PI-5222", "PI-5322", "PI-5422", "PI-5522", "PI-5622", "P-5722"],
                "4": ["PI-2621", "PI-2721", "PI-2821", "PI-2921", "P-2621 A"]
            },
            "direction_3": {
                "1": ["S-6024", "S-6124", "S-6224", "S-6324", "S-6424", "S-6524", "S-6624", "Gigiyena-24(Magistratura)",
                      "Gigiyena-24(uzbek)", "Mehnat gigiyenasi-24(uzbek)", "Sog'liqni saqlash-24(magistratura)"],
                "2": ["S-6023", "S-6123", "S-6223", "S-6323", "S-6423", "S-6523", "Gigiena-23", "Mehnat gigienasi-23",
                      "Kommunal gigiena-23", "JSS-23 (uzbek)"],
                "3": ["S-6022", "S-6122", "S-6222", "S-6322", "S-6422", "S-6522", "Gigiena-22 (uzbek)",
                      "Kommunal-22 (uzbek)", "Sog'liqni saqlash-22 (magistratura) qishki"],
                "4": ["S-3121", "S-3021", "S-3421", "S-3021 A"],
                "5": ["S-4020", "S-4220", "S-4120"]
            },
            "direction_4": {
                "1": ["MD-111", "MD-112", "MD-113", "MD-114", "MD-115", "MD-116", "MD-117", "MD-118", "MD-119",
                      "MD-121", "MD-122", "MD-123", "MD-241", "MD-242", "MD-243", "MD-351", "MD-352", "MD-353",
                      "MD-354", "MD-355", "MD-356", "MD-357", "MD-358", "MD-361", "MD-362", "MD-363", "MD-471",
                      "MD-472", "MD-473", "MD-474", "MD-475", "MD-476", "MD-477", "MD-478", "MD-481", "MD-482",
                      "MD-591", "MD-592", "MD-593", "MD-611/1", "MD-611/2", "MD-611/3", "MD-611/4", "MD-611/5",
                      "MD-611/6", "MD-611/7", "MD-611/8", "MD-611/9", "MD-611/10", "ЛД-111", "ЛД-121", "ЛД-122", "0125",
                      "0225", "0325", "Anesteziologiya va reanimatologiya-24(uzbek)",
                      "Allergologiya va klinik immunologiya-24(uzbek)", "Dermatovnerologiya-24(uzbek)",
                      "Laboratoriya ishi-24(uzbek)", "Nevrologiya-24(uzbek)", "Otorinolaringologiya-24(uzbek)",
                      "Oftalmologiya-24(uzbek)", "Patologik anatomiya-24(uzbek)", "Psixiatriya-24(uzbek)",
                      "Travmatologiya va ortopediya-24(uzbek)", "Ftiziatriya-24(uzbek)", "Umumiy xirurgiya-24(uzbek)",
                      "Urologiya-24(uzbek)", "Endokrinalogiya-24 (uzbek)", "Bolalar nevrologiyasi-24(uzbek)",
                      "Pulmonologiya-24 (uzbek)", "Kardiologiya-24(uzbek)", "Epidemiologiya-24(uzbek)",
                      "Neonatologiya-24(uzbek)", "Terapiya-24(uzbek)", "Akusherlik va ginekalogiya-24",
                      "Bolalar anesteziologiya va reanimatologiyasi-24(uzbek)",
                      "Bolalar va o'smir qizlar ginekologiyasi-24", "Bolalar xirurgiyasi-24(uzbek)",
                      "Narkologiya-24(uzbek)", "Neyro-24", "Revmatologiya-24(uzbek)",
                      "Terapevtik stomatologiya-24(uzbek)", "Tibbiy radiologiya-24", "Umumiy onkologiya-24 (uzbek)",
                      "Yuz-jag' jarrohligi-24(uzbek)", "rentgen-24", "Tibbiy-biologik apparatlar,tizimlar va majmualar",
                      "Yuqumli kasalliklar-24", "Tibbiy psixologiya-24(uzbek)", "Kardiologiya-24",
                      "Endokrinologiya-24 (uzbek)"],
                "2": ["MD-231", "MD-232", "MD-233", "MD-234", "MD-235", "MD-236", "MD-237", "MD-238", "MD-239",
                      "MD-2310", "MD-2311", "MD-2312", "MD-2313", "MD-2314", "MD-2315", "MD-2316",
                      "Anesteziologiya-23 (uzbek)", "Allergologiya-23 (uzbek)", "Dermatovenerologiya-23",
                      "Laboratoriya ishi-23", "Nevrologiya-23", "Otorinolaringologiya-23", "Oftalmologiya-23",
                      "Patologik anatomiya-23", "Psixiatriya-23", "Travmotologiya va ortopediya-23", "Ftiziatriya-23",
                      "Umumiy xirurgiya-23", "Urologiya-23", "Endokrinologiya-23", "Bolalar nevrologiyasi-23 (uzbek)",
                      "Pulmonologiya-23-24", "Kardiologiya-23", "Epidemiologiya-23", "Neonatologiya-23",
                      "Neyroxirurgiya-23", "Ichki kasalliklar-23", "Akusher-23 (uzbek)", "Nutritsiologiya-23",
                      "Bolalar anesteziologiya va reanimatologiyasi-23", "Bolalar  va o'smir qizlar ginekologiyasi-23",
                      "Bolalar xirurgiyasi-23 (uzbek)", "Narkologiya-23", "Nefrologiya gemodializ bilan-23",
                      "Revmatologiya-23", "Terapevtik stomatologiya-23", "Umumiy onkologiya-23", "Endokrin-23 (uzbek)",
                      "Terapiya-23 (uzbek)", "Patan-23 (uzbek)", "Onkologiya -23 (uzbek)"],
                "3": ["Anesteziologiya-22 (uzbek)", "Allergologiya-22 (uzbek)", "Dermatovenerologiya-22 (uzbek)",
                      "Laboratoriya-22 (uzbek)", "Nevrologiya-22 (uzbek)", "Lor-22 (uzbek)", "Oftalmologiya-22 (uzbek)",
                      "Patan-22 (uzbek)", "Pediatriya-22 (uzbek)", "Psixiatriya-22 (uzbek)",
                      "Travmotologiya-22 (uzbek)", "Umumiy xirurgiya-22 (uzbek)", "Urologiya-22 (uzbek)",
                      "Endokrinologiya-22 (uzbek)", "Bolalar nevrologiyasi-22 (uzbek)", "Pulmonologiya-22 (uzbek)",
                      "Stomatologiya-22 (uzbek)", "Kardiologiya-22 (uzbek)", "Epidemiologiya-22 (uzbek)",
                      "Neonatologiya-22 (uzbek)", "Ichki kasalliklar-22 (uzbek)", "Akusher-22 (uzbek)",
                      "Mehnat-22 (uzbek)", "Nutritsiologiya-22 (uzbek)", "Lor-22 (rus)",
                      "Laboratoriya-22 (uzbek) qishki", "Xirurgiya 22 (rus)", "Onkologiya-22 (uzbek) qishki"]
            },
            "direction_5": {
                "1": ["FT -1724", "FT-1624", "FT-1524", "F-7024", "F-7124", "F-7224", "F-7324", "F-7424"],
                "2": ["F-7023", "F-7123", "F-7223", "F-7323", "F-7423"],
                "3": ["F-7022", "F-7122", "F-7222"],
                "4": ["F-3221", "F-3321", "F-3321(A)"],
                "5": ["F-4420", "F-4320"]
            },
            "direction_6": {
                "1": ["DI-1", "DI-2", "DI-3", "DI-4", "DI-5", "DI-6", "DI-7", "DI-8", "DI-9", "DI-10", "DI-11", "DI-12",
                      "DI-13", "DI-14", "DI-16", "DI-17", "DI-15", "DI-18", "DI-19", "DI-20", "DI-21", "DI-22", "DI-23",
                      "DI-24", "DI-25", "DI-26", "DI-27", "DI-28", "DI-29", "DI-30", "DI-31", "DI-32", "DI-33", "DI-34",
                      "DI-35", "DI-36", "DI-37", "DI-38", "DI-39", "DI-40", "DI-61", "DI-62", "DI-63", "DI-64", "DI-65",
                      "DI-66", "DI-67", "DI-68", "DI-119", "DI-119-А", "DI-219", "DI-319", "DI-2424", "DI-2524",
                      "DI-2624", "DI-2724", "DI-2824", "DI-2924", "DI-3024", "DI-3124", "DI-3224", "DI-3324", "DI-3424",
                      "DI-3524", "DI-3624", "DI-3724", "DI-3824", "DI-3924", "DI-4024", "DI-4124", "DI-4224", "DI-4324",
                      "DI-4424", "DI-4524", "DI-4624", "DI-4724", "DI-4824", "DI-4924", "Pediatriya-24(uzbek)",
                      "Pediatriya-24", "Bolalar nefrologiyasi-24(uzbek)"],
                "2": ["DI-2423", "DI-2523", "DI-2623", "DI-2723", "DI-2823", "DI-2923", "DI-3023", "DI-3123", "DI-3223",
                      "DI-3323", "DI-3423", "DI-3523", "DI-3623", "DI-3723", "DI-3923", "DI-4023", "DI-4123", "DI-4223",
                      "DI-4323", "DI-4423"],
                "3": ["DI-2422", "DI-2522", "DI-2622", "DI-2722", "DI-2822", "DI-2922", "DI-3022", "DI-3122", "DI-3222",
                      "DI-3322", "DI-3422", "DI-3522", "DI-3622", "DI-3722", "DI-3822", "DI-3922", "DI-4022", "DI-4122",
                      "DI-4222", "DI-4322", "DI-4522-", "DI-4622", "DI-4722"],
                "4": ["DI-1521", "DI-1621", "DI-1721", "DI-1821", "DI-1921", "DI-2021", "DI-2121", "DI-2221", "DI-2321",
                      "DI-2421", "DI-2521", "DI-2621", "DI-2721", "DI-3521", "DI-3621", "DI-3721", "3821DI", "3921 DI",
                      "4021 DI"],
                "5": ["DI-2220", "DI-2320", "DI-2420", "DI-2520", "DI-2620", "DI-2720", "39/20 DI", "DI-2920",
                      "DI-2820", "DI-3020", "DI-3120", "DI-3220", "DI-3320", "DI-3420", "DI-3520", "DI-3720", "DI-3820",
                      "DI-3620", "4020 DI"]
            },
            "direction_7": {
                "1": ["TPI-124", "TPI-224", "TPI-324", "TPI-424", "TPI-524", "TPI-624", "TPI-724", "TPI-924",
                      "TPI-1024"],
                "2": ["TPI-1023", "TPI-1123", "TPI-1323", "TPI-1423"],
                "3": ["TPI-1022", "TPI-1122", "TPI-1222", "TPI-1322", "TPI-1422", "TPI-1522"],
                "4": ["TPI-321", "TPI-421", "TPI-521", "TPI-621", "TPI-721", "TPI-821", "TPI-921", "TPI-1021",
                      "TPI-1121", "TPI-1221", "TPI-323", "TPI-423", "TPI-523", "TPI-623", "TPI-723", "TPI-823",
                      "TPI-923"],
                "5": ["TPI-320", "TPI-420", "TPI-520", "TPI-620", "TPI-720", "TPI-820", "TPI-920", "TPI-1020"]
            },
            "direction_8": {
                "1": ["XT-121", "XT-122", "XT-123"],
                "2": ["XT-221", "XT-222", "XT-223"]
            }
        }

        # Validate data
        # if not isinstance(json_data, list):
        #     self.stderr.write("Error: Data must be a list")
        #     return
        # if not all(isinstance(name, str) for name in json_data):
        #     self.stderr.write("Error: All items must be strings")
        #     return

        group_objects = []
        for direction_data, course_data in json_data.items():
            direction_obj = Direction.objects.get(id = int(direction_data.split("_")[-1]))
            for course_id, groups in course_data.items():
                for group in groups:
                    group_objects.append(Group(name=group, direction=direction_obj, course=int(course_id)))


        # # Remove duplicates and strip whitespace
        # group_names = list(set(name.strip() for name in json_data if name.strip()))
        #
        # # Check existing groups to avoid duplicates
        # existing_groups = set(Group.objects.values_list('name', flat=True))
        # new_groups = [name for name in group_names if name not in existing_groups]

        # if not new_groups:
        #     self.stdout.write("No new groups to add")
        #     return



        # Use bulk_create for efficiency
        try:
            Group.objects.bulk_create(group_objects, ignore_conflicts=True)
            self.stdout.write(f"Successfully added {len(group_objects)} groups")
        except Exception as e:
            self.stderr.write(f"Error adding groups: {str(e)}")
