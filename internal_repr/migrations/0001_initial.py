# Generated by Django 4.2.14 on 2024-08-10 13:10

from django.db import migrations, models
import django.db.models.deletion
import internal_repr.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=256, null=True)),
                ('jurisdiction', models.CharField(max_length=256, null=True)),
                ('agency_type', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AgencyContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(max_length=256)),
                ('full_name', models.CharField(max_length=512)),
                ('agency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='internal_repr.agency')),
            ],
        ),
        migrations.CreateModel(
            name='AgencyContactJobTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='AgencyContactRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='AgencyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='CaseImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CaseSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=4096)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='ConditionOfRemains',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='DescriptiveFeatureCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='DescriptiveItemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='DetailsOfRecovery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head_not_recovered', models.BooleanField(blank=True, default=False)),
                ('torso_not_recovered', models.BooleanField(blank=True, default=False)),
                ('limbs_not_recovered', models.BooleanField(blank=True, default=False)),
                ('hands_not_recovered', models.BooleanField(blank=True, default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EstimatedAgeGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Ethnicity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='EyeColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='FoundOnTribalLand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='HairColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='HeightCertainty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poster_href', models.CharField(max_length=4096)),
                ('thumbnail_href', models.CharField(max_length=4096)),
                ('file_path', models.CharField(blank=True, default='-', max_length=512)),
                ('height_poster', models.IntegerField(null=True)),
                ('width_poster', models.IntegerField(null=True)),
                ('height_thumbnail', models.IntegerField(null=True)),
                ('width_thumbnail', models.IntegerField(null=True)),
                ('download_link', models.CharField(max_length=4096, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvestigatingAgencyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_number', models.CharField(max_length=256, null=True)),
                ('date_reported', models.DateField(max_length=256, null=True)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='investigations', to='internal_repr.agency')),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='investigations', to='internal_repr.agencycontact')),
            ],
        ),
        migrations.CreateModel(
            name='Jurisdiction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=256)),
                ('zip_code', models.CharField(max_length=256, null=True)),
                ('street', models.CharField(blank=True, max_length=256, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lon', models.FloatField(blank=True, null=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='internal_repr.city')),
                ('county', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='internal_repr.county')),
            ],
        ),
        migrations.CreateModel(
            name='MissingFromTribalLand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='MPSubjectIdentification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(max_length=256)),
                ('middle_name', models.CharField(max_length=256, null=True)),
                ('nicknames', models.CharField(max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrimaryResidenceOnTribalLand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('source_type', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectRelatedItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TribalAffiliation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Tribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='UIDStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='UIDSubjectIdentification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('possible_first_name', models.CharField(max_length=256)),
                ('possible_last_name', models.CharField(max_length=256)),
                ('possible_middle_name', models.CharField(max_length=256, null=True)),
                ('nicknames', models.CharField(max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleMake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleStyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='WeightCertainty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_year', models.IntegerField(null=True)),
                ('tag_expiration_year', models.IntegerField(null=True)),
                ('tag_number', models.CharField(blank=True, max_length=256, null=True)),
                ('comment', models.CharField(blank=True, max_length=256, null=True)),
                ('vehicle_make', models.CharField(blank=True, max_length=256, null=True)),
                ('subject_related_items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles_info', to='internal_repr.subjectrelateditems')),
                ('tag_state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='internal_repr.state')),
                ('vehicle_color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='internal_repr.vehiclecolor')),
                ('vehicle_model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='internal_repr.vehiclemodel')),
                ('vehicle_style', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='internal_repr.vehiclestyle')),
            ],
        ),
        migrations.CreateModel(
            name='UIDSubjectDemographics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimated_age_from', models.FloatField(null=True)),
                ('estimated_age_to', models.FloatField(null=True)),
                ('estimated_year_of_birth_from', models.FloatField(null=True)),
                ('estimated_year_of_birth_to', models.FloatField(null=True)),
                ('estimated_year_of_death_from', models.FloatField(null=True)),
                ('estimated_year_of_death_to', models.FloatField(null=True)),
                ('height_from_inches', models.FloatField(null=True)),
                ('height_to_inches', models.FloatField(null=True)),
                ('weight_from_lbs', models.FloatField(null=True)),
                ('weight_to_lbs', models.FloatField(null=True)),
                ('estimated_age_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='uid_subject_descriptions', to='internal_repr.estimatedagegroup')),
                ('ethnicities', models.ManyToManyField(related_name='uid_subject_demographics_mixed', to='internal_repr.ethnicity')),
                ('gender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='uid_subject_descriptions', to='internal_repr.gender')),
                ('height_certainty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='uid_subject_descriptions', to='internal_repr.heightcertainty')),
                ('primary_ethnicity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='uid_subject_demographics_primary', to='internal_repr.ethnicity')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='uid_cases', to='internal_repr.uidstatus')),
                ('weight_certainty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='uid_subject_descriptions', to='internal_repr.weightcertainty')),
            ],
        ),
        migrations.CreateModel(
            name='UIDCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_type', models.CharField(blank=True, default=internal_repr.models.CaseType['UID'], editable=False, max_length=64)),
                ('case_id', models.CharField(db_index=True, editable=False, max_length=64, unique=True)),
                ('case_internal_created', models.DateField(auto_now=True)),
                ('case_created', models.DateField()),
                ('case_last_modified', models.DateField()),
                ('namus_id', models.CharField(max_length=256)),
                ('namus_id_formatted', models.CharField(max_length=256)),
                ('ncmec_number', models.CharField(max_length=256, null=True)),
                ('circumstances_of_recovery', models.TextField(max_length=10000, null=True)),
                ('date_found', models.DateField()),
                ('is_resolved', models.BooleanField(null=True)),
                ('is_archived', models.BooleanField(blank=True, default=False)),
                ('case_images', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='uid_case', to='internal_repr.caseimages')),
                ('found_on_tribal_land', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='uid_cases', to='internal_repr.foundontriballand')),
                ('location_found', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uid_cases', to='internal_repr.location')),
                ('primary_investigating_agency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='uid_cases_primary', to='internal_repr.investigatingagencydata')),
                ('primary_source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='uid_cases_primary', to='internal_repr.casesource')),
                ('secondary_investigating_agencies', models.ManyToManyField(related_name='uid_cases_secondary', to='internal_repr.investigatingagencydata')),
                ('secondary_sources', models.ManyToManyField(related_name='uid_cases_secondary', to='internal_repr.casesource')),
            ],
        ),
        migrations.CreateModel(
            name='TribalAssociation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_enrolled', models.BooleanField(null=True)),
                ('tribe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='associations', to='internal_repr.tribe')),
            ],
        ),
        migrations.CreateModel(
            name='Sighting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sightings', to='internal_repr.location')),
            ],
        ),
        migrations.CreateModel(
            name='MPSubjectDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head_hair_description', models.CharField(max_length=512, null=True)),
                ('body_hair_description', models.CharField(max_length=512, null=True)),
                ('facial_hair_description', models.CharField(max_length=512, null=True)),
                ('eye_description', models.CharField(max_length=512, null=True)),
                ('hair_color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mp_subject_descriptions', to='internal_repr.haircolor')),
                ('left_eye_color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mp_subject_left_eye_descriptions', to='internal_repr.eyecolor')),
                ('right_eye_color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mp_subject_right_eye_descriptions', to='internal_repr.eyecolor')),
            ],
        ),
        migrations.CreateModel(
            name='MPSubjectDemographics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_min_age', models.FloatField(null=True)),
                ('current_max_age', models.FloatField(null=True)),
                ('missing_min_age', models.FloatField(null=True)),
                ('missing_max_age', models.FloatField(null=True)),
                ('height_from_inches', models.FloatField(null=True)),
                ('height_to_inches', models.FloatField(null=True)),
                ('weight_from_lbs', models.FloatField(null=True)),
                ('weight_to_lbs', models.FloatField(null=True)),
                ('ethnicities', models.ManyToManyField(related_name='mp_subject_demographics_mixed', to='internal_repr.ethnicity')),
                ('gender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mp_subject_descriptions', to='internal_repr.gender')),
                ('primary_ethnicity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mp_subject_demographics_primary', to='internal_repr.ethnicity')),
                ('tribal_affiliation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mp_subject_demographics', to='internal_repr.tribalaffiliation')),
                ('tribal_associations', models.ManyToManyField(related_name='mp_subject_demographics', to='internal_repr.tribalassociation')),
            ],
        ),
        migrations.CreateModel(
            name='MPCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_type', models.CharField(blank=True, default=internal_repr.models.CaseType['MP'], editable=False, max_length=64)),
                ('case_id', models.CharField(db_index=True, editable=False, max_length=64, unique=True)),
                ('case_internal_created', models.DateField(auto_now=True)),
                ('case_created', models.DateField()),
                ('case_last_modified', models.DateField()),
                ('namus_id', models.CharField(max_length=256)),
                ('namus_id_formatted', models.CharField(max_length=256)),
                ('ncmec_number', models.CharField(max_length=256, null=True)),
                ('circumstances_of_disappearance', models.TextField(max_length=10000, null=True)),
                ('is_resolved', models.BooleanField(null=True)),
                ('is_archived', models.BooleanField(blank=True, default=False)),
                ('case_images', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mp_cases', to='internal_repr.caseimages')),
                ('demographics', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='mp_case', to='internal_repr.mpsubjectdemographics')),
                ('description', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='mp_case', to='internal_repr.mpsubjectdescription')),
                ('identification', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='mp_case', to='internal_repr.mpsubjectidentification')),
                ('last_known_location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mp_cases', to='internal_repr.sighting')),
                ('missing_from_tribal_land', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mp_cases', to='internal_repr.missingfromtriballand')),
                ('primary_investigating_agency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mp_cases_primary', to='internal_repr.investigatingagencydata')),
                ('primary_residence_on_tribal_land', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mp_cases', to='internal_repr.primaryresidenceontriballand')),
                ('primary_source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mp_cases_primary', to='internal_repr.casesource')),
                ('related_items', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='mp_case', to='internal_repr.subjectrelateditems')),
                ('secondary_investigating_agencies', models.ManyToManyField(related_name='mp_cases_secondary', to='internal_repr.investigatingagencydata')),
                ('secondary_sources', models.ManyToManyField(related_name='mp_cases_secondary', to='internal_repr.casesource')),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='internal_repr.state'),
        ),
        migrations.CreateModel(
            name='DescriptiveItemArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=1000)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='internal_repr.descriptiveitemcategory')),
                ('subject_related_items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clothing_and_accessories', to='internal_repr.subjectrelateditems')),
            ],
        ),
        migrations.CreateModel(
            name='DescriptiveFeatureArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=1000)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='articles', to='internal_repr.descriptivefeaturecategory')),
                ('subject_description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distinctive_physical_features', to='internal_repr.mpsubjectdescription')),
            ],
        ),
        migrations.AddField(
            model_name='casesource',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_cases', to='internal_repr.source'),
        ),
        migrations.AddField(
            model_name='caseimages',
            name='default_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case_images_default', to='internal_repr.image'),
        ),
        migrations.AddField(
            model_name='caseimages',
            name='other_images',
            field=models.ManyToManyField(related_name='case_images_other', to='internal_repr.image'),
        ),
        migrations.AddField(
            model_name='agencycontact',
            name='job_title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='internal_repr.agencycontactjobtitle'),
        ),
        migrations.AddField(
            model_name='agencycontact',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='internal_repr.agencycontactrole'),
        ),
        migrations.AddField(
            model_name='agency',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agencies', to='internal_repr.location'),
        ),
    ]
