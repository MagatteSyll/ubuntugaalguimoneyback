# Generated by Django 4.0.3 on 2022-03-24 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_depot_staf_id_retrait_staf_id_viacode_staf_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationtransaction',
            name='nom_complet_client',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]