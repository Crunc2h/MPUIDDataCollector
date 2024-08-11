# Generated by Django 4.2.14 on 2024-08-11 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internal_repr', '0003_alter_uidsubjectidentification_possible_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uidcase',
            name='demographics',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='uid_case', to='internal_repr.uidsubjectdemographics'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uidcase',
            name='identification',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='uid_case', to='internal_repr.uidsubjectidentification'),
            preserve_default=False,
        ),
    ]
