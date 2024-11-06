<script setup>
import { ref } from 'vue'

const fullname = ref('__fullname__')
const ccnumber = ref('0000-0000-0000-0000')
const month = ref('01')
const year = ref('1980')
const ccv = ref('123')

defineExpose({
    fullname,
    ccnumber,
    month,
    year,
    ccv
})

</script>

<template>
    <!-- BEGIN components/BookingPaymentForm.vue -->
    <div class="card-body">
        <h4>Dettagli di pagamento.</h4>
        <form id="BookingPaymentForm" class="row g-3">
            <div id="bpf_div1" class="col-md-9">
                <label for="bpf_name" class="form-label">Titolare</label>
                <input id="bpf_name" type="text" class="form-control" v-model="fullname" required>
            </div> <!-- bpf_div1 -->
            <div class="row no-gutters">
                <div id="bpf_div3" class="col-md-6">
                    <label for="bpf_ccnumber" class="form-label">Numero di carta di credito</label>
                    <input id="bpf_ccnumber" type="text" class="form-control" v-model="ccnumber" required>
                </div> <!-- bpf_div3 -->
            </div>
            <div class="row no-gutters">
                <div id="bpf_div4" class="col-md-3">
                    <label for="bpf_month" class="form-label">Mese</label>
                    <input id="bpf_month" type="number" class="form-control" v-model="month" required>
                </div> <!-- bpf_div4 -->
                <div id="bpf_div5" class="col-md-3">
                    <label for="bpf_year" class="form-label">Anno</label>
                    <input id="bpf_year" type="number" class="form-control" v-model="year" required>
                </div> <!-- bpf_div5 -->
                <div id="bpf_div6" class="col-md-3">
                    <label for="bpf_ccv" class="form-label">CCV</label>
                    <input id="bpf_ccv" type="number" class="form-control" v-model="ccv" required>
                </div> <!-- bpf_div6 -->
            </div>
        </form>
        {{ fullname }}
    </div>
    <!-- BEGIN components/BookingDetailsForm.vue -->
</template>