import { reactive } from 'vue'
import { createResource } from 'frappe-ui'
import router from '../router'

export const session = reactive({
  login: null,
  logout: null,
  user: null,
  isLoggedIn: false,
})

// --- CHANGE: We export this resource now ---
export const userResource = createResource({
  url: 'frappe.auth.get_logged_user',
  cache: 'User',
  auto: true,
  onSuccess(data) {
    session.user = data
    session.isLoggedIn = true
    // If we are on login page, go home
    if (window.location.pathname === '/frontend/login') {
      router.push('/')
    }
  },
  onError() {
    session.user = null
    session.isLoggedIn = false
    // If we are NOT on login page, go to login
    if (window.location.pathname !== '/frontend/login') {
      router.push('/login')
    }
  },
})

session.login = async (email, password) => {
  try {
    const res = await fetch('/api/method/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ usr: email, pwd: password }),
    })

    const data = await res.json()
    if (!res.ok) {
      throw new Error(data.message || 'Login Failed')
    }

    if (data.message === 'Logged In') {
      userResource.reload()
      return 'Logged In'
    }
  } catch (error) {
    throw error
  }
}

session.logout = async () => {
  await fetch('/api/method/logout')
  userResource.reset()
  session.user = null
  session.isLoggedIn = false
  router.push('/login')
}