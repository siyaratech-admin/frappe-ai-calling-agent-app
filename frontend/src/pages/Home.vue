<template>
  <div class="max-w-7xl mx-auto space-y-8">
    <!-- Header -->
    <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Dashboard Overview</h1>
        <p class="text-gray-500 mt-1">Track your AI agent's performance and recent activity.</p>
      </div>
      <div class="flex items-center gap-3">
         <span class="text-xs font-medium text-gray-500 bg-white px-3 py-1.5 rounded-full border border-gray-200 shadow-sm">
            Last updated: {{ new Date().toLocaleTimeString() }}
         </span>
        <Button
          variant="solid"
          class="!bg-primary-600 hover:!bg-primary-700 !text-white !border-transparent !rounded-xl !shadow-lg shadow-primary-500/20 active:!scale-95 transition-all"
          @click="logs.fetch()"
        >
          <template #prefix><FeatherIcon name="refresh-cw" class="h-4 w-4" /></template>
          Refresh Data
        </Button>
      </div>
    </header>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-2xl shadow-soft border border-gray-100 relative overflow-hidden group">
        <div class="absolute right-0 top-0 w-32 h-32 bg-primary-50 rounded-full -mr-10 -mt-10 transition-transform group-hover:scale-110"></div>
        <div class="relative z-10">
          <div class="flex items-center gap-3 mb-2">
            <div class="p-2 bg-primary-100 rounded-lg text-primary-600">
               <FeatherIcon name="phone" class="h-5 w-5" />
            </div>
            <span class="text-xs font-semibold text-gray-500 uppercase tracking-wider">Total Calls</span>
          </div>
          <div class="text-4xl font-bold text-gray-900 mt-2">{{ logs.data?.length || 0 }}</div>
          <div class="mt-2 flex items-center text-xs text-green-600 font-medium">
             <FeatherIcon name="trending-up" class="w-3 h-3 mr-1" />
             <span>+12% from last week</span>
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-2xl shadow-soft border border-gray-100 relative overflow-hidden group">
        <div class="absolute right-0 top-0 w-32 h-32 bg-green-50 rounded-full -mr-10 -mt-10 transition-transform group-hover:scale-110"></div>
        <div class="relative z-10">
           <div class="flex items-center gap-3 mb-2">
            <div class="p-2 bg-green-100 rounded-lg text-green-600">
               <FeatherIcon name="check-circle" class="h-5 w-5" />
            </div>
            <span class="text-xs font-semibold text-gray-500 uppercase tracking-wider">Hot Leads</span>
          </div>
          <div class="text-4xl font-bold text-gray-900 mt-2">
            {{ logs.data?.filter((l) => l.lead_status === 'Hot').length || 0 }}
          </div>
          <div class="mt-2 text-xs text-gray-400">
             High potential conversions
          </div>
        </div>
      </div>

       <div class="bg-white p-6 rounded-2xl shadow-soft border border-gray-100 relative overflow-hidden group">
        <div class="absolute right-0 top-0 w-32 h-32 bg-indigo-50 rounded-full -mr-10 -mt-10 transition-transform group-hover:scale-110"></div>
        <div class="relative z-10">
           <div class="flex items-center gap-3 mb-2">
            <div class="p-2 bg-indigo-100 rounded-lg text-indigo-600">
               <FeatherIcon name="clock" class="h-5 w-5" />
            </div>
            <span class="text-xs font-semibold text-gray-500 uppercase tracking-wider">Avg Duration</span>
          </div>
          <div class="text-4xl font-bold text-gray-900 mt-2">
            {{ calculateAvgDuration(logs.data) }}
          </div>
          <div class="mt-2 text-xs text-gray-400">
             Per successful connection
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Activity Chart -->
      <div class="bg-white p-6 rounded-2xl shadow-soft border border-gray-100">
        <div class="flex items-center justify-between mb-6">
           <h3 class="text-lg font-bold text-gray-800">Weekly Activity</h3>
           <Button variant="ghost" class="text-xs bg-gray-50 hover:bg-gray-100 text-gray-500 font-medium !px-3 rounded-md">
              Last 7 Days
              <template #suffix>
                 <FeatherIcon name="chevron-down" class="w-3 h-3 ml-2" />
              </template>
           </Button>
        </div>
        
        <div class="h-64 flex items-end gap-3 justify-between px-2">
          <div
            v-for="(day, index) in dailyActivity"
            :key="index"
            class="flex flex-col items-center gap-3 group flex-1 h-full justify-end"
          >
            <div class="relative w-full flex justify-center items-end bg-gray-50 rounded-xl overflow-hidden h-full">
               <div class="absolute bottom-0 w-full bg-primary-100/30 h-full rounded-xl"></div>
              <div
                class="w-full mx-1.5 bg-gradient-to-t from-primary-600 to-primary-500 rounded-t-lg transition-all duration-500 relative group-hover:to-primary-400"
                :style="{ height: `${Math.max(day.percentage, 5)}%` }"
              ></div>
              
              <!-- Tooltip -->
              <div
                class="absolute bottom-full mb-2 bg-gray-900 text-white text-[10px] py-1 px-2 rounded-md opacity-0 group-hover:opacity-100 transition-all transform translate-y-2 group-hover:translate-y-0 z-10 whitespace-nowrap shadow-xl"
              >
                {{ day.count }} calls
                <div class="absolute -bottom-1 left-1/2 -ml-1 border-4 border-transparent border-t-gray-900"></div>
              </div>
            </div>
            <span class="text-[10px] uppercase font-bold text-gray-400 rotate-0 truncate w-full text-center tracking-wider">
              {{ day.label }}
            </span>
          </div>

          <div v-if="dailyActivity.length === 0" class="w-full h-full flex flex-col items-center justify-center text-gray-400">
             <FeatherIcon name="bar-chart-2" class="w-8 h-8 opacity-20 mb-2" />
             <span class="text-sm">No activity data yet</span>
          </div>
        </div>
      </div>

      <!-- Lead Status Distribution -->
      <div class="bg-white p-6 rounded-2xl shadow-soft border border-gray-100 flex flex-col">
        <h3 class="text-lg font-bold text-gray-800 mb-6">Lead Quality</h3>
        <div class="space-y-5 flex-1 overflow-y-auto pr-2 custom-scrollbar">
          <div v-for="(stat, index) in statusDistribution" :key="index" class="group">
            <div class="flex justify-between text-sm mb-2">
              <span class="font-medium text-gray-700 flex items-center">
                 <span class="w-2 h-2 rounded-full mr-2" :class="stat.dotClass"></span>
                 {{ stat.label }}
              </span>
              <span class="text-gray-500 font-mono text-xs bg-gray-50 px-1.5 py-0.5 rounded">{{ stat.count }}</span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-2 overflow-hidden shadow-inner">
              <div
                class="h-full rounded-full transition-all duration-1000 ease-out relative overflow-hidden"
                :class="stat.colorClass"
                :style="{ width: `${stat.percentage}%` }"
              >
                 <div class="absolute inset-0 bg-white/20 w-full h-full animate-[shimmer_2s_infinite]"></div>
              </div>
            </div>
          </div>
           
           <div v-if="statusDistribution.length === 0" class="flex-1 flex flex-col items-center justify-center text-gray-400">
             <FeatherIcon name="pie-chart" class="w-8 h-8 opacity-20 mb-2" />
             <span class="text-sm">No lead data available</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Logs -->
    <div class="bg-white rounded-2xl shadow-soft border border-gray-100 overflow-hidden">
      <div class="px-6 py-5 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
        <div>
           <h3 class="text-lg font-bold text-gray-900">Recent Calls</h3>
           <p class="text-xs text-gray-500 mt-0.5">Real-time update of agent interactions</p>
        </div>
        <Button variant="subtle" size="sm" @click="$router.push('/call-logs')">
           View All
           <template #suffix><FeatherIcon name="arrow-right" class="w-3 h-3" /></template>
        </Button>
      </div>

      <div v-if="logs.loading && !logs.data" class="p-12 text-center text-gray-400">
         <div class="animate-pulse flex flex-col items-center">
            <div class="h-4 w-48 bg-gray-200 rounded mb-3"></div>
            <div class="h-3 w-32 bg-gray-100 rounded"></div>
         </div>
      </div>

      <div v-else-if="logs.data && logs.data.length === 0" class="p-16 text-center text-gray-400">
         <FeatherIcon name="phone-off" class="w-10 h-10 mx-auto opacity-20 mb-3" />
        <p>No calls have been made yet.</p>
      </div>

      <div v-else class="divide-y divide-gray-50">
        <div
          v-for="log in logs.data"
          :key="log.name"
          @click="openLogDetails(log)"
          class="px-6 py-4 hover:bg-gray-50/80 transition-all cursor-pointer group relative"
        >
           <div class="absolute left-0 top-0 bottom-0 w-[3px] bg-primary-500 opacity-0 group-hover:opacity-100 transition-opacity"></div>
           
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <!-- Left: Contact Info -->
             <div class="flex items-start gap-4">
                <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-500 font-bold text-xs shadow-sm border border-white">
                   <FeatherIcon name="user" class="w-4 h-4" />
                </div>
                <div>
                   <div class="flex items-center gap-2">
                      <h4 class="font-bold text-gray-900 group-hover:text-primary-600 transition-colors">{{ log.phone_number }}</h4>
                      <span class="px-1.5 py-0.5 rounded text-[10px] font-medium bg-gray-100 text-gray-600 border border-gray-200">{{ log.party || 'Unknown' }}</span>
                   </div>
                   <div class="flex items-center gap-3 text-xs text-gray-400 mt-1">
                      <span class="flex items-center"><FeatherIcon name="calendar" class="w-3 h-3 mr-1" /> {{ formatDateTime(log.creation) }}</span>
                      <span class="flex items-center"><FeatherIcon name="clock" class="w-3 h-3 mr-1" /> {{ formatDuration(log.duration) }}</span>
                   </div>
                </div>
             </div>
             
             <!-- Right: Status & Summary -->
             <div class="flex items-center gap-4">
                <div class="flex flex-col items-end gap-1">
                   <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold border"
                      :class="getBadgeClasses(log.lead_status)"
                   >
                      {{ log.lead_status || 'Unknown' }}
                   </span>
                   <span class="text-[10px] text-gray-400 uppercase tracking-widest">{{ log.call_status }}</span>
                </div>
                <FeatherIcon name="chevron-right" class="w-5 h-5 text-gray-300 group-hover:text-primary-500 transform group-hover:translate-x-1 transition-all" />
             </div>
          </div>
          
           <!-- AI Summary Snippet -->
           <div v-if="log.ai_summary" class="mt-3 ml-14 bg-gray-50 p-2.5 rounded-lg border border-gray-100 text-xs text-gray-600 leading-relaxed italic relative">
               <div class="absolute -top-1 left-4 w-2 h-2 bg-gray-50 border-t border-l border-gray-100 transform rotate-45"></div>
              "{{ stripHtml(log.ai_summary) }}"
           </div>
        </div>
      </div>
       
       <div class="p-4 bg-gray-50 border-t border-gray-100 flex justify-center">
          <Button
             v-if="logs.data?.length >= currentLimit"
             variant="ghost"
             :loading="logs.loading"
             @click="loadMore"
             class="text-gray-500 hover:text-primary-600 hover:bg-white border hover:border-gray-200 transition-all"
          >
             Load More History
          </Button>
       </div>
    </div>

    <!-- Modals -->
    <Dialog v-model="showLogDialog" :options="{ size: '2xl' }">
			<template #body-title>
				<h3 class="text-xl font-bold flex items-center gap-2">
               <div class="w-8 h-8 rounded-lg bg-primary-100 flex items-center justify-center text-primary-600">
                  <FeatherIcon name="phone-call" class="w-4 h-4" />
               </div>
               Call Details
            </h3>
			</template>
			<template #body-content>
				<div v-if="selectedLog" class="mt-6 space-y-8">
               <!-- Key Details Cards -->
					<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div class="bg-gray-50 p-4 rounded-xl border border-gray-200/60">
                     <span class="text-xs font-bold text-gray-400 uppercase tracking-wider block mb-1">Contact</span>
                     <div class="font-bold text-gray-900">{{ selectedLog.phone_number }}</div>
                     <div class="text-xs text-primary-600 mt-1">{{ selectedLog.party }}</div>
                  </div>
                   <div class="bg-gray-50 p-4 rounded-xl border border-gray-200/60">
                     <span class="text-xs font-bold text-gray-400 uppercase tracking-wider block mb-1">Duration</span>
                     <div class="font-bold text-gray-900">{{ formatDuration(selectedLog.duration) }}</div>
                     <div class="text-xs text-gray-500 mt-1">{{ formatDateTime(selectedLog.creation) }}</div>
                  </div>
                   <div class="bg-gray-50 p-4 rounded-xl border border-gray-200/60">
                     <span class="text-xs font-bold text-gray-400 uppercase tracking-wider block mb-1">Outcome</span>
                     <div class="flex items-center gap-2 mt-1">
                        <span class="px-2 py-0.5 rounded text-xs font-bold bg-white border shadow-sm" :class="getBadgeClasses(selectedLog.lead_status)">
                           {{ selectedLog.lead_status }}
                        </span>
                     </div>
                  </div>
					</div>

               <!-- Audio Player -->
					<div v-if="selectedLog.recording_url" class="p-4 rounded-xl border border-gray-200 bg-white shadow-sm">
						<label class="text-sm font-bold text-gray-700 mb-3 flex items-center gap-2">
							<FeatherIcon name="mic" class="w-4 h-4 text-primary-500" /> Recording
						</label>
						<audio controls :src="selectedLog.recording_url" class="w-full h-10 rounded shadow-inner bg-gray-100"></audio>
					</div>

               <!-- Status Editors -->
					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Lead Status</label>
							<select
								v-model="selectedLog.lead_status"
								class="block w-full rounded-lg border-gray-200 bg-gray-50 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm py-2.5 transition-shadow"
							>
								<option value="Hot">🔥 Hot Lead</option>
								<option value="Warm">⛅ Warm Lead</option>
								<option value="Cold">❄️ Cold Lead</option>
								<option value="Negative">⛔ Negative</option>
								<option value="Not a Lead">🤷‍♂️ Not a Lead</option>
							</select>
						</div>
                  <div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Call Status</label>
							<select
								v-model="selectedLog.call_status"
								class="block w-full rounded-lg border-gray-200 bg-gray-50 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm py-2.5 transition-shadow"
							>
								<option value="Completed">Completed</option>
								<option value="No Answer">No Answer</option>
								<option value="Failed">Failed</option>
                        <option value="Busy">Busy</option>
							</select>
						</div>
					</div>

               <!-- AI Summary -->
					<div class="bg-indigo-50/50 p-5 rounded-xl border border-indigo-100">
						<div class="flex justify-between items-center mb-3">
							<label class="text-sm font-bold text-indigo-900 flex items-center gap-2">
								<FeatherIcon name="cpu" class="w-4 h-4 text-indigo-600" /> AI Insights
							</label>
							<button
								@click="isSummaryRawMode = !isSummaryRawMode"
								class="text-xs text-indigo-600 hover:text-indigo-800 font-medium underline"
							>
								{{ isSummaryRawMode ? 'Preview' : 'Edit' }}
							</button>
						</div>
						<div
							v-if="!isSummaryRawMode"
							class="text-sm text-indigo-900/80 leading-relaxed prose-indigo max-w-none"
							v-html="renderMarkdown(selectedLog.ai_summary)"
						></div>
						<textarea
							v-else
							v-model="selectedLog.ai_summary"
							rows="4"
							class="w-full rounded-lg border-indigo-200 bg-white px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500"
						></textarea>
					</div>

               <!-- Transcription -->
					<div>
						<div class="flex justify-between items-center mb-3">
							<label class="text-sm font-bold text-gray-700">Full Transcription</label>
							<button
								@click="isRawMode = !isRawMode"
								class="text-xs text-gray-500 hover:text-gray-900 font-medium"
							>
								{{ isRawMode ? 'Show Preview' : 'Show Raw' }}
							</button>
						</div>
                  <div class="relative">
                     <div
                        v-if="!isRawMode"
                        class="w-full max-h-64 overflow-y-auto rounded-xl border border-gray-200 bg-gray-50 px-5 py-4 text-sm text-gray-600 leading-7 font-mono"
                        v-html="renderMarkdown(selectedLog.transcription)"
                     ></div>
                     <textarea
                        v-else
                        v-model="selectedLog.transcription"
                        rows="10"
                        class="w-full rounded-xl border-gray-200 bg-white px-4 py-3 text-sm font-mono shadow-sm focus:border-primary-500 focus:ring-primary-500"
                     ></textarea>
                     <!-- Fade effect at bottom if content is long? omitted for simplicity but good for UI -->
                  </div>
					</div>
				</div>
			</template>
			<template #actions>
				<Button variant="subtle" class="hover:bg-gray-100 text-gray-600" @click="showLogDialog = false">Cancel</Button>
				<Button
					variant="solid"
					:loading="saving"
					@click="saveLog"
					class="!bg-primary-600 hover:!bg-primary-700 !text-white border-transparent shadow-md shadow-primary-500/20"
				>
					Save Changes
				</Button>
			</template>
		</Dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { createResource, Button, Dialog, FeatherIcon } from 'frappe-ui'

