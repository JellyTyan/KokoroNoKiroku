<template>
  <nav
    class="flex flex-row justify-around items-center max-h-[100px] bg-[#16423c] text-white px-4 py-2 shadow-xl"
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
            class="absolute mt-2 w-48 bg-white text-black border rounded shadow z-50 p-[10px]"
          >
            <ul>
              <li class="p-2 hover:bg-gray-100 cursor-pointer">
                <router-link to="/top-anime">
                  <p>Top anime</p>
                </router-link>
              </li>
              <li class="p-2 hover:bg-gray-100 cursor-pointer">
                <router-link to="/genres">
                  <p>Genres</p>
                </router-link>
              </li>
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
            v-model="username"
            required
          />
          <input
            type="text"
            :placeholder="isLoginMode ? 'Username or Email' : 'Email'"
            class="px-3 py-2 border rounded"
            v-model="email"
            required
          />
          <input
            type="password"
            placeholder="Password"
            class="px-3 py-2 border rounded"
            v-model="password"
            required
          />
          <button
            type="submit"
            class="px-4 py-2 border rounded bg-white hover:bg-[#16423c] hover:text-white transition duration-300"
          >
            {{ isLoginMode ? 'Login' : 'Register' }}
          </button>
        </form>

        <p v-if="componentError" style="color: red;">Ошибка: {{ componentError }}</p>
        <p class="text-red-500 text-sm" v-if="error">{{ error }}</p>
        <p class="text-green-600 text-sm" v-if="success">{{ success }}</p>
        <p class="mt-2 text-sm">
          {{ isLoginMode ? 'No account?' : 'Already have one?' }}
          <a href="#" @click.prevent="toggleMode" class="text-[#16423c] underline hover:opacity-80">
            {{ isLoginMode ? 'Sign up now!' : 'Sign in!' }}
          </a>
        </p>
      </Modal>
    </div>
  </nav>
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

<script setup lang="ts">
import { ref, watch } from 'vue';
import Modal from '../components/Modal.vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import type { UserCredentials } from '../types/auth';

const authStore = useAuthStore();
const router = useRouter();

const showModal = ref<boolean>(false);
const isLoginMode = ref<boolean>(true);
const modalKey = ref<number>(0);
const isOpen = ref<boolean>(false);

const email = ref<string>('');
const username = ref<string>('');
const password = ref<string>('');
const componentError = ref<string | null>(null);
const error = ref<string | null>(null);
const success = ref<string | null>(null);

const toggleMode = (): void => {
  isLoginMode.value = !isLoginMode.value;
  componentError.value = null;
  error.value = null;
  success.value = null;
  authStore.error = null;
  modalKey.value++;
  // Clear form fields when switching modes
  email.value = '';
  username.value = '';
  password.value = '';
};

const handleSubmit = async (): Promise<void> => {
  componentError.value = null;
  error.value = null;
  success.value = null;
  authStore.error = null;

  const credentials: UserCredentials = {
    email: email.value,
    username: isLoginMode.value ? email.value : username.value,
    password: password.value,
  };

  try {
    if (isLoginMode.value) {
      const loginSuccess = await authStore.login(credentials);
      if (loginSuccess) {
        showModal.value = false;
        router.push('/');
      }
    } else {
      const registerSuccess = await authStore.register(credentials);
      if (registerSuccess) {
        isLoginMode.value = true;
        email.value = '';
        username.value = '';
        password.value = '';
        success.value = 'Регистрация прошла успешно! Теперь вы можете войти.';
      }
    }
  } catch (err) {
    error.value = authStore.error;
    componentError.value = authStore.error;
  } finally {
    if (componentError.value || !authStore.isAuthenticated) {
      email.value = '';
      username.value = '';
      password.value = '';
    }
  }
};

const handleLogout = (): void => {
  authStore.logout();
  router.push('/');
};

// Отслеживаем изменения в состоянии аутентификации
watch(
  () => authStore.isAuthenticated,
  (newVal) => {
    if (newVal) {
      showModal.value = false; // Закрыть модальное окно при успешном логине
    }
  }
);
</script>

