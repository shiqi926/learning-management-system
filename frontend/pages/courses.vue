<template>
    <div>
        <div class="hero is-light">
            <div class="hero-body container">
                <p class="title">
                    My Courses
                </p>
            </div>
        </div>

        <!-- LEARNER -->
        <div v-if="loginStatus == 'Learner'" class="container py-3">
            <div class="columns py-3 is-multiline">
                <b-message v-if="enrolledCourses == null" title="No Course Found" type="is-warning"  has-icon class="column">
                    You are currently not enrolled in any courses.
                </b-message>
                <CourseCard
                    v-else
                    v-for="(item,index) in enrolledCourses"
                    :course_name="item.course_name"
                    :desc="item.description"
                    :course_id="item.id"
                    :key="index"
                />
            </div>
        </div>

        <!-- TRAINER -->
        <div v-if="loginStatus == 'Trainer'" class="container py-3">
            <CourseCreate/>
            <div class="columns py-3 is-multiline">
                <b-message v-if="taughtCourses == null" title="No Course Found" type="is-warning"  has-icon class="column">
                    You are currently not teaching any courses.
                </b-message>
                <CourseCard
                    v-else
                    v-for="(item,index) in taughtCourses"
                    :course_name="item.course_name"
                    :desc="item.description"
                    :course_id="item.id"
                    :key="index"
                />
            </div>
        </div>

        <!-- ADMIN -->
        <div v-if="loginStatus == 'Admin'" class="container py-3">
            <div class="columns py-3 is-multiline">
                <CourseCard
                    v-for="(item,index) in courses"
                    :course_name="item.course_name"
                    :desc="item.description"
                    :course_id="item.id"
                    :key="index"
                />
            </div>
        </div>

    </div>
</template>

<script>
import CourseCard from '@/components/course/CourseCard.vue'
import CourseCreate from '@/components/courseTrainer/CourseCreate.vue'

export default {
    name: 'CoursePage',
    components: {
        CourseCard,
        CourseCreate,
    },
    data() {
        return {
            courses: [],
            enrolledCourses: [],
            taughtCourses: []
        }
    },
    computed: {
        loginStatus () {
            return this.$store.state.login
        },
        username () {
            return this.$store.state.username
        }
    },
    async fetch(){
        var request = await fetch(`${this.$store.state.base}/api/courses/`).then((res) => res.json()).catch(console.error)
        this.courses = request.data
        
        if (this.loginStatus == 'Learner') {
            console.log("loginStatus > learner")
            var request = await fetch(`${this.$store.state.base}/api/enroll/user_enrolled/${this.username}/`).then((res) => {
                if (res.status == 200) {
                    return res.json().then((data) => {
                        let enrolledId = data.map(obj => obj.course_id)
                        this.courses.forEach(e => {
                            if (enrolledId.includes(e.id)) {
                                this.enrolledCourses.push(e)
                            }
                        });
                    })
                }
                if (res.status == 404) {
                    this.enrolledCourses = null
                }
            }).catch(console.error)
        } else if (this.loginStatus == 'Trainer') {
            console.log("loginStatus > trainer")
            var request = await fetch(`${this.$store.state.base}/api/trainer/course/${this.username}/`).then((res) => {
                if (res.status == 200) {
                    return res.json().then((data) => {
                        let taughtId = data.map(obj => obj.course_id)
                        this.courses.forEach(e => {
                            if (taughtId.includes(e.id)) {
                                this.taughtCourses.push(e)
                            }
                        })
                    })
                }
                if (res.status == 404) {
                    this.taughtCourses = null
                }
            }).catch(console.error)
        }
    },
    fetchOnServer: false
}
</script>