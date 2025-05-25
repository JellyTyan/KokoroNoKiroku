<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
        <Transition name="modal-switch" mode="out-in">
          <div class="modal-content" :key="modalKey">
            <slot></slot>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { defineProps } from 'vue'

defineProps({
  isOpen: Boolean,
  modalKey: Number,
})
</script>

<style scoped>
/* 🔥 Анимация появления/исчезновения модального окна */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* 🔄 Анимация смены модальных окон */
.modal-switch-enter-active,
.modal-switch-leave-active {
  transition:
    transform 0.4s ease,
    opacity 0.4s ease;
}

.modal-switch-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.modal-switch-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Затемнение фона */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Контейнер окна */
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  width: 300px;
  text-align: center;
}
</style>
