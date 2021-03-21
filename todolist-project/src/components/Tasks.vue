<template>
    <div class="row d-flex justify-content-center">
        <div class="col-md-10 mt-4">
            <div class="card-hover-shadow-2x mb-3 card">
                <div class="card-header-tab card-header  bg-info">
                    <div class="navbar-start">
                        <router-link to="/" class="border-0 btn-transition btn btn-outline-info bg-dark">
                            <font-awesome-icon icon="home"/>
                        </router-link>
                    </div>
                    <div class="card-header-title font-size-lg text-capitalize font-weight-normal h2 text-center">{{todolist['name']}}</div>
                </div>
                <div class="scroll-area-sm">
                    <div style="position: static;" class="ps ps--active-y">
                        <div class="ps-content">
                            <ul class=" list-group list-group-flush" v-for="(task, index) in taskslist" v-bind:index="index" v-bind:key="task.index">
                                <li class="list-group-item">
                                    <div class="todo-indicator bg-gradient"></div>
                                    <div class="widget-content p-0 ml-4">
                                        <div class="widget-content-wrapper">
                                            <div class="widget-content-left">
                                                <div class="widget-heading">{{task.name}}
                                                </div>
                                                <div class="widget-subheading"><i>{{new Date(task.created_at).toDateString() }}</i></div>
                                            </div>
                                            <div class="widget-content-right">
                                                <button class="border-0 btn-transition btn btn-outline-success" v-if="task.do" v-on:click="editDoTask(index, false)"><font-awesome-icon icon="check"/></button>
                                                 <button class="border-0 btn-transition btn btn-outline-danger" v-else v-on:click="editDoTask(index, true)"><font-awesome-icon icon="times"/></button> 
                                                <button class="border-0 btn-transition btn btn-outline-info" v-b-modal.view-task-modal v-on:click="getTask(index)"><font-awesome-icon icon="eye"/></button>
                                                <button class="border-0 btn-transition btn btn-outline-warning" v-b-modal.edit-task-modal v-on:click="editTaskId(index)"><font-awesome-icon icon="pencil-alt"/></button>
                                                <button class="border-0 btn-transition btn btn-outline-danger" v-on:click="deleteTask(index)"><font-awesome-icon icon="trash"/></button>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="d-block text-center card-footer bg-info">
                    <button class="btn btn-txt" v-b-modal.add-task-modal><font-awesome-icon class="font" icon="plus"/> &nbsp;Add Task</button>
                </div>
            </div>
        </div>
        <b-modal ref="addTaskModal"
                id="add-task-modal"
                title="Add a new Task"
                hide-footer>
            <b-form @submit="onSubmitAddTask" @reset="onResetAddTask" class="w-100">
                <b-form-group id="form-title-add-group"
                            label="Title:"
                            label-for="form-title-add-input">
                    <b-form-input id="form-title-add-input"
                                type="text"
                                v-model="addTaskForm.name"
                                required
                                placeholder="Enter title">
                    </b-form-input>
                </b-form-group>
                <b-button pill type="submit" variant="info" class="ml-4 mr-4">Submit</b-button>
                <b-button pill type="reset" variant="danger" class="ml-4">Reset</b-button>
            </b-form>
        </b-modal>
        <b-modal ref="editTaskModal"
                id="edit-task-modal"
                title="Edit a Task"
                hide-footer>
            <b-form @submit="onSubmitEditTask" @reset="onResetEditTask" class="w-100">
                <b-form-group id="form-title-edit-group"
                            label="Title:"
                            label-for="form-title-edit-input">
                    <b-form-input id="form-title-edit-input"
                                type="text"
                                v-model="editTaskForm.name"
                                required
                                placeholder="Enter title">
                    </b-form-input>
                </b-form-group>
                <b-button pill type="submit" variant="info" class="ml-4 mr-4">Submit</b-button>
                <b-button pill type="reset" variant="danger" class="ml-4">Reset</b-button>
            </b-form>
        </b-modal>
        <b-modal ref="viewTaskModal"
                id="view-task-modal"
                title="View a Task"
                hide-footer>
                <div div class="widget-heading"> Name : {{ task.name }}</div>
                <div class="widget-heading"><i>Date : {{new Date(task.created_at).toDateString() }}</i></div>
                <div class="widget-heading"><i>Do : {{task.do}}</i></div>
        </b-modal>
    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        data() {
            return {
                todolist: {},
                taskslist: [],
                task: {},
                addTaskForm: {
                    name: '',
                    created_at: '',
                    do: null,
                },
                editTaskForm: {
                    id: '',
                    name: ''
                }
            };
        },
        methods: {
            getTodolist() {
            const path = 'http://127.0.0.1:5001/api/lists/' + this.$route.params.id;
            const auth = this.$store.getters.getJwtToken;
            axios.get(path, {headers: {token: auth}})
                .then((res) => {
                    this.todolist = res.data.data;
                })
                .catch((error) => {
                    console.error(error);
                });
            },
            getTaskslist() {
            const path = 'http://127.0.0.1:5001/api/lists/todos/' + this.$route.params.id;
            const auth = this.$store.getters.getJwtToken;
            axios.get(path, {headers: {token: auth}})
                .then((res) => {
                    this.taskslist = res.data.data;
                })
                .catch((error) => {
                    console.error(error);
                });
            },
            getTask(index) {
            const path = 'http://127.0.0.1:5001/api/lists/todos/' + this.$route.params.id + '/' + index;
            const auth = this.$store.getters.getJwtToken;
            axios.get(path, {headers: {token: auth}})
                .then((res) => {
                    this.task = res.data.data;
                })
                .catch((error) => {
                    console.error(error);
                });
            },
            addTask(payload) {
            const path = 'http://127.0.0.1:5001/api/lists/todos/' + this.$route.params.id;
            const auth = this.$store.getters.getJwtToken;
            axios.put(path, payload, {headers: {token: auth}})
                .then(() => {
                    this.getTaskslist();
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getTaskslist();
                });
            },
            deleteTask(taskId) {
                const path = 'http://127.0.0.1:5001/api/lists/todos/' + this.$route.params.id + '/'+ taskId;
                const auth = this.$store.getters.getJwtToken;
                axios.delete(path, {headers: {token: auth}})
                    .then(() => {
                        this.getTaskslist();
                        console.log("Delete list " + taskId + " in api");
                    })
                    .catch((error) => {
                        console.error(error);
                        this.getTaskslist();
                    });
            },
            editTask(payload) {
                const path = 'http://127.0.0.1:5001/api/lists/todos/' + this.$route.params.id + '/'+ this.editTaskForm.id;
                const auth = this.$store.getters.getJwtToken;
                axios.patch(path, payload, {headers: {token: auth}})
                .then(() => {
                    console.log("Edit task " + payload + " in api")
                    this.getTaskslist();
                })
                .catch((error) => {
                    console.log(error);
                    this.getTaskslist();
                });
            },
            initFormAddTask() {
                this.addTaskForm.name = '';
                this.do = false;
            },
            onSubmitAddTask(evt) {
                evt.preventDefault();
                this.$refs.addTaskModal.hide();
                const payload = {
                    name: this.addTaskForm.name,
                    created_at: new Date(),
                    do: false
                };
                this.addTask(payload);
                this.initFormAddTask();
            },
            onResetAddTask(evt) {
                evt.preventDefault();
                this.initFormAddTask();
            },
            editTaskId(todo_id) {
                this.editTaskForm.id = todo_id;
            },
            initFormEditTask() {
                this.editTaskForm.name = '';
            },
            onSubmitEditTask(evt) {
                evt.preventDefault();
                this.$refs.editTaskModal.hide();
                const payload = {
                    name: this.editTaskForm.name,
                };
                this.editTask(payload);
                this.initFormEditTask();
            },
            onResetEditTask(evt) {
                evt.preventDefault();
                this.initFormEditTask();
            },
            editDoTask(index, bool_do) {
                this.editTaskId(index);
                const payload = {
                    do: bool_do,
                };
                this.editTask(payload);
            },
        },
        beforeMount() {
            console.log('Tasks.beforeMount -> :id ===', this.$route.params.id)
        },
        created() {
            this.getTodolist();
            this.getTaskslist();
        },
    };
</script>

