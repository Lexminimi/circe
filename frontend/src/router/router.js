import { createMemoryHistory, createRouter } from 'vue-router'

import HomeView from '../components/HomeView.vue'
import Groups from '../components/Groups.vue'
import GetRequest from '@/components/GetRequest.vue'
import GroupDetails from '@/components/GroupDetails.vue'

const routes = [
  { path: '/groups', component: GetRequest },
  { path: '/group/:id', name: 'GroupDetails', component: GroupDetails },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router
