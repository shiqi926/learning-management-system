<template>
    <div class="hero is-fullheight has-background-primary">
        <div class="hero-body">
            <div class="container">
                <form class="box">
                    <div class="field">
                        <label class="label">Username</label>
                        <div class="control">
                        <input class="input" type="username" v-model="username" placeholder="e.g. alex@example.com">
                        </div>
                    </div>

                    <div class="field">
                        <label class="label">Password</label>
                        <div class="control">
                        <input class="input" type="password" placeholder="********">
                        </div>
                    </div>

                    <div class="select">
                        <select v-model="loginType" @click="tryLogin()">
                            <option value="Learner">Learner</option>
                            <option value="Trainer">Trainer</option>
                            <option value="Admin">Admin</option>
                        </select>
                    </div>
                    
                    <div v-if="canLogin">
                        <br>
                        <button v-if="loginType=='Learner'" class="button is-primary"  @click="loginLearner(username)">Login</button>
                        <button v-if="loginType=='Trainer'" class="button is-primary" @click="loginTrainer(username)">Login</button>
                        <button v-if="loginType=='Admin'" class="button is-primary" @click="loginAdmin(username)">Login</button>
                    </div> 
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
    name: 'LoginPage',
    methods: {
        ...mapMutations({
            loginLearner: 'loginLearner',
            loginTrainer: 'loginTrainer',
            loginAdmin: 'loginAdmin'
        }),
        tryLogin() {
            event.preventDefault()
            console.log(this.loginDetails)
            var request = fetch(`${this.$store.state.base}/api/user/${this.username}/`).then((res) => {
                return res.json().then((data) => {
                    console.log(data)
                    this.isUser = true
                    this.isAdmin = data[0].is_admin
                    console.log()
                    if (this.loginType == "Admin" && !this.isAdmin) {
                        // alert("You are not an admin")
                    }
                    else {
                        this.canLogin = true
                    }
                });
            }).catch(error => {
                alert("You do not have an account")
            }) 
        }
    },
    data() {
        return {
            username: '',
            loginType: '',
            isUser: false,
            isAdmin: false,
            canLogin: false
        }
    }
}
</script>