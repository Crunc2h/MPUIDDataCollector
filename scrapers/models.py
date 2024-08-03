from django.db import models

def reset_db():
    Gender.objects.all().delete()
    Ethnicity.objects.all().delete()
    
    HairColor.objects.all().delete()
    EyeColor.objects.all().delete()
    
    TribalAffiliation.objects.all().delete()
    MPCase.objects.all().delete()
    SubjectDescription.objects.all().delete()
    SubjectIdentification.objects.all().delete()
    SubjectRelatedItems.objects.all().delete()
    DescriptiveFeatureArticle.objects.all().delete()
    DescriptiveItemArticle.objects.all().delete()
    Location.objects.all().delete()
    Sighting.objects.all().delete()
    VehicleInformation.objects.all().delete()
    State.objects.all().delete()
    County.objects.all().delete()
    City.objects.all().delete()
    VehicleColor.objects.all().delete()
    VehicleMake.objects.all().delete()
    VehicleModel.objects.all().delete()
    VehicleStyle.objects.all().delete()
    DescriptiveFeatureCategory.objects.all().delete()
    DescriptiveItemCategory.objects.all().delete()
    PrimaryResidenceOnTribalLand.objects.all().delete()
    MissingFromTribalLand.objects.all().delete()
    Tribe.objects.all().delete()

    Agency.objects.all().delete()
    InvestigatingAgencyData.objects.all().delete()
    AgencyContact.objects.all().delete()





######============================MISC DATA TYPES============================######

###==============LOCATION DATA==============###

