<script setup>
import { myAuthStore } from '@/stores/authUserStore'
import { onMounted } from 'vue';

console.log("LogoutView")

onMounted(() => {
    const authUserStore = myAuthStore();
    authUserStore.logout();
})
</script>

<template>
    <!-- BEGIN views/LogoutView.vue -->
    <h1 class="d-flex justify-content-center">Ciao!</h1>
    <div class="row row-cols-1 alert alert-info align-items-center justify-content-center" role="alert">
        <div class="col">
            <p class="text-center">
            <i class="fa-solid fa-circle-info"></i>
            La tua sessione è stata scollegata.
            <i class="fa-solid fa-circle-info"></i>
            </p>
            <br>
            <p class="text-center">
            Torna a trovarci presto!
            </p>
            <hr>
            <p class="text-center">
            O anche <a href="/">subito</a> :)
            </p>
        </div>
    </div>
    <!-- END views/LogoutView.vue -->
</template>