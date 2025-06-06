<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">Top Anime</h1>
    
    <div ref="grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
      <AnimeCard
        v-for="anime in animeList"
        :key="anime.mal_id"
        :anime="anime"
      />
    </div>

    <div v-if="loading" class="text-center mt-8">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-[#16423c] border-t-transparent"></div>
      <p class="mt-2 text-gray-600">Loading more anime...</p>
    </div>

    <div v-if="error" class="text-center mt-8 text-red-500">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'
import AnimeCard from '../components/AnimeCard.vue'

interface Anime {
  mal_id: number;
  title: string;
  images: {
    jpg: {
      large_image_url: string;
    };
  };
  score: number;
  year: number | null;
  type: string;
}

const animeList = ref<Anime[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const page = ref(1)
const hasMore = ref(true)
const grid = ref<HTMLElement | null>(null)

const fetchAnime = async () => {
  if (loading.value || !hasMore.value) return
  
  loading.value = true
  error.value = null

  try {
    const response = await axios.get(`https://api.jikan.moe/v4/top/anime?page=${page.value}`)
    const newAnime = response.data.data

    if (newAnime.length === 0) {
      hasMore.value = false
      return
    }

    animeList.value.push(...newAnime)
    page.value++
  } catch (err) {
    error.value = 'Failed to load anime. Please try again later.'
    console.error('Error fetching anime:', err)
  } finally {
    loading.value = false
  }
}

const onScroll = () => {
  if (!grid.value) return

  const { bottom } = grid.value.getBoundingClientRect()
  const windowHeight = window.innerHeight

  if (bottom < windowHeight + 200) {
    fetchAnime()
  }
}

onMounted(() => {
  fetchAnime()
  window.addEventListener('scroll', onScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
/* Можно добавить кастомные стили, если не используешь Tailwind */
</style>
