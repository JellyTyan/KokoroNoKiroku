<template>
  <NavBar />
  <FooterBar />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Iansui&display=swap');
@import 'tailwindcss';

html,
body {
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Iansui', cursive;
}
</style>

<script setup>
import NavBar from '@/components/NavBar.vue'
import FooterBar from '@/components/FooterBar.vue'
</script>
