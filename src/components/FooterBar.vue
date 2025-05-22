<template>
  <footer
    class="relative bg-gradient-to-br from-[#16423c] to-[#112e2a] text-white py-12 mt-16 shadow-2xl overflow-hidden"
  >
    <!-- Decorative background (like sakura petals or noise layer) -->
    <div
      class="absolute inset-0 opacity-[0.03] bg-[url('/sakura-pattern.svg')] bg-repeat pointer-events-none"
    ></div>

    <div
      class="relative z-10 max-w-7xl mx-auto px-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-10"
    >
      <!-- Logo and Description -->
      <div>
        <h2 class="text-3xl font-bold font-mono tracking-wider mb-4">
          Kokoro<span class="text-pink-400">No</span>Kiroku
        </h2>
        <p class="text-sm text-gray-300">
          Your anime-impressions story.<br />記憶を記す、心の中で。
        </p>
      </div>

      <!-- Navigation -->
      <div>
        <h3 class="text-xl font-semibold mb-4">Navigation</h3>
        <ul class="space-y-2 text-sm text-gray-300">
          <li><router-link to="/" class="hover:text-pink-400 transition">Home</router-link></li>
          <li><a href="#" class="hover:text-pink-400 transition">About</a></li>
          <li><a href="#" class="hover:text-pink-400 transition">Sitemap</a></li>
        </ul>
      </div>

      <!-- Contacts -->
      <div>
        <h3 class="text-xl font-semibold mb-4">Contacts</h3>
        <ul class="text-sm text-gray-300 space-y-2">
          <li>
            Telegram:
            <a href="https://t.me/jellytyan" class="hover:text-pink-400 transition">@jellytyan</a>
          </li>
          <li>
            GitHub:
            <a href="https://github.com/jellytyan" class="hover:text-pink-400 transition"
              >/jellytyan</a
            >
          </li>
        </ul>
      </div>

      <!-- Social Media -->
      <div>
        <h3 class="text-xl font-semibold mb-4">Follow Us</h3>
        <div class="flex space-x-4 text-gray-300 text-lg">
          <a
            href="https://github.com/jellytyan"
            class="hover:text-pink-400 transition flex items-center space-x-1"
          >
            <i class="fab fa-github"></i>
            <span>GitHub</span>
          </a>
        </div>
      </div>
    </div>

    <!-- Bottom Bar -->
    <div
      class="relative z-10 border-t border-gray-700 mt-12 pt-6 text-center text-sm text-gray-400"
    >
      &copy; 2025 KokoroNoKiroku. All rights reserved.
    </div>
  </footer>
</template>
