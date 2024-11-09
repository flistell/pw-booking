<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router'
import { settings } from '@/assets/data/settings.js';
import ItemCardSmall from '@/components/ItemCardSmall.vue';

const route = useRoute()
const booking = ref({})
const item = ref({
    item_details: {}
})
const booking_id = ref()
const person = ref({})

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
    // Dovrei are una api speciale /users/me
    // Che restituisca i dettagli dell'utente loggato.
    const url = `${settings.resourcesUrl}/users/${user_id}`
    console.log("url", url)
    return axios.get(
        url,
        { withCredentials: true }
    )
        .then((response) => {
            console.log(response);
            person.value = response.data;
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
    <!-- BEGIN components/BookingWizard.vue -->

    <div id="bw_main">
        <div id="bw_row" class="row align-items-start">
            <div id="bw_r1c1" class="card col-lg-4 sticky p-lg-0">
                <ItemCardSmall :brand="item.item_details.brand" :model="item.item_details.model"
                    :photo="item.item_details.photo" />
            </div>
            <div id="bw_r1c2" class="card col-lg-8">
                <div id="booking_card" class="card-body">
                    <h2 class="card-title">Dettagli prenotazione</h2>
                    <table class="table">
                        <tbody>
                            <tr>
                                <th scope="row">Codice prenotazione</th>
                                <td>{{ booking.id }}</td>
                            </tr>
                            <tr>
                                <th scope="row">Auto</th>
                                <td>{{ item.item_details.brand }} {{ item.item_details.model }}</td>
                            </tr>
                            <tr>
                                <th scope="row">
                                    <font-awesome-icon icon="fa-solid fa-car" />
                                    Potenza
                                </th>
                                <td> {{ item.item_details.horsepower }} Kw </td>
                            </tr>
                            <tr>
                                <th scope="row">
                                    <font-awesome-icon icon="fa-solid fa-smog" />
                                    Emissioni
                                </th>
                                <td> {{ item.item_details.emission }} CO<sub>2</sub> g/Km </td>
                            </tr>
                            <tr>
                                <th scope="row">
                                    <font-awesome-icon icon="fa-solid fa-gas-pump" />
                                    Consumo
                                </th>
                                <td> {{ item.item_details.fuel_consumption }} l/100Km </td>
                            </tr>
                            <tr>
                                <th scope="row">Data di ritiro</th>
                                <td>{{ fromDate.toLocaleDateString('it-IT') }}</td>
                            </tr>
                            <tr>
                                <th scope="row">Data di restituzione</th>
                                <td>{{ toDate.toLocaleDateString('it-IT') }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <h2 class="card-title">Luogo di ritiro</h2>
                    <table class="table">
                        <tbody>
                            <tr>
                                <th scope="row">Città</th>
                                <td>{{ item.city }} ({{ item.state }})</td>
                            </tr>
                            <tr>
                                <th scope="row">Indirizzo</th>
                                <td>{{ item.address_line1 }} {{ item.address_line2 }}</td>
                            </tr>
                            <tr>
                                <th scope="row">Possessore</th>
                                <td>{{ item.owner }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <h2 class="card-title">Utilizzatore</h2>
                    <table class="table">
                        <tbody>
                            <tr>
                                <th scope="row">Nome</th>
                                <td>{{ person.common_name }}</td>
                            </tr>
                            <tr>
                                <th scope="row">Congnome</th>
                                <td>{{ person.family_name }} </td>
                            </tr>
                            <tr>
                                <th scope="row">Codice utente</th>
                                <td>{{ person.username }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div><!-- bw_r1c1 -->
        </div><!-- bw_row -->
    </div> <!-- bw_main -->

    <!-- END components/BookingWizard.vue -->
</template>

<style lang="css" scoped>
#item_card_small {
    border: 0
}
</style>