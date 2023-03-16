<template>
  <div class="has-background-link-light">
    <div class="hero is-warning">
      <div class="hero-body container">
        <p class="title">
          Creating Chapter {{chapterNo}} of {{courseName}} {{className}}
        </p>
      </div>
    </div>
    <section class="container mt-4 p-2">
      <b-field label="Chapter Title">
        <b-input v-model="chapterTitle"/>
      </b-field>
      <b-field label="Chapter Description">
        <b-input type="textarea"  maxlength="1000" v-model="chapterDesc"/>
      </b-field>
    </section>
    <section class="is-flex is-justify-content-center">
      <button class="button is-success m-5" @click="createChapter">
        Create Chapter
      </button>
    </section>
  </div>
</template>

<script>

export default {
  name: 'ChapterCreatePage',
  methods: {
    createChapter() {
      let postData = {
        course_id: this.courseId,
        course_class_id: this.classId,
        chapter_no: this.chapterNo,
        title: this.chapterTitle,
        description: this.chapterDesc
      }

      fetch(`${this.$store.state.base}/api/content/create/`, {
        body: JSON.stringify(postData),
        method: 'post',
        headers: { "Content-Type": "application/json"},
        referrerPolicy: 'no-referrer'
      }).then(function (response) {
        console.log(response)
        if (response.status === 201) {
          alert("Chapter successfully created!");
        } else {
          alert("Something bad happened...");
          console.log(response);
        }
      }).catch(function (error) {
        alert("Something bad happened..")
        console.log(error);
      })
    }
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
      chapterTitle: '',
      chapterDesc: ''
    }
  },
  async asyncData({ $axios, params, store }) {
    const slug = params.slug
    const course = params.course

    var request = await $axios.$get(`${store.state.base}/api/content/${slug}/`)
    let chapterNums = request.map((chapter) => {
      return chapter.chapter_no
    })
    let latestChapter = Math.max(...chapterNums)
    var chapterNo
    if (latestChapter != -1) {
      chapterNo = latestChapter + 1
    } else {
      chapterNo = 1
    }

    var classReq = await $axios.$get(`${store.state.base}/api/class/${slug}/`)
    let className = classReq[0].class_name

    var courseReq = await $axios.$get(`${store.state.base}/api/courses/${course}/`)
    let courseName = courseReq[0].course_name

    return { classId: slug, courseId: course, chapterNo: chapterNo, className: className, courseName: courseName }
  }
}
</script>