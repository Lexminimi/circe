<template>
  <div>
    <h1>Group Details for Group ID: {{ groupId }}</h1>
    <div v-if="groupData">
      <h2>{{ groupData.name }}</h2>
      <!-- Render other details about the group here -->
    </div>
    <div v-else>
      <p>Loading group data...</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      groupId: this.$route.params.id,
      groupData: null,
    }
  },
  methods: {
    async fetchGroupDetails() {
      try {
        const response = await fetch(
          `https://fischerb2.pythonanywhere.com/group/${this.groupId}`,
          {
            headers: {
              Authorization: 'Basic ' + btoa('reka:B1a9l8i8'),
            },
          },
        )
        if (!response.ok) {
          throw new Error('Failed to fetch group details')
        }
        const data = await response.json()
        this.groupData = data // assuming data is an object with details
      } catch (error) {
        console.error('Error fetching group details:', error)
      }
    },
  },
  watch: {
    // Watch for route changes to fetch new data
    '$route.params.id'(newId) {
      this.groupId = newId
      this.fetchGroupDetails()
    },
  },
  mounted() {
    this.fetchGroupDetails()
  },
}
</script>

<style scoped>
/* Optional styling */
</style>
