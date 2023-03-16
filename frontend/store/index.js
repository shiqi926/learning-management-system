import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'

Vue.use(Vuex)

const store = {
    state() {
        return {
            // base: "http://localhost:8000",
            base: "https://spmg7-backend.herokuapp.com",
            login: null,
            username: null,
        }
    },
    mutations: {
        loginLearner(state, payload) {
            state.login = "Learner"
            state.username = payload
        },
        loginTrainer(state, payload) {
            state.login = "Trainer"
            state.username = payload
        },
        loginAdmin(state, payload) {
            state.login = "Admin"
            state.username = payload
        },
        logout(state) {
            state.login = null
            state.username = null
        }
    },
    plugins: [new VuexPersistence().plugin]
};

export default store;