<template>
  <div class="max-w-[1200px] mx-auto px-4 py-8">
    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center h-[400px]">
      <div class="text-[#16423c] text-xl">Loading...</div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-12">
      <h1 class="text-6xl font-bold text-[#16423c] mb-4">404</h1>
      <p class="text-xl text-gray-600">
        Anime with ID <b>{{ $route.params.id }}</b> not found
      </p>
    </div>

    <!-- Main Content -->
    <div v-else class="flex flex-col lg:flex-row gap-8">
      <!-- Left column -->
      <div class="lg:w-1/3">
        <div class="bg-white rounded-xl shadow-md overflow-hidden">
          <img
            :src="anime?.image"
            :alt="anime?.title"
            class="w-full h-auto cursor-pointer"
            @click="openModal(anime?.large_image)"
          />
        </div>

        <div v-if="isAuthenticated" class="mt-4">
          <div v-if="!entryLoaded" class="text-center text-gray-600">Loading...</div>

          <BaseButton
            v-else-if="!userEntry"
            variant="primary"
            class="w-full"
            @click="addToList"
          >
            Add to List
          </BaseButton>

          <div v-else class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">Status:</label>
            <StatusSelect
              v-model="userEntry.status"
              @update:modelValue="(value: string) => updateStatus(value as AnimeStatus)"
            />
          </div>
        </div>

        <!-- Info blocks -->
        <div class="mt-6 space-y-4">
          <div v-if="anime?.type" class="info-block">
            <p class="text-sm font-medium text-gray-500">Format</p>
            <p class="text-base text-[#16423c]">{{ anime.type }}</p>
          </div>

          <div v-if="anime?.source" class="info-block">
            <p class="text-sm font-medium text-gray-500">Source</p>
            <p class="text-base text-[#16423c]">{{ anime.source }}</p>
          </div>

          <div v-if="anime?.status" class="info-block">
            <p class="text-sm font-medium text-gray-500">Status</p>
            <p class="text-base text-[#16423c]">{{ anime.status }}</p>
          </div>

          <div v-if="anime?.startDate" class="info-block">
            <p class="text-sm font-medium text-gray-500">Start Date</p>
            <p class="text-base text-[#16423c]">{{ formattedDate(anime.startDate) }}</p>
          </div>

          <div v-if="anime?.endDate?.year" class="info-block">
            <p class="text-sm font-medium text-gray-500">End Date</p>
            <p class="text-base text-[#16423c]">{{ formattedDate(anime.endDate) }}</p>
          </div>

          <div v-if="anime?.nextAiringEpisode" class="info-block">
            <p class="text-sm font-medium text-gray-500">Next Episode</p>
            <p class="text-base text-[#16423c]">
              {{ formatAring(anime.nextAiringEpisode.airingTime) }}
            </p>
          </div>

          <div v-if="anime?.episodeDuration" class="info-block">
            <p class="text-sm font-medium text-gray-500">Duration</p>
            <p class="text-base text-[#16423c]">{{ anime.episodeDuration }} min</p>
          </div>

          <div v-if="anime?.totalEpisodes" class="info-block">
            <p class="text-sm font-medium text-gray-500">Episodes</p>
            <p class="text-base text-[#16423c]">
              {{ anime.currentEpisode }}/{{ anime.totalEpisodes }}
            </p>
          </div>

          <div v-if="anime?.rating" class="info-block">
            <p class="text-sm font-medium text-gray-500">Rating</p>
            <p class="text-base text-[#16423c]">{{ anime.rating }}</p>
          </div>

          <div v-if="anime?.season" class="info-block">
            <p class="text-sm font-medium text-gray-500">Season</p>
            <p class="text-base text-[#16423c]">{{ anime.season }} {{ anime.year }}</p>
          </div>

          <div v-if="anime?.genres" class="info-block">
            <p class="text-sm font-medium text-gray-500">Genres</p>
            <div class="flex flex-wrap gap-2 mt-1">
              <span
                v-for="genre in anime.genres"
                :key="genre"
                class="px-2 py-1 bg-[#98c1ae] text-[#16423c] rounded-full text-sm"
              >
                {{ genre }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right column -->
      <div class="lg:w-2/3">
        <div class="bg-white rounded-xl shadow-md p-6">
          <div class="mb-6">
            <h1 class="text-3xl font-bold text-[#16423c] mb-2">{{ anime?.title }}</h1>
            <h3 v-if="anime?.title_japanese" class="text-xl text-gray-600">
              {{ anime.title_japanese }}
            </h3>
          </div>

          <div v-if="anime?.synopsis" class="prose max-w-none">
            <p class="text-gray-700">{{ anime.synopsis }}</p>
          </div>

          <div v-if="anime?.youtube_embed" class="mt-6">
            <h3 class="text-xl font-semibold text-[#16423c] mb-4">Trailer</h3>
            <div class="aspect-video">
              <iframe
                :src="anime.youtube_embed + '?autoplay=1&mute=1'"
                class="w-full h-full rounded-lg"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
              ></iframe>
            </div>
          </div>
        </div>
      </div>
    </div>

    <ImageModal :show="showImageModal" :src="selectedImage" @close="showImageModal = false" />

    <!-- Error Message -->
    <div
      v-if="errorMessage"
      class="fixed top-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg"
    >
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import ImageModal from '@/components/ImageModal.vue'
import BaseButton from '@/components/BaseButton.vue'
import StatusSelect from '@/components/StatusSelect.vue'
import { AnimeStatus, type AnimeCreate } from '@/types/anime'
import { animeApi, ApiError } from '@/utils/api'

interface DateObject {
  year: number | null
  month: number | null
  day: number | null
}

interface NextAiringEpisode {
  airingTime: number
  timeUntilAiring: number
  episode: number
}

interface Anime {
  id: number
  title: string
  title_english: string
  title_japanese: string
  image: string
  large_image: string
  youtube_embed: string
  score: string
  scored_by: string
  type: string
  source: string
  episodeDuration: number
  totalEpisodes: number
  currentEpisode: number
  status: string
  releaseDate: string
  startDate: DateObject
  endDate: DateObject
  nextAiringEpisode: NextAiringEpisode | null
  rating: string
  season: string
  year: string
  synopsis: string
  genres: string[]
}

interface Props {
  id: number
}

const props = defineProps<Props>()
const route = useRoute()
const anime = ref<Anime | null>(null)
const loading = ref(true)
const error = ref(false)
const isAuthenticated = ref(false)

const userEntry = ref<null | {
  status: AnimeStatus;
  user_score: number | null;
  user_review: string | null;
  complete_episodes: number;
}>(null)

const entryLoaded = ref(false)
const errorMessage = ref<string | null>(null)

onMounted(async () => {
  // Getting anime info
  try {
    const response = await axios.get(`/api/anime/${props.id}`)
    anime.value = response.data
  } catch (err) {
    error.value = true
    console.error('Ошибка загрузки:', err)
  } finally {
    loading.value = false
  }

  // Check Auth Status
  try {
    const response = await fetch('/users/me', {
      credentials: 'include',
    })

    isAuthenticated.value = response.ok;
  } catch (error) {
    isAuthenticated.value = false
  }

  // Check if in list
  try {
    const statuses = Object.values(AnimeStatus)

    for (const status of statuses) {
      const entries = await animeApi.getAnimeByStatus(status)
      const found = entries.find(a => a.mal_id === anime.value?.id)
      if (found) {
        userEntry.value = {
          status: found.status,
          user_score: found.user_score ?? null,
          user_review: found.user_review ?? null,
          complete_episodes: found.complete_episodes ?? 0
        }
        break
      }
    }
  } catch (error) {
    console.error('Ошибка при проверке списка:', error)
    if (error instanceof ApiError) {
      errorMessage.value = error.message
    }
  } finally {
    entryLoaded.value = true
  }
})

const showImageModal = ref(false)
const selectedImage = ref('')

const openModal = (imgUrl: string | undefined) => {
  if (imgUrl) {
    selectedImage.value = imgUrl
    showImageModal.value = true
  }
}

const formattedDate = (date: DateObject): string => {
  let formatted = ''
  if (date.day !== null) formatted += `${date.day}/`
  if (date.month !== null) formatted += `${date.month}/`
  if (date.year !== null) formatted += `${date.year}`
  return formatted
}

const formatAring = (timeAring: number): string => {
  const date = new Date(timeAring * 1000)
  return date.toLocaleDateString('en-GB', {
    year: 'numeric',
    day: 'numeric',
    month: 'numeric',
  })
}

const validateAnimeData = (data: Partial<AnimeCreate>): data is AnimeCreate => {
  const required = ['mal_id', 'title', 'thumbnail', 'total_episodes', 'status']
  for (const field of required) {
    if (!data[field as keyof AnimeCreate]) {
      throw new Error(`Отсутствует обязательное поле: ${field}`)
    }
  }

  if (!Object.values(AnimeStatus).includes(data.status as AnimeStatus)) {
    throw new Error('Некорректное значение статуса')
  }

  return true
}

const addToList = async () => {
  try {
    errorMessage.value = null

    if (!anime.value) {
      throw new Error('Данные аниме не загружены')
    }

    const animeData: AnimeCreate = {
      mal_id: anime.value.id,
      title: anime.value.title,
      thumbnail: anime.value.image,
      total_episodes: anime.value.totalEpisodes,
      status: AnimeStatus.PLANNED,
      user_score: null,
      user_review: null,
      complete_episodes: 0
    }

    const response = await animeApi.addToList(animeData)
    userEntry.value = {
      status: response.status,
      user_score: response.user_score ?? null,
      user_review: response.user_review ?? null,
      complete_episodes: response.complete_episodes ?? 0
    }
  } catch (error) {
    console.error('Ошибка при добавлении аниме:', error)
    if (error instanceof ApiError) {
      errorMessage.value = error.message
    } else {
      errorMessage.value = 'Произошла неизвестная ошибка'
    }
  }
}

const updateStatus = async (newStatus: AnimeStatus) => {
  try {
    errorMessage.value = null

    if (!userEntry.value || !anime.value) {
      throw new Error('Запись не найдена')
    }

    const response = await animeApi.updateAnime(anime.value.id, {
      status: newStatus
    })

    userEntry.value.status = response.status
  } catch (error) {
    console.error('Ошибка при обновлении статуса:', error)
    if (error instanceof ApiError) {
      errorMessage.value = error.message
    } else {
      errorMessage.value = 'Произошла неизвестная ошибка'
    }
  }
}
</script>
