<template>
  <div class="has-background-link-light">
    <div class="hero is-warning">
      <div class="hero-body container">
        <p class="title">
          Create quiz for {{chapterName}}
        </p>
      </div>
    </div>
    <section class="container mt-4 p-2">
      <b-field label="Quiz Title">
        <b-input v-model="quizTitle"/>
      </b-field>
      <b-field label="Quiz Duration">
        <b-numberinput v-model="duration"/>
      </b-field>
      <div
        v-for="(question, idx) in questions"
        :key="idx"
        class="box mt-5 p-5"
      >
        <div class="columns is-vcentered">
          <p class="column is-1 has-text-weight-medium">Question {{idx+1}}</p>
          <b-input
            class="column"
            placeholder="Question"
            v-model="question.question"
          />
          <button
            class="column button is-danger is-outlined is-1 is-align-items-center is-flex"
            @click="deleteQuestion(idx)"
          >
            Delete
          </button>
        </div>
        <div class="control mb-4">
          <p class="mb-2 has-text-weight-medium">Options 
            <span class="is-italic has-text-weight-normal">(select the correct answer)</span>
          </p>
          <div
            v-for="(option, id) in question.options"
            class="columns is-vcentered m-2"
            :key="id"
          >
            <div class="column is-1">
              <b-button type="is-danger" class="is-small" icon-right="delete" @click="deleteOption(idx, id)"  outlined>
                Delete
              </b-button>
            </div>
            <label
              class="radio column"
            >
              <input type="radio" :name="idx" v-model="question.answer" :value="option">
                {{option}}
            </label>
          </div>
        </div>
        <div class="columns is-vcentered">
          <b-input
            class="column is-5"
            placeholder="Enter new option here"
            v-model="question.newOption"
          />
          <button
            class="button column is-info is-outlined is-2 is-align-items-center is-flex"
            @click="addOption(idx)"
          >
            Add Option
          </button>
        </div>
      </div>
    </section>
    <section class="is-flex is-justify-content-center">
      <button class="button is-info is-outlined m-5" @click="addQuestion">
        Add Question
      </button>
      <button class="button is-success m-5" @click="createQuiz">
        Create Quiz
      </button>
    </section>
  </div>
</template>

<script>

export default {
  name: 'QuizCreatePage',
  methods: {
    addQuestion() {
      this.questions.push({ answer: '', options: [], question: '', newOption: ''})
    },
    deleteQuestion(idx) {
      this.questions.splice(idx, 1)
    },
    addOption(idx) {
      let toAdd = this.questions[idx].newOption
      this.questions[idx].options.push(toAdd)
      this.questions[idx].newOption = ''
      console.log(this.questions[idx].answer)
    },
    deleteOption(idx, id) {
      this.questions[idx].options.splice(id, 1)
    },
    createQuiz() {
      let postData = { chapter_id: parseInt(this.chapterId), trainer_id: this.$store.state.username }
      let quiz = { title: this.quizTitle, duration: this.duration }
      let qns = {}
      this.questions.forEach((question, index) => {
        let qn = { answer: question.answer, options: question.options, question: question.question }
        let num = index + 1
        qns[num.toString()] = qn
      })
      quiz["questions"] = qns
      postData["quiz"] = quiz
      console.log(postData);
      fetch(`${this.$store.state.base}/api/quiz/create_quiz/`, {
        body: JSON.stringify(postData),
        method: 'post',
        headers: { "Content-Type": "application/json"}
      }).then(function (response) {
        console.log(response)
        if (response.status === 201) {
          alert("Quiz successfully created!");
        } else {
          alert(response)
        }
      }).catch(function (error) {
        alert(error);
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
      quizTitle: '',
      questions: [],
      duration: 10
    }
  },
  async asyncData({ $axios, params, store }) {
    const slug = params.slug
    
    var request = await $axios.$get(`${store.state.base}/api/content/chapter/${slug}/`)
    const title = request.title
    console.log(store.state)
    return { chapterId: slug, chapterName: title }
  }
}
</script>