class State(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_state_from_str(state_str):
        states = State.objects.all()
        matching_state = states.filter(name=state_str)
        if matching_state.count() > 1:
            raise ValueError("There are duplicate states in the database!")
        elif matching_state.count() == 1:
            return matching_state.first()
        elif matching_state.count() == 0:
            new_state = State(name=state_str.title())
            new_state.save()
            return new_state
        
class County(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_county_from_str(county_str):
        counties = County.objects.all()
        matching_county = counties.filter(name=county_str)
        
        if matching_county.count() > 1:
            raise ValueError("There are duplicate counties in the database!")
        elif matching_county.count() == 1:
            return matching_county.first()
        elif matching_county.count() == 0:
            new_county = County(name=county_str.title())
            new_county.save()
            return new_county
        
class City(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_city_from_str(city_str):
        counties = County.objects.all()
        cities = City.objects.all()
        
        matching_city = cities.filter(name=city_str)
        if matching_city.count() > 1:
            raise ValueError("There are duplicate cities in the database!")
        elif matching_city.count() == 1:
            return matching_city.first()
        elif city_str in list(map(lambda county: county.name, counties)):
            return None
        elif matching_city.count() == 0:
            new_city = City(name=city_str.title())
            new_city.save()
            return new_city

class Location(models.Model):
    address = models.CharField(max_length=256, blank=True, null=True)
    zip_code = models.CharField(max_length=256, blank=True, null=True)
    
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="locations", blank=True, null=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="locations", blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="locations", blank=True, null=True)

    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

class Sighting(models.Model):
    date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sightings")

    @staticmethod
    def create_sighting(sighting_data):
        location_data = sighting_data["location_data"]
        
        location = Location(
            address = location_data["formatted_address"],
            zip_code = location_data["zip_code"],
            
            state = None if not location_data["state"] else State.get_state_from_str(location_data["state"].title()),
            county = None if not location_data["county"] else County.get_county_from_str(location_data["county"].title()),
            city = None if not location_data["city"] else City.get_city_from_str(location_data["city"].title()),

            lat = location_data["latitude"],
            lon  = location_data["longitude"]
        )
        location.save()

        sighting = Sighting(
            date = sighting_data["date"],
            location = location
        )
        
        sighting.save()
        return sighting

###============================###

###==============AGENCY RELATED==============###

class AgencyType(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_agency_type_from_str(agency_type_str):
        agency_types = AgencyType.objects.all()
        matching_agency_type = agency_types.filter(name=agency_type_str)
        if matching_agency_type.count() > 1:
            raise ValueError("There are duplicate agency types in the database!")
        elif matching_agency_type.count() == 1:
            return matching_agency_type.first()
        elif matching_agency_type.count() == 0:
            new_agency_type = AgencyType(name=agency_type_str.title())
            new_agency_type.save()
            return new_agency_type

class Jurisdiction(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_jurisdiction_from_str(jurisdiction_str):
        jurisdictions = Jurisdiction.objects.all()
        matching_jurisdiction = jurisdictions.filter(name=jurisdiction_str)
        if matching_jurisdiction.count() > 1:
            raise ValueError("There are duplicate jurisdictions in the database!")
        elif matching_jurisdiction.count() == 1:
            return matching_jurisdiction.first()
        elif matching_jurisdiction.count() == 0:
            new_jurisdiction = Jurisdiction(name=jurisdiction_str.title())
            new_jurisdiction.save()
            return new_jurisdiction

class AgencyContactJobTitle(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_agency_contact_job_title(job_title_str):
        job_titles = AgencyContactJobTitle.objects.all()
        matching_job_title = job_titles.filter(name=job_title_str)
        if matching_job_title.count() > 1:
            raise ValueError("There are duplicate agency contact job titles in the database!")
        elif matching_job_title.count() == 1:
            return matching_job_title.first()
        elif matching_job_title.count() == 0:
            new_job_title = AgencyContactJobTitle(name=job_title_str.title())
            new_job_title.save()
            return new_job_title

class AgencyContactRole(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_agency_contact_role(jurisdiction_str):
        roles = AgencyContactRole.objects.all()
        matching_role = roles.filter(name=jurisdiction_str)
        if matching_role.count() > 1:
            raise ValueError("There are duplicate agency contact roles in the database!")
        elif matching_role.count() == 1:
            return matching_role.first()
        elif matching_role.count() == 0:
            new_role = AgencyContactRole(name=jurisdiction_str.title())
            new_role.save()
            return new_role

class Agency(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=256, blank=True, null=True)

    jurisdiction = models.CharField(max_length=256, blank=True, null=True)
    agency_type = models.CharField(max_length=256, blank=True, null=True)
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="agencies", blank=True, null=True)

    @staticmethod
    def get_agency_from_str(agency_str):
        agencies = Agency.objects.all()
        matching_agency = agencies.filter(name=agency_str)
        if matching_agency.count() > 1:
            raise ValueError("There are duplicate agencies in the database!")
        elif matching_agency.count() == 1:
            return matching_agency.first()
        elif matching_agency.count() == 0:
            return None
    
    @staticmethod
    def create_agency(agency_data):
        agency = Agency(
            name = None if not agency_data["name"] else agency_data["name"].title(),
            phone = None if not agency_data["phone"] else agency_data["phone"].title(),

            jurisdiction = None if not agency_data["jurisdiction"] else Jurisdiction.get_jurisdiction_from_str(agency_data["jurisdiction"].title()),
            agency_type = None if not agency_data["agency_type"] else AgencyType.get_agency_type_from_str(agency_data["agency_type"].title()) 
        )
        agency.save()
        
        
        location = Location(
            state = None if not agency_data["state"] else State.get_state_from_str(agency_data["state"].title()),
            county = None if not agency_data["county"] else County.get_county_from_str(agency_data["county"].title()),
            city = None if not agency_data["city"] else City.get_city_from_str(agency_data["city"].title()),
            
            zip_code = agency_data["zip_code"],
            address = f"{'' if not agency_data['state'] else agency_data['state'] + ', '}\
            {'' if not agency_data['county'] else agency_data['county'] + ', '}\
            {'' if not agency_data['city'] else agency_data['city'] + ', '}\
            {'' if not agency_data['street'] else agency_data['street']}"            
        )
        location.save()

        agency.location = location

        return agency

class AgencyContact(models.Model):
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    full_name = models.CharField(max_length=512, blank=True, null=True)
    
    job_title = models.ForeignKey(AgencyContactJobTitle, on_delete=models.CASCADE, related_name="contacts",blank=True, null=True)
    role = models.ForeignKey(AgencyContactRole, on_delete=models.CASCADE, related_name="contacts",blank=True, null=True)

    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="contacts", blank=True, null=True)

    @staticmethod
    def get_agency_contact_from_str(agency_contact_str):
        agency_contacts = AgencyContact.objects.all()
        matching_contact = agency_contacts.filter(full_name=agency_contact_str)
        if matching_contact.count() > 1:
            raise ValueError("There are duplicate agency contacts in the database!")
        elif matching_contact.count() == 1:
            return matching_contact.first()
        elif matching_contact.count() == 0:
            return None

    @staticmethod
    def create_contact(contact_data):
        contact = AgencyContact(
            first_name = contact_data["first_name"].title(),
            last_name = contact_data["last_name"].title(),
            full_name = contact_data["first_name"].title() + ' ' +contact_data["last_name"].title(), 
            job_title = None if not contact_data["job_title"] else AgencyContactJobTitle.get_agency_contact_job_title(contact_data["job_title"].title()),
            role = None if not contact_data["role"] else AgencyContactRole.get_agency_contact_role(contact_data["role"].title())
        )
        contact.save()
        return contact

class InvestigatingAgencyData(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="investigations", blank=True, null=True)
    contact = models.ForeignKey(AgencyContact, on_delete=models.CASCADE, related_name="investigations", blank=True, null=True)

    case_number = models.CharField(max_length=256, blank=True, null=True)
    date_reported = models.CharField(max_length=256, blank=True, null=True)

    @staticmethod
    def create_investigating_agency_data(investigating_agency_data):
        data = InvestigatingAgencyData(
            case_number = investigating_agency_data["case_number"],
            date_reported = investigating_agency_data["date_reported"]
        )
        data.save()

        agency = None if not investigating_agency_data["name"] else Agency.get_agency_from_str(investigating_agency_data["name"].title())
        if not agency:
            agency = Agency.create_agency(investigating_agency_data)
        
        data.agency = agency
        
        if investigating_agency_data["contact"]:
            contact = AgencyContact.get_agency_contact_from_str(investigating_agency_data["contact"]["first_name"].title() + investigating_agency_data["contact"]["last_name"].title())
            if not contact:
                contact = AgencyContact.create_contact(investigating_agency_data["contact"])
        
            contact.agency = agency
            data.contact = contact
        return data

###============================###

######============================######



######============================SUBJECT INFORMATION============================######

###==============SUBJECT DEMOGRAPHICS==============###

class Gender(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_gender_from_str(gender_str):
        genders = Gender.objects.all()
        matching_gender = genders.filter(name=gender_str)
        if matching_gender.count() > 1:
            raise ValueError("There are duplicate genders in the database!")
        elif matching_gender.count() == 1:
            return matching_gender.first()
        elif matching_gender.count() == 0:
            new_gender = Gender(name=gender_str.title())
            new_gender.save()
            return new_gender
        
class Ethnicity(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_ethnicity_from_str(ethnicity_str):
        ethnicities = Ethnicity.objects.all()
        matching_ethnicity = ethnicities.filter(name=ethnicity_str)
        if matching_ethnicity.count() > 1:
            raise ValueError("There are duplicate ethnicities in the database!")
        elif matching_ethnicity.count() == 1:
            return matching_ethnicity.first()
        elif matching_ethnicity.count() == 0:
            new_ethnicity = Ethnicity(name=ethnicity_str.title())
            new_ethnicity.save()
            return new_ethnicity
             
class TribalAffiliation(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_tribal_affiliation_from_str(affiliation_str):
        affiliations = TribalAffiliation.objects.all()
        matching_affiliation = affiliations.filter(name=affiliation_str)
        if matching_affiliation.count() > 1:
            raise ValueError("There are duplicate tribal affiliations in the database!")
        elif matching_affiliation.count() == 1:
            return matching_affiliation.first()
        elif matching_affiliation.count() == 0:
            new_affiliation = TribalAffiliation(name=affiliation_str.title())
            new_affiliation.save()
            return new_affiliation
        
class Tribe(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_tribe_from_str(tribe_str):
        tribes = Tribe.objects.all()
        matching_tribe = tribes.filter(name=tribe_str)
        if matching_tribe.count() > 1:
            raise ValueError("There are duplicate tribes in the database!")
        elif matching_tribe.count() == 1:
            return matching_tribe.first()
        elif matching_tribe.count() == 0:
            new_tribe = Tribe(name=tribe_str.title())
            new_tribe.save()
            return new_tribe

class TribalAssociation(models.Model):
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE, related_name="associations", blank=True, null=True)
    is_enrolled = models.BooleanField(blank=True, null=True)

class SubjectDemographics(models.Model):
    current_min_age = models.FloatField(blank=True, null=True)
    current_max_age = models.FloatField(blank=True, null=True)
    missing_min_age = models.FloatField(blank=True, null=True)
    missing_max_age = models.FloatField(blank=True, null=True)
    
    height_from_inches = models.FloatField(blank=True, null=True)
    height_to_inches = models.FloatField(blank=True, null=True)
    weight_from_lbs = models.FloatField(blank=True, null=True)
    weight_to_lbs = models.FloatField(blank=True, null=True)

    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name="subject_descriptions", blank=True, null=True)

    primary_ethnicity = models.ForeignKey(Ethnicity, on_delete=models.CASCADE, related_name="subject_demographics_primary", blank=True, null=True)
    ethnicities = models.ManyToManyField(Ethnicity, related_name="subject_demographics_mixed", blank=True)

    tribal_affiliation = models.ForeignKey(TribalAffiliation, on_delete=models.CASCADE, related_name="subject_demographics", blank=True, null=True)
    tribal_associations = models.ManyToManyField(TribalAssociation, related_name="subject_demographics")

    @staticmethod
    def create_subject_demographics(subject_demographics_data):
        
        demographics = SubjectDemographics(
            current_min_age = subject_demographics_data["current_min_age"],
            current_max_age = subject_demographics_data["current_max_age"],
            missing_min_age = subject_demographics_data["missing_min_age"],
            missing_max_age = subject_demographics_data["missing_max_age"],
            
            height_from_inches = subject_demographics_data["height_from_inches"],
            height_to_inches = subject_demographics_data["height_to_inches"],
            weight_from_lbs = subject_demographics_data["weight_from_lbs"],
            weight_to_lbs = subject_demographics_data["weight_to_lbs"],

            primary_ethnicity = None if not subject_demographics_data["primary_ethnicity"] else Ethnicity.get_ethnicity_from_str(subject_demographics_data["primary_ethnicity"].title()),
            gender = None if not subject_demographics_data["gender"] else Gender.get_gender_from_str(subject_demographics_data["gender"].title()),
            tribal_affiliation = None if not subject_demographics_data["tribal_affiliation"] else TribalAffiliation.get_tribal_affiliation_from_str(subject_demographics_data["tribal_affiliation"].title()),
        )
        demographics.save()

        for ethnicity in subject_demographics_data["ethnicities"]:
            if ethnicity and ethnicity["name"]:
                demographics.ethnicities.add(Ethnicity.get_ethnicity_from_str(ethnicity["name"].title()))

        for tribal_association in subject_demographics_data["tribe_associations"]:
            if tribal_association["tribe_name"]:
                tribe = Tribe.get_tribe_from_str(tribal_association["tribe_name"].title())
                enrollment = tribal_association["is_enrolled"]
                association = TribalAssociation(
                    tribe = tribe,
                    is_enrolled = enrollment
                )
                association.save()
                demographics.tribal_associations.add(association)

        return demographics

###============================###

###==============SUBJECT DESCRIPTION==============###

class EyeColor(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_eye_color_from_str(color_str):
        colors = EyeColor.objects.all()
        matching_color = colors.filter(name=color_str)
        if matching_color.count() > 1:
            raise ValueError("There are duplicate eye colors in the database!")
        elif matching_color.count() == 1:
            return matching_color.first()
        elif matching_color.count() == 0:
            new_color = EyeColor(name=color_str.title())
            new_color.save()
            return new_color

class HairColor(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_hair_color_from_str(color_str):
        colors = HairColor.objects.all()
        matching_color = colors.filter(name=color_str)
        if matching_color.count() > 1:
            raise ValueError("There are duplicate hair colors in the database!")
        elif matching_color.count() == 1:
            return matching_color.first()
        elif matching_color.count() == 0:
            new_color = HairColor(name=color_str.title())
            new_color.save()
            return new_color

class DescriptiveFeatureCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_desc_feature_category_from_str(desc_feature_category_str):
        desc_feature_categories = DescriptiveFeatureCategory.objects.all()
        matching_category = desc_feature_categories.filter(name=desc_feature_category_str)
        if matching_category.count() > 1:
            raise ValueError("There are duplicate descriptive feature categories in the database!")
        elif matching_category.count() == 1:
            return matching_category.first()
        elif matching_category.count() == 0:
            new_category = DescriptiveFeatureCategory(name=desc_feature_category_str.title())
            new_category.save()
            return new_category

class SubjectDescription(models.Model):

    hair_color = models.ForeignKey(HairColor, on_delete=models.CASCADE, related_name="subject_descriptions", blank=True, null=True)
    left_eye_color = models.ForeignKey(EyeColor, on_delete=models.CASCADE, related_name="subject_left_eye_descriptions", blank=True, null=True)
    right_eye_color = models.ForeignKey(EyeColor, on_delete=models.CASCADE, related_name="subject_right_eye_descriptions", blank=True, null=True)
    
    head_hair_description = models.CharField(max_length=512, blank=True, null=True)
    body_hair_description = models.CharField(max_length=512, blank=True, null=True)
    facial_hair_description = models.CharField(max_length=512, blank=True, null=True)
    eye_description = models.CharField(max_length=512, blank=True, null=True)

    @staticmethod
    def create_subject_description(**subject_description_data):
        physical_features = subject_description_data["physical_features"]
        
        description = SubjectDescription(

            hair_color = None if not physical_features["hair_color"] else HairColor.get_hair_color_from_str(physical_features["hair_color"].title()),
            left_eye_color = None if not physical_features["left_eye_color"] else EyeColor.get_eye_color_from_str(physical_features["left_eye_color"].title()),
            right_eye_color = None if not physical_features["right_eye_color"] else EyeColor.get_eye_color_from_str(physical_features["right_eye_color"].title()),

            head_hair_description = physical_features["head_hair_description"],
            body_hair_description = physical_features["body_hair_description"],
            facial_hair_description = physical_features["facial_hair_description"],
            eye_description = physical_features["eye_description"],
        )
        description.save()
        
        for distinctive_physical_feature in subject_description_data["distinctive_physical_features"]:
            feature = DescriptiveFeatureArticle(
                category = DescriptiveFeatureCategory.get_desc_feature_category_from_str(distinctive_physical_feature["category_name"].title()),
                description = distinctive_physical_feature["description"],
                subject_description = description
            )
            feature.save()
        
        description.save()
        return description

class DescriptiveFeatureArticle(models.Model):
    category = models.ForeignKey(DescriptiveFeatureCategory, on_delete=models.CASCADE, related_name="articles")
    description = models.TextField(max_length=1000)

    subject_description = models.ForeignKey(SubjectDescription, on_delete=models.CASCADE, related_name="distinctive_physical_features")

###============================###

###==============SUBJECT IDENTIFICATION==============###

class SubjectIdentification(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    
    middle_name = models.CharField(blank=True, null=True, max_length=256)
    nicknames = models.CharField(blank=True, null=True, max_length=1024)
    
    @staticmethod
    def create_subject_identification(subject_identification_data):
        identification = SubjectIdentification(
            first_name = subject_identification_data["first_name"],
            last_name = subject_identification_data["last_name"],
            middle_name = subject_identification_data["middle_name"],
            nicknames = subject_identification_data["nicknames"],
        )

        identification.save()
        return identification

###============================###

###==============SUBJECT RELATED ITEMS==============###

class VehicleColor(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_vehicle_color_from_str(vehicle_color_str):
        vehicle_colors = VehicleColor.objects.all()
        matching_vehicle_color = vehicle_colors.filter(name=vehicle_color_str)
        if matching_vehicle_color.count() > 1:
            raise ValueError("There are duplicate vehicle colors in the database!")
        elif matching_vehicle_color.count() == 1:
            return matching_vehicle_color.first()
        elif matching_vehicle_color.count() == 0:
            new_color = VehicleColor(name=vehicle_color_str.title())
            new_color.save()
            return new_color  

class VehicleMake(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_vehicle_make_from_str(vehicle_make_str):
        vehicle_makes = VehicleMake.objects.all()
        matching_vehicle_make = vehicle_makes.filter(name=vehicle_make_str)
        if matching_vehicle_make.count() > 1:
            raise ValueError("There are duplicate vehicle makes in the database!")
        elif matching_vehicle_make.count() == 1:
            return matching_vehicle_make.first()
        elif matching_vehicle_make.count() == 0:
            new_make = VehicleMake(name=vehicle_make_str.title())
            new_make.save()
            return new_make
        
class VehicleModel(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_vehicle_model_from_str(vehicle_model_str):
        vehicle_models = VehicleModel.objects.all()
        matching_vehicle_model = vehicle_models.filter(name=vehicle_model_str)
        if matching_vehicle_model.count() > 1:
            raise ValueError("There are duplicate vehicle models in the database!")
        elif matching_vehicle_model.count() == 1:
            return matching_vehicle_model.first()
        elif matching_vehicle_model.count() == 0:
            new_model = VehicleModel(name=vehicle_model_str.title())
            new_model.save()
            return new_model
        
class VehicleStyle(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_vehicle_style_from_str(vehicle_style_str):
        vehicle_styles = VehicleStyle.objects.all()
        matching_vehicle_style = vehicle_styles.filter(name=vehicle_style_str)
        if matching_vehicle_style.count() > 1:
            raise ValueError("There are duplicate vehicle styles in the database!")
        elif matching_vehicle_style.count() == 1:
            return matching_vehicle_style.first()
        elif matching_vehicle_style.count() == 0:
            new_style = VehicleStyle(name=vehicle_style_str.title())
            new_style.save()
            return new_style

class DescriptiveItemCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_desc_item_category_from_str(desc_item_category_str):
        desc_item_categories = DescriptiveItemCategory.objects.all()
        matching_category = desc_item_categories.filter(name=desc_item_category_str)
        if matching_category.count() > 1:
            raise ValueError("There are duplicate descriptive item categories in the database!")
        elif matching_category.count() == 1:
            return matching_category.first()
        elif matching_category.count() == 0:
            new_category = DescriptiveItemCategory(name=desc_item_category_str.title())
            new_category.save()
            return new_category

class SubjectRelatedItems(models.Model):
    @staticmethod
    def create_subject_related_items(**subject_related_items_data):
        related_items = SubjectRelatedItems()
        related_items.save()

        for item_article in subject_related_items_data["clothing_and_accessories_info"]:
            item = DescriptiveItemArticle(
                category = DescriptiveItemCategory.get_desc_item_category_from_str(item_article["category_name"].title()),
                description = item_article["description"],

                subject_related_items = related_items
            )
            item.save()

        for vehicle_info in subject_related_items_data["vehicles_info"]:
            vehicle = VehicleInformation(
                vehicle_year = vehicle_info["vehicle_year"],
                tag_expiration_year = vehicle_info["tag_expiration_year"],
                
                tag_state = None if not vehicle_info["tag_state"] else State.get_state_from_str(vehicle_info["tag_state"].title()),
                tag_number = vehicle_info["tag_number"],
                comment = vehicle_info["comment"],
                
                vehicle_make = None if not vehicle_info["vehicle_make"] else VehicleMake.get_vehicle_make_from_str(vehicle_info["vehicle_make"].title()),
                vehicle_model = None if not vehicle_info["vehicle_model"] else VehicleModel.get_vehicle_model_from_str(vehicle_info["vehicle_model"].title()),
                vehicle_style = None if not vehicle_info["vehicle_style"] else VehicleStyle.get_vehicle_style_from_str(vehicle_info["vehicle_style"].title()),
                vehicle_color = None if not vehicle_info["vehicle_color"] else VehicleColor.get_vehicle_color_from_str(vehicle_info["vehicle_color"].title()),

                subject_related_items = related_items
            )
            vehicle.save()
        
        return related_items

class DescriptiveItemArticle(models.Model):
    category = models.ForeignKey(DescriptiveItemCategory, on_delete=models.CASCADE, related_name="items")
    description = models.TextField(max_length=1000)

    subject_related_items = models.ForeignKey(SubjectRelatedItems, on_delete=models.CASCADE, related_name="clothing_and_accessories")

class VehicleInformation(models.Model):
    vehicle_year = models.IntegerField(blank=True, null=True)
    tag_expiration_year = models.IntegerField(blank=True, null=True)
    
    tag_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="vehicles", blank=True, null=True)
    
    tag_number = models.CharField(max_length=256, blank=True, null=True)
    comment = models.CharField(max_length=256, blank=True, null=True)
    
    vehicle_make = models.CharField(max_length=256, blank=True, null=True)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, related_name="vehicles", blank=True, null=True)
    vehicle_style = models.ForeignKey(VehicleStyle, on_delete=models.CASCADE, related_name="vehicles", blank=True, null=True)
    vehicle_color = models.ForeignKey(VehicleColor, on_delete=models.CASCADE, related_name="vehicles", blank=True, null=True)

    subject_related_items = models.ForeignKey(SubjectRelatedItems, on_delete=models.CASCADE, related_name="vehicles_info")

###============================###

######============================######



######============================CASES============================######

###==============MPCASE==============###

class MissingFromTribalLand(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_missing_from_tribal_land_from_str(missing_from_tbland_str):
        missing_from_tblands = MissingFromTribalLand.objects.all()
        matching_mftbland = missing_from_tblands.filter(name=missing_from_tbland_str)
        if matching_mftbland.count() > 1:
            raise ValueError("There are duplicate mftlands in the database!")
        elif matching_mftbland.count() == 1:
            return matching_mftbland.first()
        elif matching_mftbland.count() == 0:
            new_mftbland = MissingFromTribalLand(name=missing_from_tbland_str.title())
            new_mftbland.save()
            return new_mftbland
        
class PrimaryResidenceOnTribalLand(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_primary_residence_on_tribal_land(primary_residence_on_tbland_str):
        pr_on_tblands = PrimaryResidenceOnTribalLand.objects.all()
        matching_pr_on_tbland = pr_on_tblands.filter(name=primary_residence_on_tbland_str)
        if matching_pr_on_tbland.count() > 1:
            raise ValueError("There are duplicate pr_on_tblands in the database!")
        elif matching_pr_on_tbland.count() == 1:
            return matching_pr_on_tbland.first()
        elif matching_pr_on_tbland.count() == 0:
            new_pr_on_tbland = PrimaryResidenceOnTribalLand(name=primary_residence_on_tbland_str.title())
            new_pr_on_tbland.save()
            return new_pr_on_tbland

class MPCase(models.Model):
    
    namus_id = models.CharField(max_length=256)
    namus_id_formatted = models.CharField(max_length=256)
    ncmec_number = models.CharField(max_length=256, blank=True, null=True)
    
    source_link = models.CharField(max_length=2048, blank=True, null=True)
    
    internal_created = models.DateField(auto_now=True)
    case_created = models.DateField()
    case_last_modified = models.DateField()

    identification = models.OneToOneField(SubjectIdentification, on_delete=models.CASCADE, related_name="case")
    demographics = models.OneToOneField(SubjectDemographics, on_delete=models.CASCADE, related_name="case")
    description = models.OneToOneField(SubjectDescription, on_delete=models.CASCADE, related_name="case")
    related_items = models.OneToOneField(SubjectRelatedItems, on_delete=models.CASCADE, related_name="case")
    last_known_location = models.ForeignKey(Sighting, on_delete=models.CASCADE, related_name="cases")

    primary_residence_on_tribal_land = models.ForeignKey(PrimaryResidenceOnTribalLand, on_delete=models.CASCADE, related_name="cases", blank=True, null=True)
    missing_from_tribal_land = models.ForeignKey(MissingFromTribalLand, on_delete=models.CASCADE, related_name="cases", blank=True, null=True)

    circumstances_of_disappearance = models.TextField(max_length=10000, blank=True, null=True)
    
    is_resolved = models.BooleanField(blank=True, null=True)
    
    primary_investigating_agency = models.ForeignKey(InvestigatingAgencyData, on_delete=models.CASCADE, related_name="cases_primary", blank=True, null=True)
    secondary_investigating_agencies = models.ManyToManyField(InvestigatingAgencyData, related_name="cases_secondary", blank=True)

    @staticmethod 
    def create_mp_case(case_data):
        subject_identification_data = case_data["subject_identification_data"]
        subject_demographics_data = case_data["demographics"]

        physical_features = case_data["physical_features"]
        distinctive_physical_features = case_data["distinctive_physical_features"]

        clothing_and_accessories_info = case_data["clothing_and_accessories_info"]
        vehicles_info = case_data["vehicles_info"]

        sighting_data = case_data["sighting_data"]

        subject_identification = SubjectIdentification.create_subject_identification(subject_identification_data)
        subject_demographics = SubjectDemographics.create_subject_demographics(subject_demographics_data)
        subject_description = SubjectDescription.create_subject_description(physical_features=physical_features,
                                                                            distinctive_physical_features=distinctive_physical_features)
        subject_related_items = SubjectRelatedItems.create_subject_related_items(clothing_and_accessories_info=clothing_and_accessories_info,
                                                                                 vehicles_info=vehicles_info)
        last_known_sighting = Sighting.create_sighting(sighting_data)
        
        case = MPCase(
            source_link = case_data["source_link"],
            
            namus_id = case_data["namus_id"],
            namus_id_formatted = case_data["namus_id_formatted"],
            ncmec_number = case_data["ncmec_number"],

            case_created = case_data["created"],
            case_last_modified = case_data["last_modified"],

            circumstances_of_disappearance = case_data["circumstances_of_disappearance"],

            is_resolved = case_data["is_resolved"],

            identification = subject_identification,
            demographics = subject_demographics,
            description = subject_description,
            related_items = subject_related_items,
            last_known_location = last_known_sighting,
            
            primary_residence_on_tribal_land = None if not sighting_data["location_data"]["primary_residence_on_tribal_land"] else PrimaryResidenceOnTribalLand.get_primary_residence_on_tribal_land(sighting_data["location_data"]["primary_residence_on_tribal_land"].title()),
            missing_from_tribal_land = None if not sighting_data["location_data"]["missing_from_tribal_land"] else MissingFromTribalLand.get_missing_from_tribal_land_from_str(sighting_data["location_data"]["missing_from_tribal_land"].title()),

            primary_investigating_agency = None if not case_data["primary_investigating_agency"] else InvestigatingAgencyData.create_investigating_agency_data(case_data["primary_investigating_agency"]),

        )

        case.save()
        
        for investigating_agency_data in case_data["secondary_investigating_agencies"]:
            data_object = InvestigatingAgencyData.create_investigating_agency_data(investigating_agency_data)
            case.secondary_investigating_agencies.add(data_object)

###============================###


    # case_contributors?
"""
    images
    default_image
    documents
    
    "viewPermission":"public",
    "hrefDefaultImageThumbnail":"/api/CaseSets/NamUs/MissingPersons/Cases/61081/Images/Default/Thumbnail",
    "hrefDefaultImagePoster":"/api/CaseSets/NamUs/MissingPersons/Cases/61081/Images/Default/Poster",
"""


















