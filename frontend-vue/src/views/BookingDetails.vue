<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { settings } from '@/assets/data/settings.js';
import BookingUserForm from '@/components/BookingUserForm.vue';
import ItemCardSmall from '@/components/ItemCardSmall.vue';

const props = defineProps({
    booking_id: String
})

const booking = ref({})

console.log("booking id", props.booking_id)

const fromDate = ref(new Date())
const toDate = ref(new Date())
// Functions

const getBookingDetails = (booking_id) => {
    const url = settings.resourcesUrl + '/bookings/' + booking_id
    console.log(url)
    axios.get(
        url,
        { withCredentials: true }
    )
        .then((response) => {
            booking.value = response.data
            console.log(booking.value)
            fromDate.setTime(booking.value.booking_start)
            toDate.setTime(booking.value.booking_end)
            getItemDetails(booking.value.booked_item_id)
        })
        .catch((error) => {
            console.log(error)
            alert(error)
        })
}


const getItemDetails = (item_id) => {
    const url = `${settings.resourcesUrl}/items/${item_id}`
    console.log("url", url)
    axios
        .get(url)
        .then((response) => {
            console.log(response);
            item.value = response.data;
        })
        .catch((error) => {
            console.error(error);
        });
}

onMounted(() => { 
    getBookingDetails(props.booking_id);
 })



</script>

<template>
    <!-- BEGIN components/BookingWizard.vue -->
    <div id="bw_main">
        <div id="bw_row" class="row align-items-start">
            <div id="bw_col1" class="card col-lg-4 sticky p-lg-0">
                <ItemCardSmall :brand="item.item_details.brand" :model="item.item_details.model"
                    :photo="item.item_details.photo" />
                <ul>
                    <li>
                        <b>Data di ritiro:</b> {{ fromDate.toLocaleDateString('it-IT') }}
                    </li>
                    <li>
                        <b>Data di restituzione</b>: {{ toDate.toLocaleDateString('it-IT') }}
                    </li>
                    <li v-if="booking_id">
                        <b>Codice di prenotazione</b>: {{ booking_id }}
                    </li>
                </ul>
            </div><!-- bw_col1 -->
            <div id="bw_col2" class="col-lg-8 mb-3 mb-lg-0">
                <div id="bw_form_card" class="card shadow">
                    <BookingUserForm :id="booking_" :from="from" :to="to" />
                </div><!-- bw_form_card -->
            </div><!-- bw_col2 -->
        </div><!-- bw_row -->
    </div> <!-- bw_main -->
    <!-- END components/BookingWizard.vue -->
</template>

<style lang="css" scoped>
#item_card_small {
    border: 0
}
</style>