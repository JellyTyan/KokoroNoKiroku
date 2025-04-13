<template>
  <NavBar />
  <FooterBar />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Iansui&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Iansui', cursive;
  font-weight: 400;
  font-style: normal;
}
</style>

<script setup>
import NavBar from '@/components/NavBar.vue'
import FooterBar from '@/components/FooterBar.vue'
</script>
