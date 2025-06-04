<template>
  <div class="block p-[10px] rounded-[8px] max-w-[200px]">
    <div class="animate-pulse">
      <!-- Скелетон для изображения -->
      <div class="w-[200px] h-[280px] bg-gray-200 rounded-lg"></div>
      <!-- Скелетон для заголовка -->
      <div class="mt-[10px]">
        <div class="h-4 bg-gray-200 rounded w-3/4 mx-auto"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// No props or logic needed for the skeleton
</script>

<style scoped>
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}
</style> 