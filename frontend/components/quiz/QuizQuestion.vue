<template>
    <div>
        <div class="card-content">
            <p class="title">
                    {{title}}
                </p>
        
            <div class="card-content" v-for="(item,index) in questions" :key=index>
                <h5>
                    Question {{index}}
                </h5>
                <h2> 
                    {{item.question}}
                </h2>
                <ul>
                    <li
                        v-for="(option,num) in item.options"
                        :key=num
                        style="margin: 3px;"
                    >
                        <input type="radio" :name=index :value=option v-model="item.selected">
                        <label>
                            {{option}}
                        </label>
                    </li>
                </ul>
            </div>
            <div class="button is-primary" v-if="!this.submitted" @click="submit">Submit</div>
        </div>
        <div v-if="this.submitted"> Total Score: {{this.score}} / {{this.total_score}}</div>
    </div>
</template>

<script>
export default {
    name: 'QuizQuestion',
    props: ['title', 'duration', 'questions', 'options', 'answer', 'chapterId'],
    data() {
        return {
            score: 0,
            total_score: 0,
            submitted: false
        }
    },
    methods: {
        submit() {
            let responses = {}
            let postData = { user_id: this.$store.state.username, chapter_id: this.chapterId }
            let keys = Object.keys(this.questions)
            keys.forEach(key => {
                let item = this.questions[key]
                responses[key] = item.selected
            })
            postData["responses"] = responses

            fetch(`${this.$store.state.base}/api/quiz/submit/`, {
                body: JSON.stringify(postData),
                method: 'post',
                headers: { "Content-Type": "application/json"}
            }).then(function (response) {
                if (response.status === 200) {
                alert("Quiz successfully submitted!");
                } else {
                alert(response)
                }
            }).catch(function (error) {
                alert(error);
            })

            var request = fetch(`${this.$store.state.base}/api/quiz/results/${this.$store.state.username}/${this.chapterId}/`, {

                }).then((res) => {
                    return res.json().then((data) => {
                        this.score = data.score
                        this.total_score = data.total_score
                        this.submitted = true
                    })
                }).catch(console.error)
        }
    }
}
</script>