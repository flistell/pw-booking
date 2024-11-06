<script setup>
import { defineProps, ref, onMounted } from 'vue';


const props = defineProps({
    id: Number
})

const booking = ref({})

const getBookingDetails = (id) => {
    console.log("getBookingDetails(" + id + ")")
}

onMounted(() => { getBookingDetails(props.id) })

</script>

<template>
    <!-- BEGIN components/BookingSuccessful.vue -->
    <div class="card-body">
        <h4>Prenotazione riuscita</h4>
        <div class="d-flex justify-content-center">
            <span>La tua prenotazione è andata a buon fine.</span>
        </div>
    </div>
    <!-- END components/BookingSuccessful.vue -->
</template>