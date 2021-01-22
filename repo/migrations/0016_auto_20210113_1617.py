# Generated by Django 3.1.3 on 2021-01-13 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0015_auto_20210112_0954'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shop',
            options={'verbose_name': '配件', 'verbose_name_plural': '配件'},
        ),
        migrations.AlterField(
            model_name='shop',
            name='shop_name',
            field=models.CharField(max_length=80, verbose_name='配件名称'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='shop_no',
            field=models.CharField(max_length=80, verbose_name='配件编号'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='shop_num',
            field=models.IntegerField(default=0, verbose_name='配件数量'),
        ),
        migrations.CreateModel(
            name='ProductRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(db_index=True, default=False)),
                ('product_no', models.CharField(max_length=80, unique=True, verbose_name='商品编码')),
                ('product_name', models.CharField(max_length=80, verbose_name='商品名称')),
                ('change_num', models.IntegerField(verbose_name='变化数量')),
                ('option', models.CharField(choices=[('Sale', '卖出'), ('Pakage', '装货')], default='Pakage', max_length=10)),
                ('entity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repo.sendout', verbose_name='配送')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]