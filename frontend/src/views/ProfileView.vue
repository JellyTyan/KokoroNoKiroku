<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
      <h1 class="text-2xl font-bold mb-6">Profile</h1>
      
      <div v-if="authStore.user" class="space-y-4">
        <div class="flex items-center space-x-4">
          <img
            :src="authStore.user.avatar_url || '/src/assets/images/blank-profile.webp'"
            alt="Profile"
            class="w-20 h-20 rounded-full object-cover border-2 border-[#6a9c89]"
          />
          <div>
            <h2 class="text-xl font-semibold">{{ authStore.user.username }}</h2>
            <p class="text-gray-600">{{ authStore.user.email }}</p>
          </div>
        </div>

        <div class="border-t pt-4">
          <h3 class="text-lg font-semibold mb-2">Account Information</h3>
          <div class="space-y-2">
            <p><span class="font-medium">Email:</span> {{ authStore.user.email }}</p>
            <p><span class="font-medium">Username:</span> {{ authStore.user.username }}</p>
            <p><span class="font-medium">Account Status:</span> {{ authStore.user.is_active ? 'Active' : 'Inactive' }}</p>
            <p><span class="font-medium">Email Verified:</span> {{ authStore.user.is_verified ? 'Yes' : 'No' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
</script> 