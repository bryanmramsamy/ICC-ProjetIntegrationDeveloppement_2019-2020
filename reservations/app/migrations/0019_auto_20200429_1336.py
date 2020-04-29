# Generated by Django 3.0.5 on 2020-04-29 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20200423_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='artisttype',
            name='artistId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Artist'),
        ),
    ]
