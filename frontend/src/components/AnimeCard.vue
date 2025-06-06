<template>
  <router-link :to="`/anime/${anime.mal_id}`" class="block">
    <div class="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <div class="relative">
        <img
          :src="anime.images.jpg.large_image_url"
          :alt="anime.title"
          class="w-full h-[300px] object-cover"
        />
        <div class="absolute top-2 right-2 bg-[#16423c] text-white px-2 py-1 rounded">
          {{ anime.score }}
        </div>
      </div>
      <div class="p-4">
        <h3 class="font-semibold text-lg mb-2 line-clamp-2">{{ anime.title }}</h3>
        <div class="flex items-center text-sm text-gray-600">
          <span class="material-icons text-sm mr-1">calendar_today</span>
          {{ anime.year || 'TBA' }}
        </div>
        <div class="flex items-center text-sm text-gray-600 mt-1">
          <span class="material-icons text-sm mr-1">movie</span>
          {{ anime.type }}
        </div>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
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

defineProps<{
  anime: Anime;
}>();
</script> 