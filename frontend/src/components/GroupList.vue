<template>
  <div>
    <h1>Groups</h1>
    <div class="options">
      <div v-if="loading" class="loading">Loading...</div>
      <div class="option" v-for="group in groups" :key="group.id">
        <router-link :to="`/group/${group.id}`">{{ group.name }}</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
const loading = ref(false)
export default {
  data() {
    return {
      groups: [],
    }
  },
  methods: {
    async fetchGroups() {
      try {
        loading.value = true
        const response = await fetch(
          'https://fischerb2.pythonanywhere.com/groups',
          {
            headers: {
              Authorization: 'Basic ' + btoa('reka:B1a9l8i8'),
            },
          },
        )
        if (!response.ok) {
          throw new Error('Failed to fetch data')
        }
        const data = await response.json()
        this.groups = data // assuming data is an array of groups
        loading.value = false
      } catch (error) {
        console.error('Error fetching groups:', error)
      }
    },
  },
  mounted() {
    this.fetchGroups()
  },
}
</script>

<style scoped>
/* Optional styling */
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin-bottom: 10px;
}

a:hover {
  text-decoration: underline;
}

.options {
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
}

.option {
  padding: 10px;
  background-color: #333;
  border-radius: 10px;
  width: 80px;
  text-align: center;
}
</style>
