<script setup>
import { defineProps } from 'vue';

const props = defineProps({
    message: String,
    link: String
})

</script>

<template>
    <!-- BEGIN components/ErrorForm.vue -->
    <div class="card-body">
        <h4 class="text-center text-danger">
            <font-awesome-icon :icon="['fas', 'skull']" />
            Errore durante l'operazione.
            <font-awesome-icon :icon="['fas', 'skull']" />
        </h4>
        <div class="row alert alert-danger justify-content-center" role="alert">
            <p class="text-center">
                {{ message }}
            </p>
            <hr>
            <p class="text-center">
                <slot></slot>
            </p>
        </div>
    </div>
    <!-- END components/ErrorForm.vue -->
</template>