<template>
  <div class="mx-auto my-[50px] text-center p-[50px] bg-[#16423c] rounded-[20px] max-w-[1300px]">
    <h1 class="text-[3rem] text-[whitesmoke] my-[10px]">KokoroNoKiroku</h1>
    <p class="text-[1.2rem] text-[#98c1ae] my-[10px]">Your anime-impressions story!</p>
    <div
      class="grid justify-center text-left gap-x-[60px] gap-y-[40px]"
      style="grid-template-columns: repeat(2, minmax(300px, 450px))"
    >
      <div class="flex items-center gap-x-4">
        <img
          src="../assets/images/checklist-icon.png"
          alt=""
          class="w-[100px] h-[140px] flex-shrink-0 mt-[20px]"
        />
        <div>
          <h2 class="text-[2rem] text-[whitesmoke] my-[20px]">Personal anime list</h2>
          <p class="text-[1.2rem] text-[#98c1ae] my-[20px]">
            Keep track of which anime you've watched, completed, dropped, or are planning. All in
            one convenient place!
          </p>
        </div>
      </div>

      <div class="flex items-center gap-x-4">
        <img
          src="../assets/images/recomend-icon.png"
          alt=""
          class="w-[100px] h-[100px] flex-shrink-0 mt-[20px]"
        />
        <div>
          <h2 class="text-[2rem] text-[whitesmoke] my-[20px]">Personalized recommendations</h2>
          <p class="text-[1.2rem] text-[#98c1ae] my-[20px]">
            Based on your ratings and preferences, the site will suggest anime that you're sure to
            get into.
          </p>
        </div>
      </div>

      <div class="flex items-center gap-x-4">
        <img
          src="../assets/images/stats-icon.png"
          alt=""
          class="w-[100px] h-[70px] flex-shrink-0 mt-[20px]"
        />
        <div>
          <h2 class="text-[2rem] text-[whitesmoke] my-[20px]">Statistics and achievements</h2>
          <p class="text-[1.2rem] text-[#98c1ae] my-[20px]">
            Keep track of your activity: how many hours spent, how many titles watched, favorite
            genres and studios. Unlock achievements for watching!
          </p>
        </div>
      </div>

      <div class="flex items-center gap-x-4">
        <img
          src="../assets/images/services-icon.png"
          alt=""
          class="w-[100px] h-[110px] flex-shrink-0 mt-[20px]"
        />
        <div>
          <h2 class="text-[2rem] text-[whitesmoke] my-[20px]">Services integrations</h2>
          <p class="text-[1.2rem] text-[#98c1ae] my-[20px]">
            Connect your lists from MyAnimeList, AniList, Shikimori and other platforms to bring all
            your anime together in one place and compare them!
          </p>
        </div>
      </div>
    </div>
  </div>

  <section class="max-w-[1240px] mx-auto">
    <div class="mt-[40px]">
      <h1 class="text-[2rem] text-[#16423c] mb-4">Top Anime Series</h1>
      <div class="mt-[20px] grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6">
        <template v-if="loading">
          <AnimeSkeleton v-for="n in 6" :key="n" />
        </template>
        <template v-else>
          <AnimeCard
            v-for="anime in TopAnimeByPopularity"
            :key="anime.mal_id"
            :anime="anime"
          />
        </template>
      </div>
    </div>

    <div class="mt-[40px]">
      <h1 class="text-[2rem] text-[#16423c] mb-4">Upcoming Anime</h1>
      <div class="mt-[20px] grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6">
        <template v-if="loading">
          <AnimeSkeleton v-for="n in 6" :key="n" />
        </template>
        <template v-else>
          <AnimeCard
            v-for="anime in UpcomingAnime"
            :key="anime.mal_id"
            :anime="anime"
          />
        </template>
      </div>
    </div>

    <div class="mt-[40px]">
      <h1 class="text-[2rem] text-[#16423c] mb-4">Airing Anime</h1>
      <div class="mt-[20px] grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6">
        <template v-if="loading">
          <AnimeSkeleton v-for="n in 6" :key="n" />
        </template>
        <template v-else>
          <AnimeCard
            v-for="anime in AiringAnime"
            :key="anime.mal_id"
            :anime="anime"
          />
        </template>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AnimeSkeleton from '../components/AnimeSkeleton.vue'
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

const TopAnimeByPopularity = ref<Anime[]>([])
const UpcomingAnime = ref<Anime[]>([])
const AiringAnime = ref<Anime[]>([])
const loading = ref(true)

const fetchAnime = async (filter: string) => {
  try {
    const response = await axios.get(`https://api.jikan.moe/v4/top/anime`, {
      params: {
        filter,
        limit: 6,
        sfw: true
      }
    })
    return response.data.data
  } catch (error) {
    console.error(`Error fetching ${filter} anime:`, error)
    return []
  }
}

onMounted(async () => {
  try {
    const [topResponse, upcomingResponse, airingResponse] = await Promise.all([
      fetchAnime(''),
      fetchAnime('upcoming'),
      fetchAnime('airing')
    ])

    TopAnimeByPopularity.value = topResponse
    UpcomingAnime.value = upcomingResponse
    AiringAnime.value = airingResponse
  } catch (error) {
    console.error('Error loading anime:', error)
  } finally {
    loading.value = false
  }
})
</script>
