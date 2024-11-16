<script setup>
import { storeToRefs } from 'pinia';
import { myAuthStore } from '@/stores/authUserStore'
const authUserStore = myAuthStore();
const { user } = storeToRefs(authUserStore);

</script>


<template>
    <!-- BEGIN components/Sidebar.vue -->
    <nav id="sidebar" class="navbar navbar-expand-lg bg-success fixed-top" data-bs-theme="dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <font-awesome-icon :icon="['fas', 'house']" />&nbsp;SocialAuto
            </a>
            <button v-if="user" class="navbar-toggler" type="button" data-bs-toggle="offcanvas"
                data-bs-target="#offcanvasDarkNavbar" aria-controls="offcanvasDarkNavbar"
                aria-label="Toggle navigation">
                <div class="profile-pic">
                    <img :src="`https://i.pravatar.cc/40?img=${70 - user.id}`" alt="Profile Picture">
                </div>
                <font-awesome-icon :icon="['fas', 'chevron-right']" />
                <!--
                <span class="navbar-toggler-icon"></span>
                    -->
            </button>
            <div v-if="user" if="offcanvas1" class="offcanvas offcanvas-end" data-bs-theme="dark" tabindex=" -1"
                id="offcanvasDarkNavbar" aria-labelledby="offcanvasDarkNavbarLabel">
                <div class="offcanvas-header">
                    <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">SocialAuto</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"
                        aria-label="Close"></button>
                </div>
                <div class="offcanvas-body">

                    <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                        <li class="nav-item">
                            <a class="nav-link pb-0">
                                <div class="profile-pic">
                                    <img :src="`https://i.pravatar.cc/50?img=${70 - user.id}`" alt="Profile Picture">
                                </div>
                                <i>&nbsp;{{ user.username }}</i>
                            </a>
                        </li>
                        <li>
                            <hr>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="/bookings"><i class="fas fa-list-check fa-fw"></i> Gestisci Prenotazioni</a>
                        </li>
                        <!--
                        <li><a class="nav-link active" href="/debug"><i class="fas fa-circle-info fa-fw"></i> Account</a>
                        </li>
                    -->
                        <li>
                            <hr>
                        </li>
                        <li>
                            <hr class="dropdown-divider">
                        </li>
                        <li><a class="nav-link active" href="/logout"><i class="fas fa-sign-out-alt fa-fw"></i> Log Out</a></li>
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

.offcanvas {
    background-color: #006335;
}
.sidebar {
    z-index: 500;
}

.offcanvas.offcanvas-end {
    width: 300px;
}

/* Profile Picture */
.profile-pic {
    display: inline-block;
    vertical-align: middle;
    width: 30px;
    height: 30px;
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
</style>