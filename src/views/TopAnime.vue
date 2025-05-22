<template>
  <div class="p-4">
    <div ref="grid" class="grid grid-cols-5 gap-4">
      <div
        v-for="(item, index) in items"
        :key="index"
        class="bg-white shadow rounded-lg p-4 h-32 flex items-center justify-center text-lg font-bold"
      >
        {{ item }}
      </div>
    </div>

    <div v-if="loading" class="text-center mt-4 text-gray-500">Загрузка...</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const items = ref([])
const loading = ref(false)
const page = ref(0)
const limit = 20
const grid = ref(null)

const fetchMoreItems = async () => {
  if (loading.value) return
  loading.value = true

  await new Promise((resolve) => setTimeout(resolve, 1000))

  const newItems = Array.from(
    { length: limit },
    (_, i) => `Карточка #${page.value * limit + i + 1}`,
  )
  items.value.push(...newItems)
  page.value++
  loading.value = false
}

const onScroll = () => {
  if (!grid.value) return

  const { bottom } = grid.value.getBoundingClientRect()
  const windowHeight = window.innerHeight

  if (bottom < windowHeight + 200) {
    fetchMoreItems()
  }
}

onMounted(() => {
  fetchMoreItems()
  window.addEventListener('scroll', onScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
/* Можно добавить кастомные стили, если не используешь Tailwind */
</style>
