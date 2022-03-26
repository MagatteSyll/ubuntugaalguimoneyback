# Generated by Django 4.0.3 on 2022-03-20 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_verificationtransaction_nature_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationAdmina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('somme', models.DecimalField(decimal_places=2, max_digits=19)),
                ('nature', models.CharField(blank=True, choices=[('envoi direct', 'envoi direct'), ('envoi via code', 'envoi via code'), ('depot', 'depot'), ('retrait', 'retrait'), ('reception', 'reception'), ('payement', 'payement'), ('code', 'code')], max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('client', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
