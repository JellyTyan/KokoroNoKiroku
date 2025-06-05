<template>
  <form @submit.prevent="register" class="flex flex-col space-y-4">
    <input v-model="email" type="email" placeholder="Email" required class="px-3 py-2 border rounded" />
    <input v-model="username" type="text" placeholder="Username" required class="px-3 py-2 border rounded" />
    <input v-model="password" type="password" placeholder="Пароль" required class="px-3 py-2 border rounded" />
    <button type="submit" class="px-4 py-2 bg-[#16423c] text-white rounded hover:bg-[#6a9c89] transition duration-300">Register</button>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import type { UserCredentials } from '../types/auth'

const authStore = useAuthStore()
const email = ref('')
const username = ref('')
const password = ref('')

const register = async () => {
  const credentials: UserCredentials = {
    email: email.value,
    username: username.value,
    password: password.value
  }
  
  try {
    const success = await authStore.register(credentials)
    if (success) {
      // Clear form
      email.value = ''
      username.value = ''
      password.value = ''
    }
  } catch (error) {
    console.error('Registration error:', error)
  }
}
</script>
