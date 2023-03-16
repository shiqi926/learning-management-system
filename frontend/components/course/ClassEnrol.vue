<template>
    <div class="column is-one-quarter">
        <div class="card">
            <header class="card-header">
                <p class="card-header-title level">
                    {{class_name}}
                    <span>Class Size: {{class_size}}</span>
                </p>
            </header>
            <div class="card-content">
                <div class="content">
                    <span class="has-text-weight-bold">Trainer: </span>{{trainer}}
                    <br>
                    <span class="has-text-weight-bold">Class Start: </span>{{start_datetime}}
                    <br>
                    <span class="has-text-weight-bold">Class End: </span>{{end_datetime}}
                </div>
            </div>
            <div class="card-footer">
                <a class="card-footer-item" v-if="!isPending.includes(course_class_id)" @click="enrol(course_class_id)">Enrol</a>
                <a class="card-footer-item" v-if="isPending.includes(course_class_id)">Pending</a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ClassEnrol',
    props: ['course_id','course_class_id','class_name','class_size','trainer','start_datetime','end_datetime'],
    data() {
        return {
            classes: [],
            isPending: [],
            isEnrolled: []
        }
    },
    computed: {
        loginStatus () {
            return this.$store.state.login
        }
    },
    methods: {
        enrol (course_class_id) {
            var body = {
                "learners" : [
                    {
                        "username": this.$store.state.username,
                        "course_class": parseInt(course_class_id),
                        "status": "PD"
                    }
                ]
            }
            console.log(body)
            fetch(`${this.$store.state.base}/api/enroll/`, {
                method: 'post',
                body: JSON.stringify(body),
                headers: {
                    'Content-Type': 'application/json'
                },
            }).then((res) => {
                if (res.status == 201) {
                    return res.json().then((data) => {
                        this.isPending.push(parseInt(course_class_id))
                        this.$buefy.toast.open({
                            message: `Enrolment Successful! Your enrolment for class ${this.class_name} is now pending approval!`,
                            type: 'is-success'
                        })
                    })
                }
                if (res.status == 400) {
                    this.$buefy.toast.open({
                        message: 'Enrolment Unsuccessful! You already registered for a class!',
                        type: 'is-danger'
                    })
                }
            }).catch(console.error)
        }
    },
    async fetch() {
        // Check if user is pending enrolment
        var request = await fetch(`${this.$store.state.base}/api/enroll/pending/`).then((res) => res.json()).catch(console.error)
        this.isPending = request.filter(learner => learner.username == this.$store.state.username).map(obj => obj.course_class)
        // console.log(this.isPending)

        // Check if uesr is already enrolled
        var request = await fetch(`${this.$store.state.base}/api/enroll/enrolled_learners/${this.course_id}/`).then((res) => res.json()).catch(console.error)
        this.isEnrolled = request
        // console.log(this.isEnrolled)

    }
}
</script>