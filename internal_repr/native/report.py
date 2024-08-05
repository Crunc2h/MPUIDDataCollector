from internal_repr.models import *

def db_enums_report(enum_types) -> str:
    res = "\n\n>> |======|ENUM TYPES CHECK|======| <<\n"
    for enum_type in enum_types:
        res += f" > {enum_type.objects.all().count()} objects for {enum_type.__name__}\n"
    res += "|============|\n\n"
    return res
    