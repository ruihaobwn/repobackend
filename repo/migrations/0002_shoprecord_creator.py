# Generated by Django 3.2.5 on 2021-10-04 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoprecord',
            name='creator',
            field=models.CharField(max_length=80, null=True, verbose_name='操作人'),
        ),
    ]
