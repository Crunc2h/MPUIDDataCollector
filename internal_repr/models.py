import enum
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .native.case_data_keys import InternalReprKeysConfig
from .native.case_stats import CaseStats

class State(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_state_from_str(state_str):
        if not state_str:
            return
        
        state_str = state_str.title()
        states = State.objects.all()
        matching_state = states.filter(name=state_str)
        if matching_state.count() > 1:
            raise ValueError("There are duplicate states in the database!")
        elif matching_state.count() == 1:
            return matching_state.first()
        elif matching_state.count() == 0:
            new_state = State(name=state_str)
            new_state.save()
            return new_state
        
class County(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_county_from_str(county_str):
        if not county_str:
            return 
        county_str = county_str.title()
        counties = County.objects.all()
        matching_county = counties.filter(name=county_str)
        
        if matching_county.count() > 1:
            raise ValueError("There are duplicate counties in the database!")
        elif matching_county.count() == 1:
            return matching_county.first()
        elif matching_county.count() == 0:
            new_county = County(name=county_str)
            new_county.save()
            return new_county
                           
class City(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_city_from_str(city_str):
        if not city_str:
            return
        city_str = city_str.title()
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
            new_city = City(name=city_str)
            new_city.save()
            return new_city

class Location(models.Model):
    address = models.CharField(max_length=256, blank=True)
    zip_code = models.CharField(max_length=256, null=True)
    
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="locations", null=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="locations", null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="locations", null=True)
    street = models.CharField(max_length=256, blank=True, null=True)

    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return self.address

    def save(self, *args, **kwargs):
        if not self.address:
            self.address = f"{'' if not self.state else str(self.state) + ', '}\
{'' if not self.county else str(self.county) + ', '}\
{'' if not self.city else str(self.city)}"
        return super().save(args, kwargs)

class Sighting(models.Model):
    date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sightings")

    def __str__(self) -> str:
        return f" » Sighting in {self.location} on {self.date.strftime('%d/%m/%Y')}"

    @staticmethod
    def create_sighting(sighting_data):
        location_data = sighting_data[InternalReprKeysConfig.LOCATION_DATA]
        
        location = Location(
            address = location_data[InternalReprKeysConfig.FORMATTED_ADDRESS],
            zip_code = location_data[InternalReprKeysConfig.ZIP_CODE],
            
            state = State.get_state_from_str(location_data[InternalReprKeysConfig.STATE]),
            county = County.get_county_from_str(location_data[InternalReprKeysConfig.COUNTY]),
            city =  City.get_city_from_str(location_data[InternalReprKeysConfig.CITY]),

            lat = location_data[InternalReprKeysConfig.LATITUDE],
            lon  = location_data[InternalReprKeysConfig.LONGITUDE]
        )
        location.save()

        sighting = Sighting(
            date = sighting_data[InternalReprKeysConfig.DT_SIGHTING],
            location = location
        )
        
        sighting.save()
        return sighting



class AgencyType(models.Model):
   name = models.CharField(max_length=64)
   def save(self, *args, **kwargs):
       self.name = self.name.title()
       super().save(args, kwargs)
   def __str__(self) -> str:
       return self.name
   @staticmethod
   def get_agency_type_from_str(agency_type_str):
       if not agency_type_str:
           return
       agency_type_str = agency_type_str.title()
       agency_types = AgencyType.objects.all()
       matching_agency_type = agency_types.filter(name=agency_type_str)
       if matching_agency_type.count() > 1:
           raise ValueError("There are duplicate agency types in the database!")
       elif matching_agency_type.count() == 1:
           return matching_agency_type.first()
       elif matching_agency_type.count() == 0:
           new_agency_type = AgencyType(name=agency_type_str)
           new_agency_type.save()
           return new_agency_type  

class Jurisdiction(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_jurisdiction_from_str(jurisdiction_str):
        if not jurisdiction_str:
            return
        jurisdiction_str = jurisdiction_str.title()
        jurisdictions = Jurisdiction.objects.all()
        matching_jurisdiction = jurisdictions.filter(name=jurisdiction_str)
        if matching_jurisdiction.count() > 1:
            raise ValueError("There are duplicate jurisdictions in the database!")
        elif matching_jurisdiction.count() == 1:
            return matching_jurisdiction.first()
        elif matching_jurisdiction.count() == 0:
            new_jurisdiction = Jurisdiction(name=jurisdiction_str)
            new_jurisdiction.save()
            return new_jurisdiction
        
class AgencyContactJobTitle(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_agency_contact_job_title(job_title_str):
        if not job_title_str:
            return
        job_title_str = job_title_str.title()
        job_titles = AgencyContactJobTitle.objects.all()
        matching_job_title = job_titles.filter(name=job_title_str)
        if matching_job_title.count() > 1:
            raise ValueError("There are duplicate agency contact job titles in the database!")
        elif matching_job_title.count() == 1:
            return matching_job_title.first()
        elif matching_job_title.count() == 0:
            new_job_title = AgencyContactJobTitle(name=job_title_str)
            new_job_title.save()
            return new_job_title

class AgencyContactRole(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_agency_contact_role(jurisdiction_str):
        if not jurisdiction_str:
            return
        jurisdiction_str = jurisdiction_str.title()
        
        roles = AgencyContactRole.objects.all()
        matching_role = roles.filter(name=jurisdiction_str)
        if matching_role.count() > 1:
            raise ValueError("There are duplicate agency contact roles in the database!")
        elif matching_role.count() == 1:
            return matching_role.first()
        elif matching_role.count() == 0:
            new_role = AgencyContactRole(name=jurisdiction_str)
            new_role.save()
            return new_role

class Agency(models.Model):
    name = models.CharField(max_length=256)
    phone = models.CharField(max_length=256, null=True)

    jurisdiction = models.CharField(max_length=256, null=True)
    agency_type = models.CharField(max_length=256, null=True)
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="agencies", null=True)

    def __str__(self) -> str:
        return self.name
    
    @staticmethod
    def get_agency_from_str(agency_str):
        if not agency_str:
            return
        agency_str = agency_str.title()
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
            name = agency_data[InternalReprKeysConfig.STR_NAME].title(),
            phone = None if not agency_data[InternalReprKeysConfig.PHONE] else agency_data[InternalReprKeysConfig.PHONE].title(),

            jurisdiction = Jurisdiction.get_jurisdiction_from_str(agency_data[InternalReprKeysConfig.JURISDICTION]),
            agency_type = AgencyType.get_agency_type_from_str(agency_data[InternalReprKeysConfig.AGENCY_TYPE]) 
        )
        agency.save()
        
        
        location = Location(
            state = State.get_state_from_str(agency_data[InternalReprKeysConfig.STATE]),
            county = County.get_county_from_str(agency_data[InternalReprKeysConfig.COUNTY]),
            city = City.get_city_from_str(agency_data[InternalReprKeysConfig.CITY]),
            street = agency_data[InternalReprKeysConfig.STREET],
            zip_code = agency_data[InternalReprKeysConfig.ZIP_CODE],         
               
        )
        location.save()

        agency.location = location

        return agency

class AgencyContact(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    full_name = models.CharField(max_length=512)
    
    job_title = models.ForeignKey(AgencyContactJobTitle, on_delete=models.CASCADE, related_name="contacts", null=True)
    role = models.ForeignKey(AgencyContactRole, on_delete=models.CASCADE, related_name="contacts", null=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="contacts", null=True)

    def __str__(self) -> str:
        return f"{self.full_name}{'' if not self.job_title else ', ' + str(self.job_title)}"

    @staticmethod
    def get_agency_contact_from_str(agency_contact_str):
        if not agency_contact_str:
            return
        agency_contact_str = agency_contact_str.title()
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
            first_name = contact_data[InternalReprKeysConfig.FIRST_NAME].title(),
            last_name = contact_data[InternalReprKeysConfig.LAST_NAME].title(),
            full_name = contact_data[InternalReprKeysConfig.FIRST_NAME].title() + ' ' +contact_data[InternalReprKeysConfig.LAST_NAME].title(), 
            job_title = AgencyContactJobTitle.get_agency_contact_job_title(contact_data[InternalReprKeysConfig.AGENCY_CONTACT_JT]),
            role = AgencyContactRole.get_agency_contact_role(contact_data[InternalReprKeysConfig.AGENCY_CONTACT_JR])
        )
        contact.save()
        return contact

class InvestigatingAgencyData(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.PROTECT, related_name="investigations")
    contact = models.ForeignKey(AgencyContact, on_delete=models.PROTECT, related_name="investigations", null=True)

    case_number = models.CharField(max_length=256, null=True)
    date_reported = models.DateField(max_length=256, null=True)

    def __str__(self) -> str:
        res = f" X Agency: {self.agency}\n"
        res += f" X Case Number: {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.case_number else self.case_number}\n"
        res += f" X Contact: {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.contact else self.contact}\n"
        res += f" X Date Reported: {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.date_reported else self.date_reported}"
        return res
    
    @staticmethod
    def create_investigating_agency_data(investigating_agency_data):
        agency = Agency.get_agency_from_str(investigating_agency_data[InternalReprKeysConfig.STR_NAME])
        if not agency:
            agency = Agency.create_agency(investigating_agency_data)
        
        if investigating_agency_data[InternalReprKeysConfig.AGENCY_CONTACT]:
            contact = AgencyContact.get_agency_contact_from_str(
                    (investigating_agency_data[InternalReprKeysConfig.AGENCY_CONTACT][InternalReprKeysConfig.FIRST_NAME] 
                    + ' ' +investigating_agency_data[InternalReprKeysConfig.AGENCY_CONTACT][InternalReprKeysConfig.LAST_NAME])
                )
            if not contact:
                contact = AgencyContact.create_contact(investigating_agency_data[InternalReprKeysConfig.AGENCY_CONTACT])
            contact.agency = agency
        else:
            contact = None

        
        data = InvestigatingAgencyData(
            agency = agency,
            contact = contact,
            case_number = investigating_agency_data[InternalReprKeysConfig.CASE_NUMBER],
            date_reported = investigating_agency_data[InternalReprKeysConfig.DT_CASE_REPORTED]
        )
        data.save()
        return data



class Gender(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_gender_from_str(gender_str):
        if not gender_str:
            return 
        gender_str = gender_str.title()
        genders = Gender.objects.all()
        matching_gender = genders.filter(name=gender_str)
        if matching_gender.count() > 1:
            raise ValueError("There are duplicate genders in the database!")
        elif matching_gender.count() == 1:
            return matching_gender.first()
        elif matching_gender.count() == 0:
            new_gender = Gender(name=gender_str)
            new_gender.save()
            return new_gender

class Ethnicity(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_ethnicity_from_str(ethnicity_str):
        if not ethnicity_str:
            return
        ethnicity_str = ethnicity_str.title() 
        ethnicities = Ethnicity.objects.all()
        matching_ethnicity = ethnicities.filter(name=ethnicity_str)
        if matching_ethnicity.count() > 1:
            raise ValueError("There are duplicate ethnicities in the database!")
        elif matching_ethnicity.count() == 1:
            return matching_ethnicity.first()
        elif matching_ethnicity.count() == 0:
            new_ethnicity = Ethnicity(name=ethnicity_str)
            new_ethnicity.save()
            return new_ethnicity
        
class EyeColor(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_eye_color_from_str(color_str):
        if not color_str:
            return
        color_str = color_str.title()
        colors = EyeColor.objects.all()
        matching_color = colors.filter(name=color_str)
        if matching_color.count() > 1:
            raise ValueError("There are duplicate eye colors in the database!")
        elif matching_color.count() == 1:
            return matching_color.first()
        elif matching_color.count() == 0:
            new_color = EyeColor(name=color_str)
            new_color.save()
            return new_color

class HairColor(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_hair_color_from_str(color_str):
        if not color_str:
            return
        color_str = color_str.title()
        colors = HairColor.objects.all()
        matching_color = colors.filter(name=color_str)
        if matching_color.count() > 1:
            raise ValueError("There are duplicate hair colors in the database!")
        elif matching_color.count() == 1:
            return matching_color.first()
        elif matching_color.count() == 0:
            new_color = HairColor(name=color_str)
            new_color.save()
            return new_color

class EstimatedAgeGroup(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_et_age_group_from_str(et_age_group_str):
        if not et_age_group_str:
            return
        et_age_group_str = et_age_group_str.title()
        et_age_groups = EstimatedAgeGroup.objects.all()
        matching_et_age_group = et_age_groups.filter(name=et_age_group_str)
        if matching_et_age_group.count() > 1:
            raise ValueError("There are duplicate et_age_group values in the database!")
        elif matching_et_age_group.count() == 1:
            return matching_et_age_group.first()
        elif matching_et_age_group.count() == 0:
            et_age_group = EstimatedAgeGroup(name=et_age_group_str)
            et_age_group.save()
            return et_age_group

class HeightCertainty(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_height_certainty_from_str(height_certainty_str):
        if not height_certainty_str:
            return
        height_certainty_str = height_certainty_str.title()
        height_certainties = HeightCertainty.objects.all()
        matching_height_certainty = height_certainties.filter(name=height_certainty_str)
        if matching_height_certainty.count() > 1:
            raise ValueError("There are duplicate height certainty values in the database!")
        elif matching_height_certainty.count() == 1:
            return matching_height_certainty.first()
        elif matching_height_certainty.count() == 0:
            new_height_certainty = HeightCertainty(name=height_certainty_str)
            new_height_certainty.save()
            return new_height_certainty

class WeightCertainty(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_weight_certainty_from_str(weight_certainty_str):
        if not weight_certainty_str:
            return
        weight_certainty_str = weight_certainty_str.title()
        weight_certainties = WeightCertainty.objects.all()
        matching_weight_certainty = weight_certainties.filter(name=weight_certainty_str)
        if matching_weight_certainty.count() > 1:
            raise ValueError("There are duplicate weight certainty values in the database!")
        elif matching_weight_certainty.count() == 1:
            return matching_weight_certainty.first()
        elif matching_weight_certainty.count() == 0:
            new_weight_certainty = WeightCertainty(name=weight_certainty_str)
            new_weight_certainty.save()
            return new_weight_certainty



class Tribe(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_tribe_from_str(tribe_str):
        if not tribe_str:
            return
        tribe_str = tribe_str.title()
        tribes = Tribe.objects.all()
        matching_tribe = tribes.filter(name=tribe_str)
        if matching_tribe.count() > 1:
            raise ValueError("There are duplicate tribes in the database!")
        elif matching_tribe.count() == 1:
            return matching_tribe.first()
        elif matching_tribe.count() == 0:
            new_tribe = Tribe(name=tribe_str)
            new_tribe.save()
            return new_tribe

class TribalAffiliation(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_tribal_affiliation_from_str(affiliation_str):
        if not affiliation_str:
            return
        affiliation_str = affiliation_str.title()
        affiliations = TribalAffiliation.objects.all()
        matching_affiliation = affiliations.filter(name=affiliation_str)
        if matching_affiliation.count() > 1:
            raise ValueError("There are duplicate tribal affiliations in the database!")
        elif matching_affiliation.count() == 1:
            return matching_affiliation.first()
        elif matching_affiliation.count() == 0:
            new_affiliation = TribalAffiliation(name=affiliation_str)
            new_affiliation.save()
            return new_affiliation

class TribalAssociation(models.Model):
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE, related_name="associations")
    is_enrolled = models.BooleanField(null=True)

    def __str__(self) -> str:
        res = f" » Tribe Name: {self.tribe.name}\n"
        if self.is_enrolled is None:
            res += f" » Enrollment: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            if self.is_enrolled:
                res += f" » Enrollment: {InternalReprKeysConfig.STR_YES}\n"
            else:
                res += f" » Enrollment: {InternalReprKeysConfig.STR_NO}\n"
        return res

class PrimaryResidenceOnTribalLand(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_primary_residence_on_tribal_land(primary_residence_on_tbland_str):
        if not primary_residence_on_tbland_str:
            return
        primary_residence_on_tbland_str = primary_residence_on_tbland_str.title()
        pr_on_tblands = PrimaryResidenceOnTribalLand.objects.all()
        matching_pr_on_tbland = pr_on_tblands.filter(name=primary_residence_on_tbland_str)
        if matching_pr_on_tbland.count() > 1:
            raise ValueError("There are duplicate pr_on_tblands in the database!")
        elif matching_pr_on_tbland.count() == 1:
            return matching_pr_on_tbland.first()
        elif matching_pr_on_tbland.count() == 0:
            new_pr_on_tbland = PrimaryResidenceOnTribalLand(name=primary_residence_on_tbland_str)
            new_pr_on_tbland.save()
            return new_pr_on_tbland

class MissingFromTribalLand(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_missing_from_tribal_land_from_str(missing_from_tbland_str):
        if not missing_from_tbland_str:
            return
        missing_from_tbland_str = missing_from_tbland_str.title()
        missing_from_tblands = MissingFromTribalLand.objects.all()
        matching_mftbland = missing_from_tblands.filter(name=missing_from_tbland_str)
        if matching_mftbland.count() > 1:
            raise ValueError("There are duplicate mftlands in the database!")
        elif matching_mftbland.count() == 1:
            return matching_mftbland.first()
        elif matching_mftbland.count() == 0:
            new_mftbland = MissingFromTribalLand(name=missing_from_tbland_str)
            new_mftbland.save()
            return new_mftbland

class FoundOnTribalLand(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_found_on_tbland_from_str(found_on_tbland_str):
        if not found_on_tbland_str:
            return
        found_on_tbland_str = found_on_tbland_str.title()
        found_on_tblands = FoundOnTribalLand.objects.all()
        matching_found_on_tbland = found_on_tblands.filter(name=found_on_tbland_str)
        if matching_found_on_tbland.count() > 1:
            raise ValueError("There are duplicate mftlands in the database!")
        elif matching_found_on_tbland.count() == 1:
            return matching_found_on_tbland.first()
        elif matching_found_on_tbland.count() == 0:
            new_found_on_tbland = FoundOnTribalLand(name=found_on_tbland_str)
            new_found_on_tbland.save()
            return new_found_on_tbland



class ConditionOfRemains(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_c_of_remains_from_str(c_of_remains_str):
        if not c_of_remains_str:
            return
        c_of_remains_str = c_of_remains_str.title()
        c_of_remains = ConditionOfRemains.objects.all()
        matching_c_of_r = c_of_remains.filter(name=c_of_remains_str)
        if matching_c_of_r.count() > 1:
            raise ValueError("There are duplicate c_of_remains values in the database!")
        elif matching_c_of_r.count() == 1:
            return matching_c_of_r.first()
        elif matching_c_of_r.count() == 0:
            new_c_of_r = ConditionOfRemains(name=c_of_remains_str)
            new_c_of_r.save()
            return new_c_of_r

class DetailsOfRecovery(models.Model):
    condition_of_remains = models.ForeignKey(ConditionOfRemains, on_delete=models.CASCADE, related_name="recovery_details", null=True)
    
    head_not_recovered = models.BooleanField(blank=True, default=False)
    torso_not_recovered = models.BooleanField(blank=True, default=False)
    limbs_not_recovered = models.BooleanField(blank=True, default=False)
    hands_not_recovered = models.BooleanField(blank=True, default=False)
    all_parts_recovered = models.BooleanField(blank=True, default=False)
    
    def __str__(self) -> str:
        res = "»» |======| DETAILS OF RECOVERY |======| ««\n"
        res += f" » Condition of Remains: {self.condition_of_remains}\n"
        if self.all_parts_recovered:
            res += " » Recovery: All parts recovered\n"
        else:
            res += f" » Head Not Recovered: {self.head_not_recovered}\n"
            res += f" » Torso Not Recovered: {self.head_not_recovered}\n"
            res += f" » Limbs Not Recovered: {self.head_not_recovered}\n"
            res += f" » Hands Not Recovered: {self.head_not_recovered}\n"
    
        return res


    @staticmethod
    def create_details_of_recovery(case_data):
        details_of_recovery = DetailsOfRecovery(
            condition_of_remains = ConditionOfRemains.get_c_of_remains_from_str(case_data[InternalReprKeysConfig.DETAILS_OF_RECOVERY][InternalReprKeysConfig.CONDITION_OF_REMAINS]),
            
            head_not_recovered = False if not case_data[InternalReprKeysConfig.DETAILS_OF_RECOVERY][InternalReprKeysConfig.HEAD_NOT_RECOVERED] else case_data[InternalReprKeysConfig.DETAILS_OF_RECOVERY][InternalReprKeysConfig.HEAD_NOT_RECOVERED],
            torso_not_recovered = False if not case_data[InternalReprKeysConfig.DETAILS_OF_RECOVERY][InternalReprKeysConfig.TORSO_NOT_RECOVERED] else case_data[InternalReprKeysConfig.DETAILS_OF_RECOVERY][InternalReprKeysConfig.TORSO_NOT_RECOVERED],
            limbs_not_recovered = False if not case_data[InternalReprKeysConfig.DETAILS_OF_RECOVERY][InternalReprKeysConfig.LIMBS_NOT_RECOVERED] else case_data[InternalReprKeysConfig.DETAILS_OF_RECOVERY][InternalReprKeysConfig.LIMBS_NOT_RECOVERED],
            hands_not_recovered = False if not case_data[InternalReprKeysConfig.DETAILS_OF_RECOVERY][InternalReprKeysConfig.HANDS_NOT_RECOVERED] else case_data[InternalReprKeysConfig.DETAILS_OF_RECOVERY][InternalReprKeysConfig.HANDS_NOT_RECOVERED]
        )
        if (not details_of_recovery.head_not_recovered and 
        not details_of_recovery.torso_not_recovered and 
        not details_of_recovery.limbs_not_recovered and 
        not details_of_recovery.hands_not_recovered):
            details_of_recovery.all_parts_recovered = True
        
        details_of_recovery.save()
        return details_of_recovery



@enum.unique
class CaseType(enum.Enum):
    MP = "Missing Persons Case"
    UID = "Unidentified Body Case"

    @classmethod
    def choices(cls):
        return [(item.name, item.value) for item in cls]

@enum.unique
class SourceType(enum.Enum):
    GOV_BACKED = "Government Backed"
    PRIVATE = "Private"

    @classmethod
    def choices(cls):
        return [(item.name, item.value) for item in cls]

class Source(models.Model):
    name = models.CharField(max_length=64)
    source_type = models.CharField(max_length=256)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super().save()

    def __str__(self) -> str:
        return self.name
    
    @staticmethod
    def get_src(src_name):
        src_name = src_name.lower()
        source = Source.objects.filter(name=src_name)
        if source.count() > 1:
            raise ValueError("Duplicate sources in the database.")
        elif source.count() == 0:
            return None
        return source.first()

class CaseSource(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="related_cases")
    link = models.CharField(max_length=4096)

    def __str__(self) -> str:
        return f" * {self.source} - {self.link}"

class Image(models.Model):
    poster_href = models.CharField(max_length=4096)
    thumbnail_href = models.CharField(max_length=4096)
    file_path = models.CharField(max_length=512, blank=True, default=InternalReprKeysConfig.STR_NONE)
    
    height_poster = models.IntegerField(null=True)
    width_poster = models.IntegerField(null=True)
    height_thumbnail = models.IntegerField(null=True)
    width_thumbnail = models.IntegerField(null=True)
    
    download_link = models.CharField(max_length=4096, null=True)

class CaseImages(models.Model):
    default_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="case_images_default")
    other_images = models.ManyToManyField(Image, related_name="case_images_other")

    @staticmethod
    def create_case_images(case_images_data):
        default_image = Image(
            poster_href = case_images_data[InternalReprKeysConfig.DEFAULT_IMAGE_POSTER],
            thumbnail_href = case_images_data[InternalReprKeysConfig.DEFAULT_IMAGE_THUMBNAIL]
        )
        default_image.save()

        case_images = CaseImages(default_image=default_image)
        case_images.save()

        for image in case_images_data[InternalReprKeysConfig.OTHER_IMAGES]:
            image_obj = Image(
                poster_href = image[InternalReprKeysConfig.IMAGE_POSTER][InternalReprKeysConfig.HREF],
                thumbnail_href = image[InternalReprKeysConfig.IMAGE_POSTER][InternalReprKeysConfig.HREF],
                download_link = image[InternalReprKeysConfig.STR_DOWNLOAD],
                height_poster = image[InternalReprKeysConfig.IMAGE_POSTER][InternalReprKeysConfig.RES_HEIGHT],
                width_poster = image[InternalReprKeysConfig.IMAGE_POSTER][InternalReprKeysConfig.RES_WIDTH],
                height_thumbnail = image[InternalReprKeysConfig.IMAGE_THUMBNAIL][InternalReprKeysConfig.RES_HEIGHT],
                width_thumbnail = image[InternalReprKeysConfig.IMAGE_THUMBNAIL][InternalReprKeysConfig.RES_WIDTH]
            )
            image_obj.save()
            case_images.other_images.add(image_obj)
        
        return case_images
@receiver(post_delete, sender=CaseImages)
def handle_case_images_delete(sender, instance, **kwargs):
    instance.default_image.delete()
    for image in instance.other_images.all():
        image.delete()



class DescriptiveItemCategory(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_desc_item_category_from_str(desc_item_category_str):
        if not desc_item_category_str:
            return
        desc_item_category_str = desc_item_category_str.title()
        desc_item_categories = DescriptiveItemCategory.objects.all()
        matching_category = desc_item_categories.filter(name=desc_item_category_str)
        if matching_category.count() > 1:
            raise ValueError("There are duplicate descriptive item categories in the database!")
        elif matching_category.count() == 1:
            return matching_category.first()
        elif matching_category.count() == 0:
            new_category = DescriptiveItemCategory(name=desc_item_category_str)
            new_category.save()
            return new_category

class DescriptiveFeatureCategory(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_desc_feature_category_from_str(desc_feature_category_str):
        if not desc_feature_category_str:
            return
        desc_feature_category_str = desc_feature_category_str.title()
        desc_feature_categories = DescriptiveFeatureCategory.objects.all()
        matching_category = desc_feature_categories.filter(name=desc_feature_category_str)
        if matching_category.count() > 1:
            raise ValueError("There are duplicate descriptive feature categories in the database!")
        elif matching_category.count() == 1:
            return matching_category.first()
        elif matching_category.count() == 0:
            new_category = DescriptiveFeatureCategory(name=desc_feature_category_str)
            new_category.save()
            return new_category



class SubjectRelatedItems(models.Model):
    def __str__(self) -> str:
        res = ""
        if self.clothing_and_accessories.count() > 0:
            res += "\n»» |======| CLOTHING AND ACCESSORIES |======| ««\n\n"
            for clothing_or_accessory in self.clothing_and_accessories.all():
                res += "--------------------------------------------------------------------------------------------------------------------\n"
                res += str(clothing_or_accessory) + '\n'
        
        if self.vehicles_info.count() > 0:
            res += "\n»» |======| VEHICLES |======| ««\n"
            for vehicle_info in self.vehicles_info.all():
                res += "--------------------------------------------------------------------------------------------------------------------\n"
                
                res += f" » Tag Number: {InternalReprKeysConfig.STR_NOT_PROVIDED if not vehicle_info.tag_number else vehicle_info.tag_number}\n"
                res += f" » Tag State: {InternalReprKeysConfig.STR_NOT_PROVIDED if not vehicle_info.tag_state else vehicle_info.tag_state}\n"
                res += f" » Tag Year: {InternalReprKeysConfig.STR_NOT_PROVIDED if not vehicle_info.vehicle_year else vehicle_info.vehicle_year}\n"
                res += f" » Tag Expiration Year: {InternalReprKeysConfig.STR_NOT_PROVIDED if not vehicle_info.tag_expiration_year else vehicle_info.tag_expiration_year}\n"
                res += f" » Make: {InternalReprKeysConfig.STR_NOT_PROVIDED if not vehicle_info.vehicle_make else vehicle_info.vehicle_make}\n"
                res += f" » Model: {InternalReprKeysConfig.STR_NOT_PROVIDED if not vehicle_info.vehicle_model else vehicle_info.vehicle_model}\n"
                res += f" » Style: {InternalReprKeysConfig.STR_NOT_PROVIDED if not vehicle_info.vehicle_style else vehicle_info.vehicle_style}\n"
                res += f" » Color: {InternalReprKeysConfig.STR_NOT_PROVIDED if not vehicle_info.vehicle_color else vehicle_info.vehicle_year}\n"

                if vehicle_info.comment:
                    res += f" * {vehicle_info.comment}\n"
        
        return res
                
    @staticmethod
    def create_subject_related_items(case_data):
        related_items = SubjectRelatedItems()
        related_items.save()

        for item_article in case_data[InternalReprKeysConfig.CLOTHING_AND_ACCESSORIES]:
            item = DescriptiveItemArticle(
                category = DescriptiveItemCategory.get_desc_item_category_from_str(item_article[InternalReprKeysConfig.STR_CATEGORY_NAME]),
                description = item_article[InternalReprKeysConfig.STR_DESCRIPTION],

                subject_related_items = related_items
            )
            item.save()

        for vehicle_info in case_data[InternalReprKeysConfig.VEHICLES]:
            vehicle = VehicleInformation(
                vehicle_year = vehicle_info[InternalReprKeysConfig.VEHICLE_YEAR],
                tag_expiration_year = vehicle_info[InternalReprKeysConfig.VEHICLE_TAG_EXPIRATION_YEAR],
                
                tag_state = State.get_state_from_str(vehicle_info[InternalReprKeysConfig.VEHICLE_TAG_STATE]),
                tag_number = vehicle_info[InternalReprKeysConfig.VEHICLE_TAG_NUM],
                comment = vehicle_info[InternalReprKeysConfig.VEHICLE_COMMENT],
                
                vehicle_make = VehicleMake.get_vehicle_make_from_str(vehicle_info[InternalReprKeysConfig.VEHICLE_MAKE]),
                vehicle_model = VehicleModel.get_vehicle_model_from_str(vehicle_info[InternalReprKeysConfig.VEHICLE_MODEL]),
                vehicle_style = VehicleStyle.get_vehicle_style_from_str(vehicle_info[InternalReprKeysConfig.VEHICLE_STYLE]),
                vehicle_color = VehicleColor.get_vehicle_color_from_str(vehicle_info[InternalReprKeysConfig.VEHICLE_COLOR]),

                subject_related_items = related_items
            )
            vehicle.save()
        
        return related_items

class SubjectDescription(models.Model):

    hair_color = models.ForeignKey(HairColor, on_delete=models.PROTECT, related_name="mp_subject_descriptions", null=True)
    left_eye_color = models.ForeignKey(EyeColor, on_delete=models.PROTECT, related_name="mp_subject_left_eye_descriptions", null=True)
    right_eye_color = models.ForeignKey(EyeColor, on_delete=models.PROTECT, related_name="mp_subject_right_eye_descriptions", null=True)
    
    head_hair_description = models.CharField(max_length=512, null=True)
    body_hair_description = models.CharField(max_length=512, null=True)
    facial_hair_description = models.CharField(max_length=512, null=True)
    eye_description = models.CharField(max_length=512, null=True)

    def __str__(self) -> str:
        res = "»» |======| DESCRIPTION |======| ««\n"
        res += f" » Hair Color: {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.hair_color else self.hair_color}\n"
        res += f" » Left Eye Color: {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.left_eye_color else self.left_eye_color}\n"
        res += f" » Right Eye Color: {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.right_eye_color else self.right_eye_color}\n"
    
        res += f" » Head Hair Description: {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.head_hair_description else self.head_hair_description}\n"
        res += f" » Body Hair Description: {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.body_hair_description else self.body_hair_description}\n"
        res += f" » Facial Hair Description: {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.facial_hair_description else self.facial_hair_description}\n"
        res += f" » Eye Description: {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.eye_description else self.eye_description}\n"

        if self.distinctive_physical_features.count() > 0:
            res += " »» Other Descriptive Features ««\n"
            for feature in self.distinctive_physical_features.all():
                res += str(feature)

        return res
    
    @staticmethod
    def create_subject_description(subject_description_data):
        physical_features = subject_description_data[InternalReprKeysConfig.PHYSICAL_FEATURES]
        
        description = SubjectDescription(

            hair_color = HairColor.get_hair_color_from_str(physical_features[InternalReprKeysConfig.HAIR_COLOR]),
            left_eye_color = EyeColor.get_eye_color_from_str(physical_features[InternalReprKeysConfig.LEFT_EYE_COLOR]),
            right_eye_color = EyeColor.get_eye_color_from_str(physical_features[InternalReprKeysConfig.RIGHT_EYE_COLOR]),

            head_hair_description = physical_features[InternalReprKeysConfig.HEAD_HAIR_DESC],
            body_hair_description = physical_features[InternalReprKeysConfig.BODY_HAIR_DESC],
            facial_hair_description = physical_features[InternalReprKeysConfig.FACIAL_HAIR_DESC],
            eye_description = physical_features[InternalReprKeysConfig.EYE_DESC],
        )
        description.save()
        
        for distinctive_physical_feature in subject_description_data[InternalReprKeysConfig.DISTINCTIVE_PHYSICAL_FEATURES]:
            feature = DescriptiveFeatureArticle(
                category = DescriptiveFeatureCategory.get_desc_feature_category_from_str(distinctive_physical_feature[InternalReprKeysConfig.STR_CATEGORY_NAME]),
                description = distinctive_physical_feature[InternalReprKeysConfig.STR_DESCRIPTION],
                subject_description = description
            )
            feature.save()
        
        description.save()
        return description



class DescriptiveItemArticle(models.Model):
    category = models.ForeignKey(DescriptiveItemCategory, on_delete=models.CASCADE, related_name="items")
    description = models.TextField(max_length=1000)

    subject_related_items = models.ForeignKey(SubjectRelatedItems, on_delete=models.CASCADE, related_name="clothing_and_accessories")

    def __str__(self) -> str:
        return f" » {self.category}: {self.description}"

class DescriptiveFeatureArticle(models.Model):
    category = models.ForeignKey(DescriptiveFeatureCategory, on_delete=models.PROTECT, related_name="articles")
    description = models.TextField(max_length=1000)

    subject_description = models.ForeignKey(SubjectDescription, on_delete=models.CASCADE, related_name="distinctive_physical_features")

    def __str__(self) -> str:
        return f" » {self.category}: {self.description}"



class VehicleColor(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_vehicle_color_from_str(vehicle_color_str):
        if not vehicle_color_str:
            return
        vehicle_color_str = vehicle_color_str.title()
        vehicle_colors = VehicleColor.objects.all()
        matching_vehicle_color = vehicle_colors.filter(name=vehicle_color_str)
        if matching_vehicle_color.count() > 1:
            raise ValueError("There are duplicate vehicle colors in the database!")
        elif matching_vehicle_color.count() == 1:
            return matching_vehicle_color.first()
        elif matching_vehicle_color.count() == 0:
            new_color = VehicleColor(name=vehicle_color_str)
            new_color.save()
            return new_color  

class VehicleMake(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_vehicle_make_from_str(vehicle_make_str):
        if not vehicle_make_str:
            return
        vehicle_make_str = vehicle_make_str.title()
        vehicle_makes = VehicleMake.objects.all()
        matching_vehicle_make = vehicle_makes.filter(name=vehicle_make_str)
        if matching_vehicle_make.count() > 1:
            raise ValueError("There are duplicate vehicle makes in the database!")
        elif matching_vehicle_make.count() == 1:
            return matching_vehicle_make.first()
        elif matching_vehicle_make.count() == 0:
            new_make = VehicleMake(name=vehicle_make_str)
            new_make.save()
            return new_make
        
class VehicleModel(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_vehicle_model_from_str(vehicle_model_str):
        if not vehicle_model_str:
            return
        vehicle_model_str = vehicle_model_str.title()
        vehicle_models = VehicleModel.objects.all()
        matching_vehicle_model = vehicle_models.filter(name=vehicle_model_str)
        if matching_vehicle_model.count() > 1:
            raise ValueError("There are duplicate vehicle models in the database!")
        elif matching_vehicle_model.count() == 1:
            return matching_vehicle_model.first()
        elif matching_vehicle_model.count() == 0:
            new_model = VehicleModel(name=vehicle_model_str)
            new_model.save()
            return new_model
        
class VehicleStyle(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_vehicle_style_from_str(vehicle_style_str):
        if not vehicle_style_str:
            return
        vehicle_style_str = vehicle_style_str.title()
        vehicle_styles = VehicleStyle.objects.all()
        matching_vehicle_style = vehicle_styles.filter(name=vehicle_style_str)
        if matching_vehicle_style.count() > 1:
            raise ValueError("There are duplicate vehicle styles in the database!")
        elif matching_vehicle_style.count() == 1:
            return matching_vehicle_style.first()
        elif matching_vehicle_style.count() == 0:
            new_style = VehicleStyle(name=vehicle_style_str)
            new_style.save()
            return new_style

class VehicleInformation(models.Model):
    vehicle_year = models.IntegerField(null=True)
    tag_expiration_year = models.IntegerField(null=True)
    
    tag_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="vehicles", null=True)
    
    tag_number = models.CharField(max_length=256, blank=True, null=True)
    comment = models.CharField(max_length=256, blank=True, null=True)
    
    vehicle_make = models.CharField(max_length=256, blank=True, null=True)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, related_name="vehicles", null=True)
    vehicle_style = models.ForeignKey(VehicleStyle, on_delete=models.CASCADE, related_name="vehicles", null=True)
    vehicle_color = models.ForeignKey(VehicleColor, on_delete=models.CASCADE, related_name="vehicles", null=True)

    subject_related_items = models.ForeignKey(SubjectRelatedItems, on_delete=models.CASCADE, related_name="vehicles_info")
 


class MPSubjectDemographics(models.Model):
    current_min_age = models.FloatField(null=True)
    current_max_age = models.FloatField(null=True)
    missing_min_age = models.FloatField(null=True)
    missing_max_age = models.FloatField(null=True)
    
    height_from_inches = models.FloatField(null=True)
    height_to_inches = models.FloatField(null=True)
    weight_from_lbs = models.FloatField(null=True)
    weight_to_lbs = models.FloatField(null=True)

    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, related_name="mp_subject_descriptions", null=True)

    primary_ethnicity = models.ForeignKey(Ethnicity, on_delete=models.PROTECT, related_name="mp_subject_demographics_primary", null=True)
    ethnicities = models.ManyToManyField(Ethnicity, related_name="mp_subject_demographics_mixed")

    tribal_affiliation = models.ForeignKey(TribalAffiliation, on_delete=models.PROTECT, related_name="mp_subject_demographics", null=True)
    tribal_associations = models.ManyToManyField(TribalAssociation, related_name="mp_subject_demographics")

    def __str__(self) -> str:
        res = "»» |======| DEMOGRAPHICS |======| ««\n\n"
        
        if self.missing_min_age and self.missing_max_age:
            if self.missing_min_age == self.missing_max_age:
                res += f" » Missing Age: {self.missing_min_age}\n"
            else:
                res += f" » Missing Age: {self.missing_min_age} - {self.missing_max_age}\n"
        
        elif not self.missing_min_age and not self.missing_max_age:
            res += f" » Missing Age: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Missing Age: {self.missing_min_age if self.missing_min_age else self.missing_max_age}\n"

        if self.current_min_age and self.current_max_age:
            if self.current_min_age == self.current_max_age:
                res += f" » Current Age: {self.current_min_age}\n"
            else:
                res += f" » Current Age: {self.current_min_age} - {self.current_max_age}\n"
        
        elif not self.current_min_age and not self.current_max_age:
            res += f" » Current Age: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Current Age: {self.current_min_age if self.current_min_age else self.current_max_age}\n"

        if self.height_from_inches and self.height_to_inches:
            res += f" » Height: {self.height_from_inches} - {self.height_to_inches} inches\n"
        elif not self.height_from_inches and not self.height_to_inches:
            res += f" » Height: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Height: {self.height_from_inches if self.height_from_inches else self.height_to_inches} inches\n"
        
        if self.weight_from_lbs and self.weight_to_lbs:
            res += f" » Weight: {self.weight_from_lbs} - {self.weight_to_lbs} lbs\n"
        elif not self.weight_from_lbs and not self.weight_to_lbs:
            res += f" » Weight: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Weight: {self.weight_from_lbs if self.weight_from_lbs else self.weight_to_lbs} inches\n"

        if not self.gender:
            res += f" » Gender: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Gender: {self.gender}\n"

        if not self.primary_ethnicity:
            res += f" » Primary Ethnicity: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Primary Ethnicity: {str(self.primary_ethnicity)}\n"
        
        if self.ethnicities.count() > 1:
            res += " »» All Ethnicities ««\n"
            for ethnicity in self.ethnicities.all():
                res += f" * {ethnicity}\n"
        
        if not self.tribal_affiliation:
            res += f" » Tribal Affiliation: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Tribal Affiliation: {str(self.tribal_affiliation)}\n"

        if self.tribal_associations.count() > 0:
            res += " »» Tribal Associations ««\n"
            for tribe_association in self.tribal_associations.all():
                res += "--------------------------------------------------------------------------------------------------------------------\n"
                res += str(tribe_association) + '\n'
        
        return res  

    @staticmethod
    def create_subject_demographics(subject_demographics_data):
        
        demographics = MPSubjectDemographics(
            current_min_age = subject_demographics_data[InternalReprKeysConfig.CURRENT_MIN_AGE],
            current_max_age = subject_demographics_data[InternalReprKeysConfig.CURRENT_MAX_AGE],
            missing_min_age = subject_demographics_data[InternalReprKeysConfig.MISSING_MIN_AGE],
            missing_max_age = subject_demographics_data[InternalReprKeysConfig.MISSING_MAX_AGE],
            
            height_from_inches = subject_demographics_data[InternalReprKeysConfig.HEIGHT_FROM_INCHES],
            height_to_inches = subject_demographics_data[InternalReprKeysConfig.HEIGHT_TO_INCHES],
            weight_from_lbs = subject_demographics_data[InternalReprKeysConfig.WEIGHT_FROM_LBS],
            weight_to_lbs = subject_demographics_data[InternalReprKeysConfig.WEIGHT_TO_LBS],

            primary_ethnicity = Ethnicity.get_ethnicity_from_str(subject_demographics_data[InternalReprKeysConfig.PRIMARY_ETHNICITY]),
            gender = Gender.get_gender_from_str(subject_demographics_data[InternalReprKeysConfig.GENDER]),
            tribal_affiliation = TribalAffiliation.get_tribal_affiliation_from_str(subject_demographics_data[InternalReprKeysConfig.TRIBAL_AFFILIATION]),
        )
        demographics.save()

        for ethnicity in subject_demographics_data[InternalReprKeysConfig.ETHNICITIES]:
            if ethnicity and ethnicity[InternalReprKeysConfig.STR_NAME]:
                demographics.ethnicities.add(Ethnicity.get_ethnicity_from_str(ethnicity[InternalReprKeysConfig.STR_NAME]))

        for tribal_association in subject_demographics_data[InternalReprKeysConfig.TRIBE_ASSOCIATIONS]:
            if tribal_association[InternalReprKeysConfig.TRIBE_NAME]:
                tribe = Tribe.get_tribe_from_str(tribal_association[InternalReprKeysConfig.TRIBE_NAME])
                enrollment = tribal_association[InternalReprKeysConfig.TRIBE_ENROLLMENT]
                association = TribalAssociation(
                    tribe = tribe,
                    is_enrolled = enrollment
                )
                association.save()
                demographics.tribal_associations.add(association)

        return demographics








    @staticmethod
    def create_subject_description(subject_description_data):
        physical_features = subject_description_data[InternalReprKeysConfig.PHYSICAL_FEATURES]
        
        description = SubjectDescription(

            hair_color = HairColor.get_hair_color_from_str(physical_features[InternalReprKeysConfig.HAIR_COLOR]),
            left_eye_color = EyeColor.get_eye_color_from_str(physical_features[InternalReprKeysConfig.LEFT_EYE_COLOR]),
            right_eye_color = EyeColor.get_eye_color_from_str(physical_features[InternalReprKeysConfig.RIGHT_EYE_COLOR]),

            head_hair_description = physical_features[InternalReprKeysConfig.HEAD_HAIR_DESC],
            body_hair_description = physical_features[InternalReprKeysConfig.BODY_HAIR_DESC],
            facial_hair_description = physical_features[InternalReprKeysConfig.FACIAL_HAIR_DESC],
            eye_description = physical_features[InternalReprKeysConfig.EYE_DESC],
        )
        description.save()
        
        for distinctive_physical_feature in subject_description_data[InternalReprKeysConfig.DISTINCTIVE_PHYSICAL_FEATURES]:
            feature = DescriptiveFeatureArticle(
                category = DescriptiveFeatureCategory.get_desc_feature_category_from_str(distinctive_physical_feature[InternalReprKeysConfig.STR_CATEGORY_NAME]),
                description = distinctive_physical_feature[InternalReprKeysConfig.STR_DESCRIPTION],
                subject_description = description
            )
            feature.save()
        
        description.save()
        return description

class MPSubjectIdentification(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    
    middle_name = models.CharField(null=True, max_length=256)
    nicknames = models.CharField(null=True, max_length=1024)

    def __str__(self) -> str:
        res = "»» |======| IDENTIFICATION |======| ««\n\n"
        res += f" » First Name: {self.first_name}\n"
        res += f" » Middle Name: {InternalReprKeysConfig.STR_NONE if not self.middle_name else self.middle_name}\n"
        res += f" » Last Name: {self.last_name}\n"
        res += f" » Nicknames: {InternalReprKeysConfig.STR_NONE if not self.nicknames else self.nicknames}\n"
        return res
    
    @staticmethod
    def create_subject_identification(subject_identification_data):
        subject_identification_data = subject_identification_data[InternalReprKeysConfig.MP_IDENTIFICATION]
        identification = MPSubjectIdentification(
            first_name = subject_identification_data[InternalReprKeysConfig.FIRST_NAME],
            last_name = subject_identification_data[InternalReprKeysConfig.LAST_NAME],
            middle_name = subject_identification_data[InternalReprKeysConfig.MIDDLE_NAME],
            nicknames = subject_identification_data[InternalReprKeysConfig.NICKNAMES],
        )

        identification.save()
        return identification

class MPCase(models.Model):
    
    case_type = models.CharField(max_length=64, blank=True, editable=False, default=CaseType.MP)
    case_id = models.CharField(max_length=64, editable=False, unique=True, db_index=True)
    case_images = models.ForeignKey(CaseImages, on_delete=models.PROTECT, related_name="mp_cases")
    
    case_internal_created = models.DateField(auto_now=True)
    case_created = models.DateField()
    case_last_modified = models.DateField()
    
    namus_id = models.CharField(max_length=256)
    namus_id_formatted = models.CharField(max_length=256)
    ncmec_number = models.CharField(max_length=256, null=True)
    
    identification = models.OneToOneField(MPSubjectIdentification, on_delete=models.PROTECT, related_name="mp_case")
    demographics = models.OneToOneField(MPSubjectDemographics, on_delete=models.PROTECT, related_name="mp_case")
    description = models.OneToOneField(SubjectDescription, on_delete=models.PROTECT, related_name="mp_case")
    related_items = models.OneToOneField(SubjectRelatedItems, on_delete=models.PROTECT, related_name="mp_case")
    
    last_known_location = models.ForeignKey(Sighting, on_delete=models.PROTECT, related_name="mp_cases")
    
    primary_residence_on_tribal_land = models.ForeignKey(PrimaryResidenceOnTribalLand, on_delete=models.PROTECT, related_name="mp_cases", null=True)
    missing_from_tribal_land = models.ForeignKey(MissingFromTribalLand, on_delete=models.PROTECT, related_name="mp_cases", null=True)

    circumstances_of_disappearance = models.TextField(max_length=10000, null=True)
    
    is_resolved = models.BooleanField(null=True)

    primary_investigating_agency = models.ForeignKey(InvestigatingAgencyData, on_delete=models.PROTECT, related_name="mp_cases_primary", null=True)
    secondary_investigating_agencies = models.ManyToManyField(InvestigatingAgencyData, related_name="mp_cases_secondary")

    primary_source = models.ForeignKey(CaseSource, on_delete=models.PROTECT, related_name="mp_cases_primary")
    secondary_sources = models.ManyToManyField(CaseSource, related_name="mp_cases_secondary")

    def __str__(self) -> str:
        res = "\n\n***---------------------------------------------------------------------------------------------------------------------***\n"
        res += f"                 {self.case_type} - {self.case_id} ({self.primary_source})\n"
        res += "***---------------------------------------------------------------------------------------------------------------------***\n"
        
        res += "\n»» |======| META |======| ««\n\n"
        res += f" » NamUs Id: {self.namus_id_formatted}\n"
        
        if self.ncmec_number:
            res += f" » NCMEC Number: {self.namus_id_formatted}\n"
        res += f" » Case Created (Internal):{self.case_internal_created}\n"
        res += f" » Case Created (Source): {self.case_created}\n"
        res += f" » Case Last Modified (Source): {self.case_last_modified}\n"
        res += f" » Resolved: {self.is_resolved}\n"
        
        res += "\n"
        res += str(self.identification)
        res += "\n"
        res += str(self.demographics)
        
        res += "\n"
        res += f" » Primary Residence On Tribal Land: {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.primary_residence_on_tribal_land else self.primary_residence_on_tribal_land}\n"
        res += f" » Missing From Tribal Land: {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.missing_from_tribal_land else self.missing_from_tribal_land}"
        
        res += "\n"
        res += str(self.related_items)

        res += f"\n»» |======| CIRCUMSTANCES OF DISAPPEARANCE |======| ««\n\n"
        res += f" » {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.circumstances_of_disappearance else self.circumstances_of_disappearance}\n"
        res += str(self.last_known_location)
        
        res += f"\n\n»» |======| AGENCIES |======| ««\n\n"
        res += f" » Primary Investigating Agency «\n"
        res += str(self.primary_investigating_agency) if self.primary_investigating_agency else ' » ' + InternalReprKeysConfig.STR_NOT_PROVIDED + '\n'
        
        if self.secondary_investigating_agencies.count() > 0:
            res += f" »» Secondary Investigating Agencies ««\n"
            for secondary_agency in self.secondary_investigating_agencies.all():
                res += "--------------------------------------------------------------------------------------------------------------------\n"
                res += str(secondary_agency) + '\n'
        
        res += f"\n\n»» |======| SOURCES |======| ««\n\n"
        res += f" » Primary Source: {self.primary_source}\n"
        if self.secondary_sources.count() > 0:
            res += " »» Secondary Sources ««\n"
            for secondary_source in self.secondary_sources.all():
                res += f" » {secondary_source}\n"
        return res
            
    @staticmethod 
    def create_mp_case(case_data):
        CaseStats.GLOBAL_CASE_COUNT += 1
        CaseStats.MP_CASE_COUNT += 1

        subject_demographics_data = case_data[InternalReprKeysConfig.MP_DEMOGRAPHICS]

        sighting_data = case_data[InternalReprKeysConfig.MP_SIGHTHING]

        subject_identification = MPSubjectIdentification.create_subject_identification(case_data)
        subject_demographics = MPSubjectDemographics.create_subject_demographics(subject_demographics_data)
        subject_description = SubjectDescription.create_subject_description(case_data)
        subject_related_items = SubjectRelatedItems.create_subject_related_items(case_data)
        last_known_sighting = Sighting.create_sighting(sighting_data)
        case_images = CaseImages.create_case_images(case_data)
        
        case_source = CaseSource(source=case_data[InternalReprKeysConfig.SOURCE], link=case_data[InternalReprKeysConfig.SOURCE_LINK])
        case_source.save()
        
        case = MPCase(
            case_id = f"C_MP{CaseStats.MP_CASE_COUNT}",      
            namus_id = case_data[InternalReprKeysConfig.NAMUS_ID],
            namus_id_formatted = case_data[InternalReprKeysConfig.NAMUS_ID_FORMATTED],
            ncmec_number = case_data[InternalReprKeysConfig.NCMEC_NUM],

            case_created = case_data[InternalReprKeysConfig.DT_SOURCE_CREATED],
            case_last_modified = case_data[InternalReprKeysConfig.DT_SOURCE_LAST_MODIFIED],

            circumstances_of_disappearance = case_data[InternalReprKeysConfig.CIRCUMSTANCES_OF_DISAPPEARANCE],

            is_resolved = case_data[InternalReprKeysConfig.CASE_RESOLVED],

            identification = subject_identification,
            demographics = subject_demographics,
            description = subject_description,
            related_items = subject_related_items,
            last_known_location = last_known_sighting,
            
            primary_residence_on_tribal_land = PrimaryResidenceOnTribalLand.get_primary_residence_on_tribal_land(
                    sighting_data[InternalReprKeysConfig.LOCATION_DATA][InternalReprKeysConfig.PRIMARY_RESIDENCE_ON_TRIBAL_LAND]
                ),
            missing_from_tribal_land = MissingFromTribalLand.get_missing_from_tribal_land_from_str(
                    sighting_data[InternalReprKeysConfig.LOCATION_DATA][InternalReprKeysConfig.MISSING_FROM_TRIBAL_LAND]
                ),

            primary_investigating_agency = None if case_data[InternalReprKeysConfig.INVESTIGATING_AGENCY_PRIMARY] == None else InvestigatingAgencyData.create_investigating_agency_data(case_data[InternalReprKeysConfig.INVESTIGATING_AGENCY_PRIMARY]),
            case_images = case_images,
            primary_source = case_source
        )

        case.save()
        
        for investigating_agency_data in case_data[InternalReprKeysConfig.INVESTIGATING_AGENCIES_SECONDARY]:
            data_object = InvestigatingAgencyData.create_investigating_agency_data(investigating_agency_data)
            case.secondary_investigating_agencies.add(data_object)
        
@receiver(post_delete, sender=MPCase)
def handle_mp_case_delete(sender, instance, **kwargs):
    instance.case_images.delete()
    instance.identification.delete()
    instance.demographics.delete()
    instance.description.delete()
    instance.related_items.delete()
    if instance.last_known_location != None:
        instance.last_known_location.delete()
    if instance.primary_investigating_agency != None:
        instance.primary_investigating_agency.delete()
    
    for secondary_investigating_agency in instance.secondary_investigating_agencies.all():
        secondary_investigating_agency.delete()
    if instance.primary_source != None:
        instance.primary_source.delete()
    for secondary_source in instance.secondary_sources.all():
        secondary_source.delete()


class UIDStatus(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(args, kwargs)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_uid_status_from_str(uid_status_str):
        if not uid_status_str:
            return
        uid_status_str = uid_status_str.title()
        uid_statuses = UIDStatus.objects.all()
        matching_uid_status = uid_statuses.filter(name=uid_status_str)
        if matching_uid_status.count() > 1:
            raise ValueError("There are duplicate uid status values in the database!")
        elif matching_uid_status.count() == 1:
            return matching_uid_status.first()
        elif matching_uid_status.count() == 0:
            new_uid_status = UIDStatus(name=uid_status_str)
            new_uid_status.save()
            return new_uid_status

class UIDSubjectIdentification(models.Model):
    possible_first_name = models.CharField(max_length=256, null=True)
    possible_last_name = models.CharField(max_length=256, null=True)
    possible_middle_name = models.CharField(max_length=256, null=True)
    possible_nicknames = models.CharField(max_length=1024, null=True)

    def __str__(self) -> str:
        res = "»» |======| IDENTIFICATION |======| ««\n\n"
        res += f" » Possible First Name: {self.possible_first_name}\n"
        res += f" » Possible Middle Name: {InternalReprKeysConfig.STR_NONE if not self.possible_middle_name else self.possible_middle_name}\n"
        res += f" » Possible Last Name: {self.possible_last_name}\n"
        res += f" » Possible Nicknames: {InternalReprKeysConfig.STR_NONE if not self.possible_nicknames else self.possible_nicknames}\n"
        return res
    
    @staticmethod
    def create_uid_identification(case_data):
        identification = UIDSubjectIdentification(
            possible_first_name = case_data[InternalReprKeysConfig.UID_IDENTIFICATION][InternalReprKeysConfig.FIRST_NAME],
            possible_last_name = case_data[InternalReprKeysConfig.UID_IDENTIFICATION][InternalReprKeysConfig.LAST_NAME],
            possible_middle_name = case_data[InternalReprKeysConfig.UID_IDENTIFICATION][InternalReprKeysConfig.MIDDLE_NAME],
            possible_nicknames = case_data[InternalReprKeysConfig.UID_IDENTIFICATION][InternalReprKeysConfig.NICKNAMES]
        )

        identification.save()
        return identification

class UIDSubjectDemographics(models.Model):
    estimated_age_group = models.ForeignKey(EstimatedAgeGroup, on_delete=models.PROTECT, related_name="uid_subject_descriptions", null=True)
    estimated_age_from = models.FloatField(null=True)
    estimated_age_to = models.FloatField(null=True)
    estimated_year_of_birth_from = models.FloatField(null=True)
    estimated_year_of_birth_to = models.FloatField(null=True)
    estimated_year_of_death_from = models.FloatField(null=True)
    estimated_year_of_death_to = models.FloatField(null=True)
    
    height_from_inches = models.FloatField(null=True)
    height_to_inches = models.FloatField(null=True)
    weight_from_lbs = models.FloatField(null=True)
    weight_to_lbs = models.FloatField(null=True)
    
    height_certainty =  models.ForeignKey(HeightCertainty, on_delete=models.PROTECT, related_name="uid_subject_descriptions", null=True)
    weight_certainty =  models.ForeignKey(WeightCertainty, on_delete=models.PROTECT, related_name="uid_subject_descriptions", null=True)

    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, related_name="uid_subject_descriptions", null=True)

    primary_ethnicity = models.ForeignKey(Ethnicity, on_delete=models.PROTECT, related_name="uid_subject_demographics_primary", null=True)
    ethnicities = models.ManyToManyField(Ethnicity, related_name="uid_subject_demographics_mixed")


    def __str__(self) -> str:
        res = " »» |======| DEMOGRAPHICS |======| ««\n\n"
        res += f" » Estimated Age Group: {self.estimated_age_group}\n"
        if self.estimated_age_from and self.estimated_age_to:
            res += f" » Estimated Age: {self.estimated_age_from} - {self.estimated_age_to}\n"
        elif not self.estimated_age_from and not self.estimated_age_to:
            res += f" » Estimated Age: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Estimated Age: {self.estimated_age_from if self.estimated_age_from else self.estimated_age_to}\n"

        if self.estimated_year_of_birth_from and self.estimated_year_of_birth_to:
            res += f" » Estimated Year of Birth: {self.estimated_year_of_birth_from} - {self.estimated_year_of_birth_to}\n"
        elif not self.estimated_year_of_birth_from and not self.estimated_year_of_birth_to:
            res += f" » Estimated Year of Birth: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Estimated Year of Birth: {self.estimated_year_of_birth_from if self.estimated_year_of_birth_from else self.estimated_year_of_birth_to}\n" 

        if self.estimated_year_of_death_from and self.estimated_year_of_death_to:
            res += f" » Estimated Year of Death: {self.estimated_year_of_birth_from} - {self.estimated_year_of_death_to}\n"
        elif not self.estimated_year_of_death_from and not self.estimated_year_of_death_to:
            res += f" » Estimated Year of Death: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Estimated Age: {self.estimated_year_of_death_from if self.estimated_year_of_death_from else self.estimated_year_of_death_to}\n"
        
        if self.height_from_inches and self.height_to_inches:
            res += f" » Height: {self.height_from_inches} - {self.height_to_inches} inches ({self.height_certainty})\n"
        elif not self.height_from_inches and not self.height_to_inches:
            res += f" » Height: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Height: {self.height_from_inches if self.height_from_inches else self.height_to_inches} inches ({self.height_certainty})\n"
        
        if self.weight_from_lbs and self.weight_to_lbs:
            res += f" » Weight: {self.weight_from_lbs} - {self.weight_to_lbs} lbs ({self.weight_certainty})\n"
        elif not self.weight_from_lbs and not self.weight_to_lbs:
            res += f" » Weight: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Weight: {self.weight_from_lbs if self.weight_from_lbs else self.weight_to_lbs} lbs ({self.weight_certainty})\n"

        if not self.gender:
            res += f" » Gender: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Gender: {self.gender}\n"

        if not self.primary_ethnicity:
            res += f" » Primary Ethnicity: {InternalReprKeysConfig.STR_NOT_PROVIDED}\n"
        else:
            res += f" » Primary Ethnicity: {str(self.primary_ethnicity)}\n"
        
        if self.ethnicities.count() > 1:
            res += " »» All Ethnicities ««\n"
            for ethnicity in self.ethnicities.all():
                res += f" * {ethnicity}\n"
        
        
        return res  

    @staticmethod
    def create_uid_demographics(case_data):
        
        demographics = UIDSubjectDemographics(
            
            estimated_age_group = EstimatedAgeGroup.get_et_age_group_from_str(case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.ESTIMATED_AGE_GROUP]),
            
            estimated_age_from = case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.ESTIMATED_AGE_FROM],
            estimated_age_to = case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.ESTIMATED_AGE_TO],

            estimated_year_of_birth_from = case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.ESTIMATED_YEAR_OF_BIRTH_FROM],
            estimated_year_of_birth_to = case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.ESTIMATED_YEAR_OF_BIRTH_TO],

            estimated_year_of_death_from = case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.ESTIMATED_YEAR_OF_DEATH_FROM],
            estimated_year_of_death_to = case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.ESTIMATED_YEAR_OF_DEATH_TO],

            height_from_inches = case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.HEIGHT_FROM_INCHES],
            height_to_inches = case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.HEIGHT_TO_INCHES],

            weight_from_lbs = case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.WEIGHT_FROM_LBS],
            weight_to_lbs = case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.WEIGHT_TO_LBS],

            height_certainty = HeightCertainty.get_height_certainty_from_str(case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.HEIGHT_CERTAINTY]),
            weight_certainty = WeightCertainty.get_weight_certainty_from_str(case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.WEIGHT_CERTAINTY]),

            primary_ethnicity = Ethnicity.get_ethnicity_from_str(case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.PRIMARY_ETHNICITY]),
            gender = Gender.get_gender_from_str(case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.GENDER]),

        )
        demographics.save()

        for ethnicity in case_data[InternalReprKeysConfig.UID_DEMOGRAPHICS][InternalReprKeysConfig.ETHNICITIES]:
            if ethnicity and ethnicity[InternalReprKeysConfig.STR_NAME]:
                demographics.ethnicities.add(Ethnicity.get_ethnicity_from_str(ethnicity[InternalReprKeysConfig.STR_NAME]))

        return demographics

class UIDCase(models.Model):
    case_type = models.CharField(max_length=64, blank=True, editable=False, default=CaseType.UID)
    case_id = models.CharField(max_length=64, editable=False, unique=True, db_index=True)
    
    case_internal_created = models.DateField(auto_now=True)
    case_created = models.DateField()
    case_last_modified = models.DateField()
    date_found = models.DateField(max_length=256, null=True)
    
    namus_id = models.CharField(max_length=256)
    namus_id_formatted = models.CharField(max_length=256)
    ncmec_number = models.CharField(max_length=256, null=True)

    description = models.OneToOneField(SubjectDescription, on_delete=models.PROTECT, related_name="uid_case")
    related_items = models.OneToOneField(SubjectRelatedItems, on_delete=models.PROTECT, related_name="uid_case")
    identification = models.OneToOneField(UIDSubjectIdentification, on_delete=models.PROTECT, related_name="uid_case")
    demographics = models.OneToOneField(UIDSubjectDemographics, on_delete=models.PROTECT, related_name="uid_case")
    details_of_recovery = models.OneToOneField(DetailsOfRecovery, on_delete=models.PROTECT, related_name="uid_case")

    case_images = models.ForeignKey(CaseImages, on_delete=models.PROTECT, related_name="uid_case")
    status = models.ForeignKey(UIDStatus, on_delete=models.PROTECT, related_name="uid_cases", null=True)
    location_found = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="uid_cases", null=True)
    found_on_tribal_land = models.ForeignKey(FoundOnTribalLand, on_delete=models.PROTECT, related_name="uid_cases", null=True)
    
    primary_investigating_agency = models.ForeignKey(InvestigatingAgencyData, on_delete=models.PROTECT, related_name="uid_cases_primary", null=True)
    secondary_investigating_agencies = models.ManyToManyField(InvestigatingAgencyData, related_name="uid_cases_secondary")
    
    primary_source = models.ForeignKey(CaseSource, on_delete=models.PROTECT, related_name="uid_cases_primary")
    secondary_sources = models.ManyToManyField(CaseSource, related_name="uid_cases_secondary")

    circumstances_of_recovery = models.TextField(max_length=10000, null=True)

    is_resolved = models.BooleanField(null=True)

    def __str__(self) -> str:
        res = "\n\n***---------------------------------------------------------------------------------------------------------------------***\n"
        res += f"                 {self.case_type} - {self.case_id} ({self.primary_source})\n"
        res += "***---------------------------------------------------------------------------------------------------------------------***\n"
        
        res += "\n»» |======| META |======| ««\n\n"
        res += f" » NamUs Id: {self.namus_id_formatted}\n"
        
        if self.ncmec_number:
            res += f" » NCMEC Number: {self.namus_id_formatted}\n"
        res += f" » Case Created (Internal): {self.case_internal_created}\n"
        res += f" » Case Created (Source): {self.case_created}\n"
        res += f" » Case Last Modified (Source): {self.case_last_modified}\n"
        res += f" » Resolved: {self.is_resolved}\n"
        
        res += "\n"
        res += str(self.identification)
        res += "\n"
        res += str(self.demographics)
        
        res += "\n"
        res += f" » Found On Tribal Land: {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.found_on_tribal_land else self.found_on_tribal_land}"
        
        
        res += "\n"
        res += str(self.related_items)

        res += f"\n»» |======| CIRCUMSTANCES OF RECOVERY |======| ««\n\n"
        res += f" » {InternalReprKeysConfig.STR_NOT_PROVIDED if not self.circumstances_of_recovery else self.circumstances_of_recovery}\n"
        res += str(self.location_found)
        
        res += f"\n\n»» |======| AGENCIES |======| ««\n\n"
        res += f" » Primary Investigating Agency «\n"
        res += str(self.primary_investigating_agency) if self.primary_investigating_agency else ' » ' + InternalReprKeysConfig.STR_NOT_PROVIDED + '\n'
        
        if self.secondary_investigating_agencies.count() > 0:
            res += f" »» Secondary Investigating Agencies ««\n"
            for secondary_agency in self.secondary_investigating_agencies.all():
                res += "--------------------------------------------------------------------------------------------------------------------\n"
                res += str(secondary_agency) + '\n'
        
        res += f"\n\n»» |======| SOURCES |======| ««\n"
        res += f" » Primary Source: {self.primary_source}\n"
        if self.secondary_sources.count() > 0:
            res += " »» Secondary Sources ««\n"
            for secondary_source in self.secondary_sources.all():
                res += f" » {secondary_source}\n"
        return res

    @staticmethod
    def create_uid_case(case_data):
        CaseStats.GLOBAL_CASE_COUNT += 1
        CaseStats.UID_CASE_COUNT += 1

        demographics = UIDSubjectDemographics.create_uid_demographics(case_data)
        identification = UIDSubjectIdentification.create_uid_identification(case_data)
        description = SubjectDescription.create_subject_description(case_data)
        subject_related_items = SubjectRelatedItems.create_subject_related_items(case_data)
        details_of_recovery = DetailsOfRecovery.create_details_of_recovery(case_data)
        case_images = CaseImages.create_case_images(case_data) 
        location = Location(
            state = State.get_state_from_str(case_data[InternalReprKeysConfig.LOCATION_DATA][InternalReprKeysConfig.STATE]),
            county = County.get_county_from_str(case_data[InternalReprKeysConfig.LOCATION_DATA][InternalReprKeysConfig.COUNTY]),
            city = City.get_city_from_str(case_data[InternalReprKeysConfig.LOCATION_DATA][InternalReprKeysConfig.CITY]),
            street = case_data[InternalReprKeysConfig.LOCATION_DATA][InternalReprKeysConfig.STREET],
            lat = case_data[InternalReprKeysConfig.LOCATION_DATA][InternalReprKeysConfig.LATITUDE],
            lon = case_data[InternalReprKeysConfig.LOCATION_DATA][InternalReprKeysConfig.LONGITUDE],
        )
        location.save()
        
        case_source = CaseSource(source=case_data[InternalReprKeysConfig.SOURCE], link=case_data[InternalReprKeysConfig.SOURCE_LINK])
        case_source.save()
        
        case = UIDCase(
            case_id = f"C_UID{CaseStats.UID_CASE_COUNT}",      
            case_images = case_images,
            
            namus_id = case_data[InternalReprKeysConfig.NAMUS_ID],
            namus_id_formatted = case_data[InternalReprKeysConfig.NAMUS_ID_FORMATTED],
            ncmec_number = case_data[InternalReprKeysConfig.NCMEC_NUM],

            case_created = case_data[InternalReprKeysConfig.DT_SOURCE_CREATED],
            case_last_modified = case_data[InternalReprKeysConfig.DT_SOURCE_LAST_MODIFIED],
            date_found = case_data[InternalReprKeysConfig.DT_BODY_FOUND],

            circumstances_of_recovery = case_data[InternalReprKeysConfig.CICUMSTANCES_OF_RECOVERY],
            location_found = location,
            details_of_recovery = details_of_recovery,
            status = UIDStatus.get_uid_status_from_str(case_data[InternalReprKeysConfig.UID_STATUS]),
            is_resolved = case_data[InternalReprKeysConfig.CASE_RESOLVED],

            identification = identification,
            demographics = demographics,
            description = description,
            related_items = subject_related_items,

            found_on_tribal_land = FoundOnTribalLand.get_found_on_tbland_from_str(case_data[InternalReprKeysConfig.FOUND_ON_TRIBAL_LAND]),

            primary_investigating_agency = None if case_data[InternalReprKeysConfig.INVESTIGATING_AGENCY_PRIMARY] == None else InvestigatingAgencyData.create_investigating_agency_data(case_data[InternalReprKeysConfig.INVESTIGATING_AGENCY_PRIMARY]),
            primary_source = case_source
        )

        case.save()
        
        for investigating_agency_data in case_data[InternalReprKeysConfig.INVESTIGATING_AGENCIES_SECONDARY]:
            data_object = InvestigatingAgencyData.create_investigating_agency_data(investigating_agency_data)
            case.secondary_investigating_agencies.add(data_object)


@receiver(post_delete, sender=UIDCase)
def handle_uid_case_delete(sender, instance, **kwargs):
    instance.case_images.delete()
    instance.identification.delete()
    instance.demographics.delete()
    instance.description.delete()
    instance.related_items.delete()
    instance.details_of_recovery.delete()
    if instance.location_found != None:
        instance.location_found.delete()
    if instance.primary_investigating_agency != None:
        instance.primary_investigating_agency.delete()
    for secondary_investigating_agency in instance.secondary_investigating_agencies.all():
        secondary_investigating_agency.delete()
    if instance.primary_source != None:
        instance.primary_source.delete()
    for secondary_source in instance.secondary_sources.all():
        secondary_source.delete()





class ActiveCases(models.Model):
    mp_cases = models.ManyToManyField(MPCase, related_name="active_storage")
    uid_cases = models.ManyToManyField(UIDCase, related_name="active_storage")

class ArchivedCases(models.Model):
    mp_cases = models.ManyToManyField(MPCase, related_name="archive_storage")
    uid_cases = models.ManyToManyField(UIDCase, related_name="archive_storage")

class CaseBatch(models.Model):
    mp_cases = models.ManyToManyField(MPCase)
    uid_cases = models.ManyToManyField(UIDCase)


    




INTERNAL_ENUMS = [
    State,
    County,
    City,
    
    AgencyType,
    Jurisdiction,
    AgencyContactJobTitle,
    AgencyContactRole,
    
    Gender,
    Ethnicity,
    EstimatedAgeGroup,
    HeightCertainty,
    WeightCertainty,
    HairColor,
    EyeColor,

    Tribe,
    TribalAffiliation,
    PrimaryResidenceOnTribalLand,
    MissingFromTribalLand,
    FoundOnTribalLand,

    VehicleColor,
    VehicleMake,
    VehicleModel,
    VehicleStyle,
    
    DescriptiveFeatureCategory,
    DescriptiveItemCategory,
    
    Source,
    
    ConditionOfRemains,
    
    UIDStatus,
]

INTERNAL_MODELS = [
    MPCase,
    MPSubjectIdentification,
    MPSubjectDemographics,

    UIDCase,
    UIDSubjectDemographics,
    UIDSubjectIdentification,
    
    SubjectDescription,
    SubjectRelatedItems,
    
    DetailsOfRecovery,
    
    InvestigatingAgencyData,
    AgencyContact,
    Agency,
    
    CaseSource,
    CaseImages,
    Image,
    
    Sighting,
    Location,
    
    VehicleInformation,

    TribalAssociation,
    
    DescriptiveFeatureArticle,
    DescriptiveItemArticle,

    ActiveCases,
    ArchivedCases,
    CaseBatch
]

ALL_TYPES = INTERNAL_MODELS + INTERNAL_ENUMS














