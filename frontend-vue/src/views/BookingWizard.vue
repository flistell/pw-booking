<script setup>
import BookingWizardForm from '@/components/BookingWizardForm.vue';
console.log("BookingWizard")
const props = defineProps({
    id: String,
    from: String,
    to: String,
    brand: String,
    model: String,
    photo: String
})
console.log("props")
console.log(props.id)
console.log(props.from)
console.log(props.brand)
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
                    <h2 class="card-title">{{ props.brand }} {{ model }}</h2>
                </div><!-- bw_item_card-->
            </div><!-- bw_col2 -->
        </div><!-- bw_row -->
    </div> <!-- bw_main -->
</template>