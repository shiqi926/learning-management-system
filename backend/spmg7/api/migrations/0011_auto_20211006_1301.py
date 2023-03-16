# Generated by Django 3.2.7 on 2021-10-06 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_enrollment_constraint_name'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='progress',
            constraint=models.UniqueConstraint(fields=('chapter', 'learner'), name='progress_cpk'),
        ),
    ]