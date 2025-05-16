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

  <section class="max-w-[1140px] mx-auto">
    <div class="mt-[40px]">
      <h1 class="text-[2rem] text-[#16423c] mb-4">Top Anime Series</h1>
      <div class="mt-[20px] flex flex-row justify-between">
        <div
          v-for="anime in TopAnimeByPopularity"
          :key="anime.mal_id"
          class="block p-[10px] rounded-[8px] transition-colors duration-300 hover:bg-[rgba(3,255,157,0.3)] max-w-[200px]"
        >
          <router-link :to="'/anime/' + anime.mal_id" class="no-underline block text-center">
            <img :src="anime.cover" alt="" class="w-[200px] h-[280px]" />
            <h4 class="text-[#16423c] mt-[10px]">{{ anime.title }}</h4>
          </router-link>
        </div>
      </div>
    </div>

    <div class="mt-[40px]">
      <h1 class="text-[2rem] text-[#16423c] mb-4">Upcoming Anime</h1>
      <div class="mt-[20px] flex flex-row justify-between">
        <div
          v-for="anime in UpcomingAnime"
          :key="anime.mal_id"
          class="block p-[10px] rounded-[8px] transition-colors duration-300 hover:bg-[rgba(3,255,157,0.3)] max-w-[200px]"
        >
          <router-link :to="'/anime/' + anime.mal_id" class="no-underline block text-center">
            <img :src="anime.cover" alt="" class="w-[200px] h-[280px]" />
            <h4 class="text-[#16423c] mt-[10px]">{{ anime.title }}</h4>
          </router-link>
        </div>
      </div>
    </div>

    <div class="mt-[40px]">
      <h1 class="text-[2rem] text-[#16423c] mb-4">Airing Anime</h1>
      <div class="mt-[20px] flex flex-row justify-between">
        <div
          v-for="anime in AiringAnime"
          :key="anime.mal_id"
          class="block p-[10px] rounded-[8px] transition-colors duration-300 hover:bg-[rgba(3,255,157,0.3)] max-w-[200px]"
        >
          <router-link :to="'/anime/' + anime.mal_id" class="no-underline block text-center">
            <img :src="anime.cover" alt="" class="w-[200px] h-[280px]" />
            <h4 class="text-[#16423c] mt-[10px]">{{ anime.title }}</h4>
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const TopAnimeByPopularity = ref([])
    const UpcomingAnime = ref([])
    const AiringAnime = ref([])

    onMounted(async () => {
      try {
        const [topResponse, trendingResponse, airingResponse] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/top-anime', { params: { filter: '' } }),
          axios.get('http://127.0.0.1:5000/api/top-anime', { params: { filter: 'upcoming' } }),
          axios.get('http://127.0.0.1:5000/api/top-anime', { params: { filter: 'airing' } }),
        ])

        TopAnimeByPopularity.value = topResponse.data
        UpcomingAnime.value = trendingResponse.data
        AiringAnime.value = airingResponse.data
      } catch (error) {
        console.error('Ошибка загрузки аниме:', error)
      }
    })

    return { TopAnimeByPopularity, UpcomingAnime, AiringAnime }
  },
}
</script>
