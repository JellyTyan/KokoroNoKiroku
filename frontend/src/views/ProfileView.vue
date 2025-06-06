<template>
  <div class="max-w-[1200px] mx-auto px-4 py-8">
    <!-- User Info -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8">
      <div class="flex flex-col md:flex-row gap-6 items-center md:items-start">
        <img
          :src="authStore.user?.avatar_url || '/src/assets/images/blank-profile.webp'"
          alt="Profile"
          class="w-32 h-32 rounded-full object-cover border-4 border-[#98c1ae]"
        />
        <div class="text-center md:text-left">
          <h1 class="text-3xl font-bold text-[#16423c] mb-2">{{ authStore.user?.username }}</h1>
          <p class="text-gray-600 mb-4">{{ authStore.user?.email }}</p>
          <div class="flex gap-8 justify-center md:justify-start">
            <div class="text-center">
              <span class="block text-2xl font-bold text-[#16423c]">{{ totalAnime }}</span>
              <span class="text-sm text-gray-600">Total Anime</span>
            </div>
            <div class="text-center">
              <span class="block text-2xl font-bold text-[#16423c]">{{ completed.length }}</span>
              <span class="text-sm text-gray-600">Completed</span>
            </div>
            <div class="text-center">
              <span class="block text-2xl font-bold text-[#16423c]">{{ watching.length }}</span>
              <span class="text-sm text-gray-600">Watching</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Anime Lists -->
    <div class="space-y-8">
      <!-- Planned -->
      <div class="bg-white rounded-xl shadow-md p-6">
        <h2 class="text-2xl font-bold text-[#16423c] mb-4">Planned</h2>
        <div v-if="planned.length === 0" class="text-center py-8 text-gray-500">
          List is empty
        </div>
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <AnimeCard
            v-for="anime in planned"
            :key="anime.mal_id"
            :anime="anime"
          />
        </div>
      </div>

      <!-- Watching -->
      <div class="bg-white rounded-xl shadow-md p-6">
        <h2 class="text-2xl font-bold text-[#16423c] mb-4">Watching</h2>
        <div v-if="watching.length === 0" class="text-center py-8 text-gray-500">
          List is empty
        </div>
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <AnimeCard
            v-for="anime in watching"
            :key="anime.mal_id"
            :anime="anime"
          />
        </div>
      </div>

      <!-- Completed -->
      <div class="bg-white rounded-xl shadow-md p-6">
        <h2 class="text-2xl font-bold text-[#16423c] mb-4">Completed</h2>
        <div v-if="completed.length === 0" class="text-center py-8 text-gray-500">
          List is empty
        </div>
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <AnimeCard
            v-for="anime in completed"
            :key="anime.mal_id"
            :anime="anime"
          />
        </div>
      </div>

      <!-- Dropped -->
      <div class="bg-white rounded-xl shadow-md p-6">
        <h2 class="text-2xl font-bold text-[#16423c] mb-4">Dropped</h2>
        <div v-if="dropped.length === 0" class="text-center py-8 text-gray-500">
          List is empty
        </div>
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <AnimeCard
            v-for="anime in dropped"
            :key="anime.mal_id"
            :anime="anime"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import AnimeCard from '../components/AnimeCard.vue'
import type { User } from '../types/auth'

const authStore = useAuthStore()

interface Anime {
  mal_id: number
  title: string
  thumbnail: string
  total_episodes: number
  status: string
  user_score: number | null
  user_review: string | null
  complete_episodes: number
}

const planned = ref<Anime[]>([])
const watching = ref<Anime[]>([])
const completed = ref<Anime[]>([])
const dropped = ref<Anime[]>([])

const totalAnime = computed(() => {
  return planned.value.length + watching.value.length + completed.value.length + dropped.value.length
})

const fetchAnimeList = async (status: string): Promise<Anime[]> => {
  try {
    const response = await axios.get(`/api/anime-list/${status}`, {
      withCredentials: true
    })
    return response.data
  } catch (error) {
    console.error(`Error fetching ${status} list:`, error)
    return []
  }
}

onMounted(async () => {
  planned.value = await fetchAnimeList('planned')
  watching.value = await fetchAnimeList('watching')
  completed.value = await fetchAnimeList('completed')
  dropped.value = await fetchAnimeList('dropped')
})
</script> 