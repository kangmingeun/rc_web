# Generated by Django 2.1.4 on 2019-02-08 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='board',
            options={'ordering': ('-create_date',)},
        ),
    ]