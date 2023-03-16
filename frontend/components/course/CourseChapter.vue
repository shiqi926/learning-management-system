<template>
    <section class="py-3">
        <div class="level">
            <p class="title">
                Class {{ course_class_id }}
            </p>
            <p class="title">
                Class Size:  {{ class_size }}
            </p>
            <p class="title">
                End Date: {{ end_date }}
            </p>
        </div>

        <b-table 
            :data="chapterDetails"
            ref="table"
            detailed
            hoverable
            default-sort="id"
            detail-key="id"
            :show-detail-icon="true"
        >
            <b-table-column field="id" label="ID" width="40" sortable numeric v-slot="props">
                {{ props.row.id }}
            </b-table-column>

            <b-table-column field="title" label="Title" sortable v-slot="props">
                {{ props.row.title }}
            </b-table-column>
            
            <template #detail="props">
                <article class="media">
                    <div class="media-content">
                        <div class="content">
                            <p>
                                <strong>Description</strong> <br>
                                {{ props.row.description }}
                            </p>
                            <span v-if="Object.entries(props.row.materials).length">
                                <strong>Materials</strong> <br>
                                <a v-for="(item, index) in props.row.materials" :key="index" class="button is-primary is-light mr-2">{{ item.title }}</a>
                                <br>
                            </span>
                            <span v-if="Object.entries(props.row.quiz).length">
                                <br>
                                <strong>Quiz</strong> <br>
                                <a class="button is-primary is-light is-fullwidth" :href="`/quiz/${props.row.id}`">Take Quiz</a>    
                            </span>
                            <span v-if="loginStatus == 'Trainer' & !Object.entries(props.row.quiz).length" >
                                <br>
                                <strong>Quiz</strong> <br>
                                <a class="button is-success is-fullwidth" :href="`/quiz_create/${props.row.id}`">Add Quiz</a>
                            </span>
                        </div>
                    </div>
                </article>
            </template>
        </b-table>
    </section>
</template>

<script>


export default {
    name: 'CourseChapter',
    props: ['course_class_id','class_size','end_date', 'learner_id'],
    data() {
        return {
            chapterDetails: [],
            current_chapter: 0
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
    methods: {
        toggle(row) {
            this.$refs.table.toggleDetails(row)
        }
    },
    async fetch() {
        var request = await fetch(`${this.$store.state.base}/api/content/current_chapter/${this.learner_id}/`).then((res) => {
            return res.json().then((data) => {
                this.current_chapter = data[0].current_chapter
            })
        }).catch(console.error)

        var request = await fetch(`${this.$store.state.base}/api/content/${this.course_class_id}/`).then((res) => {
            return res.json().then((data) => {
                let chapter_id = data.map(obj => obj.id)
                chapter_id.forEach(e => {
                    if (e <= this.current_chapter) {
                        var req = fetch(`${this.$store.state.base}/api/content/chapter/${e}/`).then((res) => {
                            return res.json().then((data) => {
                                this.chapterDetails.push(data)
                            })
                        }).catch(console.error)
                    }
                });
            })
        }).catch(console.error)
    }
}
</script>
