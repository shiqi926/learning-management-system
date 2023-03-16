<template>
    <section>
        <b-field label="Search for courses">
            <b-autocomplete
                rounded
                v-model="name"
                :data="filteredDataArray"
                placeholder="e.g. IS111 Intro Prog"
                icon="magnify"
                clearable
                :open-on-focus="openOnFocus"
                @select="option => selected = option">
                <template #empty>No results found</template>
            </b-autocomplete>
        </b-field>

        <p class="content"><b>Matching Course:</b> {{ selected }}</p>

        <div class="columns is-multiline">
            <CourseCard 
                v-for="(item,index) in courses"
                :course_name="item.course_name"
                :desc="item.description"
                :course_id="item.id"
                :key="index"
            />
        </div>
    </section>
</template>

<script>
    import CourseCard from './CourseCard.vue'

    export default {
        name: 'CourseSearch',
        components: {
            CourseCard
        },
        data() {
            return {
                name: '',
                selected: null,
                openOnFocus: true,

                courses: [],
                courseName: []
            }
        },
        computed: {
            filteredDataArray() {
                return this.courseName.filter((option) => {
                    return option
                        .toString()
                        .toLowerCase()
                        .indexOf(this.name.toLowerCase()) >= 0
                })
            }
        },
        async fetch() {
            var request = await fetch(`${this.$store.state.base}/api/courses/`).then((res) => res.json()).catch(console.error)
            this.courses = request.data
            this.courseName = this.courses.map(obj => obj.course_name)
            // console.log(this.courses)
        }
    }
</script>