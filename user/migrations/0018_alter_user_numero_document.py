# Generated by Django 4.0.3 on 2022-03-25 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_alter_messages_commission_alter_messages_montant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='numero_document',
            field=models.CharField(default='0', max_length=255),
        ),
    ]