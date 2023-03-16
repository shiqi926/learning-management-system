<template>
    <div>
        <div class="hero is-light">
            <div class="hero-body container">
                <p class="title">
                    Quiz
                </p>
            </div>
        </div>

        <div>
            <div class="container py-3">
                <div class="columns py-3 is-multiline">
                    <QuizQuestion 
                        :title=this.quizName
                        :duration=this.quizDuration
                        :questions=this.quizQuestions
                        :chapterId=this.chapterId
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import QuizQuestion from '@/components/quiz/QuizQuestion.vue'

export default {
    name: 'QuizPage',
    components: {
        QuizQuestion
    },
    data() {
        return {
            answers: []
        }
    },
    computed: {
        loginStatus () {
            return this.$store.state.loginStatus
        },
        username () {
            return this.$store.state.username
        }
    },
    async asyncData({ $axios, params }) {
        const slug = params.slug

        // var request = await $axios.$get(`http://localhost:8000/api/quiz/${slug}/`)
        var request = await $axios.$get(`https://spmg7-backend.herokuapp.com//api/quiz/${slug}/`)
        const title = request.title
        const duration = request.duration
        const questions = request.questions

        return { chapterId: slug, quizName: title, quizDuration: duration, quizQuestions: questions }
    }
}
</script>