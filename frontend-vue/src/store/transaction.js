import { defineStore } from 'pinia';

export const txStore = defineStore('tx', {
    state: () => ({
        tx: [{
            userId: null,
        }
        ]

    })
})