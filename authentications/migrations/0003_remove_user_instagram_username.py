# Generated by Django 4.1 on 2022-12-15 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0002_alter_user_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='instagram_username',
        ),
    ]