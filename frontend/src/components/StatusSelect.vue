<template>
  <select
    :value="modelValue"
    @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
    class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#16423c] focus:ring-2 focus:ring-[#98c1ae] focus:ring-opacity-50 outline-none transition-all duration-200"
  >
    <option value="planned">Planned</option>
    <option value="watching">Watching</option>
    <option value="completed">Completed</option>
    <option value="dropped">Dropped</option>
  </select>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string
}>()

defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()
</script> 