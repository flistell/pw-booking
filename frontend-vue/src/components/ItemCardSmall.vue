<script setup>
const props = defineProps({
    brand: String,
    model: String,
    photo: String
})
</script>

<template>
    <div id="item_card_small" class="card">
        <div>
            <h2 class="card-title">{{ brand }} {{ model }}</h2>
            <img class="img-thumbnail item-card-image" :src="`/public/static/images/${photo}`">
        </div>

    </div><!-- bw_item_card-->
</template>