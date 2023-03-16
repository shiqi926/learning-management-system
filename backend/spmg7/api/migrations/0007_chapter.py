# Generated by Django 3.2.7 on 2021-09-25 13:04

from django.db import migrations

def create_data(apps, schema_editor):
    Chapter = apps.get_model('api', 'Chapter')
    Course = apps.get_model('api', 'Course')
    Classroom = apps.get_model('api', 'Classroom')

    intro_prog = Course.objects.get(id=1)
    prog1 = Course.objects.get(id=2)
    prog2 = Course.objects.get(id=3)
    prog3 = Course.objects.get(id=4)
    prog4 = Course.objects.get(id=5)


    intro_prog_g1 = Classroom.objects.get(class_name="g1", course_id=1)
    intro_prog_g2 = Classroom.objects.get(class_name="g2", course_id=1)

    prog1_g1 = Classroom.objects.get(class_name="g1", course_id=2)
    prog1_g2 = Classroom.objects.get(class_name="g2", course_id=2)

    prog2_g1 = Classroom.objects.get(class_name="g1", course_id=3)
    prog2_g2 = Classroom.objects.get(class_name="g2", course_id=3)

    prog3_g1 = Classroom.objects.get(class_name="g1", course_id=4)
    prog3_g2 = Classroom.objects.get(class_name="g2", course_id=4)

    prog4_g1 = Classroom.objects.get(class_name="g1", course_id=5)
    prog4_g2 = Classroom.objects.get(class_name="g2", course_id=5)

    quiz_bank = {
        "questions": {
            1: {
                "question": "Is engineering fun?",
                "options": [
                    "Yes",
                    "No"
                ],
                "answer": "Yes"
            },
            2: {
                "question": "Why is Rafe sad?",
                "options": [
                    "He is hungry",
                    "He has too much work to do",
                    "He doesn't know what to do with his life",
                    "All of the above"
                ],
                "answer": "All of the above"
            }
        },
        "title": "Fun Quiz",
        "duration": 3600,
        }

    material_bank = {
            0: {
                "title": "Sample Material",
                "type": "pdf",
                "url": "s3.bucket.fake.com"
            },
            1: {
                "title": "Sample Material 2",
                "type": "doc",
                "url": "s3.bucket.fake.com"
            }
        }

    Chapter(course=intro_prog, course_class=intro_prog_g1, description="python basics", title="intro prog g1 chapter 1").save()
    Chapter(course=intro_prog, course_class=intro_prog_g1, chapter_no=2, title="intro prog g1 chapter 2", description="python basics", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=intro_prog, course_class=intro_prog_g1, chapter_no=3, title="intro prog g1 chapter 3", description="python basics", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=intro_prog, course_class=intro_prog_g1, chapter_no=4, title="intro prog g1 chapter 4", description="python basics", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=intro_prog, course_class=intro_prog_g1, chapter_no=-1, title="intro prog g1 final chapter", description="python basics", quiz=quiz_bank, materials=material_bank).save()

    Chapter(course=intro_prog, course_class=intro_prog_g2, chapter_no=1, title="intro prog g2 chapter 1").save()
    Chapter(course=intro_prog, course_class=intro_prog_g2, chapter_no=2, title="intro prog g2 chapter 2", description="python basics", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=intro_prog, course_class=intro_prog_g2, chapter_no=3, title="intro prog g2 chapter 3", description="python basics", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=intro_prog, course_class=intro_prog_g2, chapter_no=4, title="intro prog g2 chapter 4", description="python basics", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=intro_prog, course_class=intro_prog_g2, chapter_no=-1, title="intro prog g2 final chapter", description="python basics", quiz=quiz_bank, materials=material_bank).save()

    Chapter(course=prog1, course_class=prog1_g1, chapter_no=1, title="progl g1 chapter 1", description="python intermediate").save()
    Chapter(course=prog1, course_class=prog1_g1, chapter_no=2, title="progl g1 chapter 2", description="python intermediate", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog1, course_class=prog1_g1, chapter_no=3, title="progl g1 chapter 3", description="python intermediate", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog1, course_class=prog1_g1, chapter_no=4, title="progl g1 chapter 4", description="python intermediate", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog1, course_class=prog1_g1, chapter_no=-1, title="progl g1 final chapter ", description="python intermediate", quiz=quiz_bank, materials=material_bank).save()

    Chapter(course=prog1, course_class=prog1_g2, chapter_no=1, title="progl g2 chapter 1", description="python intermediate").save()
    Chapter(course=prog1, course_class=prog1_g2, chapter_no=2, title="progl g2 chapter 2", description="python intermediate", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog1, course_class=prog1_g2, chapter_no=3, title="progl g2 chapter 3", description="python intermediate", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog1, course_class=prog1_g2, chapter_no=4, title="progl g2 chapter 4", description="python intermediate", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog1, course_class=prog1_g2, chapter_no=-1, title="progl g2 final chapter", description="python intermediate", quiz=quiz_bank, materials=material_bank).save()

    Chapter(course=prog2, course_class=prog2_g1, chapter_no=1, title="progll g1 chapter 1", description="python advanced").save()
    Chapter(course=prog2, course_class=prog2_g1, chapter_no=2, title="progll g1 chapter 2", description="python advanced", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog2, course_class=prog2_g1, chapter_no=3, title="progll g1 chapter 3", description="python advanced", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog2, course_class=prog2_g1, chapter_no=-1, title="progll g1 final chapter", description="python advanced", quiz=quiz_bank, materials=material_bank).save()

    Chapter(course=prog2, course_class=prog2_g2, chapter_no=1, title="progll g2 chapter 1", description="python advanced").save()
    Chapter(course=prog2, course_class=prog2_g2, chapter_no=2, title="progll g2 chapter 2", description="python advanced", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog2, course_class=prog2_g2, chapter_no=-1, title="progll g2 final chapter", description="python advanced", quiz=quiz_bank, materials=material_bank).save()

    Chapter(course=prog3, course_class=prog3_g1, chapter_no=1, title="Data g1 chapter 1", description="Data").save()
    Chapter(course=prog3, course_class=prog3_g1, chapter_no=2, title="Data g1 chapter 2", description="Data", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog3, course_class=prog3_g1, chapter_no=3, title="Data g1 chapter 3", description="Data", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog3, course_class=prog3_g1, chapter_no=4, title="Data g1 chapter 4", description="Data", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog3, course_class=prog3_g1, chapter_no=-1, title="Data g1 final chapter ", description="Data", quiz=quiz_bank, materials=material_bank).save()

    Chapter(course=prog3, course_class=prog3_g2, chapter_no=1, title="Data g2 chapter 1", description="Data").save()
    Chapter(course=prog3, course_class=prog3_g2, chapter_no=2, title="Data g2 chapter 2", description="Data", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog3, course_class=prog3_g2, chapter_no=3, title="Data g2 chapter 3", description="Data", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog3, course_class=prog3_g2, chapter_no=4, title="Data g2 chapter 4", description="Data", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog3, course_class=prog3_g2, chapter_no=-1, title="Data g2 final chapter", description="Data", quiz=quiz_bank, materials=material_bank).save()

    Chapter(course=prog4, course_class=prog4_g1, chapter_no=1, title="Finance g1 chapter 1", description="Finance").save()
    Chapter(course=prog4, course_class=prog4_g1, chapter_no=2, title="Finance g1 chapter 2", description="Finance", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog4, course_class=prog4_g1, chapter_no=3, title="Finance g1 chapter 3", description="Finance", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog4, course_class=prog4_g1, chapter_no=4, title="Finance g1 chapter 4", description="Finance", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog4, course_class=prog4_g1, chapter_no=-1, title="Finance g1 final chapter ", description="Finance", quiz=quiz_bank, materials=material_bank).save()

    Chapter(course=prog4, course_class=prog4_g2, chapter_no=1, title="Finance g2 chapter 1", description="Finance").save()
    Chapter(course=prog4, course_class=prog4_g2, chapter_no=2, title="Finance g2 chapter 2", description="Finance", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog4, course_class=prog4_g2, chapter_no=3, title="Finance g2 chapter 3", description="Finance", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog4, course_class=prog4_g2, chapter_no=4, title="Finance g2 chapter 4", description="Finance", quiz=quiz_bank, materials=material_bank).save()
    Chapter(course=prog4, course_class=prog4_g2, chapter_no=-1, title="Finance g2 final chapter", description="Finance", quiz=quiz_bank, materials=material_bank).save()



class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_chapter_title'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]
