<script setup>
import axios from 'axios';
import Datepicker from 'vue3-datepicker'
import { ref } from 'vue'
</script>

<template>
    <div>
        <div class="row align-items-start">
            <!-- About Hotel -->
            <div class="col-lg-8 mb-3 mb-lg-0">
                <div class="card shadow">
                    <h1 class="mb-3">{{ item.item_details.brand }} {{ item.item_details.model }}</h1>
                    <img class="img-thumbnail item-card-image" :src="`/public/static/images/${ item.item_details.photo }`">
                    <hr>

                    <!-- Location -->
                    <section>
                        <div class="d-flex flex-wrap align-items-center mb-2">
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
                                    {{ item.item_details.fuel }}
                                </span>
                            </div>
                        </div>
                        <div>
                            <i class="fas fas-location-dot mr-2 text-primary"></i>
                            " {{ item.item_details.location }} "
                        </div>
                    </section>

                    <hr>

                    <!-- desc -->
                    <div class="mt-4">
                        <p>
                        {{ item.item_details.description }}
                        </p>
                    </div>

                    <hr>

                    <!-- Book -->
                    <div class="col-lg-4 sticky p-lg-0">
                        <div class="card shadow">
                            <div class="d-flex justify-content-between align-items-end flex-wrap">
                                <h2 class="mb-0">Book Now</h2>
                                <span v-if="totalPrice > 0">
                                    Total: {{ totalPrice }} $
                                </span>
                            </div>
                            <hr>

                            <Datepicker v-model="selected" :locale="locale" :upperLimit="to" :lowerLimit="from"
                                :clearable="true" />

                            <div class="d-flex justify-content-between">
                                <!-- book -->
                                <button type="button" class="btn btn-primary" @click="book()">
                                    Prenota ora
                                </button>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            item: []
        };
    },
    methods: {
        getItem(id) {
            console.log("getItem(" + id + ")")
            const path = 'http://localhost:5000/resources/items/' + id;
            axios.get(path)

                .then((res) => {
                    this.item = res.data;
                    console.log(res.data);
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created() {
        const itemId = this.$route.params.id;
        this.getItem(itemId);
    }
}
</script>