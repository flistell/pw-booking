<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router'
import { settings } from '@/assets/data/settings.js';
import BookingUserForm from '@/components/BookingUserForm.vue';
import ItemCardSmall from '@/components/ItemCardSmall.vue';

const route = useRoute()
const booking = ref({})
const item = ref({})
const booking_id = ref()
const user = ref({})

booking_id.value = route.params.booking_id

console.log("booking id", booking_id.value)

const fromDate = new Date()
const toDate = new Date()
// Functions

const getBookingDetails = (booking_id) => {
    console.log("getBookingDetails")
    const url = settings.resourcesUrl + '/bookings/' + booking_id
    console.log(url)
    return axios.get(
        url,
        { withCredentials: true }
    )
        .then((response) => {
            booking.value = response.data
            console.log(booking.value)
            fromDate.setTime(booking.value.booking_start)
            toDate.setTime(booking.value.booking_end)
            console.log("booking: ", booking.value)
            console.log("booked item: ", booking.value.booked_item_id)
            console.log("after")
        })
        .catch((error) => {
            console.log(error)
            alert(error)
        })
}

const getItemDetails = (item_id) => {
    console.log("getItemDetails")
    const url = `${settings.resourcesUrl}/items/${item_id}`
    console.log("url", url)
    return axios.get(
            url,
            { withCredentials: true }
        )
        .then((response) => {
            console.log(response);
            item.value = response.data;
        })
        .catch((error) => {
            console.error(error);
        });
}

const getUserDetails = (user_id) => {
    console.log("getUserDetails")
    const url = `${settings.resourcesUrl}/users/${user_id}`
    console.log("url", url)
    return axios.get(
        url,
        { withCredentials: true }
    )
        .then((response) => {
            console.log(response);
            user.value = response.data;
        })
        .catch((error) => {
            console.error(error);
        });
}

onMounted(() => { 
    // Promise chaining
    getBookingDetails(booking_id.value)
    .then(result => getItemDetails(booking.value.booked_item_id))
    .then(result => getUserDetails(booking.value.user_id))
})


</script>

<template>
    {{ booking }}
    <hr>
    {{ item }}
    <hr>
    {{ user }}
    <!-- BEGIN components/BookingWizard.vue -->

    <!-- END components/BookingWizard.vue -->
</template>

<style lang="css" scoped>
#item_card_small {
    border: 0
}
</style>