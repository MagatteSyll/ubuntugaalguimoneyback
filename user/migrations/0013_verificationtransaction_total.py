# Generated by Django 4.0.3 on 2022-03-24 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_verificationtransaction_commission_incluse'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationtransaction',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
    ]
