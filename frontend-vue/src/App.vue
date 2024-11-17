<script setup>
import { RouterView } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
</script>

<template>
  <div id="app" class="app">
    <div class="container">
      <Sidebar/>
      <RouterView />
    </div>
  </div>
</template>


<style scoped>
#app {
  margin-top: 60px
}


header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}


</style>
