import datetime

def filter_mp_json_for_internal_repr(json, url):
    case_data = {}
    case_data["source_link"] = url
    case_data["namus_id"] = json["id"]
    case_data["ncmec_number"] = json.get("caseIdentification", {}).get("ncmecNumber")
    case_data["namus_id_formatted"] = json["idFormatted"]

    case_data["created"] = datetime.datetime.strptime(json["createdDateTime"].split("T")[0], "%Y-%m-%d")
    case_data["last_modified"] = datetime.datetime.strptime(json["modifiedDateTime"].split("T")[0], "%Y-%m-%d")

    case_data["circumstances_of_disappearance"] = json.get("circumstances", {}).get("circumstancesOfDisappearance")
    case_data["is_resolved"] = json.get("caseIsResolved")

    primary_investigating_agency_name = json.get("primaryInvestigatingAgency", {}).get("name")
    case_data["primary_investigating_agency"] = None
    case_data["secondary_investigating_agencies"] = []
    
    for investigating_agency_data in json.get("investigatingAgencies"):
        contact_info = investigating_agency_data.get("selection", {}).get("contact", {})
        if investigating_agency_data.get("name") == primary_investigating_agency_name and primary_investigating_agency_name != None:
            case_data["primary_investigating_agency"] = {
                "name": primary_investigating_agency_name,
                "state": investigating_agency_data.get("state", {}).get("name"),
                "county": investigating_agency_data.get("county", {}).get("name"),
                "city": investigating_agency_data.get("city"),
                "street": investigating_agency_data.get("selection", {}).get("agency", {}).get("street1"),
                "zip_code": investigating_agency_data.get("selection", {}).get("agency", {}).get("zipCode"),
                "phone": investigating_agency_data.get("selection", {}).get("agency", {}).get("phone"),
                "jurisdiction": investigating_agency_data.get("selection", {}).get("agency", {}).get("jurisdiction", {}).get("name"),
                "agency_type": investigating_agency_data.get("selection", {}).get("agency", {}).get("agencyType", {}).get("name"),
                "case_number": investigating_agency_data.get("caseNumber"),
                "date_reported": None if not investigating_agency_data.get("dateReported") else datetime.datetime.strptime(investigating_agency_data.get("dateReported"), "%Y-%m-%d"),
                "contact": None if contact_info == {} else {
                    "first_name": contact_info.get("firstName"),
                    "last_name": contact_info.get("lastName"),
                    "job_title": contact_info.get("jobTitle"),
                    "role": contact_info.get("role")
                }
            }
        else:
            case_data["secondary_investigating_agencies"].append(
                {
                    "name": investigating_agency_data.get("name"),
                    "state": investigating_agency_data.get("state", {}).get("name"),
                    "county": investigating_agency_data.get("county", {}).get("name"),
                    "city": investigating_agency_data.get("city"),
                    "street": investigating_agency_data.get("selection", {}).get("agency", {}).get("street1"),
                    "zip_code": investigating_agency_data.get("selection", {}).get("agency", {}).get("zipCode"),
                    "phone": investigating_agency_data.get("selection", {}).get("agency", {}).get("phone"),
                    "jurisdiction": investigating_agency_data.get("selection", {}).get("agency", {}).get("jurisdiction", {}).get("name"),
                    "agency_type": investigating_agency_data.get("selection", {}).get("agency", {}).get("agencyType", {}).get("name"),
                    "case_number": investigating_agency_data.get("caseNumber"),
                    "date_reported": investigating_agency_data.get("dateReported"),
                    "contact": None if contact_info == {} else {
                        "first_name": contact_info.get("firstName"),
                        "last_name": contact_info.get("lastName"),
                        "job_title": contact_info.get("jobTitle"),
                        "role": contact_info.get("role")
                    }
                }
            )


    case_data["subject_identification_data"] = {
        "first_name": json.get("subjectIdentification", {}).get("firstName"),
        "last_name": json.get("subjectIdentification", {}).get("lastName"),
        
        "middle_name": json.get("subjectIdentification", {}).get("middleName"),
        "nicknames": json.get("subjectIdentification", {}).get("nicknames"),
        
    }

    case_data["demographics"] = {
        "current_min_age": json.get("subjectIdentification", {}).get("currentMinAge"),
        "current_max_age": json.get("subjectIdentification", {}).get("currentMaxAge"),
        "missing_min_age": json.get("subjectIdentification", {}).get("computedMissingMinAge"),
        "missing_max_age": json.get("subjectIdentification", {}).get("computedMissingMaxAge"),
        
        "height_from_inches": json.get("subjectDescription", {}).get("heightFrom"),
        "height_to_inches": json.get("subjectDescription", {}).get("heightTo"),
        "weight_from_lbs": json.get("subjectDescription", {}).get("weightFrom"),
        "weight_to_lbs": json.get("subjectDescription", {}).get("weightTo"),

        "primary_ethnicity": json.get("subjectDescription", {}).get("primaryEthnicity", {}).get("name"),
        "ethnicities": json.get("subjectDescription", {}).get("ethnicities"),
        "gender": json.get("subjectDescription", {}).get("sex", {}).get("name"),
        
        "tribal_affiliation": json.get("subjectDescription", {}).get("tribalAffiliation", {}).get("name"),
        "tribe_associations": [], 
        
    }

    for tribe_association in json.get("subjectDescription", {}).get("tribeAssociations"):
        case_data["demographics"]["tribe_associations"].append(
            {
                "tribe_name": tribe_association.get("tribe", {}).get("tribeName"),
                "is_enrolled": tribe_association.get("isEnrolled")
            }
        )

    case_data["physical_features"] = {
        "hair_color": json.get("physicalDescription", {}).get("hairColor", {}).get("name"),
        "left_eye_color": json.get("physicalDescription", {}).get("leftEyeColor", {}).get("name"),
        "right_eye_color": json.get("physicalDescription", {}).get("rightEyeColor", {}).get("name"),

        "head_hair_description": json.get("physicalDescription", {}).get("headHairDescription"),
        "body_hair_description": json.get("physicalDescription", {}).get("bodyHairDescription"),
        "facial_hair_description": json.get("physicalDescription", {}).get("facialHairDescription"),
        "eye_description": json.get("physicalDescription", {}).get("eyeDescription")
    }

    case_data["distinctive_physical_features"] = [ 
        {
            "category_name": physical_feature_description.get("physicalFeature", {}).get("name"),
            "description": physical_feature_description.get("description")
        } for physical_feature_description in json.get("physicalFeatureDescriptions")
          if physical_feature_description.get("physicalFeature", {}).get("name") != None and physical_feature_description.get("description") != None
    ]

    case_data["clothing_and_accessories_info"] = [
        {
            "category_name": clothing_and_accesory_info.get("article", {}).get("name"),
            "description": clothing_and_accesory_info.get("description")
        } for clothing_and_accesory_info in json.get("clothingAndAccessoriesArticles") 
          if clothing_and_accesory_info.get("description") != None and clothing_and_accesory_info.get("article", {}).get("name") != None
    ]

    case_data["vehicles_info"] = [
        {
            "vehicle_year": vehicle_info.get("vehicleYear"),
            "vehicle_style": vehicle_info.get("vehicleStyle"),
            "vehicle_color": vehicle_info.get("vehicleColor"),
            "vehicle_make": vehicle_info.get("vehicleMake"),
            "vehicle_model": vehicle_info.get("vehicleModel"),
            "tag_state": vehicle_info.get("tagState"),
            "tag_number": vehicle_info.get("tagNumber"),
            "tag_expiration_year": vehicle_info.get("tagExpirationYear"),
            "comment": vehicle_info.get("comment")
        } for vehicle_info in json.get("vehicles")
    ]

    case_data["sighting_data"] = {
        "date": None if not json.get("sighting", {}).get("date") else datetime.datetime.strptime(json.get("sighting", {}).get("date"), "%Y-%m-%d"),
        "location_data": {
            "formatted_address": json.get("sighting", {}).get("publicGeolocation", {}).get("formattedAddress"),
            "latitude": json.get("sighting", {}).get("publicGeolocation", {}).get("coordinates", {}).get("lat"),
            "longitude": json.get("sighting", {}).get("publicGeolocation", {}).get("coordinates", {}).get("lon"),
            "city": json.get("sighting", {}).get("address", {}).get("city"),
            "county": json.get("sighting", {}).get("address", {}).get("county", {}).get("name"),
            "state": json.get("sighting", {}).get("address", {}).get("state", {}).get("name"),
            "zip_code": json.get("sighting", {}).get("address", {}).get("zipCode"),
            "primary_residence_on_tribal_land": json.get("sighting", {}).get("primaryResidenceOnTribalLand", {}).get("name"),
            "missing_from_tribal_land": json.get("sighting", {}).get("missingFromTribalLand", {}).get("name")
        }
    }

    return case_data