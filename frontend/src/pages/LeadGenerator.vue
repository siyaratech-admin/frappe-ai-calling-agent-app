<template>
  <div class="flex h-full bg-gray-50 overflow-hidden relative rounded-2xl border border-gray-200">
    <!-- Mobile Filter Overlay -->
    <div
      v-if="showMobileFilters"
      class="fixed inset-0 bg-gray-900/50 z-20 lg:hidden backdrop-blur-sm transition-opacity"
      @click="showMobileFilters = false"
    ></div>

    <!-- Sidebar Filters -->
    <aside
       class="fixed lg:static inset-y-0 left-0 z-30 bg-white border-r border-gray-200 flex flex-col shadow-soft w-80 shrink-0 transition-transform duration-300 transform lg:transform-none"
       :class="showMobileFilters ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="p-6 border-b border-gray-100 flex justify-between items-center">
        <h2 class="text-lg font-bold text-gray-900 flex items-center gap-2">
           <div class="bg-primary-100 p-1.5 rounded-lg text-primary-600">
              <FeatherIcon name="filter" class="w-4 h-4" />
           </div>
           Filter Leads
        </h2>
        <button class="lg:hidden text-gray-500 hover:text-gray-700" @click="showMobileFilters = false">
           <FeatherIcon name="x" class="w-5 h-5" />
        </button>
      </div>
      
      <p class="px-6 text-xs text-gray-500 mt-4 lg:hidden">
         Refine your search criteria below.
      </p>

      <div class="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
        <div class="space-y-4">
          <div>
            <label class="block text-xs font-bold text-gray-700 uppercase mb-1.5 ml-1">Job Title</label>
            <div class="relative">
               <FeatherIcon name="briefcase" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
               <input
                 v-model="filters.job_title"
                 type="text"
                 placeholder="e.g. CEO, Founder"
                 class="w-full pl-9 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 transition-shadow"
                 :disabled="leads.loading"
               />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-700 uppercase mb-1.5 ml-1">Location</label>
            <div class="relative">
               <FeatherIcon name="map-pin" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
               <input
                 v-model="filters.location"
                 type="text"
                 placeholder="e.g. San Francisco, London"
                 class="w-full pl-9 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 transition-shadow"
                 :disabled="leads.loading"
               />
            </div>
          </div>

          <div>
             <label class="block text-xs font-bold text-gray-700 uppercase mb-1.5 ml-1">Industry</label>
            <div class="relative">
               <FeatherIcon name="globe" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
               <input
                 v-model="filters.industry"
                 type="text"
                 placeholder="e.g. SaaS, Healthcare"
                 class="w-full pl-9 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 transition-shadow"
                 :disabled="leads.loading"
               />
            </div>
          </div>
        </div>
      </div>

      <div class="p-6 border-t border-gray-100 bg-gray-50/50">
        <Button
          variant="solid"
          class="w-full justify-center py-3 !bg-primary-600 hover:!bg-primary-700 !text-white !rounded-xl shadow-lg shadow-primary-500/20 active:scale-95 transition-all text-sm font-bold"
          :loading="leads.loading"
          @click="searchLeads"
        >
          <template #prefix><FeatherIcon name="search" class="w-4 h-4" /></template>
          Find Leads
        </Button>
        <button 
           v-if="hasFilters" 
           @click="clearFilters" 
           class="w-full mt-3 text-xs font-medium text-gray-500 hover:text-primary-600 flex items-center justify-center gap-1 transition-colors"
        >
           <FeatherIcon name="x" class="w-3 h-3" /> Clear Filters
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col overflow-hidden relative w-full">
       <!-- Top Bar -->
       <div class="h-16 border-b border-gray-200 bg-white flex items-center justify-between px-4 md:px-8 z-10 shrink-0">
          <div class="flex items-center gap-3">
             <button class="lg:hidden p-2 -ml-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors" @click="showMobileFilters = true">
                <FeatherIcon name="filter" class="w-5 h-5" />
             </button>
             <h1 class="text-xl font-bold text-gray-900 truncate">Results <span v-if="leads.data?.length" class="text-gray-400 font-normal text-sm ml-2 hidden sm:inline">({{ leads.data.length }} found)</span></h1>
          </div>
          
          <div class="flex items-center gap-2" v-if="leads.data?.length">
              <span class="text-xs font-medium text-gray-500 mr-2 hidden sm:inline">Page {{ currentPage }}</span>
             <button 
                class="p-2 rounded-lg border border-gray-200 hover:bg-gray-50 text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                :disabled="currentPage === 1 || leads.loading"
                @click="changePage(-1)"
             >
                <FeatherIcon name="chevron-left" class="w-4 h-4" />
             </button>
             <button 
                class="p-2 rounded-lg border border-gray-200 hover:bg-gray-50 text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                :disabled="!leads.data || leads.data.length < 10 || leads.loading"
                @click="changePage(1)"
             >
                <FeatherIcon name="chevron-right" class="w-4 h-4" />
             </button>
          </div>
       </div>

      <div class="flex-1 overflow-y-auto p-4 md:p-8 relative custom-scrollbar">
        <!-- Empty State -->
        <div
          v-if="!leads.data && !leads.loading"
          class="h-full flex flex-col items-center justify-center text-center max-w-md mx-auto"
        >
          <div class="w-20 h-20 bg-primary-50 rounded-full flex items-center justify-center mb-6 animate-pulse">
            <FeatherIcon name="search" class="w-10 h-10 text-primary-400" />
          </div>
          <h3 class="text-xl font-bold text-gray-900 mb-2">Start Your Search</h3>
          <p class="text-gray-500 leading-relaxed">
            Use the filters on the left to discover verified B2B contacts. Access millions of leads powered by Apollo.io.
          </p>
        </div>

        <!-- Loading State -->
        <div v-else-if="leads.loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="i in 6"
            :key="i"
            class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm animate-pulse h-48 flex flex-col justify-between"
          >
            <div class="flex items-start gap-4">
              <div class="h-12 w-12 bg-gray-200 rounded-full shrink-0"></div>
              <div class="flex-1 space-y-2">
                <div class="h-4 bg-gray-200 rounded w-3/4"></div>
                <div class="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
            </div>
            <div class="h-8 bg-gray-100 rounded-lg w-full mt-4"></div>
          </div>
        </div>

        <!-- Results Grid -->
        <div v-else class="grid grid-cols-1 xl:grid-cols-2 gap-6 pb-20">
          <div
            v-for="lead in leads.data"
            :key="lead.id"
            @click="openLeadDetails(lead)"
            class="group bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg hover:border-primary-200 hover:-translate-y-1 transition-all duration-300 cursor-pointer relative overflow-hidden"
          >
             <div class="absolute top-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity">
                <FeatherIcon name="arrow-up-right" class="w-5 h-5 text-primary-500" />
             </div>
             
            <div class="flex items-start gap-5">
              <div
                class="w-14 h-14 rounded-full bg-gradient-to-br from-primary-50 to-indigo-100 text-primary-700 flex items-center justify-center font-bold text-lg shadow-inner border border-white shrink-0"
              >
                {{ getInitials(lead.name) }}
              </div>

              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-1">
                  <h4 class="font-bold text-lg text-gray-900 truncate group-hover:text-primary-600 transition-colors">
                    {{ lead.name }}
                  </h4>
                  <Badge v-if="lead.is_saved" theme="green" variant="subtle" size="sm" class="shrink-0 flex items-center gap-1">
                     <FeatherIcon name="check" class="w-3 h-3" /> Saved
                  </Badge>
                </div>
                
                <p class="text-sm font-medium text-primary-600 truncate mb-3">{{ lead.title || 'Unknown Title' }}</p>

                 <div class="flex flex-wrap gap-y-2 gap-x-4 text-xs text-gray-500">
                    <div v-if="lead.company" class="flex items-center gap-1.5 bg-gray-50 px-2 py-1 rounded border border-gray-100">
                       <FeatherIcon name="briefcase" class="w-3 h-3 text-gray-400" />
                       <span class="truncate max-w-[120px]">{{ lead.company }}</span>
                    </div>
                    <div v-if="lead.location" class="flex items-center gap-1.5 bg-gray-50 px-2 py-1 rounded border border-gray-100">
                       <FeatherIcon name="map-pin" class="w-3 h-3 text-gray-400" />
                       <span class="truncate max-w-[120px]">{{ lead.location }}</span>
                    </div>
                 </div>
              </div>
            </div>
            
             <div class="mt-5 pt-4 border-t border-gray-100 flex justify-between items-center">
                <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Apollo Verified</span>
                <span class="text-xs text-primary-600 font-medium group-hover:underline">View Profile</span>
             </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Details Modal -->
    <Dialog v-model="showDetailsDialog" :options="{ size: 'xl' }">
      <template #body-title>
         <h3 class="text-xl font-bold flex items-center gap-2">
            <div class="p-1.5 bg-primary-100 rounded-lg text-primary-600"><FeatherIcon name="user-plus" class="w-5 h-5" /></div>
            Verified Profile
         </h3>
      </template>
      <template #body-content>
        <div v-if="selectedLead" class="mt-6">
          <div class="text-center mb-8">
             <div class="w-24 h-24 rounded-full bg-gray-100 mx-auto flex items-center justify-center text-3xl font-bold text-gray-400 mb-4 border-4 border-white shadow-lg">
                {{ getInitials(selectedLead.name) }}
             </div>
             <h2 class="text-2xl font-bold text-gray-900">{{ selectedLead.name }}</h2>
             <p class="text-lg text-gray-500 font-medium">{{ selectedLead.title }}</p>
          </div>

          <div class="bg-gray-50 rounded-2xl p-6 border border-gray-200 grid grid-cols-1 md:grid-cols-2 gap-8 relative overflow-hidden">
             <!-- Background decoration -->
             <div class="absolute -right-10 -bottom-10 w-40 h-40 bg-indigo-50 rounded-full opacity-50 pointer-events-none"></div>
             
             <div class="relative z-10">
                <label class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 block">Organization</label>
                <div class="flex items-center gap-3">
                   <div class="p-2 bg-white rounded-lg shadow-sm">
                      <FeatherIcon name="briefcase" class="w-5 h-5 text-gray-600" />
                   </div>
                   <span class="font-bold text-gray-900 text-lg">{{ selectedLead.company || 'N/A' }}</span>
                </div>
             </div>
             
             <div class="relative z-10">
                <label class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 block">Location</label>
                <div class="flex items-center gap-3">
                   <div class="p-2 bg-white rounded-lg shadow-sm">
                      <FeatherIcon name="map-pin" class="w-5 h-5 text-gray-600" />
                   </div>
                   <span class="font-bold text-gray-900 text-lg">{{ selectedLead.location || 'N/A' }}</span>
                </div>
             </div>
          </div>

          <div class="mt-8 bg-blue-50 border border-blue-100 rounded-xl p-4 flex items-start gap-3">
             <FeatherIcon name="info" class="w-5 h-5 text-blue-600 mt-0.5 shrink-0" />
             <div>
                <h4 class="font-bold text-blue-900 text-sm">Credit Usage Info</h4>
                <p class="text-sm text-blue-700 mt-1">
                   Clicking <strong>"Reveal & Save"</strong> will deduct <strong>1 credit</strong> from your Apollo quota to fetch verified email/phone data and add this contact to your CRM.
                </p>
             </div>
          </div>
        </div>
      </template>
      <template #actions>
        <div class="flex justify-between w-full">
           <Button variant="subtle" @click="showDetailsDialog = false">Cancel</Button>
           
           <Button
             v-if="!selectedLead?.is_saved"
             variant="solid"
             class="!bg-primary-600 hover:!bg-primary-700 !text-white !rounded-xl !px-6 shadow-lg shadow-primary-500/20"
             :loading="savingId === selectedLead?.id"
             @click="saveLead(selectedLead)"
           >
             <template #prefix><FeatherIcon name="download-cloud" class="w-4 h-4" /></template>
             Reveal & Save Contact
           </Button>
           <Button v-else variant="outline" class="!bg-green-50 !text-green-700 !border-green-200 cursor-default">
             <template #prefix><FeatherIcon name="check" class="w-4 h-4" /></template>
             Saved to CRM
           </Button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { createResource, Button, Badge, FeatherIcon, Dialog } from 'frappe-ui'

