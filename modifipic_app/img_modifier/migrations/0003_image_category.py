# Generated by Django 3.0.3 on 2020-02-22 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('img_modifier', '0002_auto_20200221_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='category',
            field=models.IntegerField(choices=[(0, 'Raw'), (1, 'Blurred'), (2, 'Gray'), (3, 'Flipped horizontally'), (4, 'Sepia')], default=0),
        ),
    ]
