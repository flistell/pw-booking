<script setup>
import { storeToRefs } from 'pinia';
import { myAuthStore } from '@/stores/authUserStore'
const authUserStore = myAuthStore();
const { user } = storeToRefs(authUserStore);

</script>


<template>
    <!-- BEGIN components/Sidebar.vue -->
    <nav id="sidebar" class="navbar bg-success fixed-top" data-bs-theme="dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">SocialAuto</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas"
                data-bs-target="#offcanvasDarkNavbar" aria-controls="offcanvasDarkNavbar"
                aria-label="Toggle navigation">
                <div class="profile-pic">
                    <img :src="`https://i.pravatar.cc/50?img=${70 - user.id}`" alt="Profile Picture">
                </div>
                <font-awesome-icon :icon="['fas', 'chevron-right']" />
                <!--
                <span class="navbar-toggler-icon"></span>
                    -->
            </button>
            <div class="offcanvas offcanvas-end" data-bs-theme="light"  tabindex=" -1" id="offcanvasDarkNavbar"
                aria-labelledby="offcanvasDarkNavbarLabel">
                <div class="offcanvas-header">
                    <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">SocialAuto</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"
                        aria-label="Close"></button>
                </div>
                <div class="offcanvas-body">
                    <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                        <li class="nav-item">
                            <div class="profile-pic">
                                <img :src="`https://i.pravatar.cc/50?img=${70 - user.id}`" alt="Profile Picture">
                            </div>
                            <i>&nbsp;{{ user.username }}</i>
                        </li>
                        <li><hr></li>
                        <li><a class="dropdown-item" href="/bookings"><i class="fas fa-list-check fa-fw"></i> Gestisci
                                Prenotazioni</a></li>
                        <li><a class="dropdown-item" href="/debug"><i class="fas fa-circle-info fa-fw"></i> Account</a>
                        </li>
                        <li><hr></li>
                        <li>
                            <hr class="dropdown-divider">
                        </li>
                        <li><a class="dropdown-item" href="/logout"><i class="fas fa-sign-out-alt fa-fw"></i> Log
                                Out</a></li>
                    </ul>
                    <!--
                    <form class="d-flex mt-3" role="search">
                        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                        <button class="btn btn-success" type="submit">Search</button>
                    </form>
                -->
                </div>
            </div>
        </div>
    </nav>
    <!-- END components/Sidebar.vue -->
</template>

<style>
.sidebar {
    z-index: 500;
}

.offcanvas.offcanvas-end {
    width: 300px;
}
</style>