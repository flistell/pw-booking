<script setup>
import { ref } from 'vue';
import ItemCardSmall from '../components/ItemCardSmall.vue'

const props = defineProps({
    booking: Object
})

// const props = defineProps(
//     {booking:{
//         default: {
//             item_details: {
//                 brand: '_brand_',
//                 model: '_model_',
//                 photo: '_photo_'
//             }
//         }
//     }
//     })


const formatDate = (date) => {
    let d = new Date()
    d.setTime(date)
    return d.toLocaleDateString('it-IT')
}

console.log('props.booking', props.booking)

</script>

<template>
    <!-- BEGIN components/BookingRow.vue-->
    <div class="card item-card shadow-sm" no-body>
        <div class="row no-gutters">
            <div class="col-md-4 col-lg-3 p-2">
                <ItemCardSmall 
                        v-if="booking && booking.item_details"
                        :brand="booking.item_details.brand" 
                        :model="booking.item_details.model"
                        :photo="booking.item_details.photo" />
            </div>
            <div class="col-md-8 col-lg-9 p-2">
                <div class="card-body d-flex flex-column h-100">
                <h3 class="card-title">&nbsp;</h3>
                    <table class="table">
                        <tbody>
                            <tr>
                                <th scope="row">Stato prenotazione</th>
                                <td v-if="booking.booking_status == 'CANCELLED'" class="table-danger">PRENOTAZIONE
                                    CANCELLATA
                                </td>
                                <td v-if="booking.booking_status == 'BOOKED'" class="table-warning">PRENOTAZIONE NON
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
                                <td>{{ formatDate(booking.booking_start) }}</td>
                            </tr>
                            <tr>
                                <th scope="row"><font-awesome-icon :icon="['fas', 'circle-info']" /> Data di
                                    restituzione</th>
                                <td>{{ formatDate(booking.booking_end) }}</td>
                            </tr>
                            <tr>
                                <th scope="row">ID Utente</th>
                                <td>{{ booking.username }}</td>
                            </tr>
                            <tr><slot name="slot1"></slot></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    <!-- END components/BookingCard.vue-->
</template>