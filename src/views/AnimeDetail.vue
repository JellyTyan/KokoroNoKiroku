<template>
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
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import ImageModal from '@/components/ImageModal.vue'

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

const route = useRoute()
const anime = ref<Anime | null>(null)
const loading = ref(true)
const error = ref(false)

onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/api/anime/${route.params.id}`)
    anime.value = response.data
  } catch (err) {
    error.value = true
    console.error('Ошибка загрузки:', err)
  } finally {
    loading.value = false
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
</style>
