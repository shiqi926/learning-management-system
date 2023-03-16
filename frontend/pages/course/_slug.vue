<template>
    <div>
        <div class="hero is-light">
            <div class="hero-body container">
                <p class="title">
                    {{course.course_name}}
                    {{username}} 
                </p>
            </div>
        </div>
        <div class="container py-3">
            <p>
                Course Description:
                {{course.description}}
            </p>
        </div>

        <!-- LEARNER -->
        <div v-if="loginStatus == 'Learner'" class="container py-3">
            <!-- IF ENROLLED -->
            <div v-if="isEnrolled" class="py-3">
                <CourseChapter 
                    :course_class_id="this.enrolledClassId"
                    :learner_id="this.learnerId"
                    :class_size="this.enrolledClass.class_size"
                    :end_date="this.enrolledClass.end_datetime"
                />
            </div>
            
            <!-- IF NOT ENROLLED -->
            <div v-if="!isEnrolled" class="py-3">
                <div class="py-3 columns is-multiline">
                    <ClassEnrol
                        v-for="(item,index) in classroom"
                        :course_id="slug"
                        :course_class_id="item.id"
                        :class_name="item.class_name"
                        :class_size="item.class_size"
                        :trainer="item.trainer"
                        :start_datetime="item.start_datetime"
                        :end_datetime="item.end_datetime"
                        :key="index"
                    />
                </div>
            </div>
        </div>

        <!-- TRAINER -->
        <div v-if="loginStatus == 'Trainer'" class="container py-3">
            <ClassCreate/>
            <CourseTrainer
                :course_id="slug">
            >
            </CourseTrainer>
        </div>

        <!-- ADMIN -->
        <div v-if="loginStatus == 'Admin'" class="container py-3">
            <CourseAdmin 
                :course_id="slug">
            </CourseAdmin>
        </div>
        
    </div>
</template>

<script>
import CourseChapter from '@/components/course/CourseChapter.vue'
import ClassEnrol from '@/components/course/ClassEnrol.vue'
import CourseAdmin from '@/components/courseAdmin/CourseAdmin.vue'
import ClassCreate from '@/components/courseTrainer/ClassCreate.vue'
import QuizCreate from '@/components/courseTrainer/QuizCreate.vue'
import CourseTrainer from '@/components/courseTrainer/CourseTrainer.vue'


export default {
    name: 'CoursePage',
    components: {
        CourseChapter,
        ClassEnrol,
        CourseAdmin,
        ClassCreate,
        QuizCreate,
        CourseTrainer
    },
    computed: {
        loginStatus () {
            return this.$store.state.login
        },username () {
            return this.$store.state.username
        }
    },
    data() {
        return {
            enrolledLearners: [],
            // isEnrolled: null,
            // learnerId: null,
            // enrolledClass: null,
            // enrolledClassId: null
        }
    },
    async asyncData({ $axios, params, store }) {
        const slug = params.slug
        
        // var request = await $axios.$get(`http://localhost:8000/api/courses/class/?course_id=${slug}`)
        var request = await $axios.$get(`${store.state.base}/api/courses/class/?course_id=${slug}`)
        const course = request.Course[0]
        const classroom = request.Classroom
        var isEnrolled
        var learnerId
        var enrolledClass
        var enrolledClassId
        var classes = classroom.map((obj) => { return obj.id })
        console.log(classes)
        classes.forEach((e) => {
            console.log(`${store.state.base}/api/enroll/enrolled_learners/${e}/`)
            fetch(`${store.state.base}/api/enroll/enrolled_learners/${e}/`).then((res) => {
                res.json().then((data) => {
                    let enrolled = data.map((obj) => { return obj.username })
                    console.log(store.state)
                    if (enrolled.includes(store.state.username)) {
                        isEnrolled = true
                        enrolledClassId = e
                        let learner = data.filter( (x) => {
                            return x.username == store.state.username
                        })
                        learnerId = learner[0].id
                        var request = fetch(`${store.state.base}/api/class/${e}/`).then((res) => {
                            res.json().then((data) => {
                                enrolledClass = data[0]
                            })
                        }).catch(console.error)
                    }
                })
            }).catch(console.error)
        });
        return { course, classroom, slug, isEnrolled, enrolledClass, learnerId, enrolledClassId }
    },
    // watch: {
    //     username: function() {
            // var classes = this.classroom.map(obj => obj.id)
            // classes.forEach(e => {
            //     var request = fetch(`${this.$store.state.base}/api/enroll/enrolled_learners/${e}/`, {
            //     }).then((res) => {
            //         return res.json().then((data) => {
            //             let enrolled = data.map(obj => obj.username)
            //             if (enrolled.includes(this.username)) {
            //                 this.isEnrolled = true
            //                 console.log(data)
            //                 this.enrolledClassId = e
            //                 let learner = data.filter( x => {
            //                     return x.username == this.username
            //                 })
            //                 this.learnerId = learner[0].id
            //                 var request = fetch(`${this.$store.state.base}/api/class/${e}/`).then((res) => {
            //                     return res.json().then((data) => {
            //                         this.enrolledClass = data[0]
            //                     })
            //                 }).catch(console.error)
            //             }
            //         })
            //     }).catch(console.error)
            // });
        // }
    // }
    fetchOnServer: false
}
</script>