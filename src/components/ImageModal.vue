<template>
  <transition name="fade">
    <div v-if="show" class="image-modal" @click.self="close">
      <div class="modal-content">
        <button class="close-btn" @click="close">&times;</button>
        <img
          :src="src"
          alt="Full size"
          class="full-image"
          :class="{ loading: isLoading }"
          @load="isLoading = false"
        />
        <div v-if="isLoading" class="loader">Загрузка моэ... (´･ω･`)</div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps({
  show: Boolean,
  src: String,
})

const emit = defineEmits(['close'])

const isLoading = ref(true)

watch(
  () => props.src,
  () => {
    isLoading.value = true
  },
)

const close = () => {
  emit('close')
}
</script>

<style scoped lang="scss">
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  position: relative;
  max-width: 90%;
  max-height: 90vh;
}

.full-image {
  max-height: 90vh;
  border-radius: 8px;
  box-shadow: 0 0 30px rgba(255, 105, 180, 0.3);
  transition: transform 0.3s;
  cursor: zoom-in;

  &.loading {
    opacity: 0;
    height: 0;
  }
}

.close-btn {
  position: absolute;
  top: -40px;
  right: -10px;
  background: none;
  border: none;
  color: #ff69b4;
  font-size: 3rem;
  cursor: pointer;
  text-shadow: 0 0 10px rgba(255, 105, 180, 0.5);
  transition: transform 0.2s;

  &:hover {
    transform: scale(1.2);
  }
}

.loader {
  color: #00ff9d;
  font-family: 'Press Start 2P', cursive;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .modal-content {
    max-width: 95%;
  }

  .full-image {
    cursor: grab;
    &:active {
      cursor: grabbing;
    }
  }
}
</style>
