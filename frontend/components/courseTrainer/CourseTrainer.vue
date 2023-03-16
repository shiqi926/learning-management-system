<template>
    <section>
        <b-tabs type="is-boxed">
            <b-tab-item v-for="(item, index) in classes" :key="index" :label="item.class_name">
                <ClassTrainer
                    :course_id="item.course"
                    :course_class_id="item.id"
                    :class_size="item.class_size"
                    :end_date="item.end_datetime"
                />
            </b-tab-item>
        </b-tabs>
    </section>
</template>

<script>
import ClassTrainer from './ClassTrainer.vue'

export default {
    name: 'CourseTrainer',
    props: ['course_id','course_class_id'],
    components: {
        ClassTrainer
    },
    data() {
        return {
            classes: [],
        }
    },
    async fetch() {
        var request = await fetch(`${this.$store.state.base}/api/trainer/class/${this.$store.state.username}/${this.course_id}/`).then((res) => res.json()).catch(console.error)
        this.classes = request
        console.log(request)
    }
}
</script>