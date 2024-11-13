<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router'
import { settings } from '@/assets/data/settings.js';
import ItemCardSmall from '@/components/ItemCardSmall.vue';
import Datepicker from 'vue3-datepicker'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import BookingSuccessful from '@/components/BookingSuccessful.vue';
import ErrorForm from '@/components/ErrorForm.vue';

const props = defineProps({
    canModify: {
        type: String,
        default: 'false'
    }
})

const onModify = ref(false)

const route = useRoute()
const booking = ref({})
const item = ref({
    item_details: {}
})
const booking_id = ref()
const person = ref({})

booking_id.value = route.params.booking_id

// console.log("booking id", booking_id.value)

const fromDate = ref(new Date())
const toDate = ref(new Date())
const fromDateNew = ref(new Date())
const toDateNew = ref(new Date())
const onSuccesForm = ref(false)
const onErrorForm = ref(false)
const errorMessage = ref("")

const resetForms = () => {
    onSuccesForm.value = false
    onErrorForm.value = false
}

// Functions

const getBookingDetails = (booking_id) => {
    console.log("getBookingDetails")
    const url = settings.resourcesUrl + '/bookings/' + booking_id
    // console.log(url)
    return axios.get(
        url,
        { withCredentials: true }
    )
        .then((response) => {
            booking.value = response.data
            // console.log(booking.value)
            fromDate.value.setTime(booking.value.booking_start)
            toDate.value.setTime(booking.value.booking_end)
            fromDateNew.value.setTime(booking.value.booking_start)
            toDateNew.value.setTime(booking.value.booking_end)

            // fromDateNew.value = fromDate.toISOString().substring(0, 10)
            // toDateNew.value = toDate.toISOString().substring(0, 10)
            // console.log("booking: ", booking.value)
            // console.log("booked item: ", booking.value.booked_item_id)
            // console.log("after")
        })
        .catch((error) => {
            console.log(error)
            alert(error)
        })
}

const getItemDetails = (item_id) => {
    console.log("getItemDetails")
    const url = `${settings.resourcesUrl}/items/${item_id}`
    // console.log("url", url)
    return axios.get(
            url,
            { withCredentials: true }
        )
        .then((response) => {
            // console.log(response);
            item.value = response.data;
        })
        .catch((error) => {
            console.error(error);
            alert(error)
        });
}

const getUserDetails = (user_id) => {
    console.log("getUserDetails")
    // Dovrei are una api speciale /users/me
    // Che restituisca i dettagli dell'utente loggato.
    const url = `${settings.resourcesUrl}/users/${user_id}`
    // console.log("url", url)
    return axios.get(
        url,
        { withCredentials: true }
    )
        .then((response) => {
            // console.log(response);
            person.value = response.data;
        })
        .catch((error) => {
            console.error(error);
            alert(error)
        });
}

const updateBooking = () => {
    console.log("updateBooking()")
    console.log("BookingID: ", booking_id.value)
    const bookingsUrl = `${settings.resourcesUrl}/bookings/${booking_id.value}`
    console.log('BookingDetailForm update booking: ', bookingsUrl)
    const payload = {
        id: Number(booking_id.value),
        booking_start: fromDateNew.value.getTime(),
        booking_end: toDateNew.value.getTime()
    }
    console.log('payload', payload)
    onModify.value = false
    axios.put(
        bookingsUrl, 
        payload,
        { withCredentials: true }
        )
        .then((response) => {
            console.log("Booking confirm: ", response)
            console.log('BookingDetailForm booked: ', response.data)
            resetForms()
            onSuccesForm.value = true
            fromDate.value = fromDateNew.value
            toDate.value = toDateNew.value
            onModify.value = false
        })
        .catch((error) => {
            console.error("Booking", error)
            alert(error)
            resetForms();
            onErrorForm.value = true;
            errorMessage.value = error.response.data
            return
        })
}
// Hooks

const canBook1 = computed(
    () =>
        toDateNew.value >= fromDateNew.value
)

const canBook2 = computed(
    () =>
        (toDateNew.value <= toDate.value) &&
        (fromDateNew.value >= fromDate.value) 
)

