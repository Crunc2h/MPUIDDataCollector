import grequests, requests, json, functools, traceback
from internal_repr.models import MPCase, UIDCase, CaseBatch
from .filters import filter_mp_json_for_internal_repr, filter_uid_json_for_internal_repr
SEARCH_LIMIT = 10000
REQUEST_BATCH_SIZE = 50
REQUEST_FEEDBACK_INTERVAL = 50
API_ENDPOINT = "https://www.namus.gov/api"
USER_AGENT = "A friendly researcher"
SEARCH_ENDPOINT = API_ENDPOINT + "/CaseSets/NamUs/{type}/Search"
STATE_ENDPOINT = API_ENDPOINT + "/CaseSets/NamUs/States"
CASE_ENDPOINT = API_ENDPOINT + "/CaseSets/NamUs/{type}/Cases/{case}"

CASE_TYPES = {
    "MissingPersons": {"stateField": "stateOfLastContact"},
    "UnidentifiedPersons": {"stateField": "stateOfRecovery"},
    "UnclaimedPersons": {"stateField": "stateFound"},
}

CASE_BATCH_HANDLER = CaseBatch.objects.first()
def fetch_case_data(case_type_r):
    ###DEBUG
    case_type = case_type_r
    ###DEBUG
    if case_type == "MissingPersons":
        feedback_func = requestFeedbackMP
    else:
        feedback_func = requestFeedbackUID
    print(f" » Fetching {case_type} data...")
    print("\n > Fetching states\n")
    states = requests.get(STATE_ENDPOINT, headers={"User-Agent": USER_AGENT}).json()

    global completedCases
    global errors
    completedCases = 0
    errors = ""

    print(" > Fetching case identifiers")
    searchRequests = (
        grequests.post(
                SEARCH_ENDPOINT.format(type=case_type),
                headers={"User-Agent": USER_AGENT, "Content-Type": "application/json"},
                data=json.dumps(
                    {
                        "take": SEARCH_LIMIT,
                        "projections": ["namus2Number"],
                        "predicates": [
                            {
                                "field": CASE_TYPES[case_type]["stateField"],
                                "operator": "IsIn",
                                "values": [state["name"]],
                            }
                        ],
                    }
                ),
            ) for state in states
    )
    searchRequests = grequests.map(searchRequests, size=REQUEST_BATCH_SIZE)

    cases = functools.reduce(
            lambda output, element: output + element.json()["results"],
            searchRequests,
            [],
        )
    print(" > Found %d cases" % len(cases))
    print(" > Starting case processing")

    caseRequests = (
            grequests.get(
                CASE_ENDPOINT.format(type=case_type, case=case["namus2Number"]),
                hooks={"response": feedback_func},
                headers={"User-Agent": USER_AGENT},
            )
            for case in cases
        )
    
    caseRequests = grequests.map(caseRequests, size=REQUEST_BATCH_SIZE)

    for index, case in enumerate(caseRequests):
            if not case:
                print(
                    " > Failed parsing case: {case} index {index}".format(
                        case=cases[index], index=index
                    )
                )
                continue
    
    with open("errors.txt", "w") as errors_file:
         errors_file.write(errors)
    
    print(" > Scraping completed")

def requestFeedbackMP(response, **kwargs):
    global errors
    
    try:
        filtered_case_data = filter_mp_json_for_internal_repr(response.json())
    except Exception as ex:
         traceback.print_exc()
         error = f" >!! {ex}\n"
         print(error)
         errors += error    
         return

    try:
        internal_case_repr = MPCase.create_mp_case(case_data=filtered_case_data)
        CASE_BATCH_HANDLER.uid_cases.add(internal_case_repr)
    except Exception as ex:
        error = f" > {filtered_case_data['namus_id']} --- {ex}\n"
        traceback.print_exc()
        errors += error
        return


    global completedCases
    completedCases = completedCases + 1
    if completedCases % REQUEST_FEEDBACK_INTERVAL == 0:
        print(" > Completed {count} cases".format(count=completedCases))

def requestFeedbackUID(response, **kwargs):
    global errors
    
    try:
        filtered_case_data = filter_uid_json_for_internal_repr(response.json()),
    except Exception as ex:
         traceback.print_exc()
         error = f" >!! {ex}\n"
         print(error)
         errors += error
         return

    try:
        internal_case_repr = UIDCase.create_uid_case(case_data=filtered_case_data)
        CASE_BATCH_HANDLER.uid_cases.add(internal_case_repr)
    except Exception as ex:
        error = f" > {filtered_case_data['namus_id']} --- {ex}\n"
        traceback.print_exc()
        errors += error
        return


    global completedCases
    completedCases = completedCases + 1
    if completedCases % REQUEST_FEEDBACK_INTERVAL == 0:
        print(" > Completed {count} cases".format(count=completedCases))


def fetch_mp_json(namus_id):
    case = requests.get(CASE_ENDPOINT.format(type="MissingPersons", case=namus_id), headers={"User-Agent": USER_AGENT})
    print(case.json())

def fetch_uid_json(namus_id):
    case = requests.get(CASE_ENDPOINT.format(type="UnidentifiedPersons", case=namus_id), headers={"User-Agent": USER_AGENT})
    print(case.json())




               