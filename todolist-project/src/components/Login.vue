  <template>
    <div class="row d-flex justify-content-center">
        <div class="col-md-10 mt-4">
            <div class="card-hover-shadow-2x mb-3 card">
                <div class="card-header-tab card-header  bg-info">
                    <div class="h2 card-header-title font-size-lg text-capitalize font-weight-normal text-center">Login</div>
                </div>
                <div class="scroll-area-sm-dis">
                    <div style="position: static;" class="ps ps--active-y">
                        <div class="text-center">
                            <div>
                                <label class="widget-heading">Username:</label>
                                <div class="control">
                                    <input type="txt" class="input is-large" id="pseudo" v-model="pseudo">
                                </div>
                            </div>
                            <div class="field">
                                <label class="widget-heading">Password:</label>
                                <div class="control">
                                    <input type="password" class="input is-large" id="password" v-model="password">
                                </div>
                            </div>
                            <p v-if="errorMessage!=null">{{ errorMessage }}</p>
                            <div class="control">
                                <a class="btn btn-info mr-4" @click="authenticate">Login</a>
                                <router-link class="btn btn-primary" to="/Signup">Sign Up</router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    import { EventBus } from '@/utils'
    import md5 from 'js-md5'
    export default {
        data() {
            return {
                pseudo: '',
                password: '',
                errorMessage: ''
            }
        },
        methods: {
            authenticate () {
                this.$store.dispatch('login', { pseudo: this.pseudo, password: md5(this.password) })
                    .then(() => this.$router.push('/'))
            },
        },
        mounted () {
            EventBus.$on('failedAuthentication', (message) => {
                this.errorMessage = message
            })
        },
        beforeDestroy () {
            EventBus.$off('failedAuthentication')
        }
        
    };


</script>

<style>
.scroll-area-sm-dis {
    height: 12em;
    overflow-x: hidden
}
</style>