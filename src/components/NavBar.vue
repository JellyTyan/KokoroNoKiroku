<template>
  <nav
    class="flex flex-row justify-around items-center max-h-[100px] bg-[#16423c] text-white px-4 py-2"
  >
    <div class="flex flex-row items-center space-x-5">
      <router-link to="/">
        <img src="../assets/images/icon.png" alt="logo" width="60" />
      </router-link>

      <div class="relative" @mouseenter="isOpen = true" @mouseleave="isOpen = false">
        <button class="text-lg font-bold">Anime</button>

        <transition name="fade">
          <div
            v-if="isOpen"
            class="absolute mt-2 w-48 bg-white text-black border rounded shadow z-50"
          >
            <ul>
              <li class="p-2 hover:bg-gray-100 cursor-pointer">Top anime</li>
              <li class="p-2 hover:bg-gray-100 cursor-pointer">Genres</li>
            </ul>
          </div>
        </transition>
      </div>
    </div>

    <div>
      <button
        @click="((showModal = true), (isLoginMode = true))"
        class="px-5 py-2 border border-black rounded bg-[#6a9c89] text-[#16423c] text-sm font-semibold hover:bg-[#16423c] hover:text-white transition duration-300"
      >
        Sign In
      </button>

      <Modal :isOpen="showModal" :modalKey="modalKey" @close="showModal = false">
        <h2 class="text-xl font-bold mb-4">{{ isLoginMode ? 'Login' : 'Register' }}</h2>
        <form @submit.prevent="handleSubmit" class="flex flex-col space-y-3">
          <input
            v-if="!isLoginMode"
            type="text"
            placeholder="Username"
            class="px-3 py-2 border rounded"
          />
          <input type="text" placeholder="Email" class="px-3 py-2 border rounded" />
          <input type="password" placeholder="Password" class="px-3 py-2 border rounded" />
          <button
            type="submit"
            class="px-4 py-2 border rounded bg-white hover:bg-[#16423c] hover:text-white transition duration-300"
          >
            {{ isLoginMode ? 'Login' : 'Register' }}
          </button>
        </form>
        <p class="mt-2 text-sm">
          {{ isLoginMode ? 'No account?' : 'Already have one?' }}
          <a href="#" @click.prevent="toggleMode" class="text-[#16423c] underline hover:opacity-80">
            {{ isLoginMode ? 'Sign up now!' : 'Sign in!' }}
          </a>
        </p>
      </Modal>
    </div>
  </nav>

  <router-view />
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>

<script setup>
import { ref } from 'vue'
import Modal from '../components/Modal.vue'

const showModal = ref(false)
const isLoginMode = ref(true)
const modalKey = ref(0)
const isOpen = ref(false)

const toggleMode = () => {
  isLoginMode.value = !isLoginMode.value
  modalKey.value++
}

const handleSubmit = () => {
  alert(isLoginMode.value ? 'Вход выполнен!' : 'Регистрация успешна!')
}
</script>
