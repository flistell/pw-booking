<script setup>
import { settings } from '@/assets/data/settings.js'
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'
import axios from 'axios';

const router = useRouter()
const bookings = ref([])

const getBookings = () => {
    const url = `${settings.resourcesUrl}/bookings`
    axios.get(
        url,
        { withCredentials: true}
        )
        .then((response) => {
            bookings.value = response.data;
            console.log(response.data);
        })
        .catch((error) => {
            console.error(error);
            if (error.status == 401){
                router.push({
                    path: '/logout'
                })  
            } else {
                router.push({
                    path: '/error/'
                })
            }
        })
    }

const activeBookingsDetailsModal = ref(false)

const booking_id = ref()

const openDetails = (id) => {
    console.log("openDetails(): " + id )
    router.push(
        `/bookings/${id}`
    )
}


onMounted(() => { getBookings() })

</script>
<template>
    <!-- BEGIN views/BookingAdmin -->
    <div class="d-flex">
        <div class="row">
            <div class="col-sm-10">
                <h1>Bookings</h1>
                <hr><br><br>
                <button type="button" class="btn btn-success btn-sm">New booking</button>
                <br><br>
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th scope="col">User</th>
                            <th scope="col">Item Id</th>
                            <th scope="col">Start</th>
                            <th scope="col">End</th>
                            <th scope="col">Status</th>
                            <th scope="col">Booked</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(booking, index) in bookings" :key="index">
                            <td>{{ booking.user_id }}</td>
                            <td>{{ booking.booked_item_id }}</td>
                            <td>{{ booking.booking_start }}</td>
                            <td>{{ booking.booking_end }}</td>
                            <td>{{ booking.booking_status }}</td>
                            <td>
                                <span v-if="!booking.booking_status > 0">No</span>
                                <span v-else>Yes</span>
                            </td>
                            <td>
                                <div class="btn-group" role="group">
                                    <button type="button" @click="openDetails(booking.id)"
                                        class="btn btn-primary btn-sm">Details</button>
                                    <button type="button" class="btn btn-warning btn-sm">Update</button>
                                    <button type="button" class="btn btn-danger btn-sm">Cancel</button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <!-- END views/BookingAdmin -->
</template>