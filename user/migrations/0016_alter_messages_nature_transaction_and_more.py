# Generated by Django 4.0.3 on 2022-03-25 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_user_nature_document_user_numero_document_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='nature_transaction',
            field=models.CharField(choices=[('envoi direct', 'envoi direct'), ('envoi via code', 'envoi via code'), ('depot', 'depot'), ('retrait', 'retrait'), ('reception', 'reception'), ('payement', 'payement'), ('code', 'code'), ('retrait par code', 'retrait par code'), ('annulation commande', 'annulation commande'), ('activation compte', 'activation compte')], max_length=100),
        ),
        migrations.AlterField(
            model_name='notificationadmina',
            name='nature',
            field=models.CharField(blank=True, choices=[('envoi direct', 'envoi direct'), ('envoi via code', 'envoi via code'), ('depot', 'depot'), ('retrait', 'retrait'), ('reception', 'reception'), ('payement', 'payement'), ('code', 'code'), ('retrait par code', 'retrait par code'), ('annulation commande', 'annulation commande'), ('activation compte', 'activation compte')], max_length=255),
        ),
        migrations.AlterField(
            model_name='verificationtransaction',
            name='nature_transaction',
            field=models.CharField(blank=True, choices=[('envoi direct', 'envoi direct'), ('envoi via code', 'envoi via code'), ('depot', 'depot'), ('retrait', 'retrait'), ('reception', 'reception'), ('payement', 'payement'), ('code', 'code'), ('retrait par code', 'retrait par code'), ('annulation commande', 'annulation commande'), ('activation compte', 'activation compte')], max_length=255),
        ),
    ]