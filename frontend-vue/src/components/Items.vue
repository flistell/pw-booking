<template>
    <div class="container">
        <div class="row">
            <div class="col-sm-10">
                <h1>Cars</h1>
                <hr><br><br>
                <button type="button" class="btn btn-success btn-sm">Add Book</button>
                <br><br>
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th scope="col">Brand</th>
                            <th scope="col">Model</th>
                            <th scope="col">HP</th>
                            <th scope="col">CO<sup>2</sup></th>
                            <th scope="col">Photo</th>
                            <th scope="col">Available</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in items" :key="index">
                            <td>{{ item.item_details.brand }}</td>
                            <td>{{ item.item_details.model }}</td>
                            <td>{{ item.item_details.horsepower }}</td>
                            <td>{{ item.item_details.emission }}</td>
                            <td>{{ item.item_details.photo }}</td>
                            <td>
                                <span v-if="item.booked">No</span>
                                <span v-else>Yes</span>
                            </td>
                            <td>
                                <div class="btn-group" role="group">
                                    <button type="button" class="btn btn-warning btn-sm">Reserve</button>
                                    <button type="button" class="btn btn-danger btn-sm">Delete</button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
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
                .then((res) => {
                    for (var i = 0; i < this.items.length; i++) {
                        const items_base = 'http://localhost:5000/resources/items/'
                        axios.get(items_base + '/' + this.items[i].id + '?is_available')
                            .then((ava) => {
                                console.log(ava)
                                this.items[i].available = ava.data.available
                            })
                    }
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