# Generated by Django 4.2.6 on 2023-10-30 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0011_alter_log_itens_geladeira_geladeira'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log_itens_geladeira',
            name='dt_modificacao',
            field=models.DateField(auto_now=True),
        ),
    ]