# Generated by Django 4.0.3 on 2022-03-25 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_verificationtransaction_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nature_document',
            field=models.CharField(default='pas de document', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='numero_document',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='messages',
            name='nature_transaction',
            field=models.CharField(choices=[('envoi direct', 'envoi direct'), ('envoi via code', 'envoi via code'), ('depot', 'depot'), ('retrait', 'retrait'), ('reception', 'reception'), ('payement', 'payement'), ('code', 'code'), ('retrait par code', 'retrait par code'), ('annulation commande', 'annulation commande')], max_length=100),
        ),
        migrations.AlterField(
            model_name='notificationadmina',
            name='nature',
            field=models.CharField(blank=True, choices=[('envoi direct', 'envoi direct'), ('envoi via code', 'envoi via code'), ('depot', 'depot'), ('retrait', 'retrait'), ('reception', 'reception'), ('payement', 'payement'), ('code', 'code'), ('retrait par code', 'retrait par code'), ('annulation commande', 'annulation commande')], max_length=255),
        ),
        migrations.AlterField(
            model_name='verificationtransaction',
            name='nature_transaction',
            field=models.CharField(blank=True, choices=[('envoi direct', 'envoi direct'), ('envoi via code', 'envoi via code'), ('depot', 'depot'), ('retrait', 'retrait'), ('reception', 'reception'), ('payement', 'payement'), ('code', 'code'), ('retrait par code', 'retrait par code'), ('annulation commande', 'annulation commande')], max_length=255),
        ),
    ]
