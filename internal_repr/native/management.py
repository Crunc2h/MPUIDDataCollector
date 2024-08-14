from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from internal_repr.models import ALL_TYPES
from internal_repr.models import Source, SourceType, ActiveCases, ArchivedCases, CaseBatch, MPCase, UIDCase
from internal_repr.native.case_stats import CaseStats
from api_accessed_data.namus.test import fetch_case_data

def reset_db(delete_types=ALL_TYPES):
    print("\n > Resetting database...")
    CaseStats.GLOBAL_CASE_COUNT = 0
    CaseStats.MP_CASE_COUNT = 0
    CaseStats.UID_CASE_COUNT = 0 
    for type in delete_types:
        message = type.objects.all().delete()
        print(f" * {type.__name__} - {message[0]} objects deleted")

def delete_all_cases(delete_types=[
    MPCase,
    UIDCase
]):
    print("\n > Deleting all cases...")
    for type in delete_types:
        message = type.objects.all().delete()
        print(f" * {type.__name__} - {message[0]} objects deleted")

def update_db(active_cases_handler, archived_cases_handler, case_batch_handler):

        print(" » Updating the database...")

        mp_cases_batch = case_batch_handler.mp_cases.all()
        mp_cases_active = active_cases_handler.mp_cases.all()
        mp_cases_archived = archived_cases_handler.mp_cases.all()
        
        uid_cases_batch = case_batch_handler.uid_cases.all()
        uid_cases_active = active_cases_handler.uid_cases.all()
        uid_cases_archived = archived_cases_handler.uid_cases.all()
        
        print(" » Updating archived MP cases...")
        mp_cases_archived = update_cases_archived(active_cases=mp_cases_active,
                              archived_cases=mp_cases_archived,
                              new_cases=mp_cases_batch)
        print(f" »  {len(mp_cases_archived)} MP cases got archived.")
        
        print(" » Updating archived UID cases...")
        uid_cases_archived = update_cases_archived(active_cases=uid_cases_active,
                              archived_cases=uid_cases_archived,
                              new_cases=uid_cases_batch)
        print(f" »  {len(uid_cases_archived)} UID cases got archived.")
        
        print(" » Updating active MP cases...")
        active_mp_cases_added, active_mp_cases_archived, active_mp_cases_updated = update_cases_active(active_cases=mp_cases_active,
                                                                                                       archived_cases=mp_cases_archived,
                                                                                                       new_cases=mp_cases_batch)
        print(f" » {len(active_mp_cases_added)} new MP cases are added to the database.\n » {len(active_mp_cases_updated)} MP cases are updated with new information.\
\n » {len(active_mp_cases_archived)} MP cases are directly archived.")
        
        print(" » Updating archived UID cases...")
        active_uid_cases_added, active_uid_cases_archived, active_uid_cases_updated = update_cases_active(active_cases=uid_cases_active,
                                                                                                          archived_cases=uid_cases_archived,
                                                                                                          new_cases=uid_cases_batch)
        print(f" » {len(active_uid_cases_added)} new UID cases are added to the database.\n » {len(active_uid_cases_updated)} UID cases are updated with new information.\
\n » {len(active_uid_cases_archived)} UID cases are directly archived.")
        

        

def update_cases_archived(active_cases, archived_cases, new_cases):
    cases_archived = []
    for case in active_cases:
            case_namus_id = case.namus_id
            try:
                matching_batch_case = new_cases.get(namus_id=case_namus_id)
            except ObjectDoesNotExist:
                active_cases.remove(case)
                archived_cases.add(case)
                cases_archived.append(case)
    return cases_archived

