<script setup>
import { Form, Field } from 'vee-validate';
import * as Yup from 'yup';
import { myAuthStore } from '@/stores/authUserStore'

const schema = Yup.object().shape({
    email: Yup.string().required('Email is required'),
    password: Yup.string().required('Password is required')
});

async function onSubmit(values) {
    const authUserStore = myAuthStore();
    const { email, password } = values;
    await authUserStore.login(email, password);
}

</script>

<template>
    <!-- BEGIN LoginView.vue -->
    <div class="card m-3">
        <h4 class="card-header">Login</h4>
        <div class="card-body">
            <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }">
                <div class="form-group">
                    <label>Email</label>
                    <Field name="email" type="text" class="form-control"
                        :class="{ 'is-invalid': errors.email }" />
                    <div class="invalid-feedback">{{ errors.email }}</div>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <Field name="password" type="password" class="form-control"
                        :class="{ 'is-invalid': errors.password }" />
                    <div class="invalid-feedback">{{ errors.password }}</div>
                </div>
                <div class="form-group">
                    <button class="btn btn-primary" :disabled="isSubmitting">
                        <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
                        Login
                    </button>
                </div>
            </Form>
        </div>
    </div>
    <div class="card m-3">
        <h5 class="card-header">
            <small class="text-body-scondary">Utenti disponibili</small>
        </h5>
        <div class="card-body">
            <table class="text-secondary">
                <tr>
                    <th>Username</th>
                    <th>Password</th>
                </tr>
                <tr>
                    <td>mrossi</td>
                    <td>password01</td>
                </tr>
                <tr>
                    <td>lbianchi</td>
                    <td>password02</td>
                </tr>
                <tr>
                    <td>averdi</td>
                    <td>password03</td>
                </tr>
                <tr>
                    <td>sneri</td>
                    <td>password04</td>
                </tr>
                <tr>
                    <td>pgialli</td>
                    <td>password05</td>
                </tr>
            </table>
        </div>
    </div>
    <!-- END LoginView.vue -->
</template>