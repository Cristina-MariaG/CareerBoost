import { createRouter, createWebHistory } from 'vue-router'
import LinkedinView from '../views/LinkedinView.vue'
import CvView from '../views/CvView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/linkedin' },
    { path: '/linkedin', component: LinkedinView },
    { path: '/cv', component: CvView },
  ],
})

export default router
