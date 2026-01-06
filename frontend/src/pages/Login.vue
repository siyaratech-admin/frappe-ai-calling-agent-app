<template>
	<div
		class="min-h-screen w-full overflow-x-hidden bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8"
	>
		<div class="sm:mx-auto sm:w-full sm:max-w-md text-center">
			<div
				class="mx-auto h-16 w-16 bg-indigo-50 rounded-full flex items-center justify-center mb-4"
			>
				<FeatherIcon name="shield" class="h-8 w-8 text-[#4318FF]" />
			</div>
			<h2 class="text-3xl font-extrabold text-gray-900">Welcome Back</h2>
			<p class="mt-2 text-sm text-gray-600">Sign in to your account to continue</p>
		</div>

		<div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
			<div
				class="bg-white py-8 px-4 shadow-xl shadow-gray-100 sm:rounded-xl sm:px-10 border border-gray-100"
			>
				<div class="mb-6 text-center">
					<h3 class="text-lg font-bold text-gray-900">Sign In</h3>
					<p class="text-xs text-gray-500 mt-1">
						Enter your credentials to access your account
					</p>
				</div>

				<form class="space-y-5" @submit.prevent="handleLogin">
					<div>
						<label for="email" class="block text-sm font-semibold text-gray-700 mb-1">
							Username
						</label>
						<div class="relative rounded-md shadow-sm">
							<div
								class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
							>
								<FeatherIcon name="user" class="h-4 w-4 text-gray-400" />
							</div>
							<input
								id="email"
								v-model="email"
								type="text"
								name="username"
								autocomplete="username"
								required
								class="block w-full pl-10 pr-3 py-2.5 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#4318FF] focus:border-[#4318FF] sm:text-sm transition-all"
								placeholder="Enter your username"
							/>
						</div>
					</div>

					<div>
						<label
							for="password"
							class="block text-sm font-semibold text-gray-700 mb-1"
						>
							Password
						</label>
						<div class="relative rounded-md shadow-sm">
							<div
								class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
							>
								<FeatherIcon name="lock" class="h-4 w-4 text-gray-400" />
							</div>
							<input
								id="password"
								v-model="password"
								:type="showPassword ? 'text' : 'password'"
								name="password"
								autocomplete="current-password"
								required
								class="block w-full pl-10 pr-10 py-2.5 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#4318FF] focus:border-[#4318FF] sm:text-sm transition-all"
								placeholder="Enter your password"
							/>
							<div
								class="absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer"
								@click="showPassword = !showPassword"
							>
								<FeatherIcon
									:name="showPassword ? 'eye-off' : 'eye'"
									class="h-4 w-4 text-gray-400 hover:text-gray-600"
								/>
							</div>
						</div>
					</div>

					<div class="flex items-center justify-between">
						<div class="flex items-center">
							<input
								id="remember_me"
								type="checkbox"
								class="h-4 w-4 text-[#4318FF] focus:ring-[#4318FF] border-gray-300 rounded"
							/>
							<label for="remember_me" class="ml-2 block text-sm text-gray-500">
								Remember me
							</label>
						</div>

						<div class="text-sm">
							<a href="#" class="font-medium text-[#4318FF] hover:text-indigo-500">
								Forgot password?
							</a>
						</div>
					</div>

					<div
						v-if="error"
						class="text-sm text-red-600 bg-red-50 p-2 rounded text-center border border-red-100"
					>
						{{ error }}
					</div>

					<div>
						<button
							type="submit"
							:disabled="loading"
							class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-bold text-white bg-[#4318FF] hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#4318FF] transition-colors disabled:opacity-70 disabled:cursor-not-allowed"
						>
							<span v-if="loading" class="mr-2">
								<svg
									class="animate-spin h-5 w-5 text-white"
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
								>
									<circle
										class="opacity-25"
										cx="12"
										cy="12"
										r="10"
										stroke="currentColor"
										stroke-width="4"
									></circle>
									<path
										class="opacity-75"
										fill="currentColor"
										d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
									></path>
								</svg>
							</span>
							<span v-if="!loading">Sign In</span>
							<span v-else>Signing in...</span>
						</button>
					</div>
				</form>

				<div class="mt-6">
					<div class="relative">
						<div class="absolute inset-0 flex items-center">
							<div class="w-full border-t border-gray-200"></div>
						</div>
						<div class="relative flex justify-center text-sm">
							<span
								class="px-2 bg-white text-gray-500 text-xs font-semibold uppercase tracking-wider"
							>
								Or continue with
							</span>
						</div>
					</div>

					<div class="mt-6 grid grid-cols-2 gap-3">
						<div>
							<button
								type="button"
								class="w-full inline-flex justify-center py-2.5 px-4 border border-gray-200 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 transition-colors"
							>
								<svg class="h-5 w-5" viewBox="0 0 24 24">
									<path
										d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
										fill="#4285F4"
									/>
									<path
										d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
										fill="#34A853"
									/>
									<path
										d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
										fill="#FBBC05"
									/>
									<path
										d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
										fill="#EA4335"
									/>
								</svg>
								<span class="ml-2">Google</span>
							</button>
						</div>

						<div>
							<button
								type="button"
								class="w-full inline-flex justify-center py-2.5 px-4 border border-gray-200 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 transition-colors"
							>
								<svg
									class="h-5 w-5 text-gray-900"
									fill="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										fill-rule="evenodd"
										d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
										clip-rule="evenodd"
									/>
								</svg>
								<span class="ml-2">GitHub</span>
							</button>
						</div>
					</div>
				</div>

				<div
					class="mt-8 flex items-center justify-center gap-2 text-xs text-gray-400 font-medium"
				>
					<FeatherIcon name="shield" class="h-3 w-3" />
					<span>Secure & Encrypted</span>
				</div>
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
		// Relying on session.login() to handle API calls
		await session.login(email.value, password.value)
		router.push('/')
	} catch (e) {
		// If session.login throws an error (e.g., 401), we catch it here
		error.value = e.message || 'Login failed. Please check your credentials.'
		console.error('Login error:', e)
	} finally {
		loading.value = false
	}
}
</script>
