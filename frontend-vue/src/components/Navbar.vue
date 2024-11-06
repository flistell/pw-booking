<script setup>
import { storeToRefs } from 'pinia';
import { myAuthStore } from '@/stores/authUserStore'
const authUserStore = myAuthStore();
const { user } = storeToRefs(authUserStore);

</script>

<template>
  <!-- BEGIN components/Navbar.vue -->
  <nav id="navbar" class="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">SocialAuto</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <form class="d-flex ms-auto" role="search">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
        <ul v-if="user" class="navbar-nav mr-auto mb-2 mb-lg-0">
          <li class="nav-item dropdown profile-menu">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown"
              aria-expanded="false">
              <div class="profile-pic">
                <img :src="`https://i.pravatar.cc/50?img=${user.id}`" alt="Profile Picture">
              </div>
              <!-- You can also use icon as follows: -->
              <!--  <i class="fas fa-user"></i> -->
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li class="dropdown-item"><i class="fas fa-sliders-h fa-fw"></i><i>{{ user.username }}</i></li>
              <li><a class="dropdown-item" href="/manage"><i class="fas fa-sliders-h fa-fw"></i> Gestisci
                  Prenotazioni</a></li>
              <li><a class="dropdown-item" href="#"><i class="fas fa-sliders-h fa-fw"></i> Account</a></li>
              <li><a class="dropdown-item" href="#"><i class="fas fa-cog fa-fw"></i> Settings</a></li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li><a class="dropdown-item" href="#"><i class="fas fa-sign-out-alt fa-fw"></i> Log Out</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <!-- END components/Navbar.vue -->
</template>

<style>
#navbar{
  z-index: 1000;
}

/* Profile Picture */
.profile-pic {
  display: inline-block;
  vertical-align: middle;
  width: 50px;
  height: 50px;
  overflow: hidden;
  border-radius: 50%;
}

.profile-pic img {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.profile-menu .dropdown-menu {
  right: 0;
  left: unset;
}

.profile-menu .fa-fw {
  margin-right: 10px;
}

.toggle-change::after {
  border-top: 0;
  border-bottom: 0.3em solid;
}

</style>