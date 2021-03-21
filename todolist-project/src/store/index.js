import Vue from 'vue'
import Vuex from 'vuex'
import { authenticate } from '@/api'
import { isValidJwt, EventBus } from '@/utils'


Vue.use(Vuex)

const state = {
    userData: {},
    jwt: {'token': ''}
}

const actions = {
    login(context, userData) {
        context.commit('setUserData', { userData })
        return authenticate(userData)
            .then( 
                response => context.commit('setJwtToken', { jwt: response.data }))
            .catch(error => {
                console.log('Error Authenticating: ', error)
                EventBus.$emit('failedAuthentication', error)
            })
    }
}

const mutations = {
    setUserData (state, payload) {
        state.userData = payload.userData
    },
    setJwtToken (state, payload) {
        localStorage.token = payload.jwt.data
        state.jwt.token = payload.jwt.data
    }
}

const getters = {
    isAuthenticated (state) {
        return isValidJwt(state.jwt.token)
    },
    getJwtToken(state){
        return state.jwt.token;
    },
    getUserData(state){
        return state.userData;
    }
}

const store = new Vuex.Store({
    state,
    actions,
    mutations,
    getters
})

export default store