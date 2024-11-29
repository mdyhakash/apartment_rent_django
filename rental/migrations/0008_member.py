# Generated by Django 5.1.3 on 2024-11-29 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0007_user_profile_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(blank=True, default='', null=True, upload_to='members/')),
                ('image2', models.ImageField(blank=True, default='', null=True, upload_to='members/')),
                ('image3', models.ImageField(blank=True, default='', null=True, upload_to='members/')),
                ('image4', models.ImageField(blank=True, default='', null=True, upload_to='members/')),
            ],
        ),
    ]