<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app">
    <header class="app-header">
      <nav>
        <RouterLink to="/">Inicio</RouterLink>
        <RouterLink to="/categorias">Categorías</RouterLink>
        <RouterLink to="/servicios">Servicios</RouterLink>
        <RouterLink to="/about">Acerca de</RouterLink>
      </nav>
    </header>

    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  padding: 1rem;
  background-color: #42b883;
  color: white;
}

.app-header nav {
  display: flex;
  gap: 1rem;
}

.app-header a {
  color: white;
  text-decoration: none;
  font-weight: 500;
}

.app-header a.router-link-active {
  text-decoration: underline;
}

.app-main {
  flex: 1;
  padding: 1rem;
}
</style>
