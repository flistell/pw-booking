<script setup>
import { defineProps, ref, onMounted } from 'vue';


const props = defineProps({
    item: Object,
    booking_id: String,
    fromDate: String,
    toDate: String
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
        <div class="row alert alert-success align-items-center justify-content-center" role="alert">
            <div class="col-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="bi flex-shrink-0 me-2" viewBox="0 0 16 16" role="img"
                    aria-label="Success:">
                    <path
                        d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z" />
                </svg>
            </div>
            <div class="col-6">
                <p>La tua prenotazione è andata a buon fine.</p>
                <p>Hai richiesto {{ item.item_details.brand }} {{ item.item_details.model }}</p>
                <hr>
                <p>L'auto sarà a tua disposizione 
                    dal {{ fromDate.toLocaleDateString('it-IT') }} 
                    al {{ toDate.toLocaleDateString('it-IT') }}.
                </p>
                <p>Potrai ritirare l'auto presso:</p>
                <p>
                    <ul>
                        <li>{{ item.item_details.address_line1 }}</li>
                        <li v-if="item.item_details.address_line2">{{ item.item_details.address_line2 }}</li>
                        <li>{{ item.item_details.zip }} - {{ item.item_details.city }} 
                            <span v-if="item.item_details.city != item.item_details.state"> </span>({{ item.item_details.state }})
                            </li>
                    </ul>
                </p>
                <hr>
                <p>Il tuo codice prenotazione è il seguente "{{ booking_id }}."</p>
            </div>
        </div>
    </div>
    <!-- END components/BookingSuccessful.vue -->
</template>