<script setup>
const props = defineProps({
    brand: String,
    model: String,
    photo: String
})
</script>

<template>
    <div id="item_card_small" class="card-body">
    <!-- BEGIN components/ItemCardSmall.vue-->
        <div>
            <h2 class="card-title">{{ brand }} {{ model }}</h2>
            <img class="img-thumbnail rounded item-card-image" :src="`/public/static/images/${photo}`">
        </div>
    <!-- END components/ItemCardSmall.vue-->
    </div><!-- bw_item_card-->
</template>

<style scoped>
.img-thumbnail {
    border-color: white;
    border-width: 3px;
    border-radius: 10px !important;
    padding: 0;
}
</style>