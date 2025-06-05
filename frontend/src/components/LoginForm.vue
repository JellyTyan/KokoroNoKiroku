<template>
  <form @submit.prevent="login" class="flex flex-col space-y-4">
    <input v-model="usernameOrEmail" type="text" placeholder="Username or Email" required class="px-3 py-2 border rounded" />
    <input v-model="password" type="password" placeholder="Пароль" required class="px-3 py-2 border rounded" />
    <button type="submit" class="px-4 py-2 bg-[#16423c] text-white rounded hover:bg-[#6a9c89] transition duration-300">Войти</button>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import type { UserCredentials } from '../types/auth'

const authStore = useAuthStore()
const usernameOrEmail = ref('')
const password = ref('')

const login = async () => {
  const credentials: UserCredentials = {
    email: usernameOrEmail.value,
    username: usernameOrEmail.value,
    password: password.value
  }
  
  try {
    const success = await authStore.login(credentials)
    if (success) {
      // Clear form
      usernameOrEmail.value = ''
      password.value = ''
    }
  } catch (error) {
    console.error('Login error:', error)
  }
}
</script>
