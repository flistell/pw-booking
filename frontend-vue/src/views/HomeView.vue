<script setup>
import ItemCard from "../components/ItemCard.vue";
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

<script>
import axios from 'axios';

export default {
    data() {
        return {
            items: []
        };
    },
    methods: {
        getItems(){
        const path = 'http://localhost:5000/resources/items'
        axios.get(path)
            .then((res) => {
                this.items = res.data;
                console.log(res.data);
            })
            .catch((error) => {
                console.error(error);
            });
        },
    },
    created(){
        this.getItems();
    }
}
</script>