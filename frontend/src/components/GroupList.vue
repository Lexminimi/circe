<template>
  <div>
    <h1>Groups</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <ul>
      <li v-for="group in groups" :key="group.id">
        <router-link :to="`/group/${group.id}`">{{ group.name }}</router-link>
      </li>
    </ul>
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
a {
  color: blue;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
</style>
