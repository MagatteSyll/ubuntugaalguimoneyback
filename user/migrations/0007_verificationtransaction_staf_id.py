# Generated by Django 4.0.3 on 2022-03-22 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_tendancepub_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationtransaction',
            name='staf_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]