import { myAuthStore } from '@/stores/authUserStore';

export default function authHeader() {
    const authStore = myAuthStore();
    const user = authStore.user
    console.log("auth-headers user", user)
    if (user && user.token) {
        console.log("auth-headers user.token", user.token)
        return { Authorization: `Bearer ${user.token}` };
    } else {
        return {};
    }
}