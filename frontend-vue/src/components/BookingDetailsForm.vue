<script setup>
import { toRef } from 'vue'
import axios from 'axios'
import { settings } from '@/assets/data/settings.js'

const props = defineProps([
    'itemId',
    'userId',
    'name',
    'familyname',
    'from',
    'to'
])

const form_userid = toRef(props, 'userId') //non so se serve, è una prova

function fetchUser(userId){
    const url = `${settings.resourcesUrl}/users/${props.id}`
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

function initTransaction(){
    const bookingsUrl = `${settings.resourcesUrl}/bookings`
    const booking = {
        user_id: props.userId,
        booked_item_id: props.itemId,
        booking_start: props.fromDate,
        booking_end: props.toDate
    }
    axios.post(bookingsUrl, )
        .then((response) => {
            this.item = response.data
        })
        .catch((error) => {
            console.error(error)
        })
    console.log(this.item)
    }

function onFocusout(userid){
    console.log("onFocusout: " + userid)

}

</script>

<template>
    <!-- BEGIN components/BookingWizardForm.vue -->
    <h4>Dettagli della prenotazione.</h4>
    <form id="BookingWizardForm">
        <div id="bwf_div1" class="mb-3">
            <label for="bwf_userid" class="form-label">User ID</label>
            <input 
                id="bwf_userid" 
                class="form-control" 
                v-model="form_userid"
                @blur="onFocusout(form_userid)"
                required>   
        </div> <!-- bwf_div1 -->
        {{  userId  }}
        <div id="bwf_div1" class="mb-3">
            <label for="bwf_name" class="form-label">Nome</label>
            <input 
                id="bwf_name" 
                class="form-control" 
                :value="name"
                required>
        </div> <!-- bwf_div1 -->
        <div id="bwf_div1" class="mb-3">
            <label for="bwf_familyname" class="form-label">Cognome</label>
            <input 
                id="bwf_faminlyname" 
                class="form-control" 
                :value="familyname"
                required>
        </div> <!-- bwf_div1 -->
        <div id="bwf_div1" class="mb-3">
            <label for="bwf_email" class="form-label">Indirizzo eMail</label>
            <input id="bwf_email" type="email" class="form-control" placeholder="nome.cognome@example.com" required>
        </div> <!-- bwf_div1 -->
        <button 
            class="btn btn-primary" 
            type="submit" 
            data-bs-toggle="modal" 
            data-bs-target="#paymentForm"
            @click.prevent="initTransaction()"
            >Procedi al pagamento</button>
    </form>
    <!-- BEGIN components/BookingDetailsForm.vue -->
</template>