// State
const showLogDialog = ref(false)
const saving = ref(false)
const selectedLog = ref({})
const isRawMode = ref(false)
const isSummaryRawMode = ref(false)
const currentLimit = ref(10)

// Resources
const logs = createResource({
	url: 'frappe.client.get_list',
	makeParams(values) {
		return {
			doctype: 'AI Call Log',
			fields: [
				'name',
				'phone_number',
				'party',
				'party_type',
				'lead_status',
				'ai_summary',
				'transcription',
				'call_status',
				'livekit_room',
				'creation',
				'duration',
				'recording_url',
			],
			order_by: 'creation desc',
			limit: currentLimit.value,
		}
	},
	auto: true,
})

// --- COMPUTED CHARTS ---

const dailyActivity = computed(() => {
	if (!logs.data) return []

	const daysMap = {}
	logs.data.forEach((log) => {
		const date = log.creation.split(' ')[0]
		daysMap[date] = (daysMap[date] || 0) + 1
	})

	const sortedDates = Object.keys(daysMap).sort().slice(-7)
	const maxCount = Math.max(...Object.values(daysMap), 1)

	return sortedDates.map((date) => {
		const d = new Date(date)
		// simple label e.g. "Mon"
		const label = d.toLocaleDateString('en-US', { weekday: 'short' })
		return {
			date,
			label,
			count: daysMap[date],
			percentage: (daysMap[date] / maxCount) * 100,
		}
	})
})

