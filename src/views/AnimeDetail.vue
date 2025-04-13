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
            <img :src="anime?.image" alt="Постер" id="anime-poster" class="poster" />
            <h1 id="anime-title-en" class="title">{{ anime?.title }}</h1>
            <h1 id="anime-title-jp" class="title">{{ anime?.title_japanese }}</h1>
          </div>

          <div id="anime-format" class="info-block">
            <p>Format</p>
            <p class="description">{{ anime!.type }}</p>
          </div>

          <div id="anime-source" class="info-block">
            <p>Source</p>
            <p class="description">{{ anime!.source }}</p>
          </div>

          <div id="anime-episodes" class="info-block">
            <p>Episodes</p>
            <p class="description">{{ anime!.episodes }}</p>
          </div>

          <div id="anime-status" class="info-block">
            <p>Status</p>
            <p class="description">{{ anime!.status }}</p>
          </div>

          <div id="anime-rating" class="info-block">
            <p>Rating</p>
            <p class="description">{{ anime!.rating }}</p>
          </div>

          <div id="anime-season" class="info-block">
            <p>Season</p>
            <p class="description">{{ anime!.season + ' ' + anime!.year }}</p>
          </div>

          <div id="anime-genres" class="info-block">
            <p>Genres</p>
            <span
              class="tag"
              v-for="genre in anime!.genres"
              :key="genre"
              :id="'genre-' + genre.toLowerCase().replace(/\\s+/g, '-')"
            >
              {{ genre }}
            </span>
          </div>
        </div>

        <p id="anime-synopsis" class="description">{{ anime!.synopsis }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

interface Anime {
  id: number
  title: string
  title_english: string
  title_japanese: string
  image: string
  background: string
  type: string
  source: string
  episodes: string
  status: string
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
</script>

<style lang="scss" scoped>
.loading {
  height: 50vh;
  display: grid;
  place-items: center;
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
}

@media (max-width: 768px) {
  #anime-top-info {
    flex-direction: column !important;

    #anime-synopsis {
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

  #anime-content {
    #anime-top-info {
      display: flex;
      flex-direction: row;
      gap: 2rem;

      .description {
        margin: 2% 0;
      }

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
            color: #ccc;
          }
        }

        #poster-block {
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          margin-bottom: 1rem;

          .title {
            color: #ff69b4;
            text-shadow: 0 0 10px rgba(255, 105, 180, 0.5);
            margin: 0.5rem 0;
          }

          .poster {
            width: 300px;
            border-radius: 10px;
            border: 3px solid #00ff9d;
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

      #anime-synopsis {
        flex: 1;
        font-size: 1rem;
        line-height: 1.5;
        margin-left: 2rem;
      }
    }
  }
}
</style>
