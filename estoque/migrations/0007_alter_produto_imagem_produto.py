# Generated by Django 4.2.6 on 2023-10-21 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0006_delete_usuario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='imagem_produto',
            field=models.ImageField(default='media/default_image_produtos', upload_to='media'),
        ),
    ]
