<template>
    <div>
        <div class="hero is-danger">
            <div class="hero-body container">
                <p class="title">Welcome, Admin {{username}}</p>
            </div>
        </div>

        <div class="container pt-3">
            <p class="title py-3 mb-0">Current Courses</p>
            <CourseSearch />
        </div>
    </div>
</template>

<script>
export default {
    name: 'AdminPage',
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