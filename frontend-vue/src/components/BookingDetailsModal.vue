<script setup>
import axios from 'axios';
import { onBeforeMount, onBeforeUpdate, reactive } from 'vue';
import { settings } from '@/assets/data/settings.js'


console.log("BookingDetailsModal")
const props = defineProps({
    id: Number
})

const booking = reactive({})

const getBooking = () => {
    const url = settings.resourcesUrl + '/bookings/' + props.id
    console.log(url)
    axios.get(
        url,
        { withCredentials: true }
    )
    .then((response) => {
        booking.value = response.data
        console.log(booking.value)
    })
    .catch((error) => {
        console.log(error)
        alert(error)
    })
}

onBeforeMount(() => { getBooking() })

</script>

<template>
    <!-- BEGIN components/BookingDetailsModal.vue -->
    <div ref="editBookModal" class="modal fade" :class="{ show: activeEditBookModal, 'd-block': activeEditBookModal }"
        tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Update</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"
                        @click="toggleDetails">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="editBookTitle" class="form-label">Title:</label>
                            <input type="text" class="form-control" id="editBookTitle" v-model="editBookForm.title"
                                placeholder="Enter title">
                        </div>
                        <div class="mb-3">
                            <label for="editBookAuthor" class="form-label">Author:</label>
                            <input type="text" class="form-control" id="editBookAuthor" v-model="editBookForm.author"
                                placeholder="Enter author">
                        </div>
                        <div class="mb-3 form-check">
                            <input type="checkbox" class="form-check-input" id="editBookRead"
                                v-model="editBookForm.read">
                            <label class="form-check-label" for="editBookRead">Read?</label>
                        </div>
                        <div class="btn-group" role="group">
                            <button type="button" class="btn btn-primary btn-sm" @click="handleEditSubmit">
                                Submit
                            </button>
                            <button type="button" class="btn btn-danger btn-sm" @click="handleEditCancel">
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    <div v-if="activeEditBookModal" class="modal-backdrop fade show"></div>
    <!-- END components/BookingDetailsModal.vue -->
</template>