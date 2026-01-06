<template>
	<div v-if="session.isLoggedIn" class="flex h-screen w-full bg-gray-50">
		<div
			class="flex-shrink-0 bg-white border-r border-gray-200 flex flex-col transition-all duration-300 ease-in-out relative z-20"
			:class="isCollapsed ? 'w-20' : 'w-64'"
		>
			<div
				class="h-16 flex items-center border-b border-gray-100 relative bg-white z-20"
				:class="isCollapsed ? 'justify-center px-0' : 'justify-between px-5'"
			>
				<div class="flex items-center overflow-hidden whitespace-nowrap">
					<div
						class="w-8 h-8 bg-[#4318FF] rounded-lg flex-shrink-0 flex items-center justify-center shadow-sm transition-all"
					>
						<FeatherIcon name="cpu" class="w-5 h-5 text-white" />
					</div>
					<span
						class="ml-3 text-lg font-bold text-gray-900 tracking-tight transition-opacity duration-200"
						:class="isCollapsed ? 'opacity-0 w-0 hidden' : 'opacity-100'"
					>
						AI Agent
					</span>
				</div>

				<button
					@click="toggleSidebar"
					class="p-1.5 rounded-md text-gray-400 hover:text-[#4318FF] hover:bg-[#4318FF]/5 transition-colors"
					:class="
						isCollapsed
							? 'absolute inset-0 w-full h-full flex items-center justify-center opacity-0 hover:opacity-100 z-10'
							: ''
					"
					title="Toggle Sidebar"
				>
					<FeatherIcon name="sidebar" class="w-4 h-4" />
				</button>
			</div>

			<nav class="flex-1 p-3 space-y-1">
				<router-link
					v-for="item in navItems"
					:key="item.name"
					:to="item.path"
					class="flex items-center px-3 py-2 text-sm font-medium rounded-md transition-all duration-200 group whitespace-nowrap relative"
					:class="[
						$route.path === item.path
							? 'bg-[#4318FF]/10 text-[#4318FF] shadow-none' // CHANGE 2: Active State using Accent
							: 'text-gray-600 hover:bg-gray-50 hover:text-gray-900',
						isCollapsed ? 'justify-center' : '',
					]"
				>
					<FeatherIcon
						:name="item.icon"
						class="w-5 h-5 transition-colors flex-shrink-0"
						:class="[
							$route.path === item.path
								? 'text-[#4318FF]' // Active Icon
								: 'text-gray-400 group-hover:text-gray-600',
							isCollapsed ? '' : 'mr-3',
						]"
					/>

					<span
						class="transition-all duration-200 overflow-hidden"
						:class="isCollapsed ? 'w-0 opacity-0' : 'w-auto opacity-100'"
					>
						{{ item.label }}
					</span>

					<div
						v-if="isCollapsed"
						class="absolute left-full ml-6 bg-gray-900 text-white text-xs px-3 py-1.5 rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 whitespace-nowrap pointer-events-none"
					>
						{{ item.label }}
						<div
							class="absolute top-1/2 -left-1 -mt-1 border-4 border-transparent border-r-gray-900"
						></div>
					</div>
				</router-link>
			</nav>

			<div class="p-4 border-t border-gray-200 overflow-hidden bg-white z-20">
				<button
					class="flex items-center w-full hover:bg-gray-50 p-2 rounded-md transition-colors whitespace-nowrap relative group"
					:class="isCollapsed ? 'justify-center' : ''"
					@click="session.logout"
				>
					<div
						class="w-8 h-8 rounded-full bg-[#4318FF]/10 border border-[#4318FF]/20 flex items-center justify-center text-xs font-bold text-[#4318FF] flex-shrink-0"
					>
						{{ session.user ? session.user.substring(0, 2).toUpperCase() : 'U' }}
					</div>

					<div
						class="ml-3 text-left overflow-hidden transition-all duration-200"
						:class="isCollapsed ? 'w-0 opacity-0 hidden' : 'w-auto opacity-100 block'"
					>
						<p class="text-sm font-medium text-gray-700 truncate">
							{{ session.user }}
						</p>
						<p class="text-xs text-gray-400 group-hover:text-[#4318FF]">Log out</p>
					</div>

					<div
						v-if="isCollapsed"
						class="absolute left-full ml-6 bg-gray-900 text-white text-xs px-3 py-1.5 rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 whitespace-nowrap pointer-events-none"
					>
						Log out
						<div
							class="absolute top-1/2 -left-1 -mt-1 border-4 border-transparent border-r-gray-900"
						></div>
					</div>
				</button>
			</div>
		</div>

		<div class="flex-1 overflow-auto bg-white">
			<router-view />
		</div>
	</div>

	<div v-else class="h-screen w-full">
		<router-view />
	</div>
</template>

<script setup>
import { ref } from 'vue'
import { session } from './data/session'
import { useRoute } from 'vue-router'
import { FeatherIcon } from 'frappe-ui'

const route = useRoute()
const isCollapsed = ref(false)

function toggleSidebar() {
	isCollapsed.value = !isCollapsed.value
}

const navItems = [
	{ name: 'Home', path: '/', label: 'Dashboard', icon: 'home' },
	{ name: 'LeadGenerator', path: '/lead-generator', label: 'Lead Generator', icon: 'search' },
	{ name: 'Contacts', path: '/contacts', label: 'Contacts', icon: 'users' },
	{ name: 'BulkCalling', path: '/bulk-calling', label: 'Bulk Calling', icon: 'layers' },
	{ name: 'BulkEmailing', path: '/bulk-emailing', label: 'Bulk Emailing', icon: 'mail' },
	{ name: 'CallLogs', path: '/call-logs', label: 'Call Logs', icon: 'phone' },
]
</script>
