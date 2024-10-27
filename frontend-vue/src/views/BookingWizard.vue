<script setup>
import { ref } from 'vue'
import BookingWizardForm from '@/components/BookingWizardForm.vue';
import axios from 'axios';
import { settings } from '@/assets/data/settings.js'

console.log("BookingWizard")
const props = defineProps({
    id: String,
    from: String,
    to: String,
})

const item = ref({ item_details: {} })

function fetchItem(){
    console.log("fetchItem(" + props.id + ")")
    const url = settings.backendUrl + props.id;
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

console.log(settings.backendUrl)
console.log("props")
console.log(props.id)
console.log(props.from)

fetchItem()

console.log("item")
console.log(item)
</script>

<template>
    <div id="bw_main">
        <div id="bw_row" class="row align-items-start">
            <div id="bw_col1" class="col-lg-8 mb-3 mb-lg-0">
                <div id="bw_form_card" class="card shadow">
                    <BookingWizardForm />
                </div><!-- bw_form_card -->
            </div><!-- bw_col1 -->
            <div id="bw_col2" class="col-lg-4 sticky p-lg-0">
                <div id="bw_item_card" class="card shadow">
                    <h2 class="card-title">{{ item.item_details.brand }} {{ item.item_details.model }}</h2>
                </div><!-- bw_item_card-->
            </div><!-- bw_col2 -->
        </div><!-- bw_row -->
    </div> <!-- bw_main -->
</template>