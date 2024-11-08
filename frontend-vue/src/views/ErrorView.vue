<script setup>
import ErrorForm from '@/components/ErrorForm.vue';
const props = defineProps({
    message: String
})
</script>

<template>
    <div>
        <ErrorForm message="Errore generico">
            Torna alla <a href="/">pagina iniziale</a> e riprova.
        </ErrorForm>
    </div>
</template>