onMounted(() => { 
    // Promise chaining
    getBookingDetails(booking_id.value)
    .then(result => getItemDetails(booking.value.booked_item_id))
    .then(result => getUserDetails(booking.value.user_id))
    .then(() => {
        // this is to assure datepicker shows correct date from booking
        nextTick().then( () =>{
            if (props.canModify == 'true'){
                onModify.value = true
            }
        })
    })
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
            <div class="card col-lg-8">
                <BookingSuccessful v-if="onSuccesForm" :item="item" :booking_id="booking_id" :booking_from="fromDateNew"
                    :booking_to="toDateNew" :status="'success'">
                    <template v-slot:title>Modifica avvenuta con successo</template>
                    <template v-slot:message>
                        Ritorna a <a href="/bookings" class="alert-link">"Gestiti prenotazioni"</a>.
                    </template>
                </BookingSuccessful>
                <ErrorForm v-if="onErrorForm" :message="errorMessage">
                    Ritorna a <a href="/bookings" class="alert-link">"Gestiti prenotazioni"</a>.
                </ErrorForm>
                <div v-if="!onSuccesForm && !onErrorForm" id="booking_card" class="card-body">
                    <h2 class="card-title">Dettagli prenotazione</h2>
                    <table class="table">
                        <tbody>
                            <tr>
                                <th scope="row">Stato prenotazione</th>
                                <td v-if="booking.booking_status == 'CANCELLED'" class="table-danger">PRENOTAZIONE
                                    CANCELLATA
                                </td>
                                <td v-if="booking.booking_status == 'NEW'" class="table-warning">PRENOTAZIONE NON
                                    CONFERMATA
                                </td>
                                <td v-if="booking.booking_status == 'CONFIRMED'" class="table-success">PRENOTAZIONE
                                    CONFERMATA
                                </td>
                            </tr>
                            <tr>
                                <th scope="row">Codice prenotazione</th>
                                <td>{{ booking.id }}</td>
                            </tr>
                            <tr>
                                <th scope="row"><font-awesome-icon :icon="['fas', 'circle-info']" /> Data di ritiro</th>
                                <td v-if="onModify">
                                    <Datepicker id="datepicker-from-date-new" v-model="fromDateNew"
                                        :lower-limit="fromDate" :upperLimit="toDate" :clearable="false" :typeable="true"
                                        inputFormat='dd/MM/yyyy' />
                                </td>
                                <td v-else>{{ fromDate.toLocaleDateString('it-IT') }}</td>
                            </tr>
                            <tr>
                                <th scope="row"><font-awesome-icon :icon="['fas', 'circle-info']" /> Data di
                                    restituzione</th>
                                <td v-if="onModify">
                                    <Datepicker id="datepicker-to-date-new" v-model="toDateNew" :clearable="false"
                                        :typeable="true" :lower-limit="fromDate" :upperLimit="toDate"
                                        inputFormat='dd/MM/yyyy' />
                                    <p class="text-danger">
                                        {{ canBook1 ? '': 'La data di restituzione deve essere successiva a quella di ritiro.' }}
                                        {{ canBook2 ? '': 'Le nuove date devono essere comprese nell\'intervallo di prenotazione precedente' }}
                                    </p>
                                </td>
                                <td v-else>{{ toDate.toLocaleDateString('it-IT') }}</td>
                            </tr>
                            <tr v-if="onModify">
                                <td colspan="2" class="table-warning">
                                    <font-awesome-icon :icon="['fas', 'circle-exclamation']" />
                                    Le nuove date devono essere comprese nell intervallo di prenotazione precedente
                                    <font-awesome-icon :icon="['fas', 'circle-exclamation']" />
                                </td>
                            </tr>
                            <tr v-if="onModify">
                                <td colspan="2">
                                    <div class="d-flex justify-content-center">
                                <button type="button" class="btn btn-warning"  @click="updateBooking()">Salva modifiche</button>
                                </div>
                            </td>
                            </tr>
                        </tbody>
                    </table>
                    <h2 class="card-title">Dettagli Veicolo</h2>
                    <table class="table">
                        <tbody>
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