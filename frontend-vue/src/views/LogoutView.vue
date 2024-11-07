<script setup>
import { myAuthStore } from '@/stores/authUserStore'
import { onMounted } from 'vue';

onMounted(() => {
    const authUserStore = myAuthStore();
    authUserStore.logout();
})
</script>

<template>
    <div>
        <h4>You have been logged out</h4>
    </div>
</template>