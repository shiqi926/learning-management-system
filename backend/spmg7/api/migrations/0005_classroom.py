# Generated by Django 3.2.7 on 2021-09-25 12:33

from django.db import migrations
from django.utils import timezone


def create_data(apps, schema_editor):
    Classroom = apps.get_model('api', 'Classroom')
    Course = apps.get_model('api', 'Course')
    Profile = apps.get_model('api', 'Profile')

    myStr = "2021-10-01 15:26"
    current_date_time = timezone.datetime.strptime(myStr, "%Y-%m-%d %H:%M")

    intro_prog = Course.objects.get(id=1)
    prog1 = Course.objects.get(id=2)
    prog2 = Course.objects.get(id=3)
    prog3 = Course.objects.get(id=4)
    prog4 = Course.objects.get(id=5)


    rafe = Profile.objects.get(username="rafeang")
    charles = Profile.objects.get(username="charleslim")
    shiqi = Profile.objects.get(username="shiqi")
    sean = Profile.objects.get(username="seantan")
    yingting = Profile.objects.get(username="yingting")

    Classroom(course=intro_prog, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
              enroll_start=current_date_time, enroll_end=current_date_time, class_size=30).save()
    Classroom(course=intro_prog, class_name="g2", start_datetime=current_date_time, end_datetime=current_date_time,
              trainer=rafe, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30).save()

    Classroom(course=prog1, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
              trainer=yingting, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30).save()
    Classroom(course=prog1, class_name="g2", start_datetime=current_date_time, end_datetime=current_date_time,
              enroll_start=current_date_time, enroll_end=current_date_time, class_size=30).save()

    Classroom(course=prog2, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
              trainer=sean, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30).save()
    Classroom(course=prog2, class_name="g2", start_datetime=current_date_time, end_datetime=current_date_time,
              trainer=charles, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30).save()

    Classroom(course=prog3, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
              enroll_start=current_date_time, enroll_end=current_date_time, class_size=30).save()
    Classroom(course=prog3, class_name="g2", start_datetime=current_date_time, end_datetime=current_date_time,
              trainer=charles, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30).save()
    
    Classroom(course=prog4, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
              enroll_start=current_date_time, enroll_end=current_date_time, class_size=30).save()
    Classroom(course=prog4, class_name="g2", start_datetime=current_date_time, end_datetime=current_date_time,
              trainer=shiqi, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30).save()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_profile'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]