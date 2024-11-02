<script setup>
import { ref } from 'vue'
import BookingDetailsForm from '@/components/BookingDetailsForm.vue';
import axios from 'axios';
import { settings } from '@/assets/data/settings.js'
import ItemCardSmall from '@/components/ItemCardSmall.vue'

console.log("BookingWizard")
const props = defineProps({
    itemId: String,
    from: String,
    to: String,
})

const item = ref({ item_details: {} })

const url = `${settings.resourcesUrl}/items/${props.itemId}`
axios
    .get(url)
    .then((response) => {
        console.log(response);
        item.value = response.data;
    })
    .catch((error) => {
        console.error(error);
    });

const fromDate = new Date()
fromDate.setTime(props.from)
console.log(props.from)
console.log(fromDate)

const toDate = new Date()
toDate.setTime(props.to)
console.log(toDate)

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
                </ul>
            </div><!-- bw_col1 -->
            <div id="bw_col2" class="col-lg-8 mb-3 mb-lg-0">
                <div id="bw_form_card" class="card shadow">
                    <BookingDetailsForm :itemId="itemId" :from="from" :to="to" />
                </div><!-- bw_form_card -->
            </div><!-- bw_col2 -->
        </div><!-- bw_row -->
    </div> <!-- bw_main -->
    <!-- END components/BookingWizard.vue -->
</template>

<style lang="css" scoped>
#item_card_small{
    border: 0
}
</style>