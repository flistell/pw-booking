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
                            <th scope="col">Start Date</th>
                            <th scope="col">End Date</th>
                            <th scope="col">Status</th>
                            <th scope="col">Pick-up Location<sup>2</sup></th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in bookings" :key="index">
                            <td>{{ item.booking_start }}</td>
                            <td>{{ item.booking_end }}</td>
                            <td>{{ item.booking_status }}</td>
                            <td>{{ item.delivery_address_id }}</td>
                            <td>
                                <div class="btn-group" role="group">
                                    <button type="button" class="btn btn-warning btn-sm"">Modify</button>
                                    <button type="button" class="btn btn-danger btn-sm">Cancel</button>
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
            const path = 'http://localhost:5000/resources/bookings'
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