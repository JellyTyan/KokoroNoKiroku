<template>
  <nav>
    <router-link to="/"
      ><img src="../assets/images/icon.png" alt="logo" width="60px"
    /></router-link>
    <div>
      <button @click="((showModal = true), (isLoginMode = true))" class="btn-sign">Sign In</button>

      <Modal :isOpen="showModal" :modalKey="modalKey" @close="showModal = false">
        <h2>{{ isLoginMode ? 'Login' : 'Register' }}</h2>
        <form @submit.prevent="handleSubmit">
          <input type="text" v-if="!isLoginMode" placeholder="Username" />
          <input type="text" placeholder="Email" />
          <input type="password" placeholder="Password" />
          <button type="submit">{{ isLoginMode ? 'Login' : 'Register' }}</button>
        </form>
        <p>
          {{ isLoginMode ? 'No account?' : 'Already have one?' }}
          <a href="#" @click.prevent="toggleMode">
            {{ isLoginMode ? 'Sign up now!' : 'Sign in!' }}
          </a>
        </p>
      </Modal>
    </div>
  </nav>
  <router-view></router-view>
</template>

<style lang="scss" scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease-in-out;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(50px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-50px);
}
nav {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  max-height: 100px;
  background-color: #16423c;
  align-items: center;
}
form {
  display: flex;
  flex-direction: column;
  button {
    padding: 5px;
    margin: 5px;
    border-bottom: 1px grey solid;
    border-right: 1px lightgrey solid;
    border-left: 1px lightgrey solid;
    border-top: 1px lightgrey solid;
    border-radius: 5px;
    background-color: white;
    transition-duration: 0.4s;
  }
  button:hover {
    background-color: #16423c;
    transition-duration: 0.4s;
  }
  input {
    padding: 5px;
    margin: 10px 10px;
  }
  p {
    a:link {
      color: #16423c;
      text-decoration: none;
    }
  }
}
.btn-sign {
  padding: 10px 20px 10px 20px;
  border: 1px solid black;
  border-radius: 5px;
  background-color: #6a9c89;
  color: #16423c;
  font-size: 15px;
}
</style>

<script setup>
import { ref } from 'vue'
import Modal from '../components/Modal.vue'

const showModal = ref(false)
const isLoginMode = ref(true)
const modalKey = ref(0)

const toggleMode = () => {
  isLoginMode.value = !isLoginMode.value
  modalKey.value++
}

const handleSubmit = () => {
  alert(isLoginMode.value ? 'Вход выполнен!' : 'Регистрация успешна!')
}
</script>
