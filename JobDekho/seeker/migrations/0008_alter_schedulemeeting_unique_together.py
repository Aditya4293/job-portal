# Generated by Django 4.0.4 on 2023-03-08 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seeker', '0007_alter_schedulemeeting_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='schedulemeeting',
            unique_together=set(),
        ),
    ]
