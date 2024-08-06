from internal_repr.models import INTERNAL_ENUMS

def db_enums_report(enum_types=INTERNAL_ENUMS):
    res = "\n\n>> |======|ENUM TYPES CHECK|======| <<\n\n"
    for enum_type in enum_types:
        res += f" > {enum_type.objects.all().count()} objects for {enum_type.__name__}\n"
    res += "\n|============|\n\n"
    print(res)
    