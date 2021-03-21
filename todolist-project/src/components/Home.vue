<template>
    <div class="row d-flex justify-content-center">
        <div class="col-md-10 mt-4">
            <div class="card-hover-shadow-2x mb-3 card">
                <div class="card-header-tab card-header bg-info">
                    <div class="h2 card-header-title font-size-lg text-capitalize text-center font-weight-normal ">{{$store.getters.getUserData.pseudo}}</div>
                </div>
                <div class="scroll-area-sm">
                    <div style="position: static;" class="ps ps--active-y">
                        <div class="ps-content">
                            <ul class=" list-group list-group-flush" v-for="(todolist,index) in todolists"  v-bind:index="index" v-bind:key="todolist.index">
                                <li class="list-group-item">
                                    <div class="todo-indicator bg-gradient"></div>
                                    <div class="widget-content p-0 ml-4">
                                        <div class="widget-content-wrapper">
                                            <div class="widget-content-left">
                                                <div class="widget-heading">{{ todolist.name }}
                                                </div>
                                                <div class="widget-subheading"><i>{{new Date(todolist.created_at).toDateString() }}</i></div>
                                            </div>
                                            <div class="widget-content-right">
                                                <router-link class="border-0 btn-transition btn btn-outline-info" :to="{path : '/Tasks/' + index}"><font-awesome-icon icon="eye"/></router-link>
                                                <button class="border-0 btn-transition btn btn-outline-warning" v-b-modal.edit-list-modal v-on:click="editListId(index)"><font-awesome-icon icon="pencil-alt"/></button>
                                                <button class="border-0 btn-transition btn btn-outline-danger" v-on:click="deleteList(index)"><font-awesome-icon icon="trash"/></button>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="d-block text-center card-footer bg-info">
                    <button class="btn btn-txt" v-b-modal.add-list-modal><font-awesome-icon class="font" icon="plus"/> &nbsp;Add List</button>
                </div>
            </div>
        </div>
        <b-modal ref="addListModal"
                id="add-list-modal"
                title="Add a new list"
                hide-footer>
            <b-form @submit="onSubmitAddList" @reset="onResetAddList" class="w-100">
                <b-form-group id="form-title-add-group"
                            label="Title:"
                            label-for="form-title-add-input">
                    <b-form-input id="form-title-add-input"
                                type="text"
                                v-model="addListForm.name"
                                required
                                placeholder="Enter title">
                    </b-form-input>
                </b-form-group>
                <b-button pill type="submit" variant="info" class="ml-4 mr-4">Submit</b-button>
                <b-button pill type="reset" variant="danger" class="ml-4">Reset</b-button>
            </b-form>
        </b-modal>
        <b-modal ref="editListModal"
                id="edit-list-modal"
                title="Edit a list"
                hide-footer>
            <b-form @submit="onSubmitEditList" @reset="onResetEditList" class="w-100">
                <b-form-group id="form-title-edit-group"
                            label="Title:"
                            label-for="form-title-edit-input">
                    <b-form-input id="form-title-edit-input"
                                type="text"
                                v-model="editListForm.name"
                                required
                                placeholder="Enter title">
                    </b-form-input>
                </b-form-group>
                <b-button pill type="submit" variant="info" class="ml-4 mr-4">Submit</b-button>
                <b-button pill type="reset" variant="danger" class="ml-4">Reset</b-button>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        data() {
            return {
                todolists: [],
                addListForm: {
                    name: '',
                    created_at: ''
                },
                editListForm: {
                    id: '',
                    name: ''
                },
            };
        },
        methods: {
            getTodolists() {
                const path = 'http://127.0.0.1:5001/api/lists';
                const auth = this.$store.getters.getJwtToken;
                axios.get(path, {headers: {token: auth}})
                    .then((res) => {               
                        this.todolists = res.data.data;
                    })
                    .catch((error) => {
                        console.error(error);
                    });
            },
            addList(payload) {
            const path = 'http://127.0.0.1:5001/api/lists';
            const auth = this.$store.getters.getJwtToken;
            axios.put(path, payload, {headers: {token: auth}})
                .then(() => {
                    this.getTodolists();
                })
                .catch((error) => {
                    console.error(error)
                    this.getTodolists();
                });
            },
            deleteList(todolist_id) {
                const path = 'http://127.0.0.1:5001/api/lists/' + todolist_id;
                const auth = this.$store.getters.getJwtToken;
                axios.delete(path, {headers: {token: auth}})
                    .then(() => {
                        this.getTodolists();
                        console.log("Delete list " + todolist_id + " in api");
                    })
                    .catch((error) => {
                        console.error(error);
                        this.getTodolists();
                    });
            },
            editList(payload) {
                const path = 'http://127.0.0.1:5001/api/lists/' + this.editListForm.id;
                const auth = this.$store.getters.getJwtToken;

                axios.patch(path, payload, {headers: {token: auth}})
                .then(() => {
                    console.log("Edit list " + payload.name + " in api")
                    this.getTodolists();
                })
                .catch((error) => {
                    console.log(error);
                    this.getTodolists();
                });
            },
            initFormAddList() {
                this.addListForm.name = '';
            },
            onSubmitAddList(evt) {
                evt.preventDefault();
                this.$refs.addListModal.hide();
                const payload = {
                    name: this.addListForm.name,
                    created_at: new Date()
                };
                this.addList(payload);
                this.initFormAddList();
            },
            onResetAddList(evt) {
                evt.preventDefault();
                this.initFormAddList();
            },
            editListId(todolist_id) {
                this.editListForm.id = todolist_id;
            },
            initFormEditList() {
                this.editListForm.name = '';
            },
            onSubmitEditList(evt) {
                evt.preventDefault();
                this.$refs.editListModal.hide();
                const payload = {
                    name: this.editListForm.name,
                };
                this.editList(payload);
                this.initFormEditList();
            },
            onResetEditList(evt) {
                evt.preventDefault();
                this.initFormEditList();
            },
        },
        created() {
            this.getTodolists();
        },
    };
</script>

<style>

</style>