<script setup>
import { watch, ref, onMounted } from 'vue';
import { Modal } from "bootstrap"

const props = defineProps({
    title: String,
    'alert-class': String,
    'btn-confirm-text': String,
    'btn-cancel-text': String,
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


console.log("props: ", props)

</script>

<template>
    <!-- BEGIN components/ConfigDialog.vue-->
    <div class="modal fade" 
        id="confirm-dialog"
        data-bs-backdrop="static" 
        data-bs-keyboard="false" 
        tabindex="-1" 
        aria-labelledby="staticBackdropLabel" 
        aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Modal title</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>Modal body text goes here.</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary">Save changes</button>
                </div>
            </div>
        </div>
    </div>
    <!-- END components/ConfigDialog.vue-->
</template>