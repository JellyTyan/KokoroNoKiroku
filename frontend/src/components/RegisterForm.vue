<template>
  <form @submit.prevent="register">
    <input v-model="email" type="email" placeholder="Email" required />
    <input v-model="password" type="password" placeholder="Пароль" required />
    <button type="submit">Register</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')

const register = () => {
  console.log('Авторизация:', email.value, password.value)
}
</script>
