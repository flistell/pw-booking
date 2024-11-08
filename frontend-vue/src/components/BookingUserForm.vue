<script setup>
import { onMounted, ref } from 'vue';

const props = defineProps({
    user_object: Object
})

const user = ref({})

onMounted(()=>{
    user.value = props.user_object
})

</script>

<template>
    <!-- BEGIN components/BookingUserForm.vue -->
    <div class="card-body">
        <h4>Dettagli utente.</h4>
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
        </form>
    </div>
    <!-- BEGIN components/BookingUserForm.vue -->
</template>