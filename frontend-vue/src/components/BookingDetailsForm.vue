<script setup>
import { defineProps, ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { settings } from '@/assets/data/settings.js'
import { storeToRefs } from 'pinia';
import { myAuthStore } from '@/stores/authUserStore'

console.log("BookingDetailsForm")
const authUserStore = myAuthStore();
const { user } = storeToRefs(authUserStore);

const props = defineProps({
    id: String,
    from: String,
    to: String
})


</script>

<template>
    <!-- BEGIN components/BookingDetailsForm.vue -->
    <div class="card-body">
        <h4>Dettagli della prenotazione.</h4>
        <form id="BookingWizardForm">
            <div id="bwf_div1" class="mb-3">
                <label for="bwf_userid" class="form-label">User ID</label>
                <input id="bwf_userid" class="form-control" :value="user.username" required readonly disabled>
            </div> <!-- bwf_div1 -->
            <div id="bwf_div1" class="mb-3">
                <label for="bwf_name" class="form-label">Nome</label>
                <input id="bwf_name" class="form-control" :value="user.common_name" required readonly disabled>
            </div> <!-- bwf_div1 -->
            <div id="bwf_div1" class="mb-3">
                <label for="bwf_familyname" class="form-label">Cognome</label>
                <input id="bwf_familyname" class="form-control" :value="user.family_name" required readonly disabled>
            </div> <!-- bwf_div1 -->
            <div id="bwf_div1" class="mb-3">
                <label for="bwf_email" class="form-label">Indirizzo eMail</label>
                <input id="bwf_email" type="email" class="form-control" :value="user.mail_address" required readony
                    disabled>
            </div> <!-- bwf_div1 -->
            <!--
            <button class="btn btn-primary" type="submit" data-bs-target="#paymentForm"
                @click.prevent="initTransaction()">Procedi al pagamento</button>
            -->
        </form>
    </div>
    <!-- BEGIN components/BookingDetailsForm.vue -->
</template>