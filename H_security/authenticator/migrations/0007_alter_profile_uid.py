# Generated by Django 4.1.5 on 2023-04-20 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0006_alter_profile_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x000001B5891311C0>', max_length=200),
        ),
    ]