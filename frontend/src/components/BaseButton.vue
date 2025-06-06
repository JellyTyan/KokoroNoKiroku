<template>
  <button
    :class="[
      'px-4 py-2 rounded-lg font-medium transition-all duration-200',
      variant === 'primary' ? 'bg-[#16423c] text-white hover:bg-[#1a524a]' :
      variant === 'secondary' ? 'bg-[#98c1ae] text-[#16423c] hover:bg-[#8ab39f]' :
      'bg-gray-200 text-gray-700 hover:bg-gray-300',
      size === 'sm' ? 'text-sm' : size === 'lg' ? 'text-lg' : 'text-base',
      disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
    ]"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary' | 'default'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
}>()

defineEmits<{
  (e: 'click'): void
}>()
</script> 