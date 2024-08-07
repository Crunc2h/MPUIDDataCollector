from internal_repr.models import ALL_TYPES
from internal_repr.models import Source, SourceType
from internal_repr.native.case_stats import CaseStats
from api_accessed_data.namus.test import fetch_missing_persons_data

def reset_db(delete_types=ALL_TYPES):
    print("\n > Resetting database...")
    CaseStats.GLOBAL_CASE_COUNT = 0
    for type in delete_types:
        message = type.objects.all().delete()
        print(f" * {type.__name__} - {message[0]} objects deleted")

def test():
    reset_db()
    namus = Source(name="namus", source_type=SourceType.GOV_BACKED)
    namus.save()
    fetch_missing_persons_data()