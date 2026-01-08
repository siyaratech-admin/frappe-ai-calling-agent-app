<template>
  <div class="min-h-screen w-full flex bg-white">
    <!-- Left Side: Branding & Visuals -->
    <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-gray-900">
      <div class="absolute inset-0 bg-gradient-to-br from-primary-800 via-primary-700 to-primary-900 opacity-90"></div>
      
      <!-- Abstract Shapes -->
      <div class="absolute top-0 left-0 w-full h-full overflow-hidden">
         <div class="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-primary-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
         <div class="absolute top-[20%] right-[-10%] w-[400px] h-[400px] bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
         <div class="absolute bottom-[-10%] left-[20%] w-[600px] h-[600px] bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <div class="relative z-10 flex flex-col justify-between p-16 h-full text-white">
        <div>
           <div class="w-12 h-12 bg-white/10 backdrop-blur-md rounded-xl flex items-center justify-center mb-8 border border-white/20 shadow-glow">
              <FeatherIcon name="cpu" class="w-6 h-6 text-white" />
           </div>
           <h1 class="text-5xl font-bold leading-tight mb-6">AI Calling <br/> Agent</h1>
           <p class="text-lg text-primary-100 max-w-md leading-relaxed">
             Automate your outreach, manage leads, and scale your communications with our intelligent calling assistant.
           </p>
        </div>
        
        <div class="flex items-center gap-4 text-sm text-primary-200 font-medium">
          <div class="flex -space-x-2">
            <div class="w-8 h-8 rounded-full border-2 border-primary-900 bg-gray-300"></div>
            <div class="w-8 h-8 rounded-full border-2 border-primary-900 bg-gray-400"></div>
            <div class="w-8 h-8 rounded-full border-2 border-primary-900 bg-gray-500"></div>
          </div>
          <span>Trusted by 100+ businesses</span>
        </div>
      </div>
    </div>

    <!-- Right Side: Login Form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-12 lg:p-16 bg-white relative">
      <div class="w-full max-w-md space-y-8">
        <div class="text-center lg:text-left">
          <h2 class="text-3xl font-bold text-gray-900 tracking-tight">Welcome back</h2>
          <p class="mt-2 text-sm text-gray-500">Please enter your details to sign in.</p>
        </div>

        <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
          <div class="space-y-5">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">Username</label>
              <div class="mt-1 relative rounded-md shadow-sm">
                 <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <FeatherIcon name="mail" class="h-5 w-5 text-gray-400" />
                 </div>
                <input
                  id="email"
                  v-model="email"
                  type="text"
                  required
                  class="block w-full pl-10 pr-3 py-3 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all sm:text-sm bg-gray-50 hover:bg-white"
                  placeholder="Enter your username"
                />
              </div>
            </div>

            <div>
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <div class="mt-1 relative rounded-md shadow-sm">
                 <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <FeatherIcon name="lock" class="h-5 w-5 text-gray-400" />
                 </div>
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  class="block w-full pl-10 pr-10 py-3 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all sm:text-sm bg-gray-50 hover:bg-white"
                  placeholder="••••••••"
                />
                <div
                  class="absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer"
                  @click="showPassword = !showPassword"
                >
                  <FeatherIcon :name="showPassword ? 'eye-off' : 'eye'" class="h-5 w-5 text-gray-400 hover:text-gray-600 transition-colors" />
                </div>
              </div>
            </div>
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded cursor-pointer"
              />
              <label for="remember-me" class="ml-2 block text-sm text-gray-900 cursor-pointer">Remember me</label>
            </div>

            <div class="text-sm">
              <a href="#" class="font-medium text-primary-600 hover:text-primary-500 hover:underline">Forgot password?</a>
            </div>
          </div>

          <div v-if="error" class="rounded-lg bg-red-50 p-4 border border-red-100 flex items-start">
             <FeatherIcon name="alert-circle" class="w-5 h-5 text-red-500 mt-0.5 mr-3 flex-shrink-0" />
             <div class="text-sm text-red-700">{{ error }}</div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center py-3.5 px-4 border border-transparent rounded-xl shadow-lg shadow-primary-500/30 text-sm font-bold text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all transform hover:-translate-y-0.5 disabled:opacity-70 disabled:cursor-not-allowed"
          >
            <svg
              v-if="loading"
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span v-else>Sign in</span>
          </button>

           <div class="relative my-8">
              <div class="absolute inset-0 flex items-center">
                 <div class="w-full border-t border-gray-200"></div>
              </div>
              <div class="relative flex justify-center text-sm">
                 <span class="px-2 bg-white text-gray-500">Or continue with</span>
              </div>
           </div>
           
           <div class="grid grid-cols-2 gap-4">
              <button type="button" class="flex items-center justify-center px-4 py-2.5 border border-gray-200 rounded-xl shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors">
                 <img src="https://www.svgrepo.com/show/475656/google-color.svg" class="h-5 w-5 mr-3" alt="Google">
                 Google
              </button>
              <button type="button" class="flex items-center justify-center px-4 py-2.5 border border-gray-200 rounded-xl shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors">
                 <img src="https://www.svgrepo.com/show/448224/github.svg" class="h-5 w-5 mr-3" alt="GitHub">
                 GitHub
              </button>
           </div>
        </form>
         
        <p class="text-center text-sm text-gray-500">
           Don't have an account? <a href="#" class="font-semibold text-primary-600 hover:text-primary-500">Sign up for free</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { FeatherIcon } from 'frappe-ui'
import { session } from '../data/session'

const router = useRouter()
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''

  try {
    await session.login(email.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.message || 'Login failed. Please check your credentials.'
    console.error('Login error:', e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
.animation-delay-4000 {
  animation-delay: 4s;
}
</style>
