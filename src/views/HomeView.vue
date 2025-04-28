<template>
  <div class="home">
    <h1>KokoroNoKiroku</h1>
    <p>Your anime-impressions story!</p>
    <div class="features-grid">
      <div>
        <h2>Personal anime list</h2>
        <p>
          Keep track of which anime you've watched, completed, dropped, or are planning. All in one
          convenient place!
        </p>
      </div>
      <div>
        <h2>Personalized recommendations</h2>
        <p>
          Based on your ratings and preferences, the site will suggest anime that you're sure to get
          into.
        </p>
      </div>
      <div>
        <h2>Statistics and achievements</h2>
        <p>
          Keep track of your activity: how many hours spent, how many titles watched, favorite
          genres and studios. Unlock achievements for watching!
        </p>
      </div>
      <div>
        <h2>Services integrations</h2>
        <p>
          Connect your lists from MyAnimeList, AniList, Shikimori and other platforms to bring all
          your anime together in one place and compare them!
        </p>
      </div>
    </div>
  </div>

  <section class="top-anime">
    <div>
      <h1>Top Anime Series</h1>
      <div class="animelist">
        <div v-for="anime in TopAnimeByPopularity" :key="anime.mal_id" class="anime-card">
          <router-link :to="'/anime/' + anime.mal_id">
            <img :src="anime.cover" alt="" />
            <h4>{{ anime.title }}</h4>
          </router-link>
        </div>
      </div>
    </div>

    <div>
      <h1>Upcoming Anime</h1>
      <div class="animelist">
        <div v-for="anime in UpcomingAnime" :key="anime.mal_id" class="anime-card">
          <router-link :to="'/anime/' + anime.mal_id">
            <img :src="anime.cover" alt="" />
            <h4>{{ anime.title }}</h4>
          </router-link>
        </div>
      </div>
    </div>

    <div>
      <h1>Airing Anime</h1>
      <div class="animelist">
        <div v-for="anime in AiringAnime" :key="anime.mal_id" class="anime-card">
          <router-link :to="'/anime/' + anime.mal_id">
            <img :src="anime.cover" alt="" />
            <h4>{{ anime.title }}</h4>
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.home {
  margin: 50px auto;
  text-align: center;
  padding: 50px;
  background-color: #16423c;
  border: none;
  border-radius: 20px;
  max-width: 1100px;

  h1,
  h2 {
    /* font-size: 2rem; */
    color: whitesmoke;
    margin: 20px;
  }

  p {
    font-size: 1.2rem;
    color: #98c1ae;
    margin: 20px;
  }

  .features-grid {
    display: grid;
    grid-gap: 70px 60px;
    grid-template-columns: repeat(2, minmax(300px, 400px));
    justify-content: center;
    text-align: start;
  }
}

.top-anime {
  max-width: 1140px;
  margin: 0 auto;
  padding: 0;

  .anime-card {
    display: block;
    border-radius: 8px;
    transition: background-color 0.3s;
    padding: 10px;

    a {
      text-decoration: none;
    }

    h4 {
      margin-top: 10px;
      text-align: center;
      color: white;
      text-decoration: none;
    }
  }

  .anime-card:hover {
    background-color: rgba(3, 255, 157, 0.3);
  }

  /* .anime-card:hover {
    background-color: #4500b5;
  } */

  > div {
    margin-top: 40px;
  }

  .animelist {
    margin-top: 20px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;

    > div {
      max-width: 200px;
    }

    h4 {
      color: #16423c;
      padding: 0;
    }

    img {
      width: 200px;
      height: 280px;
    }
  }
}
</style>

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
