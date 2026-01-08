<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Header -->
    <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Call History</h1>
        <div class="flex items-center gap-2 text-gray-500 mt-1">
           <span class="text-sm">Log of all AI voice interactions</span>
           <span class="w-1 h-1 bg-gray-300 rounded-full"></span>
           <span class="text-sm">{{ logs.data?.length || 0 }} calls recorded</span>
        </div>
      </div>
      <div class="flex items-center gap-3">
         <div class="relative hidden sm:block">
           <FeatherIcon name="search" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
           <input 
              type="text" 
              placeholder="Search by phone..." 
              class="pl-9 pr-4 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 w-64 transition-shadow bg-white"
           >
        </div>
        <Button
          variant="solid"
          class="!bg-primary-600 hover:!bg-primary-700 !text-white !border-transparent !rounded-xl shadow-md shadow-primary-500/20"
          :loading="logs.loading"
          @click="logs.fetch()"
        >
          <template #prefix><FeatherIcon name="refresh-cw" class="h-4 w-4" /></template>
          Refresh
        </Button>
      </div>
    </header>

    <!-- Logs Table -->
    <div class="bg-white rounded-2xl border border-gray-200 shadow-soft overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-gray-50/50 border-b border-gray-200">
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Contact Details</th>
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Date & Duration</th>
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Call Outcome</th>
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Lead Status</th>
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-if="logs.loading">
               <td colspan="5" class="px-6 py-12 text-center text-gray-500">
                 <div class="flex flex-col items-center animate-pulse">
                    <div class="h-4 w-32 bg-gray-200 rounded mb-2"></div>
                    <div class="h-3 w-48 bg-gray-100 rounded"></div>
                 </div>
              </td>
            </tr>
            <tr v-else-if="!logs.data || logs.data.length === 0">
              <td colspan="5" class="px-6 py-16 text-center text-gray-500">
                 <FeatherIcon name="phone-off" class="w-10 h-10 mx-auto text-gray-300 mb-3" />
                 <p class="font-medium text-gray-900">No calls found</p>
                 <p class="text-sm mt-1">Start a campaign or call a contact to see logs here.</p>
              </td>
            </tr>
            <tr
              v-else
              v-for="log in logs.data"
              :key="log.name"
              class="group hover:bg-gray-50/80 transition-colors"
            >
              <td class="px-6 py-4">
                 <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-500 border border-gray-200">
                       <FeatherIcon name="user" class="w-4 h-4" />
                    </div>
                    <div>
                        <div class="font-bold text-gray-900 group-hover:text-primary-600 transition-colors">{{ log.party || 'Unknown Person' }}</div>
                        <div class="text-xs text-gray-500 font-mono mt-0.5">{{ log.phone_number }}</div>
                    </div>
                 </div>
              </td>
              <td class="px-6 py-4">
                <div class="flex flex-col gap-1">
                   <div class="flex items-center text-sm text-gray-900 font-medium">
                      {{ formatDateTime(log.creation).split(',')[0] }}
                   </div>
                   <div class="flex items-center text-xs text-gray-500">
                      <FeatherIcon name="clock" class="w-3 h-3 mr-1" />
                      {{ formatDuration(log.duration) }}
                   </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold border"
                  :class="getCallBadgeClasses(log.call_status)"
                >
                   <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="getCallDotClass(log.call_status)"></span>
                  {{ log.call_status || 'Unknown' }}
                </span>
              </td>
              <td class="px-6 py-4">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium bg-white border border-gray-200 shadow-sm"
                >
                  {{ log.lead_status || 'Unclassified' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                 <div class="flex items-center justify-end gap-2">
                    <button 
                       @click="openLogDetails(log)" 
                       class="p-2 bg-white border border-gray-200 rounded-lg text-gray-600 hover:text-primary-600 hover:border-primary-200 hover:shadow-sm transition-all"
                       title="View Details"
                    >
                       <FeatherIcon name="eye" class="w-4 h-4" />
                    </button>
                    <button 
                       @click="confirmDelete(log)" 
                       class="p-2 bg-white border border-gray-200 rounded-lg text-gray-600 hover:text-red-600 hover:border-red-200 hover:shadow-sm transition-all"
                       title="Delete Log"
                    >
                       <FeatherIcon name="trash-2" class="w-4 h-4" />
                    </button>
                 </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination Placeholder -->
       <div class="px-6 py-4 border-t border-gray-200 flex items-center justify-between bg-gray-50/50">
          <span class="text-xs text-gray-500">Auto-loading latest 50 logs</span>
           <div class="flex gap-2">
             <button class="p-1 rounded hover:bg-white hover:shadow-sm text-gray-400 hover:text-gray-600 disabled:opacity-50" disabled><FeatherIcon name="chevron-left" class="w-4 h-4" /></button>
             <button class="p-1 rounded hover:bg-white hover:shadow-sm text-gray-400 hover:text-gray-600 disabled:opacity-50" disabled><FeatherIcon name="chevron-right" class="w-4 h-4" /></button>
          </div>
       </div>
    </div>

    <!-- Details Dialog -->
    <Dialog v-model="showDialog" :options="{ size: '2xl' }">
      <template #body-title>
         <h3 class="text-xl font-bold flex items-center gap-3">
            <div class="p-2 bg-primary-100 rounded-lg text-primary-600">
               <FeatherIcon name="phone-call" class="w-5 h-5" />
            </div>
            <span>Call Analysis</span>
            <span class="ml-auto text-sm font-normal text-gray-400 bg-gray-50 px-2 py-1 rounded border border-gray-200 font-mono">{{ selectedLog.name }}</span>
         </h3>
      </template>
      <template #body-content>
        <div v-if="selectedLog" class="mt-6 space-y-8">
           <!-- Summary Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
             <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm relative overflow-hidden group">
                 <div class="absolute top-0 right-0 w-16 h-16 bg-blue-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"></div>
                <div class="relative z-10">
                   <label class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 block">Contact</label>
                   <div class="font-bold text-gray-900 truncate">{{ selectedLog.party }}</div>
                   <div class="text-xs text-primary-600 mt-1 font-mono">{{ selectedLog.phone_number }}</div>
                </div>
             </div>
             
             <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm relative overflow-hidden group">
                 <div class="absolute top-0 right-0 w-16 h-16 bg-green-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"></div>
                <div class="relative z-10">
                   <label class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 block">Duration</label>
                   <div class="font-bold text-gray-900 text-xl font-mono">{{ formatDuration(selectedLog.duration) }}</div>
                </div>
             </div>
             
             <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm relative overflow-hidden group">
                 <div class="absolute top-0 right-0 w-16 h-16 bg-orange-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"></div>
                <div class="relative z-10">
                   <label class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 block">Status</label>
                   <Badge :theme="selectedLog.call_status === 'Completed' ? 'green' : 'red'">{{ selectedLog.call_status }}</Badge>
                </div>
             </div>
          </div>

          <!-- Player -->
          <div v-if="selectedLog.recording_url" class="p-5 rounded-xl bg-gray-900 text-white shadow-lg">
            <label class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
               <FeatherIcon name="mic" class="w-3 h-3" /> Voice Recording
            </label>
            <audio controls :src="selectedLog.recording_url" class="w-full h-10 rounded contrast-125 filter"></audio>
          </div>
          <div v-else class="flex items-center justify-center p-6 border-2 border-dashed border-gray-200 rounded-xl bg-gray-50 text-gray-400">
             <FeatherIcon name="mic-off" class="w-5 h-5 mr-2" /> No recording available
          </div>

          <!-- AI Summary -->
          <div class="bg-gradient-to-br from-indigo-50 to-white p-6 rounded-2xl border border-indigo-100 shadow-sm">
            <div class="flex justify-between items-center mb-4">
              <label class="text-sm font-bold text-indigo-900 flex items-center gap-2">
                <div class="p-1 bg-indigo-200 rounded text-indigo-700">
                   <FeatherIcon name="cpu" class="w-3 h-3" />
                </div>
                AI Insights & Summary
              </label>
              <button
                @click="isSummaryRawMode = !isSummaryRawMode"
                class="text-xs text-indigo-600 hover:text-indigo-800 font-bold bg-white px-2 py-1 rounded shadow-sm border border-indigo-100"
              >
                {{ isSummaryRawMode ? 'Preview' : 'Edit' }}
              </button>
            </div>
            
            <div
              v-if="!isSummaryRawMode"
              class="text-sm text-gray-700 leading-relaxed prose-indigo max-w-none"
              v-html="renderMarkdown(selectedLog.ai_summary)"
            ></div>
            <textarea
              v-else
              v-model="selectedLog.ai_summary"
              rows="4"
              class="w-full rounded-xl border-indigo-200 bg-white px-4 py-3 text-sm focus:border-indigo-500 focus:ring-indigo-500 shadow-inner"
            ></textarea>
          </div>

          <!-- Status Editor -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-gray-50/50 p-6 rounded-2xl border border-gray-200">
             <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Lead Classification</label>
                <select
                  v-model="selectedLog.lead_status"
                  class="block w-full rounded-lg border-gray-200 bg-white shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm py-2.5"
                >
                  <option value="Hot">🔥 Hot</option>
                  <option value="Warm">⛅ Warm</option>
                  <option value="Cold">❄️ Cold</option>
                  <option value="Negative">⛔ Negative</option>
                  <option value="Not a Lead">🤷 Not a Lead</option>
                </select>
             </div>
             <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Technical Status</label>
                <select
                  v-model="selectedLog.call_status"
                  class="block w-full rounded-lg border-gray-200 bg-white shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm py-2.5"
                >
                  <option value="Completed">Completed</option>
                  <option value="No Answer">No Answer</option>
                  <option value="Failed">Failed</option>
                  <option value="Initiated">Initiated</option>
                </select>
             </div>
          </div>
          
          <!-- Transcription -->
             <div>
                <div class="flex justify-between items-center mb-2 px-1">
                   <label class="text-xs font-bold text-gray-500 uppercase">Full Transcription</label>
                   <button @click="isRawMode = !isRawMode" class="text-xs text-gray-400 hover:text-gray-600">{{ isRawMode ? 'View Formatted' : 'View Raw' }}</button>
                </div>
                <div class="relative">
                   <div
                      v-if="!isRawMode"
                      class="w-full h-64 overflow-y-auto rounded-xl border border-gray-200 bg-gray-50 px-5 py-4 text-xs text-gray-600 font-mono leading-relaxed"
                      v-html="renderMarkdown(selectedLog.transcription)"
                   ></div>
                   <textarea
                      v-else
                      v-model="selectedLog.transcription"
                      rows="10"
                      class="w-full rounded-xl border border-gray-200 bg-white px-5 py-4 text-xs font-mono leading-relaxed"
                   ></textarea>
                </div>
             </div>

        </div>
      </template>
      <template #actions>
         <Button variant="subtle" class="hover:bg-gray-100" @click="showDialog = false">Close</Button>
        <Button
          variant="solid"
          class="!bg-primary-600 hover:!bg-primary-700 !text-white !rounded-xl shadow-lg shadow-primary-500/20"
          :loading="saving"
          @click="saveLog"
        >
          Save Updates
        </Button>
      </template>
    </Dialog>

    <!-- Delete Confirmation -->
    <Dialog v-model="showDeleteDialog" :options="{ size: 'md' }">
      <template #body-title>
         <div class="bg-red-50 p-2 rounded-full w-fit mb-2"><FeatherIcon name="trash-2" class="w-5 h-5 text-red-600" /></div>
         <h3 class="text-xl font-bold text-gray-900">Delete Call Log?</h3>
      </template>
      <template #body-content>
        <p class="text-gray-500 mt-2">
           Are you sure you want to permanently delete this call log? This will remove the recording and transcript as well.
        </p>
         <div class="mt-4 p-3 bg-gray-50 rounded-lg border border-gray-200 font-mono text-xs text-gray-600">
            Log ID: {{ logToDelete?.name }}
         </div>
      </template>
      <template #actions>
        <Button variant="subtle" @click="showDeleteDialog = false">Cancel</Button>
        <Button variant="solid" theme="red" :loading="deleting" @click="deleteLog">Confirm Delete</Button>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createResource, Button, Dialog, Badge, FeatherIcon } from 'frappe-ui'

const showDialog = ref(false)
const showDeleteDialog = ref(false)
const selectedLog = ref({})
const logToDelete = ref(null)
const saving = ref(false)
const deleting = ref(false)
const isRawMode = ref(false)
const isSummaryRawMode = ref(false)

const logs = createResource({
	url: 'frappe.client.get_list',
	params: {
		doctype: 'AI Call Log',
		fields: [
			'name',
			'party',
			'party_type',
			'phone_number',
			'call_status',
			'lead_status',
			'livekit_room',
			'transcription',
			'ai_summary',
			'creation',
			'duration',
			'recording_url',
		],
		order_by: 'creation desc',
		limit: 50,
	},
	auto: true,
})

// --- HELPERS ---

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
		year: 'numeric',
		hour: '2-digit',
		minute: '2-digit',
	})
}

