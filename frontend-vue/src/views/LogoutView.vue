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
    <div class="row row-cols-2 alert alert-info align-items-center justify-content-center" role="alert">
        <div class="col-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2"
                viewBox="0 0 16 16" role="img" aria-label="Info:">
                <path
                    d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z" />
            </svg>
        </div>
        <div class="col-4">
            La tua sessione è stata scollegata.
            <br>
            Torna a trovarci presto! 
            <hr>
            O anche <a href="/">subito</a> :)
        </div>
    </div>
    <!-- END views/LogoutView.vue -->
</template>