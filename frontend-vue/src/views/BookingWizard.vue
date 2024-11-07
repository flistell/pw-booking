<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { settings } from '@/assets/data/settings.js';
import BookingDetailsForm from '@/components/BookingDetailsForm.vue';
import ItemCardSmall from '@/components/ItemCardSmall.vue';
import BookingPaymentForm from '@/components/BookingPaymentForm.vue';
import BookingProcessing from '@/components/BookingProcessing.vue';
import BookingSuccessful from '@/components/BookingSuccessful.vue';
import ErrorForm from '@/components/ErrorForm.vue';
import { storeToRefs } from 'pinia';
import { myAuthStore } from '@/stores/authUserStore'
import { hide } from '@popperjs/core';

const authUserStore = myAuthStore();
const { user } = storeToRefs(authUserStore);

const props = defineProps({
    id: String,
    from: String,
    to: String,
})

const item = ref({
    item_details: {
        brand: null,
        model: null,
        photo: null
    }
})

// Technical Debt: non il massimo dell'eleganza...

const onDetailsForm = ref(true)
const onPaymentForm = ref(false)
const onProcessingForm = ref(false)
const onSuccesForm = ref(false)
const onErrorForm = ref(false)
const paymentDetails = ref({})
const errorMessage = ref(null)
const booking_id = ref(-1)

const fromDate = new Date()
fromDate.setTime(props.from)

const toDate = new Date()
toDate.setTime(props.to)

const booking_confirmation_id = ref(null)

console.log("item id", props.id)

// Functions

const getItemDetails = () => {
    const url = `${settings.resourcesUrl}/items/${props.id}`
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

const hideAll = () => {
    onDetailsForm.value = false
    onPaymentForm.value = false
    onProcessingForm.value = false
    onSuccesForm.value = false
    onErrorForm.value = false
}


const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

const initBooking = async () => {
    console.log("initBooking")

    const bookingsUrl = `${settings.resourcesUrl}/bookings`
    const booking = {
        user_id: user.value.id,
        booked_item_id: props.id,
        booking_start: props.from,
        booking_end: props.to
    }
    console.log('BookingDetailForm create booking: ', booking)
    try {
        const response = await axios.post(bookingsUrl, booking);
        console.log("Booking response data:", response.data);
        console.log("Booking response data is:", response.data.id);
        booking_id.value = response.data.id;
        console.log('BookingDetailForm booked: ', booking_id);
    } catch (error) {
        console.error("Booking", error);
        hideAll();
        onErrorForm.value = true;
        errorMessage.value = error.response.data;
        return null;
    }
}

const confirmBooking = () => {
    console.log("confirmBooking()")
    console.log("BookingID: ", booking_id)
    const bookingsUrl = `${settings.resourcesUrl}/bookings/${booking_id.value}`
    console.log('BookingDetailForm update booking: ', bookingsUrl)
    const payload = {
        'id': booking_id.value,
        'booking_status': 'CONFIRMED'
    }
    axios.put(bookingsUrl, payload)
        .then((response) => {
            console.log("Booking confirm: ", response)
            hideAll()
            onSuccesForm.value = true
            console.log('BookingDetailForm booked: ', booking_confirmation_id)
        })
        .catch((error) => {
            console.error("Booking", error)
            hideAll();
            onErrorForm.value = true;
            errorMessage.value = error.response.data
            return
        })
}

onMounted(() => {getItemDetails()})

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
                    <BookingDetailsForm v-if="onDetailsForm" :id="id" :from="from" :to="to" />
                    <div id="button_row" class="btn-group" role="group">
                        <button v-if="onDetailsForm" id="canel-booking" type="button" class="btn btn-secondary btn-md"
                            @click="cancelBooking()">Annulla</button>
                        <button v-if="onDetailsForm" id="to-payment" type="button" class="btn btn-success"
                            @click="initBooking().then((resposne) => { confirmBooking() })"
                            >Conferma</button>
                        </div>

                    <!--
                    <BookingPaymentForm v-if="onPaymentForm" ref="paymentDetails" />
                    <div id="button_row" class="btn-group" role="group">
                        <button v-if="onPaymentForm" id="to-booking" type="button" class="btn btn-secondary btn-md"
                            @click="hideAll(); onDetailsForm = true"> &lt; Ritorna alla prenotazione</button>
                        <button v-if="onPaymentForm" id="confirm-payment" type="button" class="btn btn-warning"
                            @click="orderPayment">Conferma il pagamento ! </button>

                    <BookingProcessing v-if="onProcessingForm" />
                    </div><!-- button_row -->
                    <BookingSuccessful v-if="onSuccesForm" 
                        :booking_id="booking_id"
                        :item="item"
                        :booking_from="from"
                        :booking_to="to"
                         />

                    <ErrorForm v-if="onErrorForm" :message="errorMessage">
                        Vai su <a href="/manage" class="alert-link">"Gestiti prenotazioni"</a>.
                    </ErrorForm>

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