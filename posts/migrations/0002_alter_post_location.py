# Generated by Django 4.1 on 2022-11-14 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='posts.location', verbose_name='スケートパーク'),
        ),
    ]
