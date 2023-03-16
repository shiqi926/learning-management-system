<template>
    <div class="column is-one-third">
        <div class="card">
            <div class="card-content">
                <p class="title">
                    {{course_name}}
                </p>
                <p class="content">
                    Course Description:<br>
                    {{desc}}
                </p>
                <a class="button is-primary" :href="'/course/' + course_id" >View More</a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CourseCard',
    props: ['course_name', 'desc', 'course_id']
}
</script>