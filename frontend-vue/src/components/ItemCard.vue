<script setup>
import ItemCardSmall from '../components/ItemCardSmall.vue'

const props = defineProps(['item'])
// console.log("ItemCard props", props.item)
</script>

<template>
    <!-- BEGIN components/ItemCard.vue-->
    <div class="card item-card shadow-sm" no-body>
        <div class="row no-gutters">
            <div class="col-md-4 col-lg-3 p-2">
                <a id="itemcardlink" :href="`/items/${item.id}`">
                <ItemCardSmall :brand="item.item_details.brand" :model="item.item_details.model"
                    :photo="item.item_details.photo" />
                </a>
            </div>
            <div class="col-md-8 col-lg-9">
                <div class="card-body d-flex flex-column h-100">
                    <div class="d-flex justify-content-between align-items-center">
                        <h4 class="card-title">{{ item.name }}</h4>
                    </div>
                    <div class="d-flex flex-wrap align-items-center mb-2">
                        <i class="fas fa-map-marker-alt mr-2 text-primary"></i>
                        <!-- city -->
                        <span class="text-body-secondary">&nbsp;{{ item.city }}</span>
                        <span class="mx-2">&#8226;</span>
                        <span class="text-body-secondary">{{ item.country }}</span>
                    </div>

                    <!-- features -->
                    <div class="d-flex flex-wrap gap-1 mb-3 flex-1">
                        <div>
                            <!-- HP -->
                            <font-awesome-icon icon="fa-solid fa-car" />
                            <span class="mx-1"></span>
                            <span class="text-body-secondary">
                                {{ item.item_details.horsepower }} Kw
                            </span>
                        </div>
                        <span class="mx-2">&#8226;</span>
                        <div>
                            <!-- CO^2 -->
                            <font-awesome-icon icon="fa-solid fa-smog" />
                            <span class="mx-1"></span>
                            <span class="text-body-secondary">
                                {{ item.item_details.emission }} CO<sub>2</sub> g/Km
                            </span>
                        </div>
                        <span class="mx-2">&#8226;</span>
                        <div>
                            <!-- CO^2 -->
                            <font-awesome-icon icon="fa-solid fa-gas-pump" />
                            <span class="mx-1"></span>
                            <span class="text-body-secondary">
                                {{ item.item_details.fuel_consumption }} l/100Km
                            </span>
                        </div>
                    </div>
                    <hr class="w-100">

                    <div class="d-flex justify-content-between align-items-center">
                        {{ item.item_details.brand }} {{ item.item_details.model }}
                    </div>

                    <div class="d-flex justify-content-between align-items-center">
                        <span class="font-1h">{{ item.item_price_weight }} crediti</span>
                        <a type="button" class="btn btn-primary" :href="`/items/${item.id}`">Dettagli</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- END components/ItemCard.vue-->
</template>

<style>
#itemcardlink {
    text-decoration: none;
}
</style>