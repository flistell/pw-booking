<script setup>
import { settings } from '@/assets/data/settings.js'
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router'
import axios from 'axios';
import ConfirmDialog from '@/components/ConfirmDialog.vue';
import BookingRow from '@/components/BookingRow.vue';

// Object properties and dynamic objects
const router = useRouter()
const bookings = ref({
    item_details: {
        brand: '_brand_',
        model: '_model_',
        photo: '_photo_'
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
            console.log("bookings", response.data);
        })
        .catch((error) => {
            console.error(error);
            if (error.status == 401) {
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

// const formatDate = (date) => {
//     let d = new Date()
//     d.setTime(date)
//     return d.toLocaleDateString('it-IT') 
// }

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
            if (error.status == 401) {
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

// Hooks
onMounted(async () => { getBookings() })
</script>

<template>
    <!-- BEGIN views/BookingAdmin -->
    <div class="d-flex">
        <ConfirmDialog title="Elimina prenotazione" ref="confirmModal" alert-class="danger" :callback="cancelConfirmed"
            btn-cancel-text="Annulla cancellazione.">
            Sei sicuro di voler eliminare la prenotazione '{{ dialogSlotProp }}' ?</ConfirmDialog>
    </div>
    <section v-for="(booking, index) in bookings">
        <BookingRow :key="index" :booking="booking" class="mb-3" >
            <template v-slot:slot1>
                <td colspan="2">
                <div class="btn-group d-flex justify-content-center" role="group">
                    <button type="button" @click="openDetails(booking.id)" class="btn btn-primary btn-sm">Dettagli</button>
                    <button type="button" class="btn btn-warning btn-sm"
                        @click="openDetails(booking.id, true)"
                        :disabled="booking.booking_status == 'CANCELLED'">Modifica</button>
                    <button type="button" class="btn btn-danger btn-sm"
                        @click="showConfirmForCancel(booking.id)"
                        :disabled="booking.booking_status == 'CANCELLED'">Cancella</button>
                </div>
                </td>
             </template>
        </BookingRow>
    </section>
    <!-- END views/BookingAdmin -->
</template>