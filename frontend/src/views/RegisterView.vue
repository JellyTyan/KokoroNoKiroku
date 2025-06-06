<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-bold text-[#16423c]">Create your account</h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Or
          <router-link to="/login" class="font-medium text-[#98c1ae] hover:text-[#16423c]">
            sign in to your account
          </router-link>
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div class="rounded-md shadow-sm space-y-4">
          <div>
            <label for="username" class="sr-only">Username</label>
            <input
              id="username"
              v-model="username"
              name="username"
              type="text"
              required
              class="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-[#98c1ae] focus:border-[#16423c] focus:z-10 sm:text-sm"
              placeholder="Username"
            />
          </div>
          <div>
            <label for="email" class="sr-only">Email address</label>
            <input
              id="email"
              v-model="email"
              name="email"
              type="email"
              required
              class="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-[#98c1ae] focus:border-[#16423c] focus:z-10 sm:text-sm"
              placeholder="Email address"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              v-model="password"
              name="password"
              type="password"
              required
              class="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-[#98c1ae] focus:border-[#16423c] focus:z-10 sm:text-sm"
              placeholder="Password"
            />
          </div>
          <div>
            <label for="confirm-password" class="sr-only">Confirm password</label>
            <input
              id="confirm-password"
              v-model="confirmPassword"
              name="confirm-password"
              type="password"
              required
              class="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-[#98c1ae] focus:border-[#16423c] focus:z-10 sm:text-sm"
              placeholder="Confirm password"
            />
          </div>
        </div>

        <div>
          <BaseButton
            type="submit"
            variant="primary"
            class="w-full"
            :disabled="loading || !isFormValid"
          >
            <span v-if="loading">Creating account...</span>
            <span v-else>Create account</span>
          </BaseButton>
        </div>
      </form>

      <!-- Error Message -->
      <div
        v-if="error"
        class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm"
      >
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import BaseButton from '../components/BaseButton.vue'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')

const isFormValid = computed(() => {
  return (
    username.value.length >= 3 &&
    email.value.includes('@') &&
    password.value.length >= 6 &&
    password.value === confirmPassword.value
  )
})

const handleSubmit = async () => {
  if (!isFormValid.value) {
    error.value = 'Please fill in all fields correctly'
    return
  }

  try {
    loading.value = true
    error.value = ''
    await authStore.register({ username: username.value, email: email.value, password: password.value })
    router.push('/')
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to create account'
  } finally {
    loading.value = false
  }
}
</script>
