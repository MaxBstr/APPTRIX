# Generated by Django 3.2.12 on 2022-03-27 21:20

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_client_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='clients/avatars'),
        ),
    ]