// State
const filters = ref({
	job_title: '',
	location: '',
	industry: '',
})
const currentPage = ref(1)
const savingId = ref(null)
const showDetailsDialog = ref(false)
const selectedLead = ref(null)
const showMobileFilters = ref(false)

onMounted(() => {
	document.title = 'Lead Generator'
})

// Computed
const hasFilters = computed(() => {
	return filters.value.job_title || filters.value.location || filters.value.industry
})

// Resources
const leads = createResource({
	url: 'ai_calling_agent.api.search_apollo_leads',
	makeParams(values) {
		return {
			job_title: filters.value.job_title,
			location: filters.value.location,
			industry: filters.value.industry,
			page: currentPage.value,
			per_page: 10,
		}
	},
	onSuccess(data) {
		return data.map((l) => ({ ...l, is_saved: false }))
	},
})

// Actions
function searchLeads() {
	if (!hasFilters.value) return
	currentPage.value = 1
	leads.fetch()
}

function changePage(delta) {
	currentPage.value += delta
	leads.fetch()
}

function clearFilters() {
	filters.value = { job_title: '', location: '', industry: '' }
	currentPage.value = 1
	leads.reset()
}

function openLeadDetails(lead) {
	selectedLead.value = lead
	showDetailsDialog.value = true
}

function getInitials(name) {
	if (!name) return '?'
	return name
		.split(' ')
		.map((n) => n[0])
		.join('')
		.toUpperCase()
		.slice(0, 2)
}

async function saveLead(lead) {
	savingId.value = lead.id
	try {
		const res = await fetch('/api/method/ai_calling_agent.api.save_apollo_lead', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ apollo_id: lead.id }),
		})

		const data = await res.json()

		if (res.ok) {
			lead.is_saved = true
			if (selectedLead.value && selectedLead.value.id === lead.id) {
				selectedLead.value.is_saved = true
			}
		} else {
			alert(data.message || 'Failed to save lead')
		}
	} catch (error) {
		console.error(error)
		alert('An error occurred')
	} finally {
		savingId.value = null
	}
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #e5e7eb;
  border-radius: 4px;
}
</style>
