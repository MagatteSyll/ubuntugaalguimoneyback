# Generated by Django 4.0.3 on 2022-03-20 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationtransaction',
            name='nature_transaction',
            field=models.CharField(blank=True, choices=[('envoi direct', 'envoi direct'), ('envoi via code', 'envoi via code'), ('depot', 'depot'), ('retrait', 'retrait'), ('reception', 'reception'), ('payement', 'payement'), ('code', 'code')], max_length=255),
        ),
    ]
