<template>
    <section class="py-3">
        <b-button
            label="Create New Course"
            type="is-success"
            size="is-fullwidth"
            @click="isComponentModalActive = true" />

        <b-modal
            v-model="isComponentModalActive"
            has-modal-card
            trap-focus
            :destroy-on-hide="false"
            aria-role="dialog"
            aria-label="Course Create"
            aria-modal>
            <template #default="props">
                <modal-form v-bind="formProps" @close="props.close"></modal-form>
            </template>
        </b-modal>
    </section>
</template>

<script>
const ModalForm = {
        props: ['courseName', 'courseDesc', 'canCancel'],
        template: `
            <form action="">
                <div class="modal-card" style="width: is-medium">
                    <header class="modal-card-head">
                        <p class="modal-card-title">Create New Course</p>
                        <button
                            type="button"
                            class="delete"
                            @click="$emit('close')"/>
                    </header>
                    <section class="modal-card-body">
                        <b-field label="Course Name">
                            <b-input
                                :value="courseName"
                                placeholder="Course Name"
                                required>
                            </b-input>
                        </b-field>

                        <b-field label="Course Description">
                            <b-input
                                type="textarea"
                                :value="courseDesc"
                                placeholder="Course Description"
                                required>
                            </b-input>
                        </b-field>

                    </section>
                    <footer class="modal-card-foot">
                        <b-button
                            label="Close"
                            @click="$emit('close')" />
                        <b-button
                            label="Submit"
                            type="is-primary" />
                    </footer>
                </div>
            </form>
        `
    }

export default {
    name: 'CourseCreate',
    components: {
        ModalForm
    },
    computed: {
    },
    data() {
        return {
            isComponentModalActive: false,
            formProps: {
                courseName: '',
                courseDesc: ''
            }
        }
    }
}
</script>