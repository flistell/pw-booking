<script setup>
import { watch, ref, onMounted } from 'vue';
import { Modal } from "bootstrap"

const props = defineProps({
    title: String,
    alertClass: String,
    btnConfirmText: String,
    btnCancelText: String,
    callback: Function
})

defineExpose({showModal, closeModal})

var thisModalObj = ref(null)

function showModal() {
    thisModalObj.value.show();
}

function closeModal() {
    thisModalObj.value.hide();
}

onMounted(async () => {
    thisModalObj.value = new Modal('#confirm-dialog', {})
    console.log("thisModalObj", thisModalObj)
})
</script>

<template>
    <!-- BEGIN components/ConfigDialog.vue-->
    <div class="modal fade" id="confirm-dialog" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
        aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-fullscreen-sm-down">
            <div class="modal-content rounded-4 shadow">
                <div :class="'modal-header alert alert-' + props.alertClass ">
                    <h5 class="modal-title">{{ props.title || 'Messaggio' }}</h5>
                    <button type="button" 
                            class="btn-close" 
                            @click="$emit('close')"
                            data-bs-dismiss="modal"
                            aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <slot>Sei sicuro di voler continuare?</slot>
                </div>
                <div class="modal-footer alert">
                    <button type="button" 
                        class="btn btn-secondary" 
                        data-bs-dismiss="modal">{{ props.btnCancelText || 'Annulla' }}</button>
                    <button type="button" 
                        @click="callback()"
                        :class="'btn btn-' + props.alertClass ">{{ props.btnConfirmText|| 'OK' }}</button>
                </div>
            </div>
        </div>
    </div>
    <!-- END components/ConfigDialog.vue-->
</template>