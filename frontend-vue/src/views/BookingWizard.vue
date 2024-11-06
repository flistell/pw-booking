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

console.log("item id", props.id)

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

const initBooking = () => {
    const bookingsUrl = `${settings.resourcesUrl}/bookings`
    const booking = {
        user_id: user.value.id,
        booked_item_id: props.id,
        booking_start: props.from,
        booking_end: props.to
    }

    axios.post(bookingsUrl, booking)
        .then((response) => {
            console.log("Booking", response.data)
            booking_id.value = response.data.id
            console.log('BookingDetailForm booked: ', booking_id)
        })


}

onMounted(() => getItemDetails())

const fromDate = new Date()
fromDate.setTime(props.from)

const toDate = new Date()
toDate.setTime(props.to)

// Technical Debt: non il massimo dell'eleganza...

const onDetailsForm = ref(true)
const onPaymentForm = ref(false)
const onProcessingForm = ref(false)
const onSuccesForm = ref(false)
const onErrorForm = ref(false)
const paymentDetails = ref({})
const errorMessage = ref(null)
const booking_id = ref(null)

const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))



const cancelBooking = () => {

}


async function hideAll(){
    console.log("hideAll")
    onDetailsForm.value = false
    onPaymentForm.value = false
    onProcessingForm.value = false
    onSuccesForm.value = false
    onErrorForm.value = false
}

async function orderPayment(){
    console.log("orderPayment")
    await hideAll()
    onProcessingForm.value = true
    
    const bookingsUrl = `${settings.resourcesUrl}/bookings`
    const booking = {
        user_id: user.value.id,
        booked_item_id: props.id,
        booking_start: props.from,
        booking_end: props.to
    }
    console.log('BookingDetailForm create booking: ', booking)
    axios.post(bookingsUrl, booking)
        .then((response) => {
            console.log("Booking", response.data)
            booking_id.value = response.data.id
            console.log('BookingDetailForm booked: ', booking_id)
        })
        .then(() => {
            const paymentData = {
                'fullname': paymentDetails.value.fullname,
                'number': paymentDetails.value.ccnumber,
                'valid_to': paymentDetails.value.month + "/" + paymentDetails.value.year,
                'ccv': paymentDetails.value.ccv,
                'booking_id': booking_id
            }
            console.log('BookingWizard going to post: ', paymentData)
            console.log('Paymnet is simulated!')
            sleep(3000)
                .then(() => {
                    console.log('After Sleep')
                    axios.put(bookingsUrl + '/' + booking_id)
                        .then((response) => {
                            console.log(response.data)
                            hideAll()
                            onSuccesForm.value = true
                })
            })
        })
        .catch((error) => {
            console.error("Booking", error)
            hideAll();
            onErrorForm.value = true;
            errorMessage.value = error.response.data
            return
        })
}

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
                        <button v-if="onDetailsForm" id="to-payment" type="button" class="btn btn-primary"
                            @click="hideAll(); onPaymentForm = true">Procedi al pagamento &gt;</button>
                        </div>

                    <BookingPaymentForm v-if="onPaymentForm" ref="paymentDetails" />
                    <div id="button_row" class="btn-group" role="group">
                        <button v-if="onPaymentForm" id="to-booking" type="button" class="btn btn-secondary btn-md"
                            @click="hideAll(); onDetailsForm = true"> &lt; Ritorna alla prenotazione</button>
                        <button v-if="onPaymentForm" id="confirm-payment" type="button" class="btn btn-warning"
                            @click="orderPayment">Conferma il pagamento ! </button>

                        <BookingProcessing v-if="onProcessingForm" />

                        <BookingSuccessful v-if="onSuccesForm" :id="booking_id" />

                        <ErrorForm v-if="onErrorForm" :message="errorMessage">
                            Vai su <a href="/manage" class="alert-link">"Gestiti prenotazioni"</a>.
                        </ErrorForm>

                    </div><!-- button_row -->
                </div><!-- bw_form_card -->
            </div><!-- bw_col2 -->
        </div><!-- bw_row -->
    </div> <!-- bw_main -->
    <!-- END components/BookingWizard.vue -->
     {{ paymentDetails  }}
</template>

<style lang="css" scoped>
#item_card_small {
    border: 0
}
</style>