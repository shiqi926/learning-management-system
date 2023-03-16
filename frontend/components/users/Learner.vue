<template>
    <div>
        <div class="hero is-success">
            <div class="hero-body container">
                <p class="title">Welcome, Learner {{username}}</p>
            </div>
        </div>

        <div class="container py-3">
            <CourseSearch />
        </div>
    </div>
</template>

<script>
import CourseSearch from '../course/CourseSearch.vue'

export default {
    name: 'LearnerPage',
    components: {
        CourseSearch
    },
    computed: {
        loginStatus () {
            return this.$store.state.login
        },
        username () {
            return this.$store.state.username
        }
    }
}
</script>