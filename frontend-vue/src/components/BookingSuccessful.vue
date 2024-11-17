<script setup>
import { ref,reactive, onMounted } from 'vue';

const props = defineProps({
    item: Object,
    booking_id: Number,
    booking_from: String,
    booking_to: String,
    status: String,
    title: String
})

const fromDate = new Date()
fromDate.setTime(props.booking_from)

const toDate = new Date()
toDate.setTime(props.booking_to)

const classObject = reactive({
    'alert-success': false,
    'alert-warning': true
})

const isSuccess = ref(true)
const isWarning = ref(false)

if (props.status == 'warning'){
    console.log("qui")
    isWarning.value = true
    isSuccess.value = false
}
if (props.status == 'success'){
    console.log("quo")
    isSuccess.value = true
    isWarning.value = false
}

</script>

<template>
    <!-- BEGIN components/BookingSuccessful.vue -->
    <div class="card-body">
        <div :class="{ 'alert-success': isSuccess, 'alert-warning': isWarning}" class="row alert align-items-center justify-content-center" role="alert">
            <div class="col-8">
                <h4 class="text-center">
                    <font-awesome-icon v-if="isWarning" :icon="['fas', 'triangle-exclamation']" />
                    <font-awesome-icon v-if="isSuccess" :icon="['fas', 'circle-check']" />
                    {{ props.title }}
                    <font-awesome-icon v-if="isWarning" :icon="['fas', 'triangle-exclamation']" />
                    <font-awesome-icon v-if="isSuccess" :icon="['fas', 'circle-check']" />
                </h4>
                <p>Hai richiesto:
                {{ props.item.item_details.brand }} {{ props.item.item_details.model }} [{{ props.item.id }}]</p>
                <hr>
                <p>L'auto sarà a tua disposizione
                    dal {{ fromDate.toLocaleDateString('it-IT') }}
                    al {{ toDate.toLocaleDateString('it-IT') }}.
                </p>
                <p>Potrai ritirare l'auto presso:</p>
                <ul>
                    <li>{{ props.item.address_line1 }}</li>
                    <li v-if="item.address_line2">{{ props.item.address_line2 }}</li>
                    <li>{{ props.item.zip }} - {{ props.item.city }}
                        <span v-if="item.city != props.item.state"> </span>({{ props.item.state }})
                    </li>
                </ul>
                <hr>
                <p>Il tuo codice prenotazione è il seguente "{{ booking_id }}".</p>
                <slot name="message"></slot>
            </div>
        </div>
    </div>
    <!-- END components/BookingSuccessful.vue -->
</template>