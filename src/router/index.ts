import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import TopAnime from '../views/TopAnime.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: HomeView },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    {
      path: '/anime/:id',
      name: 'anime-details',
      component: () => import('@/views/AnimeDetail.vue'),
      props: true,
    },
    { path: '/top-anime', component: TopAnime },
  ],
})

export default router
