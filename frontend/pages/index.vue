<template>
    <div>
        <!-- LANDING -->
        <section v-if="!loginStatus" class="hero is-light is-fullheight">
            <div class="hero-body">
                <div class="">
                    <p class="title">
                        Learn continually - there's always "one more thing" to learn.
                    </p>
                    <p class="subtitle">
                        Steves Jobs
                    </p>
                    <p>
                        <a href="" class="button is-primary">
                            Sign Up
                        </a>
                        <a href="/login" class="button is-primary is-light">
                            Log In
                        </a>
                    </p>
                </div>
            </div>
        </section>

        <!-- LEARNER -->
        <Learner v-if="loginStatus == 'Learner'"></Learner>

        <!-- TRAINER -->
        <Trainer v-if="loginStatus == 'Trainer'"></Trainer>

        <!-- ADMIN -->
        <Admin v-if="loginStatus == 'Admin'"></Admin>

    </div>
</template>

<script>
import Learner from '@/components/users/Learner.vue'
import Trainer from '@/components/users/Trainer.vue'
import Admin from '@/components/users/Admin.vue'

export default {
    name: 'HomePage',
    components: {
        Learner,
        Trainer,
        Admin
    },
    computed: {
        loginStatus () {
            return this.$store.state.login
        }
    },
    data(){
        return {
            carousels: [
                { text: 'Slide 1', color: 'primary' },
                { text: 'Slide 2', color: 'info' },
                { text: 'Slide 3', color: 'success' },
                { text: 'Slide 4', color: 'warning' },
                { text: 'Slide 5', color: 'danger' }
            ]
        }
    }
}
</script>