<template>
    <section>
        <div class="columns">
            <div class="column is-half">
                <p class="title">
                    Class List
                </p>
                <b-table 
                    :data="filterClass" 
                    :columns="columns">
                </b-table>
            </div>
            <div class="column is-half">
                <p class="title">
                    Enrol Students
                </p>
                <b-tabs>
                    <b-tab-item label="Eligible Students">
                        <b-table
                            :data="learnersEligible"
                            :columns="columns"
                            :selected.sync="selectedEligible"
                            focusable>
                        </b-table>
                        <button @click="enrol" class="button is-primary">Enrol</button>
                        <!-- <pre>{{ selectedEligible }}</pre> -->
                    </b-tab-item>
                    
                    <b-tab-item label="Pending Approval">
                        <b-table
                            :data="learnersPending"
                            :columns="columns"
                            :selected.sync="selectedPending"
                            focusable>
                        </b-table>
                        <a @click="approve" class="button is-success">Approve</a>
                        <a @click="reject" class="button is-danger">Reject</a>
                        <!-- <pre>{{ selectedPending }}</pre> -->
                    </b-tab-item>
                </b-tabs>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    name: 'ClassAdmin',
    props: ['course_id', 'course_class_id'],
    data() {
        return {
            columns: [
                {
                    field: 'id',
                    label: 'ID',
                    width: '50',
                    numeric: true
                },
                {
                    field: 'username',
                    label: 'Username',
                }
            ],
            learnersEnrolled: [],
            learnersEligible: [],
            learnersPending: [],
            selectedEligible: {},
            selectedPending: {}
        }
    },
    computed: {
        filterClass() {
            var enrolled = []
            this.learnersEnrolled.forEach(e => {
                if (e.course_class == this.course_class_id) {
                    enrolled.push(
                        {
                            "id": e.id,
                            "username": e.username
                        }
                    )
                }
            });
            return enrolled
        }
    },
    methods: {
        enrol () {
            var body = {
                "learners" : [
                    {
                        "username": this.selectedEligible.username,
                        "course_class": this.course_class_id,
                        "status": "IP"
                    }
                ]
            }
            console.log(JSON.stringify(body))
            fetch(`${this.$store.state.base}/api/enroll/`, {
                method: 'post',
                body: JSON.stringify(body),
                headers: {
                    'Content-Type': 'application/json'
                },
            }).then((res) => {
                return res.json().then((data) => {
                    this.learnersEnrolled.push(data)
                    this.learnersEligible = this.learnersEligible.filter(learner => learner.username != this.selectedEligible.username)
                })
            }).catch(console.error)
        },
        approve () {
            var body = {
                "learners" : [
                    {
                        "enrollment_id": this.selectedPending.id,
                        "status": "IP"
                    }
                ]
            }
            console.log(JSON.stringify(body))
            fetch(`${this.$store.state.base}/api/enroll/hr/`, {
                method: 'put',
                body: JSON.stringify(body),
                headers: {
                    'Content-Type': 'application/json'
                },
            }).then((res) => {
                return res.json().then((data) => {
                    console.log(data)
                    this.learnersEnrolled.push(data)
                    this.learnersPending = this.learnersPending.filter(learner => learner.username != this.selectedPending.username)
                })
            }).catch(console.error)
        },
        reject () {
            var body = {
                "learners" : [
                    {
                        "enrollment_id": this.selectedPending.id,
                        "status": "R"
                    }
                ]
            }
            console.log(JSON.stringify(body))
            fetch(`${this.$store.state.base}/api/enroll/hr/`, {
                method: 'put',
                body: JSON.stringify(body),
                headers: {
                    'Content-Type': 'application/json'
                },
            }).then((res) => {
                return res.json().then((data) => {
                    this.learnersPending = this.learnersPending.filter(learner => learner.username != this.selectedPending.username)
                })
            }).catch(console.error)
        }
    },
    async fetch() {
        // Get enrolled learners
        var request = await fetch(`${this.$store.state.base}/api/enroll/enrolled_learners/${this.course_class_id}/`, {

        }).then((res) => res.json()).catch(console.error)
        this.learnersEnrolled = request
        console.log(request)
        var enrolledUsername = this.learnersEnrolled.map(obj => obj.username)

        // Get eligible learners w/o enrolled learners
        var request = await fetch(`${this.$store.state.base}/api/enroll/${this.course_id}/`, {

        }).then((res) => res.json()).catch(console.error)
        request.forEach(e => {
            if (!enrolledUsername.includes(e.username) ) {
                this.learnersEligible.push(e)
            }
        });

        // Get pending learners
        var request = await fetch(`${this.$store.state.base}/api/enroll/pending/`).then((res) => res.json()).catch(console.error)
        request.forEach(e => {
            if (e.course_class == this.course_class_id) {
                this.learnersPending.push(
                    {
                        "id": e.id,
                        "username": e.username
                    }
                )
            }
        });
    }
}
</script>