def update_cases_active(active_cases, archived_cases, new_cases):
    new_cases_added = []
    new_cases_archived = []
    cases_active_updated = []

    for case in new_cases:
           case_namus_id = case.namus_id
           try:
               matching_active_case = active_cases.get(namus_id=case_namus_id)
               if case.last_modified != matching_active_case.last_modified:
                   active_cases.remove(matching_active_case)
                   active_cases.add(case)
                   matching_active_case.delete()
                   cases_active_updated.append(case)
               else:
                    case.delete()
           except ObjectDoesNotExist:
               if not case.is_resolved:    
                   active_cases.add(case)
                   new_cases_added.append(case)
               else:
                   try:
                       matching_archived_case = archived_cases.get(namus_id=case_namus_id)
                       case.delete()
                   except ObjectDoesNotExist:
                       archived_cases.mp_cases.add(case)
                       new_cases_archived.append(case)
    return new_cases_added, new_cases_archived, cases_active_updated

def check_untethered_cases():
    
    print(" » Checking the database for untethered cases...")

    untethered_mps = []
    untethered_uids = []
    
    for case in MPCase.objects.all():
        if case.active_storage.count() == 0 and case.archive_storage.count() == 0:
            untethered_mps.append(case)

    for case in UIDCase.objects.all():
        if case.active_storage.count() == 0 and case.archive_storage.count() == 0:
            untethered_uids.append(case)
    
    print(f" » Found and deleted {len(untethered_mps)} MP cases")
    print(f" » Found and deleted {len(untethered_uids)} UID cases")
    
    [case.delete() for case in untethered_mps]
    [case.delete() for case in untethered_uids]

def check_duplicate_cases(active_cases_handler, archived_cases_handler):
    
    print(" » Checking the database for duplicate cases...")
    
    active_mps = active_cases_handler.mp_cases.all()
    active_uids = active_cases_handler.uid_cases.all()
    archived_mps = archived_cases_handler.mp_cases.all()
    archived_uids = archived_cases_handler.uid_cases.all()
    
    duplicate_mps = []
    duplicate_uids = []
    
    mp_del_count = 0
    uid_del_count = 0
    
    for case in active_mps:
        namus_id = case.namus_id
        filtered = active_mps.filter(namus_id=namus_id)
        if filtered.count() > 1:
            filtered.pop()
            duplicate_mps.append(filtered)

    for case in archived_mps:
        namus_id = case.namus_id
        filtered = archived_mps.filter(namus_id=namus_id)
        if filtered.count() > 1:
            filtered.pop()
            duplicate_mps.append(filtered)
    
    for case in active_uids:
        namus_id = case.namus_id
        filtered = active_uids.filter(namus_id=namus_id)
        if filtered.count() > 1:
            filtered.pop()
            duplicate_mps.append(filtered)

    for case in archived_uids:
        namus_id = case.namus_id
        filtered = archived_uids.filter(namus_id=namus_id)
        if filtered.count() > 1:
            filtered.pop()
            duplicate_mps.append(filtered)

    for case_list in duplicate_mps:
        for case in case_list:
            mp_del_count += 1
            case.delete()
    for case_list in duplicate_uids:
        for case in case_list:
            uid_del_count += 1
            case.delete()
    print(f" » Found and deleted {mp_del_count} duplicated MP cases.\n » Found and deleted {uid_del_count} UID cases.")




def reset_test_all():
    delete_all_cases()
    case_batch_handler = CaseBatch()
    active_cases_handler, archived_cases_handler = ActiveCases(), ArchivedCases()
    case_batch_handler.save()
    active_cases_handler.save()
    archived_cases_handler.save()
    namus = Source(name="namus", source_type=SourceType.GOV_BACKED)
    namus.save()
    fetch_case_data("UnidentifiedPersons")
    fetch_case_data("MissingPersons")
    active_cases_handler, archived_cases_handler = ActiveCases.objects.first(), ArchivedCases.objects.first()
    update_db(active_cases_handler, archived_cases_handler, case_batch_handler)
    case_batch_handler.delete()
    check_untethered_cases()
    check_duplicate_cases(active_cases_handler, archived_cases_handler)