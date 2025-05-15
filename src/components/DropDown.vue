<template>
  <div class="relative" ref="dropdownRef">
    <slot name="trigger" :toggle="toggle" />

    <div v-show="open" class="absolute z-50 bg-white border rounded shadow mt-2">
      <slot name="menu" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const open = ref(false)
const dropdownRef = ref(null)

const toggle = () => (open.value = !open.value)
const close = () => (open.value = false)

const handleClickOutside = (e) => {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    close()
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', handleClickOutside))
</script>
