<script setup>
import { settings } from '@/assets/data/settings.js'
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'
import axios from 'axios';
import ConfirmDialog from '@/components/ConfirmDialog.vue';

// Object properties and dynamic

const router = useRouter()
const bookings = ref([])
const dialogSlotProp = ref()
const showConfirm = ref(false)

// Functions

const getBookings = () => {
    const url = `${settings.resourcesUrl}/bookings`
    axios.get(
        url,
        { withCredentials: true}
        )
        .then((response) => {
            bookings.value = response.data;
            console.log(response.data);
        })
        .catch((error) => {
            console.error(error);
            if (error.status == 401){
                router.push({
                    path: '/logout'
                })  
            } else {
                router.push({
                    path: '/error/'
                })
            }
        })
    }

const openDetails = (id) => {
    console.log("openDetails(): " + id )
    router.push(
        `/bookings/${id}`
    )
}

const formatDate = (date) => {
    let d = new Date()
    d.setTime(date)
    return d.toLocaleDateString('it-IT') 
}

const showConfirmForCancel = (booking_id) => {
    console.log("showConfirmForCancel: " + booking_id)
    dialogSlotProp.value = booking_id.value
    showConfirm.value = true
}

const deleteConfirmed = () => {
    console.log("deleteConfirmed(): ", dialogSlotProp.value)
}

const confirmModal = ref(null)

function showModal() {
    console.log('showModal', confirmModal.value)
    confirmModal.value.showModal();
}

// Hooks

onMounted(() => { getBookings() })

console.log(ConfirmDialog)

</script>
<template>
    <!-- BEGIN views/BookingAdmin -->
    <div class="d-flex">
        showConfirm: {{ showConfirm }}
                #
        <ConfirmDialog 
            title="Elimina prenotazione" 
            ref="confirmModal"
            alert-class="warning">
            Sei sicuro di voler eliminare la prenotazione '{{ dialogSlotProp }}' ?</ConfirmDialog>
        #
        <div class="row">
            <div v-if="showConfirm"><br>Adesso si</div>
            <div class="col-sm-10">
                <br>
                <h3>Prenotazioni</h3>
                <hr><br>
                <button type="button" class="btn btn-success btn-sm">New booking</button>
                <br><br>
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th scope="col">Id</th>
                            <th scope="col">User</th>
                            <th scope="col">Item Id</th>
                            <th scope="col">Start</th>
                            <th scope="col">End</th>
                            <th scope="col">Status</th>
                            <th scope="col">Booked</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(booking, index) in bookings" :key="index">
                            <td>{{ booking.id }}</td>
                            <td>{{ booking.user_id }}</td>
                            <td>{{ booking.booked_item_id }}</td>
                            <td>{{ formatDate(booking.booking_start) }}</td>
                            <td>{{ formatDate(booking.booking_end) }}</td>
                            <td>{{ booking.booking_status }}</td>
                            <td>
                                <span v-if="!booking.booking_status > 0">No</span>
                                <span v-else>Yes</span>
                            </td>
                            <td>
                                <div class="btn-group" role="group">
                                    <button type="button" @click="openDetails(booking.id)"
                                        class="btn btn-primary btn-sm">Dettagli</button>
                                    <button type="button" class="btn btn-warning btn-sm">Modifica</button>
                                    <button type="button" class="btn btn-danger btn-sm"
                                        @click="showModal">Cancella</button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        </div>
    <!-- END views/BookingAdmin -->
</template>