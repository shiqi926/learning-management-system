from .views.chapters import get_all_chapters_in_class, get_chapter_in_class, create_new_chapter, update_chapter, get_chapter_by_id, update_progress, user_progress
from .views.quiz import get_quiz_results
from .views.classroom import get_class_by_id, get_course, get_class_in_course
from .views.profile import get_user_by_username
from .views import *
from django.urls import path

urlpatterns = [
    # courses
    path('courses/', all_courses, name='get_all_courses'),
    path('courses/<int:course_id>/', get_course_by_id, name='get_course_by_id'),
    path('courses/pre_req/<int:course_id>/', pre_req, name='get_pre_req'),
    path('courses/class/', CourseClassAPIView.as_view()),
    # enroll
    path('enroll/<int:course_id>/', eligible_learners,
         name="get_eligible_learners"),
    path('enroll/', enroll_learners, name="post_enroll_learners"),
    path('enroll/hr/', hr_action_learners, name="put_hr_action_learners"),
    path('enroll/pending/', pending_enrollment, name="get_pending_enrollment"),
    path('enroll/trainers/', get_trainers, name="get_trainers"),
    path('enroll/assign_trainer/', assign_trainer, name="post_assign_trainer"),
    path('enroll/user_enrolled/<username>/',
         user_enrolled_classes, name="get_user_enrolled"),
    path('enroll/enrolled_learners/<int:course_class_id>/',
         class_enrolled_learners, name="get_class_enrolled_learners"),
    # chapter
    path('content/chapter/<int:chapter_id>/', get_chapter_by_id, name="get_chapter_by_id"),
    path('content/progress/<int:chapter_id>/<username>/', user_progress, name="get_user_progress"),
    path('content/update_progress/', update_progress, name="update_user_progress"),
    path('content/current_chapter/<int:enrollment_id>/', current_chapter),
    path('content/<int:classroom_id>/', get_all_chapters_in_class, name="get_all_chapters_in_class"),
    path('content/<int:classroom_id>/<int:chapter_no>/', get_chapter_in_class, name="get_chapter_in_class"),
    path('content/create/', create_new_chapter, name="create_new_chapter"),
    path('content/update/', update_chapter, name="update_chapter"),
    # quiz
    path('quiz/create_quiz/', create_quiz, name="create_quiz"),
    path('quiz/<int:id>/', get_quiz, name="get_quiz"),
    path('quiz/submit/', submit_quiz, name="submit_quiz"),
    path('quiz/results/<str:learner_id>/<int:chapter_id>/',
         get_quiz_results, name="get_quiz_results"),
    # classroom
    path('trainer/course/<str:username>/', get_course, name="get_course_of_trainer"),
    path('trainer/class/<str:username>/<int:course_id>/', get_class_in_course, name="get_classes_of_trainer"),
    path('class/<int:classroom_id>/', get_class_by_id, name="get_class_by_id"),
    # user
    path('user/<str:username>/', get_user_by_username, name="get_user_by_username"),
]