const statusDistribution = computed(() => {
	if (!logs.data) return []

	const counts = {}
	logs.data.forEach((log) => {
		const status = log.lead_status || 'Unknown'
		counts[status] = (counts[status] || 0) + 1
	})

	const total = logs.data.length

	const colors = {
		Hot: 'bg-green-500',
		Warm: 'bg-orange-400',
		Cold: 'bg-blue-400',
		Negative: 'bg-red-500',
		Unknown: 'bg-gray-300',
		'Not a Lead': 'bg-gray-400',
	}
   
   const dots = {
      Hot: 'bg-green-500',
      Warm: 'bg-orange-500',
      Cold: 'bg-blue-500',
      Negative: 'bg-red-500',
      Unknown: 'bg-gray-400',
      'Not a Lead': 'bg-gray-400'
   }

	return Object.keys(counts)
		.map((status) => ({
			label: status,
			count: counts[status],
			percentage: Math.round((counts[status] / total) * 100),
			colorClass: colors[status] || 'bg-gray-500',
         dotClass: dots[status] || 'bg-gray-400',
		}))
		.sort((a, b) => b.count - a.count)
})

// --- ACTIONS ---

function loadMore() {
	currentLimit.value += 10
	logs.fetch()
}

function openLogDetails(log) {
	selectedLog.value = { ...log }
	isRawMode.value = false
	isSummaryRawMode.value = false
	showLogDialog.value = true
}

