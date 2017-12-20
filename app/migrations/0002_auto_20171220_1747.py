# Generated by Django 2.0 on 2017-12-20 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='getimage',
            name='uploaded_by',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='getimage',
            name='image',
            field=models.ImageField(upload_to='app/static/app/images/'),
        ),
    ]
