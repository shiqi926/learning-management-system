<template>
    <div class="py-3">

        <b-button
            label="Create New Class"
            type="is-success"
            size="is-fullwidth"
            @click="isComponentModalActive = true" />

        <b-modal
            v-model="isComponentModalActive"
            has-modal-card
            trap-focus
            :destroy-on-hide="false"
            aria-role="dialog"
            aria-label="Class Create"
            aria-modal>
            <template #default="props">
                <modal-form v-bind="formProps" @close="props.close"></modal-form>
            </template>
        </b-modal>
    </div>
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
                                :value="className"
                                placeholder="Class Name"
                                required>
                            </b-input>
                        </b-field>

                        <b-field label="Class Start Date">
                            <b-datepicker
                                ref="datepicker"
                                expanded
                                placeholder="Select a date">
                            </b-datepicker>
                            <b-button
                                @click="$refs.datepicker.toggle()"
                                icon-left="calendar-today"
                                type="is-primary" />
                        </b-field>
                        
                        <b-field label="Class End Date">
                            <b-datepicker
                                ref="datepicker"
                                expanded
                                placeholder="Select a date">
                            </b-datepicker>
                            <b-button
                                @click="$refs.datepicker.toggle()"
                                icon-left="calendar-today"
                                type="is-primary" />
                        </b-field>
                        
                        <b-field label="Enrol Start Date">
                            <b-datepicker
                                ref="datepicker"
                                expanded
                                placeholder="Select a date">
                            </b-datepicker>
                            <b-button
                                @click="$refs.datepicker.toggle()"
                                icon-left="calendar-today"
                                type="is-primary" />
                        </b-field>
                        
                        <b-field label="Enrol End Date">
                            <b-datepicker
                                ref="datepicker"
                                expanded
                                placeholder="Select a date">
                            </b-datepicker>
                            <b-button
                                @click="$refs.datepicker.toggle()"
                                icon-left="calendar-today"
                                type="is-primary" />
                        </b-field>

                        <b-field label="Class Size">
                            <b-numberinput v-model="number"></b-numberinput>
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
    name: 'ClassCreate',
    components: {
        ModalForm
    },
    computed: {
    },
    data() {
        return {
            isComponentModalActive: false,
            formProps: {
                className: '',
                startDate: '',
                endDate: '',
                enrolStart: '',
                enrolEnd: '',
                classSize: ''
            }
        }
    }
}
</script>