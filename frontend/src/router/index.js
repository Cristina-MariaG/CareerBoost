import { createRouter, createWebHistory } from 'vue-router'
import LinkedinView from '../views/LinkedinView.vue'
import CvView from '../views/CvView.vue'
import HistoryView from '../views/HistoryView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/linkedin' },
    { path: '/linkedin', component: LinkedinView },
    { path: '/cv', component: CvView },
    { path: '/history', component: HistoryView },
  ],
})

export default router