async function saveLog() {
	saving.value = true
	try {
		await fetch(`/api/resource/AI Call Log/${selectedLog.value.name}`, {
			method: 'PUT',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				call_status: selectedLog.value.call_status,
				lead_status: selectedLog.value.lead_status,
				ai_summary: selectedLog.value.ai_summary,
				transcription: selectedLog.value.transcription,
			}),
		})
		await logs.fetch()
		showLogDialog.value = false
	} catch (e) {
		console.error(e)
		// alert('Failed to save log.')
	} finally {
		saving.value = false
	}
}

// --- FORMATTERS ---

function calculateAvgDuration(data) {
	if (!data || data.length === 0) return '00:00'
	const validCalls = data.filter((l) => l.duration > 0)
	if (validCalls.length === 0) return '00:00'
	const totalSeconds = validCalls.reduce((acc, curr) => acc + (curr.duration || 0), 0)
	const avgSeconds = Math.floor(totalSeconds / validCalls.length)
	return formatDuration(avgSeconds)
}

function formatDuration(seconds) {
	if (!seconds) return '00:00'
	const m = Math.floor(seconds / 60)
	const s = Math.floor(seconds % 60)
	return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

function formatDateTime(dateStr) {
	if (!dateStr) return ''
	const date = new Date(dateStr)
	return date.toLocaleString('en-GB', {
		day: '2-digit',
		month: 'short',
		hour: '2-digit',
		minute: '2-digit',
	})
}

function getBadgeClasses(status) {
	const s = (status || '').trim()
	if (s === 'Hot') return 'bg-green-50 text-green-700 border-green-200'
	if (s === 'Warm') return 'bg-orange-50 text-orange-700 border-orange-200'
	if (s === 'Cold') return 'bg-blue-50 text-blue-700 border-blue-200'
	if (s === 'Negative') return 'bg-red-50 text-red-700 border-red-200'
	return 'bg-gray-100 text-gray-700 border-gray-200'
}

function renderMarkdown(text) {
	if (!text) return '<span class="text-gray-400 italic">No detailed summary available.</span>'
	return text
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/\n/g, '<br>')
		.replace(/\*\*(.*?)\*\*/g, '<strong class="text-gray-900 font-bold">$1</strong>')
		.replace(/(Alex \(AI\):)/g, '<span class="text-primary-600 font-bold">$1</span>')
      .replace(/(User:)/g, '<span class="text-gray-700 font-bold">$1</span>')
		.replace(/^- (.*)/gm, '<li class="ml-4 list-disc marker:text-gray-300">$1</li>')
}

function stripHtml(html) {
	if (!html) return ''
	return (
		html
			.replace(/\*\*/g, '')
			.replace(/Alex \(AI\):/g, '')
         .replace(/User:/g, '')
         .replace(/<br>/g, ' ')
			.substring(0, 120) + '...'
	)
}
</script>

<style scoped>
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
</style>
