<template>
  <div class="anime-detail">
    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center h-full py-12">
      <div class="font-f">Loading moe...</div>
    </div>

    <!-- Error -->
    <div
      v-else-if="error"
      class="flex flex-col items-center text-center max-w-[1200px] mx-auto p-8 my-12"
    >
      <h1 class="text-6xl font-bold mb-4">404 Nya~</h1>
      <p class="text-2xl">
        Anime with ID <b>{{ $route.params.id }}</b> not found (╥_╥)
      </p>
    </div>

    <!-- Main Content -->
    <div v-else class="flex flex-row gap-8 justify-center max-w-[1200px] mx-auto mt-8">
      <div class="flex flex-row gap-8">
        <!-- Left column -->
        <div class="flex flex-col gap-4">
          <div id="poster-block" class="flex flex-col text-center items-center">
            <img
              :src="anime?.image"
              id="poster"
              alt="Poster"
              @click="openModal(anime?.large_image)"
            />

            <ImageModal :show="showImageModal" :src="selectedImage" @close="showImageModal = false" />
          </div>

          <div v-if="isAuthenticated" class="flex justify-center">
            <div v-if="!entryLoaded">Загрузка...</div>

            <!-- Если аниме не добавлено -->
            <button
              v-else-if="!userEntry"
              @click="addToList"
              class="bg-emerald-600 p-[10px] rounded-[10px]"
            >
              Добавить в список
            </button>

            <!-- Если аниме уже есть — показать select -->
            <div v-else>
              <label for="status">Статус:</label>
              <select
                id="status"
                v-model="userEntry.status"
                @change="updateStatus(userEntry.status)"
                class="border border-gray-300 rounded px-2 py-1"
              >
                <option :value="AnimeStatus.PLANNED">Запланировано</option>
                <option :value="AnimeStatus.WATCHED">Смотрю</option>
                <option :value="AnimeStatus.COMPLETED">Просмотрено</option>
              </select>
            </div>
          </div>

          <!-- Info blocks -->
          <div class="info-block">
            <p class="category-name">Format</p>
            <p class="category-description">{{ anime!.type }}</p>
          </div>

          <div v-if="anime?.source" class="info-block">
            <p class="category-name">Source</p>
            <p class="category-description">{{ anime.source }}</p>
          </div>

          <div v-if="anime?.status" class="info-block">
            <p class="category-name">Status</p>
            <p class="category-description">{{ anime.status }}</p>
          </div>

          <div v-if="anime?.startDate" class="info-block">
            <p class="category-name">Start Date</p>
            <p class="category-description">{{ formattedDate(anime.startDate) }}</p>
          </div>

          <div v-if="anime?.endDate?.year" class="info-block">
            <p class="category-name">End Date</p>
            <p class="category-description">{{ formattedDate(anime.endDate) }}</p>
          </div>

          <div v-if="anime?.nextAiringEpisode" class="info-block">
            <p class="category-name">Next episode</p>
            <p class="category-description">
              {{ formatAring(anime.nextAiringEpisode.airingTime) }}
            </p>
          </div>

          <div v-if="anime?.episodeDuration" class="info-block">
            <p class="category-name">Duration</p>
            <p class="category-description">{{ anime.episodeDuration }}</p>
          </div>

          <div v-if="anime?.totalEpisodes" class="info-block">
            <p class="category-name">Current/Total Episodes</p>
            <p class="category-description">
              {{ anime.currentEpisode + '/' + anime.totalEpisodes }}
            </p>
          </div>

          <div v-if="anime?.rating" class="info-block">
            <p class="category-name">Rating</p>
            <p class="category-description">{{ anime.rating }}</p>
          </div>

          <div v-if="anime?.season" class="info-block">
            <p class="category-name">Season</p>
            <p class="category-description">{{ anime.season + ' ' + anime.year }}</p>
          </div>

          <div v-if="anime?.genres" class="info-block" id="anime-genres">
            <p class="category-name">Genres</p>
            <span
              class="category-description"
              v-for="genre in anime.genres"
              :key="genre"
              :id="'genre-' + genre.toLowerCase().replace(/\\s+/g, '-')"
            >
              {{ genre }}
            </span>
          </div>
        </div>

        <!-- Right column -->
        <div class="overview">
          <div class="anime-titles">
            <h1 id="anime-title-en" class="title text-3xl">{{ anime?.title }}</h1>
            <h3 v-if="anime?.title_japanese" id="anime-title-jp" class="title">
              {{ anime.title_japanese }}
            </h3>
          </div>

          <div v-if="anime?.synopsis" class="synopsis">
            <p v-html="anime.synopsis"></p>
          </div>

          <div v-if="anime?.youtube_embed" class="trailer">
            <h3>Trailer</h3>
            <iframe
              :src="anime.youtube_embed + '?autoplay=1&mute=1'"
              frameborder="0"
              width="380"
              height="214"
            ></iframe>
          </div>
        </div>
      </div>
    </div>

    <!-- Добавляем отображение ошибок -->
    <div v-if="errorMessage" class="fixed top-4 right-4 bg-red-500 text-white p-4 rounded shadow-lg">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import ImageModal from '@/components/ImageModal.vue'
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

<style scoped lang="scss">
@media (max-width: 768px) {
  #anime-top-info {
    flex-direction: column !important;

    .overview {
      margin-left: 0 !important;
      margin-top: 2rem;
    }
  }

  .poster {
    width: 200px !important;
  }
}

.info-block {
  display: flex;
  flex-direction: column;

  p:first-child {
    font-weight: bold;
    margin-bottom: 0.25rem;
  }

  .category-name {
    margin: 0;
  }

  .category-description {
    margin: 0;
    color: grey;
  }
}

#poster-block {
  margin-bottom: 1rem;

  #poster {
    cursor: pointer;
    transition: transform 0.3s;

    &:hover {
      transform: scale(1.05);
      box-shadow: 0 0 20px rgba(0, 255, 157, 0.5);
    }
  }
}

.overview {
  flex: 1;
  font-size: 1rem;
  line-height: 1.5;
  margin-left: 2rem;

  .anime-titles {
    .title {
      color: #ff69b4;
      text-shadow: 0 0 10px rgba(255, 105, 180, 0.5);
      margin: 0.5rem 0;
      line-height: 70%;
    }
  }

  .trailer {
    margin-top: 40px;
  }
}

.anime-detail {
  min-height: 100vh;
  padding: 2rem 0;
}
</style>
