<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import authHeader from '@/helpers/auth-header';
import { settings } from '@/assets/data/settings';

const data = ref()

const ping = () => {
  const url = `${settings.backendUrl}/ping`
  const payload = {
    one: 1,
    two: 2
  }
  axios.post(
    url,
    payload,
    { headers: authHeader(),
      withCredentials: true
     }
  ).then((response) => {
    console.log("response.data", response.data)
    data.value = response.data
  })

}

onMounted(() => { ping() })

</script>

<template>
  <div>
    <ul>
      <li v-for="(value, key) in data">
        {{ key }}:
        <span v-if="typeof value === 'object'">
          <ul v-for="(v2, k2) in value">
            <li>
              {{ k2 }}: {{ v2 }}
            </li>
          </ul>
        </span>
        <span v-else>
          {{ value }}
        </span>
      </li>
    </ul>
    <hr>
    {{ authHeader() }}
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
