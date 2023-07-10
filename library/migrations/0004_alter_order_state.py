# Generated by Django 3.2.19 on 2023-05-26 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20230521_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(choices=[('未付款', '未付款'), ('已付款', '已付款'), ('已退货', '已退货'), ('已添加', '已添加')], max_length=6),
        ),
    ]
