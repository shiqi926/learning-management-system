<template>
    <div class="py-3">
        <a class="button is-success is-fullwidth" :href="`/chapter_create/${course_id}/${course_class_id}/`">Add Chapter</a>
    </div> 
</template>

<script>
export default {
    name: 'ChapterCreate',
    props: ['course_id','course_class_id'],
    computed: {
    },
    data() {
        return {
        }
    }
}
</script>