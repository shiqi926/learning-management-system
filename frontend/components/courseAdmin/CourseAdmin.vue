<template>
    <section>
        <b-tabs type="is-boxed">
            <b-tab-item v-for="(item, index) in classes" :key="index" :label="item.class_name">
                <ClassAdmin 
                    :course_id="course_id"
                    :course_class_id="item.id"
                />
            </b-tab-item>
        </b-tabs>
    </section>
</template>

<script>
import ClassAdmin from "./ClassAdmin.vue"

export default {
    name: 'CourseAdmin',
    props: ['course_id'],
    components: {
        ClassAdmin
    },
    data() {
        return {
            classes: [],
        }
    },
    async fetch() {
        var request = await fetch(`${this.$store.state.base}/api/courses/class/?course_id=${this.course_id}`).then((res) => res.json()).catch(console.error)
        this.classes = request.Classroom
    }
}
</script>