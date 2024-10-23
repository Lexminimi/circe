<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    <div class="profile">
      <div class="profile-icon">F</div>
      <h1>Teacher name</h1>
      <p>2024. Október 23., Szerda</p>
    </div>
  </header>
  <main>
    <RouterView />

    <div class="scratch-pad">
      <h2>Scratch Pad</h2>
      <p>Start writing...</p>
    </div>
  </main>
  <footer>
    <div class="footer-nav">
      <RouterLink to="/"><div class="nav-item">Home</div></RouterLink>
      <div class="nav-item">Menu 1</div>
      <div class="nav-item">Menu 1</div>
      <div class="nav-item">Menu 1</div>
      <div class="nav-item">Calendar</div>
    </div>
  </footer>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}

body {
  background-color: #000;
  color: #fff;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background-color: #000;
  font-size: 14px;
  color: #fff;
}

.profile {
  text-align: center;
  padding: 20px 0;
  background-color: #1c1c1c;
}

.profile-icon {
  display: inline-block;
  background-color: #2e7d32;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: white;
  font-weight: bold;
  line-height: 40px;
  text-align: center;
  margin-bottom: 10px;
}

h1 {
  font-size: 24px;
}

p {
  font-size: 14px;
  color: #aaa;
}

.search-bar {
  text-align: center;
  padding: 15px;
}

.search-bar input {
  width: 80%;
  padding: 10px;
  border-radius: 25px;
  border: none;
  background-color: #333;
  color: white;
  font-size: 16px;
}

.scratch-pad {
  padding: 20px;
  background-color: #1c1c1c;
}

.scratch-pad h2 {
  font-size: 18px;
  margin-bottom: 10px;
}

.footer-nav {
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  background-color: #1c1c1c;
}

.nav-item {
  text-align: center;
  font-size: 14px;
}
</style>
