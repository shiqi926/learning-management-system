<template>
    <section>
        <CourseChapter
            :course_class_id="course_class_id"
            :class_size="class_size"
            :end_date="end_date"
        />
        <ChapterCreate
            :course_id="course_id"
            :course_class_id="course_class_id"
        />
    </section>
</template>

<script>
import CourseChapter from '@/components/course/CourseChapter.vue'
import ChapterCreate from '@/components/courseTrainer/ChapterCreate.vue'
import QuizCreate from '@/components/courseTrainer/QuizCreate.vue'

export default {
    name: 'CourseTrainer',
    props: ['course_id','course_class_id','class_size','end_date'],
    components: {
        CourseChapter,
        ChapterCreate,
        QuizCreate
    },
    data() {
        return {
            classes: [],
        }
    },
    async fetch() {
        
    }
}
</script>