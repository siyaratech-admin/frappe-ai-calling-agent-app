<template>
  <div v-if="session.isLoggedIn" class="flex h-screen w-full bg-gray-50 font-sans overflow-hidden">
    <!-- Mobile Sidebar Overlay -->
    <div
      v-if="showMobileSidebar"
      class="fixed inset-0 bg-gray-900/50 z-20 md:hidden backdrop-blur-sm transition-opacity"
      @click="showMobileSidebar = false"
    ></div>

    <!-- Sidebar -->
    <aside
      class="fixed md:static inset-y-0 left-0 z-30 bg-white border-r border-gray-100 flex flex-col transition-all duration-300 ease-in-out shadow-[4px_0_24px_rgba(0,0,0,0.02)] h-full"
      :class="[
        isCollapsed ? 'w-20' : 'w-72',
        showMobileSidebar ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
      ]"
    >
      <!-- Logo Area -->
      <div
        class="h-20 flex items-center relative flex-shrink-0"
        :class="isCollapsed ? 'justify-center px-0' : 'justify-between px-6'"
      >
        <div class="flex items-center overflow-hidden whitespace-nowrap">
          <div
            class="w-10 h-10 bg-gradient-to-br from-primary-600 to-primary-700 rounded-xl flex-shrink-0 flex items-center justify-center shadow-lg shadow-primary-500/20"
          >
            <FeatherIcon name="cpu" class="w-5 h-5 text-white" />
          </div>
          <div
            class="ml-3 flex flex-col transition-opacity duration-200"
            :class="isCollapsed ? 'opacity-0 w-0 hidden' : 'opacity-100'"
          >
            <span class="text-lg font-bold text-gray-900 tracking-tight leading-none">AI Agent</span>
            <span class="text-[10px] text-gray-400 font-medium uppercase tracking-wider mt-0.5">Workspace</span>
          </div>
        </div>

        <button
          @click="toggleSidebar"
          class="w-6 h-6 rounded-full bg-white border border-gray-200 flex items-center justify-center text-gray-400 hover:text-primary-600 shadow-sm absolute -right-3 top-9 z-50 transition-transform hidden md:flex"
           :class="isCollapsed ? 'rotate-180' : ''"
        >
          <FeatherIcon name="chevron-left" class="w-3 h-3" />
        </button>
        
        <!-- Mobile Close Button -->
        <button
          @click="showMobileSidebar = false"
          class="md:hidden p-1 text-gray-400 hover:text-gray-600"
        >
           <FeatherIcon name="x" class="w-5 h-5" />
        </button>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto custom-scrollbar overflow-x-hidden">
         <div v-if="!isCollapsed" class="px-2 mb-2 text-xs font-semibold text-gray-400 uppercase tracking-wider">Menu</div>
        <router-link
          v-for="item in navItems"
          :key="item.name"
          :to="item.path"
          class="flex items-center px-3 py-3 text-sm font-medium rounded-xl transition-all duration-200 group whitespace-nowrap relative"
          :class="[
            $route.path === item.path
              ? 'bg-primary-50 text-primary-700 shadow-sm'
              : 'text-gray-500 hover:bg-gray-50 hover:text-gray-900',
            isCollapsed ? 'justify-center' : '',
          ]"
          @click="showMobileSidebar = false"
        >
          <div class="relative flex items-center justify-center">
             <FeatherIcon
               :name="item.icon"
               class="w-[22px] h-[22px] transition-colors flex-shrink-0"
               :class="[
                 $route.path === item.path ? 'text-primary-600' : 'text-gray-400 group-hover:text-gray-600',
               ]"
             />
             <span v-if="isCollapsed && $route.path === item.path" class="absolute -right-2 top-0 w-2 h-2 bg-primary-500 rounded-full border-2 border-white"></span>
          </div>

          <span
            class="ml-3 transition-opacity duration-200"
            :class="isCollapsed ? 'w-0 opacity-0 hidden' : 'w-auto opacity-100'"
          >
            {{ item.label }}
          </span>

          <!-- Tooltip for collapsed state -->
          <div
            v-if="isCollapsed"
            class="absolute left-full ml-4 bg-gray-900 text-white text-xs px-2.5 py-1.5 rounded-md shadow-xl opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 whitespace-nowrap pointer-events-none hidden md:block"
          >
            {{ item.label }}
             <div class="absolute top-1/2 -left-1 -mt-1 border-4 border-transparent border-r-gray-900"></div>
          </div>
        </router-link>
      </nav>

      <!-- User Profile -->
      <div class="p-4 border-t border-gray-100 bg-white z-20 flex-shrink-0">
        <button
          class="flex items-center w-full hover:bg-gray-50 p-2 rounded-xl transition-all duration-200 group relative outline-none focus:ring-2 focus:ring-primary-100"
          :class="isCollapsed ? 'justify-center' : ''"
          @click="session.logout"
        >
          <div class="relative">
             <div
               class="w-10 h-10 rounded-full bg-gradient-to-tr from-primary-100 to-indigo-100 border-2 border-white shadow-sm flex items-center justify-center text-sm font-bold text-primary-700 flex-shrink-0"
             >
               {{ session.user ? session.user.substring(0, 2).toUpperCase() : 'U' }}
             </div>
             <div class="absolute bottom-0 right-0 w-3 h-3 bg-green-500 border-2 border-white rounded-full"></div>
          </div>

          <div
            class="ml-3 text-left overflow-hidden transition-all duration-200"
            :class="isCollapsed ? 'w-0 opacity-0 hidden' : 'w-auto opacity-100 block'"
          >
            <p class="text-sm font-semibold text-gray-800 truncate leading-snug">
              {{ session.user }}
            </p>
            <p class="text-xs text-gray-400 font-medium group-hover:text-red-500 transition-colors">Tap to logout</p>
          </div>
           
           <!-- Tooltip for collapsed state -->
          <div
            v-if="isCollapsed"
            class="absolute left-full ml-4 bg-gray-900 text-white text-xs px-2.5 py-1.5 rounded-md shadow-xl opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 whitespace-nowrap pointer-events-none hidden md:block"
          >
            Logout
             <div class="absolute top-1/2 -left-1 -mt-1 border-4 border-transparent border-r-gray-900"></div>
          </div>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50/50 relative w-full h-full flex flex-col">
       <!-- Top decorative bar -->
       <div class="sticky top-0 z-10 h-16 bg-white/80 backdrop-blur-md border-b border-gray-100 flex items-center justify-between px-4 md:px-8 flex-shrink-0">
          <div class="flex items-center gap-3">
             <button
               @click="showMobileSidebar = true"
               class="md:hidden p-2 -ml-2 text-gray-600 hover:bg-gray-100 rounded-lg active:bg-gray-200 transition-colors"
             >
                <FeatherIcon name="menu" class="w-5 h-5" />
             </button>
             <h2 class="text-xl font-bold text-gray-800 tracking-tight">{{ $route.meta.title || 'Dashboard' }}</h2>
          </div>
          
          <div class="flex items-center gap-2 md:gap-4">
             <button class="p-2 text-gray-400 hover:text-gray-600 transition-colors relative">
                <FeatherIcon name="bell" class="w-5 h-5" />
                <span class="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border border-white"></span>
             </button>
             <button class="p-2 text-gray-400 hover:text-gray-600 transition-colors hidden sm:block">
                <FeatherIcon name="help-circle" class="w-5 h-5" />
             </button>
          </div>
       </div>
       
       <div class="p-4 md:p-8 flex-1 overflow-y-auto w-full">
          <router-view />
       </div>
    </main>
  </div>

  <div v-else class="h-screen w-full font-sans antialiased text-gray-900 bg-white">
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
const showMobileSidebar = ref(false)

function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
}

const navItems = [
  { name: 'Home', path: '/', label: 'Dashboard', icon: 'home' },
  { name: 'LeadGenerator', path: '/lead-generator', label: 'Lead Generator', icon: 'search' },
  { name: 'Contacts', path: '/contacts', label: 'Contacts', icon: 'users' },
  { name: 'BulkCalling', path: '/bulk-calling', label: 'Bulk Calling', icon: 'phone-call' },
  { name: 'BulkEmailing', path: '/bulk-emailing', label: 'Bulk Emailing', icon: 'mail' },
  { name: 'CallLogs', path: '/call-logs', label: 'Call Logs', icon: 'list' },
]
</script>

<style>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #f1f1f1;
  border-radius: 4px;
}
.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: #d1d5db;
}
</style>
