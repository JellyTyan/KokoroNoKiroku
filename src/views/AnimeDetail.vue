<template>
  <div v-if="loading" class="loading">
    <div class="loader">Loading moe...</div>
  </div>

  <div v-else-if="error" class="error">
    <h2>404 Nya~</h2>
    <p>Anime with ID {{ $route.params.id }} not found (╥_╥)</p>
  </div>

  <div v-else id="anime-detail" class="anime-detail">
    <div id="anime-content" class="content">
      <div id="anime-top-info" class="top-info">
        <div id="anime-info" class="info">
          <div id="poster-block" class="poster-block">
            <img
              :src="anime?.image"
              alt="Постер"
              class="poster"
              @click="openModal(anime?.large_image)"
            />

            <ImageModal
              :show="showImageModal"
              :src="selectedImage"
              @close="showImageModal = false"
            />
          </div>

          <div id="anime-format" class="info-block">
            <p>Format</p>
            <p class="description">{{ anime!.type }}</p>
          </div>

          <div id="anime-source" v-if="anime?.source" class="info-block">
            <p>Source</p>
            <p class="description">{{ anime?.source }}</p>
          </div>

          <div id="anime-status" v-if="anime?.status" class="info-block">
            <p>Status</p>
            <p class="description">{{ anime?.status }}</p>
          </div>

          <div v-if="anime?.startDate" class="info-block">
            <p>Start Date</p>
            <p class="description">{{ formattedDate(anime.startDate) }}</p>
          </div>

          <div v-if="anime?.endDate?.year" class="info-block">
            <p>End Date</p>
            <p class="description">{{ formattedDate(anime.endDate) }}</p>
          </div>

          <div v-if="anime?.nextAiringEpisode" class="info-block">
            <p>Next episode</p>
            <p class="description">{{ formatAring(anime?.nextAiringEpisode?.airingTime) }}</p>
          </div>

          <div id="anime-episodes" v-if="anime?.episodeDuration" class="info-block">
            <p>Duration</p>
            <p class="description">{{ anime?.episodeDuration }}</p>
          </div>

          <div id="anime-episodes" v-if="anime?.totalEpisodes" class="info-block">
            <p>Current/Total Episodes</p>
            <p class="description">{{ anime?.currentEpisode + '/' + anime?.totalEpisodes }}</p>
          </div>

          <div id="anime-rating" v-if="anime?.rating" class="info-block">
            <p>Rating</p>
            <p class="description">{{ anime?.rating }}</p>
          </div>

          <div id="anime-season" v-if="anime?.season" class="info-block">
            <p>Season</p>
            <p class="description">{{ anime?.season + ' ' + anime?.year }}</p>
          </div>

          <div id="anime-genres" v-if="anime?.genres" class="info-block">
            <p>Genres</p>
            <span
              class="tag"
              v-for="genre in anime?.genres"
              :key="genre"
              :id="'genre-' + genre.toLowerCase().replace(/\\s+/g, '-')"
            >
              {{ genre }}
            </span>
          </div>
        </div>
        <div class="overview">
          <div class="anime-titles">
            <h1 id="anime-title-en" class="title">{{ anime?.title }}</h1>
            <h3 v-if="anime?.title_japanese" id="anime-title-jp" class="title">
              {{ anime?.title_japanese }}
            </h3>
          </div>
          <div v-if="anime?.synopsis" class="synopsis">
            <p v-html="anime?.synopsis"></p>
          </div>
          <div v-if="anime?.youtube_embed" class="trailer">
            <h3>Trailer</h3>
            <iframe
              :src="anime?.youtube_embed ? anime.youtube_embed + '?autoplay=1&mute=1' : undefined"
              frameborder=""
              width="380"
              height="214"
            ></iframe>
          </div>
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
  const date: Date = new Date(timeAring * 1000)
  const formattedDate: string = date.toLocaleDateString('en-GB', {
    year: 'numeric',
    day: 'numeric',
    month: 'numeric',
  })
  return formattedDate
}
</script>

<style lang="scss" scoped>
.loading {
  height: 50vh;
  display: grid;
  place-items: center;
  flex: 1;
}

.loader {
  font-family: 'Press Start 2P', cursive;
  animation: glitch 1s infinite;
}

.error {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 10px;
  border: 3px solid #00ff9d;
  background: #2a2a2a;
  flex: 1;
}

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
/* --- ANIME DETAIL PAGE --- */
.anime-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  flex: 1;

  #anime-content {
    #anime-top-info {
      display: flex;
      flex-direction: row;
      gap: 2rem;

      #anime-info {
        display: flex;
        flex-direction: column;
        gap: 1rem;

        .info-block {
          display: flex;
          flex-direction: column;
          p:first-child {
            font-weight: bold;
            margin-bottom: 0.25rem;
          }

          .description {
            color: grey;
          }
        }

        #poster-block {
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          margin-bottom: 1rem;

          .poster {
            cursor: pointer;
            transition: transform 0.3s;

            &:hover {
              transform: scale(1.05);
              box-shadow: 0 0 20px rgba(0, 255, 157, 0.5);
            }
          }
        }

        #anime-genres {
          .tag {
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;

            margin: 0.3rem;
            display: inline-block;
            font-size: 0.85rem;
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
    }
  }
}
</style>
