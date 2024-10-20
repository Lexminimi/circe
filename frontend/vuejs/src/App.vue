<template>
  <div>
    <h1>Groups</h1>
    <ul>
      <li v-for="group in groups" :key="group.id">
        <a :href="`https://fischerb2.pythonanywhere.com/group/${group.id}`">{{ group.name }}</a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      groups: [],
    };
  },
  methods: {
    async fetchGroups() {
      try {
        const response = await fetch("https://fischerb2.pythonanywhere.com/groups", {
          headers: {
            Authorization: "Basic " + btoa("reka:B1a9l8i8"),
          },
        });
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const data = await response.json();
        this.groups = data; // assuming data is an array of groups
      } catch (error) {
        console.error("Error fetching groups:", error);
      }
    },
  },
  mounted() {
    this.fetchGroups();
  },
};
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
