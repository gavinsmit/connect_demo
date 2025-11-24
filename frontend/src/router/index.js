import { createRouter, createWebHistory } from 'vue-router'
import ContactForm from '../components/ContactForm.vue'

const routes = [
  {
    path: '/contact-us',
    name: 'ContactForm',
    component: ContactForm,
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/contact-us',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    // always scroll to top
    return { top: 0 }
  },
})

export default router
