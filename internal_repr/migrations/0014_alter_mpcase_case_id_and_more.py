# Generated by Django 4.2.14 on 2024-08-07 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internal_repr', '0013_alter_mpcase_case_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpcase',
            name='case_id',
            field=models.CharField(db_index=True, editable=False, max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='mpcase',
            name='primary_investigating_agency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cases_primary', to='internal_repr.investigatingagencydata'),
        ),
    ]
