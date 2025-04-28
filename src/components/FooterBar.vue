<template>
  <footer>
    <div class="neon-timer">
      <div class="glitch-text" data-text="До нового эпизода:">
        До 1488-го эпизода One Piece осталось:
      </div>
      <div class="time-boxes">
        <div v-for="(value, name) in time" :key="name" class="time-unit">
          <div class="number">{{ value }}</div>
          <div class="label">{{ labels[name] }}</div>
        </div>
      </div>
      <div class="progress">
        <div class="progress-bar" :style="progressStyle"></div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  targetDate: {
    type: Date,
    default: () => new Date(Date.now() + 128586800000),
  },
})

const now = ref(new Date())
const labels = { days: 'days', hours: 'hours', minutes: 'minutes', seconds: 'seconds' }

const time = computed(() => {
  const diff = props.targetDate.getTime() - now.value.getTime()
  return {
    days: Math.floor(diff / (1000 * 60 * 60 * 24)),
    hours: Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
    minutes: Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60)),
    seconds: Math.floor((diff % (1000 * 60)) / 1000),
  }
})

const progressStyle = computed(() => ({
  width: `${Math.abs(((Date.now() % 2000) / 2000) * 100)}%`,
}))

onMounted(() => {
  setInterval(() => {
    now.value = new Date()
  }, 1000)
})
</script>

<style lang="scss" scoped>
footer {
  height: 150px;
  background-color: #16423c;
  margin-top: 50px;
  width: 100%;
}
.neon-timer {
  background: #16423c;
  padding: 1rem;
  border: 2px solid darkgreen;
  box-shadow: 0 0 15px darkgreen;
}

.time-boxes {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  margin: 1rem 0;
}

.time-unit {
  text-align: center;
  position: relative;
}

.number {
  font-family: 'Courier New', monospace;
  font-size: 2rem;
  color: #00ff9d;
  text-shadow: 0 0 10px #00ff9d80;
  background: #000;
  padding: 0.5rem;
  border: 1px solid #00ff9d;
  margin-bottom: 0.5rem;
}

.label {
  font-size: 0.8rem;
  color: #ff00ff;
  text-transform: uppercase;
}

.progress {
  height: 3px;
  background: #1a1a1a;
  position: relative;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, darkgreen, #00ffff);
  animation: progress-panic 2s infinite;
}

@keyframes progress-panic {
  0% {
    left: 0;
  }
  50% {
    left: 90%;
  }
  100% {
    left: 0;
  }
}

.glitch-text {
  position: relative;
  color: #fff;
  animation: glitch 3s infinite;
}

@keyframes glitch {
  0% {
    transform: translate(0);
  }
  20% {
    transform: translate(-2px, 2px);
  }
  40% {
    transform: translate(-2px, -2px);
  }
  60% {
    transform: translate(2px, 2px);
  }
  80% {
    transform: translate(2px, -2px);
  }
  100% {
    transform: translate(0);
  }
}
</style>
