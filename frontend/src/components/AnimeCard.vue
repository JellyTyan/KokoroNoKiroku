<template>
  <router-link :to="`/anime/${anime.mal_id}`" class="block">
    <div class="anime-card bg-white rounded-xl shadow-md overflow-hidden transition-transform duration-200 hover:scale-105">
      <img
        :src="anime.images?.jpg?.large_image_url || anime.thumbnail"
        :alt="anime.title"
        class="w-full h-[280px] object-cover"
      />
      <div class="p-4">
        <h3 class="text-lg font-semibold text-[#16423c] mb-2 line-clamp-2">{{ anime.title }}</h3>
        <div class="flex justify-between items-center text-sm text-gray-600">
          <span>{{ anime.type }}</span>
          <span v-if="anime.score" class="flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
            {{ anime.score }}
          </span>
        </div>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
interface Anime {
  mal_id: number
  title: string
  images?: {
    jpg?: {
      large_image_url: string
    }
  }
  thumbnail?: string
  type?: string
  score?: number
}

defineProps<{
  anime: Anime
}>()
</script> 