<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import ItemCard from "../components/ItemCard.vue";
import { settings } from '@/assets/data/settings.js'

const items = ref([])

const getItems = () => {
    const path = `${settings.backendUrl}/resources/items`
    axios.get(path)
        .then((res) => {
            items.value = res.data;
            // console.log(res.data);
        })
        .catch((error) => {
            console.error(error);
        });
}

onMounted(() => {getItems()})
</script>

<template>
    <section>
        <ItemCard 
            v-for="(item, index) in items" 
            :key="index" 
            :item="item" 
            class="mb-3"
            />
    </section>
</template>