import { defineStore } from 'pinia';
import axios from 'axios'
import { router } from '@/router';
import { settings } from '@/assets/data/settings.js'

const baseUrl = `${settings.backendUrl}`;


export const myAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        user: JSON.parse(localStorage.getItem('user')),
        returnUrl: null
    }),
    actions: {
        login(email, password) {
            axios
                .post( 
                    `${baseUrl}/login/jwt`, 
                    { 
                        'email': email,
                        'password': password
                    },
                    { withCredentials: true }
                )
                .then((response) => {
                    console.log(response)
                    this.user = response.data;
                    localStorage.setItem('user', JSON.stringify(this.user));
                    router.push(this.returnUrl || '/');
                })
                .catch((error) =>  {
                    console.error(error);
                    router.push(this.errorUrl);
                });
        },
        logout() {
            this.user = null;
            localStorage.removeItem('user');
            router.push('/logout');
        }
    }
});