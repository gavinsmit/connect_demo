<template>
  <div class="flex flex-col h-screen">
    <div class="flex flex-1 bg-linear-to-b from-background1 to-background2">
      <main class="flex-1 overflow-y-auto paragraph">
        <router-view />
      </main>
    </div>
    <footer class="text-sm text-center sticky-bottom bg-background2">
      <div class="px-4 py-3 text-charcoal">{{ this.footerYear }} © Connect</div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      footerYear: new Date().getFullYear(),
    }
  },
}
</script>

<style scoped>
#app {
  font-family: 'Roboto', sans-serif;
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
