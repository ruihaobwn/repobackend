# Generated by Django 3.1.3 on 2021-01-14 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0016_auto_20210113_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrecord',
            name='product_no',
            field=models.CharField(max_length=80, verbose_name='商品编码'),
        ),
    ]
