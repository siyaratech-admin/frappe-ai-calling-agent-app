import { createRouter, createWebHistory } from 'vue-router'
import { session, userResource } from './data/session'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('./pages/Home.vue'),
    meta: { title: 'Dashboard' } // <--- Title for this page
  },
  {
    path: '/contacts',
    name: 'Contacts',
    component: () => import('./pages/Contacts.vue'),
    meta: { title: 'Contacts' }
  },
  {
    path: '/call-logs',
    name: 'CallLogs',
    component: () => import('./pages/CallLogs.vue'),
    meta: { title: 'Call Logs' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('./pages/Login.vue'),
    meta: { title: 'Login' }
  },
  {
    path: '/lead-generator',  // <--- ADD THIS BLOCK
    name: 'LeadGenerator',
    component: () => import('./pages/LeadGenerator.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/bulk-calling',
    name: 'BulkCalling',
    component: () => import('./pages/BulkCalling.vue'),
  },
  {
    path: '/bulk-emailing',
    name: 'BulkEmailing',
    component: () => import('./pages/BulkEmailing.vue'),
  },
]

let router = createRouter({
  history: createWebHistory('/ai_calling_agent'),
  routes,
})

router.beforeEach(async (to, from, next) => {
  // 1. Dynamic Title Logic
  const siteTitle = 'AI Agent'
  document.title = to.meta.title ? `${to.meta.title} - ${siteTitle}` : siteTitle

  // 2. Authentication Logic
  const isLoggedIn = session.isLoggedIn
  try {
    await userResource.promise
  } catch (error) {
    // session fetch failed
  }

  const userValid = session.isLoggedIn

  if (to.name === 'Login' && userValid) {
    next({ name: 'Home' })
  } else if (to.name !== 'Login' && !userValid) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router