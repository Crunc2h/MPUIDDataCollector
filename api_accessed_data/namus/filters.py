import datetime
from internal_repr.native.case_data_keys import InternalReprKeysConfig
from internal_repr.models import Source

BASE_URL =  "https://www.namus.gov"
MP_URL_BASE = BASE_URL + "/MissingPersons/Case#/{NAMUS_ID}"


def filter_mp_json_for_internal_repr(json):
    case_data = {}
    case_data[InternalReprKeysConfig.SOURCE] = Source.get_src("namus")
    case_data[InternalReprKeysConfig.SOURCE_LINK] = MP_URL_BASE.format(NAMUS_ID=json["id"])
    case_data[InternalReprKeysConfig.NAMUS_ID] = json["id"]
    case_data[InternalReprKeysConfig.NAMUS_ID_FORMATTED] = json["idFormatted"]
    case_data[InternalReprKeysConfig.NCMEC_NUM] = json.get("caseIdentification", {}).get("ncmecNumber")

    case_data[InternalReprKeysConfig.DT_SOURCE_CREATED] = datetime.datetime.strptime(json["createdDateTime"].split("T")[0], "%Y-%m-%d")
    case_data[InternalReprKeysConfig.DT_SOURCE_LAST_MODIFIED] = datetime.datetime.strptime(json["modifiedDateTime"].split("T")[0], "%Y-%m-%d")

    case_data[InternalReprKeysConfig.CIRCUMSTANCES_OF_DISAPPEARANCE] = json.get("circumstances", {}).get("circumstancesOfDisappearance")
    case_data[InternalReprKeysConfig.CASE_RESOLVED] = json.get("caseIsResolved")

    case_data[InternalReprKeysConfig.DEFAULT_IMAGE_POSTER] = BASE_URL + json.get("hrefDefaultImagePoster")
    case_data[InternalReprKeysConfig.DEFAULT_IMAGE_THUMBNAIL] = BASE_URL + json.get("hrefDefaultImageThumbnail")
    case_data[InternalReprKeysConfig.OTHER_IMAGES] = []
    for image in json.get("images"):
        case_data[InternalReprKeysConfig.OTHER_IMAGES].append(
            {
                InternalReprKeysConfig.IMAGE_POSTER: {
                    InternalReprKeysConfig.RES_HEIGHT: image.get("files", {}).get("original", {}).get("height"),
                    InternalReprKeysConfig.RES_WIDTH: image.get("files", {}).get("original", {}).get("width"),
                    InternalReprKeysConfig.HREF: BASE_URL + image.get("files", {}).get("original", {}).get("href"),
                },
                InternalReprKeysConfig.IMAGE_THUMBNAIL: {
                    InternalReprKeysConfig.RES_HEIGHT: image.get("files", {}).get("thumbnail", {}).get("height"),
                    InternalReprKeysConfig.RES_WIDTH: image.get("files", {}).get("thumbnail", {}).get("width"),
                    InternalReprKeysConfig.HREF: BASE_URL + image.get("files", {}).get("thumbnail", {}).get("href"),
                },
                InternalReprKeysConfig.STR_DOWNLOAD: BASE_URL + image.get("hrefDownload")
            }
        )

    primary_investigating_agency_name = json.get("primaryInvestigatingAgency", {}).get("name")
    case_data[InternalReprKeysConfig.CASE_DATA_INVESTIGATING_AGENCY_PRIMARY] = None
    case_data[InternalReprKeysConfig.CASE_DATA_INVESTIGATING_AGENCIES_SECONDARY] = []
    
    for investigating_agency_data in json.get("investigatingAgencies"):
        contact_info = investigating_agency_data.get("selection", {}).get("contact")
        if investigating_agency_data.get("name") == primary_investigating_agency_name and primary_investigating_agency_name != None:
            case_data[InternalReprKeysConfig.CASE_DATA_INVESTIGATING_AGENCY_PRIMARY] = {
                InternalReprKeysConfig.STR_NAME: primary_investigating_agency_name,
                InternalReprKeysConfig.STATE: investigating_agency_data.get("state", {}).get("name"),
                InternalReprKeysConfig.COUNTY: investigating_agency_data.get("county", {}).get("name"),
                InternalReprKeysConfig.CITY: investigating_agency_data.get("city"),
                InternalReprKeysConfig.STREET: investigating_agency_data.get("selection", {}).get("agency", {}).get("street1"),
                InternalReprKeysConfig.ZIP_CODE: investigating_agency_data.get("selection", {}).get("agency", {}).get("zipCode"),
                InternalReprKeysConfig.PHONE: investigating_agency_data.get("selection", {}).get("agency", {}).get("phone"),
                InternalReprKeysConfig.JURISDICTION: investigating_agency_data.get("selection", {}).get("agency", {}).get("jurisdiction", {}).get("name"),
                InternalReprKeysConfig.AGENCY_TYPE: investigating_agency_data.get("selection", {}).get("agency", {}).get("agencyType", {}).get("name"),
                InternalReprKeysConfig.CASE_NUMBER: investigating_agency_data.get("caseNumber"),
                InternalReprKeysConfig.DT_CASE_REPORTED: None if not investigating_agency_data.get("dateReported") else datetime.datetime.strptime(investigating_agency_data.get("dateReported"), "%Y-%m-%d"),
                
                InternalReprKeysConfig.AGENCY_CONTACT: None if not contact_info else {
                    InternalReprKeysConfig.FIRST_NAME: contact_info.get("firstName"),
                    InternalReprKeysConfig.LAST_NAME: contact_info.get("lastName"),
                    InternalReprKeysConfig.AGENCY_CONTACT_JT: contact_info.get("jobTitle"),
                    InternalReprKeysConfig.AGENCY_CONTACT_JR: contact_info.get("role")
                }
            }
        elif investigating_agency_data.get("name") != None:
            case_data[InternalReprKeysConfig.CASE_DATA_INVESTIGATING_AGENCIES_SECONDARY].append(
                {
                    InternalReprKeysConfig.STR_NAME: investigating_agency_data.get("name"),
                    InternalReprKeysConfig.STATE: investigating_agency_data.get("state", {}).get("name"),
                    InternalReprKeysConfig.COUNTY: investigating_agency_data.get("county", {}).get("name"),
                    InternalReprKeysConfig.CITY: investigating_agency_data.get("city"),
                    InternalReprKeysConfig.STREET: investigating_agency_data.get("selection", {}).get("agency", {}).get("street1"),
                    InternalReprKeysConfig.ZIP_CODE: investigating_agency_data.get("selection", {}).get("agency", {}).get("zipCode"),
                    InternalReprKeysConfig.PHONE: investigating_agency_data.get("selection", {}).get("agency", {}).get("phone"),
                    InternalReprKeysConfig.JURISDICTION: investigating_agency_data.get("selection", {}).get("agency", {}).get("jurisdiction", {}).get("name"),
                    InternalReprKeysConfig.AGENCY_TYPE: investigating_agency_data.get("selection", {}).get("agency", {}).get("agencyType", {}).get("name"),
                    InternalReprKeysConfig.CASE_NUMBER: investigating_agency_data.get("caseNumber"),
                    InternalReprKeysConfig.DT_CASE_REPORTED: None if not investigating_agency_data.get("dateReported") else datetime.datetime.strptime(investigating_agency_data.get("dateReported"), "%Y-%m-%d"),
                    
                    InternalReprKeysConfig.AGENCY_CONTACT: None if not contact_info else {
                        InternalReprKeysConfig.FIRST_NAME: contact_info.get("firstName"),
                        InternalReprKeysConfig.LAST_NAME: contact_info.get("lastName"),
                        InternalReprKeysConfig.AGENCY_CONTACT_JT: contact_info.get("jobTitle"),
                        InternalReprKeysConfig.AGENCY_CONTACT_JR: contact_info.get("role")
                    }
                }
            )

    case_data[InternalReprKeysConfig.CASE_DATA_SUBJECT_IDENTIFICATION] = {
        InternalReprKeysConfig.FIRST_NAME: json.get("subjectIdentification", {}).get("firstName"),
        InternalReprKeysConfig.MIDDLE_NAME: json.get("subjectIdentification", {}).get("middleName"),
        InternalReprKeysConfig.LAST_NAME: json.get("subjectIdentification", {}).get("lastName"),
        InternalReprKeysConfig.NICKNAMES: json.get("subjectIdentification", {}).get("nicknames"),   
    }

    case_data[InternalReprKeysConfig.CASE_DATA_SUBJECT_DEMOGRAPHICS] = {
        InternalReprKeysConfig.CURRENT_MIN_AGE: json.get("subjectIdentification", {}).get("currentMinAge"),
        InternalReprKeysConfig.CURRENT_MAX_AGE: json.get("subjectIdentification", {}).get("currentMaxAge"),
        InternalReprKeysConfig.MISSING_MIN_AGE: json.get("subjectIdentification", {}).get("computedMissingMinAge"),
        InternalReprKeysConfig.MISSING_MAX_AGE: json.get("subjectIdentification", {}).get("computedMissingMaxAge"),
        
        InternalReprKeysConfig.HEIGHT_FROM_INCHES: json.get("subjectDescription", {}).get("heightFrom"),
        InternalReprKeysConfig.HEIGHT_TO_INCHES: json.get("subjectDescription", {}).get("heightTo"),
        InternalReprKeysConfig.WEIGHT_FROM_LBS: json.get("subjectDescription", {}).get("weightFrom"),
        InternalReprKeysConfig.WEIGHT_TO_LBS: json.get("subjectDescription", {}).get("weightTo"),

        InternalReprKeysConfig.PRIMARY_ETHNICITY: json.get("subjectDescription", {}).get("primaryEthnicity", {}).get("name"),
        InternalReprKeysConfig.ETHNICITIES: json.get("subjectDescription", {}).get("ethnicities"),
        InternalReprKeysConfig.GENDER: json.get("subjectDescription", {}).get("sex", {}).get("name"),
        
        InternalReprKeysConfig.TRIBAL_AFFILIATION: json.get("subjectDescription", {}).get("tribalAffiliation", {}).get("name"),
        InternalReprKeysConfig.TRIBE_ASSOCIATIONS: [], 
        
    }

    for tribe_association in json.get("subjectDescription", {}).get("tribeAssociations"):
        case_data[InternalReprKeysConfig.CASE_DATA_SUBJECT_DEMOGRAPHICS][InternalReprKeysConfig.TRIBE_ASSOCIATIONS].append(
            {
                InternalReprKeysConfig.TRIBE_NAME: tribe_association.get("tribe", {}).get("tribeName"),
                InternalReprKeysConfig.TRIBE_ENROLLMENT: tribe_association.get("isEnrolled")
            }
        )

    case_data[InternalReprKeysConfig.CASE_DATA_SUBJECT_PHYSICAL_FEATURES] = {
        InternalReprKeysConfig.HAIR_COLOR: json.get("physicalDescription", {}).get("hairColor", {}).get("name"),
        InternalReprKeysConfig.LEFT_EYE_COLOR: json.get("physicalDescription", {}).get("leftEyeColor", {}).get("name"),
        InternalReprKeysConfig.RIGHT_EYE_COLOR: json.get("physicalDescription", {}).get("rightEyeColor", {}).get("name"),

        InternalReprKeysConfig.HEAD_HAIR_DESC: json.get("physicalDescription", {}).get("headHairDescription"),
        InternalReprKeysConfig.BODY_HAIR_DESC: json.get("physicalDescription", {}).get("bodyHairDescription"),
        InternalReprKeysConfig.FACIAL_HAIR_DESC: json.get("physicalDescription", {}).get("facialHairDescription"),
        InternalReprKeysConfig.EYE_DESC: json.get("physicalDescription", {}).get("eyeDescription")
    }

    case_data[InternalReprKeysConfig.CASE_DATA_SUBJECT_DISTINCTIVE_PHYSICAL_FEATURES] = [ 
        {
            InternalReprKeysConfig.STR_CATEGORY_NAME: physical_feature_description.get("physicalFeature", {}).get("name"),
            InternalReprKeysConfig.STR_DESCRIPTION: physical_feature_description.get("description")
        } for physical_feature_description in json.get("physicalFeatureDescriptions")
          if physical_feature_description.get("physicalFeature", {}).get("name") != None and physical_feature_description.get("description") != None
    ]

    case_data[InternalReprKeysConfig.CASE_DATA_SUBJECT_CLOTHING_AND_ACCESSORIES] = [
        {
            InternalReprKeysConfig.STR_CATEGORY_NAME: clothing_and_accesory_info.get("article", {}).get("name"),
            InternalReprKeysConfig.STR_DESCRIPTION: clothing_and_accesory_info.get("description")
        } for clothing_and_accesory_info in json.get("clothingAndAccessoriesArticles") 
          if clothing_and_accesory_info.get("description") != None and clothing_and_accesory_info.get("article", {}).get("name") != None
    ]

    case_data[InternalReprKeysConfig.CASE_DATA_SUBJECT_VEHICLES] = [
        {
            InternalReprKeysConfig.VEHICLE_YEAR: vehicle_info.get("vehicleYear"),
            InternalReprKeysConfig.VEHICLE_STYLE: vehicle_info.get("vehicleStyle"),
            InternalReprKeysConfig.VEHICLE_COLOR: vehicle_info.get("vehicleColor"),
            InternalReprKeysConfig.VEHICLE_MAKE: vehicle_info.get("vehicleMake"),
            InternalReprKeysConfig.VEHICLE_MODEL: vehicle_info.get("vehicleModel"),
            InternalReprKeysConfig.VEHICLE_TAG_STATE: vehicle_info.get("tagState"),
            InternalReprKeysConfig.VEHICLE_TAG_NUM: vehicle_info.get("tagNumber"),
            InternalReprKeysConfig.VEHICLE_TAG_EXPIRATION_YEAR: vehicle_info.get("tagExpirationYear"),
            InternalReprKeysConfig.VEHICLE_COMMENT: vehicle_info.get("comment")
        } for vehicle_info in json.get("vehicles")
    ]

    case_data[InternalReprKeysConfig.CASE_DATA_SUBJECT_SIGHTING] = {
        InternalReprKeysConfig.DT_SIGHTING: None if not json.get("sighting", {}).get("date") else datetime.datetime.strptime(json.get("sighting", {}).get("date"), "%Y-%m-%d"),
        InternalReprKeysConfig.LOCATION_DATA: {
            InternalReprKeysConfig.FORMATTED_ADDRESS: json.get("sighting", {}).get("publicGeolocation", {}).get("formattedAddress"),
            InternalReprKeysConfig.LATITUDE: json.get("sighting", {}).get("publicGeolocation", {}).get("coordinates", {}).get("lat"),
            InternalReprKeysConfig.LONGITUDE: json.get("sighting", {}).get("publicGeolocation", {}).get("coordinates", {}).get("lon"),
            InternalReprKeysConfig.CITY: json.get("sighting", {}).get("address", {}).get("city"),
            InternalReprKeysConfig.COUNTY: json.get("sighting", {}).get("address", {}).get("county", {}).get("name"),
            InternalReprKeysConfig.STATE: json.get("sighting", {}).get("address", {}).get("state", {}).get("name"),
            InternalReprKeysConfig.ZIP_CODE: json.get("sighting", {}).get("address", {}).get("zipCode"),
            InternalReprKeysConfig.PRIMARY_RESIDENCE_ON_TRIBAL_LAND: json.get("sighting", {}).get("primaryResidenceOnTribalLand", {}).get("name"),
            InternalReprKeysConfig.MISSING_FROM_TRIBAL_LAND: json.get("sighting", {}).get("missingFromTribalLand", {}).get("name")
        }
    }

    return case_data