function getCallBadgeClasses(status) {
	const s = (status || '').trim()
	if (s === 'Completed') return 'bg-green-50 text-green-700 border border-green-200'
	if (s === 'Failed') return 'bg-red-50 text-red-700 border border-red-200'
	if (s === 'Initiated') return 'bg-blue-50 text-blue-700 border border-blue-200'
	if (s === 'No Answer') return 'bg-orange-50 text-orange-700 border border-orange-200'
	return 'bg-gray-50 text-gray-700 border border-gray-200'
}

function getCallDotClass(status) {
   const s = (status || '').trim()
   if (s === 'Completed') return 'bg-green-500'
   if (s === 'Failed') return 'bg-red-500' 
   if (s === 'Initiated') return 'bg-blue-500'
   if (s === 'No Answer') return 'bg-orange-500'
   return 'bg-gray-400'
}

function renderMarkdown(text) {
	if (!text) return '<span class="text-gray-400 italic">No detailed summary available.</span>'

	let html = text
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/\n/g, '<br>')
		.replace(/\*\*(.*?)\*\*/g, '<strong class="text-gray-900 font-bold">$1</strong>')
		.replace(/(Alex \(AI\):)/g, '<span class="text-primary-600 font-bold">$1</span>')
      .replace(/(User:)/g, '<span class="text-gray-700 font-bold">$1</span>')
		.replace(/^- (.*)/gm, '<li class="ml-4 list-disc text-gray-600">$1</li>')

	return html
}

// --- ACTIONS ---

function openLogDetails(log) {
	selectedLog.value = { ...log }
	isRawMode.value = false
	isSummaryRawMode.value = false
	showDialog.value = true
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
		showDialog.value = false
	} catch (e) {
		console.error(e)
		// alert('Failed to save log.')
	} finally {
		saving.value = false
	}
}

function confirmDelete(log) {
	logToDelete.value = log
	showDeleteDialog.value = true
}

async function deleteLog() {
	if (!logToDelete.value) return
	deleting.value = true
	try {
		const res = await fetch(`/api/resource/AI Call Log/${logToDelete.value.name}`, {
			method: 'DELETE',
		})
		if (res.ok) {
			await logs.fetch()
			showDeleteDialog.value = false
			logToDelete.value = null
		} else {
			throw new Error('Server returned error')
		}
	} catch (e) {
		console.error(e)
		// alert('Failed to delete log.')
	} finally {
		deleting.value = false
	}
}
</script>
