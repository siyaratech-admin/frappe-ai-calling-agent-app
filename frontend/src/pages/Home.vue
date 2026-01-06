<template>
	<div class="p-8 max-w-6xl mx-auto">
		<div class="flex justify-between items-center mb-8">
			<div>
				<h1 class="text-3xl font-bold text-gray-900">AI Calling Agent</h1>
				<p class="text-gray-600 mt-1">Manage your AI sales team and campaigns</p>
			</div>
			<Button
				variant="solid"
				class="!bg-[#4318FF] hover:!bg-[#3311CC] !text-white border-transparent"
				@click="logs.fetch()"
			>
				<template #prefix><FeatherIcon name="refresh-cw" class="h-4 w-4" /></template>
				Refresh Data
			</Button>
		</div>

		<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
			<div class="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
				<div class="text-gray-500 text-sm font-medium">Total Calls</div>
				<div class="text-3xl font-bold mt-2">{{ logs.data?.length || 0 }}</div>
			</div>
			<div class="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
				<div class="text-gray-500 text-sm font-medium">Hot Leads</div>
				<div class="text-3xl font-bold mt-2 text-green-600">
					{{ logs.data?.filter((l) => l.lead_status === 'Hot').length || 0 }}
				</div>
			</div>
			<div class="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
				<div class="text-gray-500 text-sm font-medium">Avg Duration</div>
				<div class="text-3xl font-bold mt-2 text-[#4318FF]">
					{{ calculateAvgDuration(logs.data) }}
				</div>
			</div>
		</div>

		<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
			<div class="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
				<h3 class="text-lg font-bold text-gray-800 mb-4">Calls Per Day</h3>
				<div class="h-48 flex items-end gap-2 justify-between px-2">
					<div
						v-for="(day, index) in dailyActivity"
						:key="index"
						class="flex flex-col items-center gap-2 group flex-1"
					>
						<div
							class="relative w-full flex justify-center items-end h-32 bg-gray-50 rounded-md overflow-hidden"
						>
							<div
								class="w-full mx-1 bg-[#4318FF] rounded-t-sm transition-all duration-500 hover:bg-[#3311CC] relative group-hover:opacity-90"
								:style="{ height: `${day.percentage}%` }"
							></div>
							<div
								class="absolute -top-8 bg-gray-900 text-white text-xs py-1 px-2 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10"
							>
								{{ day.count }} calls
							</div>
						</div>
						<span
							class="text-xs text-gray-400 font-medium rotate-0 truncate w-full text-center"
						>
							{{ day.label }}
						</span>
					</div>

					<div
						v-if="dailyActivity.length === 0"
						class="w-full h-full flex items-center justify-center text-gray-400 text-sm"
					>
						No data available
					</div>
				</div>
			</div>

			<div class="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
				<h3 class="text-lg font-bold text-gray-800 mb-4">Leads by Status</h3>
				<div class="space-y-4 h-48 overflow-y-auto pr-2">
					<div v-for="(stat, index) in statusDistribution" :key="index">
						<div class="flex justify-between text-sm mb-1">
							<span class="font-medium text-gray-700">{{ stat.label }}</span>
							<span class="text-gray-500"
								>{{ stat.count }} ({{ stat.percentage }}%)</span
							>
						</div>
						<div class="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
							<div
								class="h-2.5 rounded-full transition-all duration-500"
								:class="stat.colorClass"
								:style="{ width: `${stat.percentage}%` }"
							></div>
						</div>
					</div>
					<div
						v-if="statusDistribution.length === 0"
						class="w-full h-full flex items-center justify-center text-gray-400 text-sm"
					>
						No data available
					</div>
				</div>
			</div>
		</div>

		<div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
			<div
				class="px-6 py-4 border-b border-gray-100 font-semibold text-gray-700 flex justify-between items-center"
			>
				<span>Recent Call Logs</span>
				<span class="text-xs text-gray-400"
					>Showing {{ logs.data?.length || 0 }} calls</span
				>
			</div>

			<div v-if="logs.loading && !logs.data" class="p-8 text-center text-gray-500">
				Loading logs...
			</div>

			<div
				v-else-if="logs.data && logs.data.length === 0"
				class="p-8 text-center text-gray-500"
			>
				No calls made yet.
			</div>

			<div v-else>
				<div
					v-for="log in logs.data"
					:key="log.name"
					@click="openLogDetails(log)"
					class="px-6 py-4 border-b border-gray-100 last:border-0 hover:bg-gray-50 transition-colors cursor-pointer group"
				>
					<div class="flex justify-between items-start">
						<div>
							<div
								class="font-medium text-gray-900 group-hover:text-[#4318FF] transition-colors"
							>
								{{ log.phone_number }}
							</div>
							<div class="text-sm text-gray-500 mt-1 flex items-center gap-2">
								<span>{{ log.party || 'Unknown Contact' }}</span>
								<span>•</span>
								<span>{{ formatDateTime(log.creation) }}</span>
								<span>•</span>
								<span
									class="font-mono text-gray-600 bg-gray-100 px-1.5 rounded text-xs"
								>
									{{ formatDuration(log.duration) }}
								</span>
							</div>
						</div>
						<div class="text-right">
							<span
								class="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium"
								:class="getBadgeClasses(log.lead_status)"
							>
								{{ log.lead_status || 'Unknown' }}
							</span>
							<div class="text-xs text-gray-400 mt-2">{{ log.name }}</div>
						</div>
					</div>

					<div class="mt-1 text-sm flex items-center gap-1 text-gray-500">
						<span>🤖</span> <strong>AI Summary</strong>
					</div>
					<div
						v-if="log.ai_summary"
						class="mt-2 text-sm text-gray-600 bg-gray-50 p-3 rounded border border-gray-100 line-clamp-2"
					>
						{{ stripHtml(log.ai_summary) }}
					</div>
				</div>

				<div class="p-4 bg-gray-50 text-center border-t border-gray-100">
					<Button
						v-if="logs.data.length >= currentLimit"
						variant="outline"
						:loading="logs.loading"
						@click="loadMore"
						class="w-full md:w-auto"
					>
						View More (Load 10)
					</Button>
					<span v-else class="text-xs text-gray-400">All logs loaded</span>
				</div>
			</div>
		</div>

		<Dialog v-model="showLogDialog" :options="{ size: '2xl' }">
			<template #body-title>
				<h3 class="text-xl font-bold">Call Details: {{ selectedLog.name }}</h3>
			</template>
			<template #body-content>
				<div v-if="selectedLog" class="mt-6 space-y-6">
					<div
						class="grid grid-cols-1 md:grid-cols-3 gap-6 bg-gray-50 p-4 rounded-lg border border-gray-100"
					>
						<div>
							<label class="block text-xs font-semibold text-gray-500 uppercase mb-1"
								>Contact</label
							>
							<a
								:href="`/app/contact/${selectedLog.party}`"
								target="_blank"
								class="text-[#4318FF] hover:underline font-medium flex items-center gap-1"
							>
								{{ selectedLog.party }}
								<FeatherIcon name="external-link" class="h-3 w-3" />
							</a>
						</div>
						<div>
							<label class="block text-xs font-semibold text-gray-500 uppercase mb-1"
								>LiveKit Room</label
							>
							<div
								class="font-mono text-gray-700 text-sm truncate"
								:title="selectedLog.livekit_room"
							>
								{{ selectedLog.livekit_room || 'N/A' }}
							</div>
						</div>
						<div>
							<label class="block text-xs font-semibold text-gray-500 uppercase mb-1"
								>Duration</label
							>
							<div class="font-mono text-gray-900 font-bold">
								{{ formatDuration(selectedLog.duration) }}
							</div>
						</div>
					</div>

					<div
						v-if="selectedLog.recording_url"
						class="bg-white border border-gray-200 p-4 rounded-lg shadow-sm"
					>
						<label
							class="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2"
						>
							<span class="text-lg">🎙️</span> Call Recording
						</label>
						<audio
							controls
							:src="selectedLog.recording_url"
							class="w-full rounded-md h-10"
						></audio>
					</div>

					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-1"
								>Call Status</label
							>
							<select
								v-model="selectedLog.call_status"
								class="form-select w-full rounded-md border border-gray-200 bg-gray-50 px-3 py-2 text-sm"
							>
								<option value="Pending">Pending</option>
								<option value="Initiated">Initiated</option>
								<option value="No Answer">No Answer</option>
								<option value="Completed">Completed</option>
								<option value="Failed">Failed</option>
							</select>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-1"
								>Lead Status</label
							>
							<select
								v-model="selectedLog.lead_status"
								class="form-select w-full rounded-md border border-gray-200 bg-gray-50 px-3 py-2 text-sm"
							>
								<option value="Hot">Hot</option>
								<option value="Warm">Warm</option>
								<option value="Cold">Cold</option>
								<option value="Negative">Negative</option>
								<option value="Not a Lead">Not a Lead</option>
							</select>
						</div>
					</div>

					<div>
						<div class="flex justify-between items-center mb-1">
							<label
								class="block text-sm font-medium text-gray-700 flex items-center gap-2"
							>
								<span class="text-lg">🤖</span> AI Summary
							</label>
							<button
								@click="isSummaryRawMode = !isSummaryRawMode"
								class="text-xs text-[#4318FF] hover:text-[#3311CC] font-medium"
							>
								{{ isSummaryRawMode ? 'Show Preview' : 'Edit Raw Text' }}
							</button>
						</div>
						<div
							v-if="!isSummaryRawMode"
							class="w-full h-auto min-h-[5rem] overflow-y-auto rounded-md border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-800 leading-relaxed"
							v-html="renderMarkdown(selectedLog.ai_summary)"
						></div>
						<textarea
							v-else
							v-model="selectedLog.ai_summary"
							rows="3"
							class="w-full rounded-md border border-gray-200 bg-white px-3 py-2 text-sm"
						></textarea>
					</div>

					<div>
						<div class="flex justify-between items-center mb-1">
							<label class="block text-sm font-medium text-gray-700"
								>Full Transcription</label
							>
							<button
								@click="isRawMode = !isRawMode"
								class="text-xs text-[#4318FF] hover:text-[#3311CC] font-medium"
							>
								{{ isRawMode ? 'Show Preview' : 'Edit Raw Text' }}
							</button>
						</div>
						<div class="relative">
							<div
								v-if="!isRawMode"
								class="w-full h-64 overflow-y-auto rounded-md border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-800 leading-relaxed whitespace-pre-wrap"
								v-html="renderMarkdown(selectedLog.transcription)"
							></div>
							<textarea
								v-else
								v-model="selectedLog.transcription"
								rows="10"
								class="w-full rounded-md border border-gray-200 bg-white px-3 py-2 text-sm font-mono"
							></textarea>
						</div>
					</div>
				</div>
			</template>
			<template #actions>
				<Button variant="subtle" @click="showLogDialog = false">Close</Button>
				<Button
					variant="solid"
					:loading="saving"
					@click="saveLog"
					class="!bg-[#4318FF] hover:!bg-[#3311CC] !text-white border-transparent"
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
		return {
			date,
			label: d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
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

	return Object.keys(counts)
		.map((status) => ({
			label: status,
			count: counts[status],
			percentage: Math.round((counts[status] / total) * 100),
			colorClass: colors[status] || 'bg-gray-500',
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
		alert('Failed to save log.')
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
		month: '2-digit',
		year: 'numeric',
		hour: '2-digit',
		minute: '2-digit',
	})
}

function getBadgeClasses(status) {
	const s = (status || '').trim()
	if (s === 'Hot') return 'bg-green-100 text-green-800'
	if (s === 'Warm') return 'bg-orange-100 text-orange-800'
	if (s === 'Cold') return 'bg-blue-100 text-blue-800'
	if (s === 'Negative') return 'bg-red-100 text-red-800'
	return 'bg-gray-100 text-gray-800'
}

function renderMarkdown(text) {
	if (!text) return '<span class="text-gray-400 italic">No data available.</span>'
	return text
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/\n/g, '<br>')
		.replace(/\*\*(.*?)\*\*/g, '<strong class="text-gray-900 font-bold">$1</strong>')
		.replace(/(Alex \(AI\):)/g, '<span class="text-[#4318FF] font-medium">$1</span>')
		.replace(/^- (.*)/gm, '<li class="ml-4 list-disc">$1</li>')
}

function stripHtml(html) {
	if (!html) return ''
	return (
		html
			.replace(/\*\*/g, '')
			.replace(/Alex \(AI\):/g, 'AI:')
			.substring(0, 150) + '...'
	)
}
</script>
