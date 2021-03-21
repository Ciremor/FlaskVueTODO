<template>
    <div class="row d-flex justify-content-center">
        <div class="col-md-10 mt-4">
            <div class="card-hover-shadow-2x mb-3 card">
                <div class="card-header-tab card-header  bg-info">
                    <div class="h2 card-header-title font-size-lg text-capitalize font-weight-normal text-center">Sign Up</div>
                </div>
                <div class="scroll-area-sm-dis">
                    <div style="position: static;" class="ps ps--active-y">
                        <div class="text-center">
                            <div>
                                <label class="widget-heading">Username:</label>
                                <div class="control">
                                    <input type="txt" class="input is-large" id="pseudo" v-model="pseudo" required>
                                </div>
                            </div>
                            <div class="field">
                                <label class="widget-heading">Password:</label>
                                <div class="control">
                                    <input type="password" class="input is-large" id="password" v-model="password" required>
                                </div>
                            </div>
                            <p v-if="errorMessage!=null">{{ errorMessage }}</p>
                            <div class="control">
                                <a class="btn btn-info mr-4" @click="register">Sign up</a>
                                <router-link class="btn btn-primary" to="/Login">Login</router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { EventBus } from '@/utils';
    import md5 from 'js-md5';
    import axios from 'axios';
    
    export default {
        data() {
            return {
                pseudo: '',
                password: '',
                errorMessage: ''
            }
        },
        methods: {
            register() {
                const path = 'http://127.0.0.1:5001/api/account';
                var user = { pseudo: this.pseudo, password: md5(this.password) };
                axios({method: 'post', url: path, data: user})
                    .then(() => {
                        this.$store.dispatch('login', { pseudo: this.pseudo, password: md5(this.password) })
                            .then(() => this.$router.push('/'))
                    })
                    .catch((error) => {
                        console.error(error.message);
                    });
            }
        },
        mounted () {
            EventBus.$on('failedRegistering', (message) => {
                this.errorMessage = message
            })
        },
        beforeDestroy () {
            EventBus.$off('failedRegistering')
        }
    };
</script>