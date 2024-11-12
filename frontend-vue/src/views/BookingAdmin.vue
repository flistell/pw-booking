<script setup>
import { settings } from '@/assets/data/settings.js'
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'
import axios from 'axios';
import ConfirmDialog from '@/components/ConfirmDialog.vue';

// Object properties and dynamic

const router = useRouter()
const bookings = ref({
    item_details: {
        brand: '',
        model: ''
    }
})
const dialogSlotProp = ref()
const confirmModal = ref(null)

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
            if (error.status == 403) {
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

const openDetails = (id, modify) => {
    console.log("openDetails(): " + id )
    var url
    if (modify){
        url = `/bookings/${id}?modify=true`
    } else {
        url = `/bookings/${id}`
    }
    console.log("url:", url)
    router.push(url)
}

const formatDate = (date) => {
    let d = new Date()
    d.setTime(date)
    return d.toLocaleDateString('it-IT') 
}

const showConfirmForCancel = (booking_id) => {
    console.log("showConfirmForCancel: " + booking_id)
    dialogSlotProp.value = booking_id
    confirmModal.value.showModal();
}

const cancelConfirmed = () => {
    console.log("deleteConfirmed(): ", dialogSlotProp.value)
    const url = `${settings.resourcesUrl}/bookings/${dialogSlotProp.value}`
    axios.delete(
        url,
        { withCredentials: true }
        )
        .then((response) => {
            console.log(response.data);
            confirmModal.value.closeModal()
            getBookings()
        })
        .catch((error) => {
            confirmModal.value.closeModal()
            console.error(error);
            if (error.status == 403) {
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
        <ConfirmDialog 
            title="Elimina prenotazione" 
            ref="confirmModal"
            alert-class="danger"
            :callback="cancelConfirmed"
            btn-cancel-text="Annulla cancellazione.">
            Sei sicuro di voler eliminare la prenotazione '{{ dialogSlotProp }}' ?</ConfirmDialog>
        <div class="row">
            <div class="col-sm-10">
                <br>
                <h3>Prenotazioni</h3>
                <hr><br>
                <button type="button" class="btn btn-success btn-sm">New booking</button>
                <br><br>
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th scope="col">Codice prenotazione</th>
                            <th scope="col">Utente</th>
                            <th scope="col">Auto</th>
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
                            <td>{{ booking.username }}</td>
                            <td v-if="booking.item_details">{{ booking.item_details.brand || ''}} {{ booking.item_details.model || ''  }}</td>
                            <td v-else="booking.item_details">{{ booking.booked_item_id }}</td>
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
                                    <button type="button" 
                                            class="btn btn-warning btn-sm"
                                            @click="openDetails(booking.id, true)"
                                    >Modifica</button>
                                    <button type="button" class="btn btn-danger btn-sm"
                                        @click="showConfirmForCancel(booking.id)">Cancella</button>
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