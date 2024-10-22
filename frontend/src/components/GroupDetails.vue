<template>
  <div>
    <h1>Group Details for Group ID: {{ groupId }}</h1>
    <div v-if="groupData">
      <h2>{{ groupData.groupName }}</h2>
      <!-- Render other details about the group here -->
      <ul>
        <li
          v-for="member in groupData.members"
          :key="member.id"
          :class="{ highlighted: selectedNames.includes(member.name) }"
          @click="toggleSelection(member.name)"
        >
          {{ member.name }}
        </li>
      </ul>
    </div>
    <div v-else></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      groupId: this.$route.params.id,
      groupData: [],
      selectedNames: [],
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
        console.log(this.groupData)
      } catch (error) {
        console.error('Error fetching group details:', error)
      }
    },
    toggleSelection(name) {
      const index = this.selectedNames.indexOf(name)
      if (index === -1) {
        this.selectedNames.push(name)
      } else {
        this.selectedNames.splice(index, 1)
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
ul {
  list-style-type: none;
}

li {
  padding: 10px;
  cursor: pointer;
  border: 1px solid #ccc;
  margin-bottom: 5px;
  width: 100px;
  text-align: center;
}

li.highlighted {
  background-color: lightblue;
  font-weight: bold;
}
</style>
