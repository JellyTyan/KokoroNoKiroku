import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import TopAnime from '../views/TopAnime.vue'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: HomeView },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    {
      path: '/anime/:id',
      name: 'anime-details',
      component: () => import('../views/AnimeDetail.vue'),
      props: (route) => ({
        id: Number(route.params.id)
      })
    },
    { path: '/top-anime', component: TopAnime },
    {
      path: '/profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
    }
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // If the route requires auth and user is not authenticated
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Try to restore session
    await authStore.init()
    
    // If still not authenticated, redirect to login
    if (!authStore.isAuthenticated) {
      next('/login')
      return
    }
  }
  
  next()
})

export default router
