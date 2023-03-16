<template>
    <b-navbar>
        <template #brand>
            <b-navbar-item tag="nuxt-link" to="/">
                <img
                    src="https://raw.githubusercontent.com/buefy/buefy/dev/static/img/buefy-logo.png"
                    alt="Lightweight UI components for Vue.js based on Bulma"
                >
            </b-navbar-item>
        </template>

        <template #start>
            <b-navbar-item tag="nuxt-link" to="/">
                Home
            </b-navbar-item>
            <b-navbar-item v-if="loginStatus" tag="nuxt-link" to="/courses">
                Courses
            </b-navbar-item>
        </template>

        <template #end>
            <b-navbar-item tag="div">
                <div class="buttons">
                    <b-navbar-item href="#" v-if="loginStatus == 'Learner'" class="button is-success is-light">
                        <span><strong>{{loginStatus}}:</strong> {{username}}</span>
                    </b-navbar-item>
                    <b-navbar-item href="#" v-if="loginStatus == 'Trainer'" class="button is-warning is-light">
                        <span><strong>{{loginStatus}}:</strong> {{username}}</span>
                    </b-navbar-item>
                    <b-navbar-item href="#" v-if="loginStatus == 'Admin'" class="button is-danger is-light">
                        <span><strong>{{loginStatus}}:</strong> {{username}}</span>
                    </b-navbar-item>
                    <b-navbar-item v-if="!loginStatus" class="button is-primary">
                        Sign Up
                    </b-navbar-item>
                    <b-navbar-item v-if="!loginStatus" tag="nuxt-link" to="/login" class="button is-light">
                        Log In
                    </b-navbar-item>
                    <b-navbar-item v-if="loginStatus" class="button is-danger" @click="logout()">
                        Log Out
                    </b-navbar-item>
                </div>
            </b-navbar-item>
        </template>
    </b-navbar>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
	name: 'NavbarDefault',
    computed: {
        loginStatus () {
            return this.$store.state.login
        },
        username () {
            return this.$store.state.username
        }
    },
    methods: {
        ...mapMutations({
            logout: 'logout',
        })
    }
}
</script>