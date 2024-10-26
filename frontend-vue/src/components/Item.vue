<script setup>
import Datepicker from 'vue3-datepicker'
import { ref } from 'vue'
//const date_from = defineModel('date_from', { default: new Date()})
//const date_to = defineModel('date_to', { default: new Date()})
const today = ref(new Date());
</script>

<template>
    <div id="item_main">
        <div id="item_row" class="row align-items-start">
            <div id="item_col" class="col-lg-8 mb-3 mb-lg-0">
                <div id="item_card" class="card shadow">
                    <h1 class="mb-3">{{ item.item_details.brand }} {{ item.item_details.model }}</h1>
                    <img class="img-thumbnail item-card-image"
                        :src="`/public/static/images/${item.item_details.photo}`">
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
                                    {{ item.item_details.fuel_consumption }}
                                </span>
                            </div>
                        </div>
                        <div>
                            <i class="fas fas-location-dot mr-2 text-primary"></i>
                            {{ item.zip }} {{ item.city }}
                        </div>
                    </section>

                    <hr>

                    <div id="description" class="mt-4">
                        <p>
                            {{ item.item_details.description }}
                        </p>
                    </div> <!-- id="description" -->
                </div><!--id="item_card" -->
            </div> <!-- id="item_col" -->


            <div id="book_col" class="col-lg-4 sticky p-lg-0">
                <div id="book_main" class="card shadow">
                    <div class="d-flex justify-content-between align-items-end flex-wrap">
                        <h2 class="mb-0">Prenota Ora</h2>
                        <span v-if="creditsCost > 0">
                            Costo: {{ creditsCost }} $
                        </span>
                    </div>
                    <hr>
                    <fieldset>
                        <legend>Data inizio</legend>
                        <Datepicker 
                            id="datepicker_from" 
                            v-model="date_from" 
                            :clearable="true"
                            :lowerLimit="today"
                        />
                    </fieldset>
                    <fieldset>
                        <legend>Data fine</legend>
                        <Datepicker 
                            id="datepicker_to" 
                            v-model="date_to" 
                            :clearable="true" 
                            :lowerLimit="date_from"
                        />
                    </fieldset>
                    <hr>

                    <div id="book_action" class="d-flex justify-content-between">
                        <button type="button" class="btn btn-primary" @click="book_it()">
                            Prenota ora
                        </button>
                    </div>

                </div> <!-- id="book_main" -->
            </div><!-- id="book_col"-->
        </div> <!-- id="item_row" -->
    </div> <!--id="item_main" -->
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            item: {
                item_details: {}
            },
            date_to: new Date(),
            date_from: new Date(),
            creditsCost: 0
        };
    },
    methods: {
        getItem() {
            const id = this.$route.params.id;
            console.log("getItem(" + id + ")")
            const url = 'http://localhost:5000/resources/items/' + id;
            axios
                .get(url)
                .then((response) => {
                    console.log(response);
                    this.item = response.data;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        book_it() {
            console.log("book_it()")
            console.log(this.item.id)
            console.log(this.date_from)
            console.log(this.date_to)
            console.log(this.item.item_details)
            this.$router.push({
                name: "BookingWizard",
                query: {
                    from: this.date_from.getTime(), 
                    to: this.date_to.getTime(), 
                    id: this.item.id,
                    brand: this.item.item_details.brand,
                    model: this.item.item_details.model,
                    image: this.item.item_details.photo
                }
            })
        }
    },
    created() {
        this.getItem();
    }
}
</script>