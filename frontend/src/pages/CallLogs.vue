<template>
	<div class="p-8 max-w-7xl mx-auto">
		<div class="flex justify-between items-center mb-6">
			<div>
				<h1 class="text-2xl font-bold text-gray-900">Call Logs</h1>
				<p class="text-sm text-gray-500 mt-1">History of AI interactions</p>
			</div>
			<Button
				variant="solid"
				class="!bg-[#4318FF] hover:!bg-[#3311CC] !text-white border-transparent"
				@click="logs.fetch()"
			>
				<template #prefix>
					<FeatherIcon name="refresh-cw" class="h-4 w-4" />
				</template>
				Refresh
			</Button>
		</div>

		<div class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
			<table class="w-full text-left text-sm">
				<thead class="bg-gray-50 border-b border-gray-200 text-gray-500 font-medium">
					<tr>
						<th class="px-6 py-3">ID & Date</th>
						<th class="px-6 py-3">Contact</th>
						<th class="px-6 py-3">Phone</th>
						<th class="px-6 py-3">Duration</th>
						<th class="px-6 py-3">Call Status</th>
						<th class="px-6 py-3">Lead Status</th>
						<th class="px-6 py-3 text-right">Actions</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-100">
					<tr v-if="logs.loading">
						<td colspan="7" class="p-6 text-center text-gray-500">Loading logs...</td>
					</tr>
					<tr v-else-if="!logs.data || logs.data.length === 0">
						<td colspan="7" class="p-6 text-center text-gray-500">
							No call logs found.
						</td>
					</tr>
					<tr
						v-else
						v-for="log in logs.data"
						:key="log.name"
						class="hover:bg-gray-50 transition-colors"
					>
						<td class="px-6 py-4">
							<div class="font-medium text-gray-900">{{ log.name }}</div>
							<div class="text-xs text-gray-400 mt-0.5">
								{{ formatDateTime(log.creation) }}
							</div>
						</td>
						<td class="px-6 py-4 text-gray-900">
							{{ log.party || 'Unknown' }}
						</td>
						<td class="px-6 py-4 text-gray-600 font-mono">
							{{ log.phone_number }}
						</td>
						<td class="px-6 py-4 font-mono text-gray-700">
							{{ formatDuration(log.duration) }}
						</td>
						<td class="px-6 py-4">
							<span
								class="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium"
								:class="getCallBadgeClasses(log.call_status)"
							>
								{{ log.call_status || 'Unknown' }}
							</span>
						</td>
						<td class="px-6 py-4">
							<span
								class="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium"
								:class="getLeadBadgeClasses(log.lead_status)"
							>
								{{ log.lead_status || 'Unknown' }}
							</span>
						</td>
						<td class="px-6 py-4 text-right flex justify-end gap-2">
							<Button
								variant="subtle"
								size="sm"
								class="text-[#4318FF] hover:bg-[#4318FF]/10"
								@click="openLogDetails(log)"
							>
								View
							</Button>
							<Button
								variant="ghost"
								theme="red"
								size="sm"
								@click="confirmDelete(log)"
							>
								<FeatherIcon name="trash-2" class="h-4 w-4" />
							</Button>
						</td>
					</tr>
				</tbody>
			</table>
		</div>

		<Dialog v-model="showDialog" :options="{ size: '2xl' }">
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
					<div
						v-else-if="selectedLog.call_status === 'Completed'"
						class="text-sm text-gray-500 italic bg-gray-50 p-3 rounded border border-gray-100"
					>
						⚠️ No recording available for this call.
					</div>

					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-1"
								>Call Status</label
							>
							<select
								v-model="selectedLog.call_status"
								class="form-select w-full rounded-md border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-900 focus:border-gray-500 focus:bg-white focus:ring-0 transition-colors"
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
								class="form-select w-full rounded-md border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-900 focus:border-gray-500 focus:bg-white focus:ring-0 transition-colors"
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
							class="w-full rounded-md border border-gray-200 bg-white px-3 py-2 text-sm text-gray-900 focus:bg-white focus:border-gray-500 focus:ring-0 transition-colors"
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
								class="w-full rounded-md border border-gray-200 bg-white px-3 py-2 text-sm font-mono text-gray-600 focus:bg-white focus:border-gray-500 focus:ring-0 transition-colors"
							></textarea>
						</div>
					</div>
				</div>
			</template>
			<template #actions>
				<Button variant="subtle" @click="showDialog = false">Close</Button>
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

		<Dialog v-model="showDeleteDialog">
			<template #body-title
				><h3 class="text-xl font-bold text-red-600">Delete Call Log</h3></template
			>
			<template #body-content>
				<div class="mt-4 text-gray-700">
					<p class="mb-2">Are you sure you want to delete this call log?</p>
					<div
						class="bg-gray-100 p-3 rounded text-sm font-mono font-bold text-gray-900 border border-gray-200"
					>
						ID: {{ logToDelete?.name }}
					</div>
					<p class="mt-2 text-sm text-gray-500">This action cannot be undone.</p>
				</div>
			</template>
			<template #actions>
				<Button variant="subtle" @click="showDeleteDialog = false">Cancel</Button>
				<Button variant="solid" theme="red" :loading="deleting" @click="deleteLog"
					>Confirm Delete</Button
				>
			</template>
		</Dialog>
	</div>
</template>

<script setup>
import { ref } from 'vue'
import { createResource, Button, Dialog, FeatherIcon } from 'frappe-ui'

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
		month: '2-digit',
		year: 'numeric',
		hour: '2-digit',
		minute: '2-digit',
	})
}

function getLeadBadgeClasses(status) {
	const s = (status || '').trim()
	if (s === 'Hot') return 'bg-green-100 text-green-800'
	if (s === 'Warm') return 'bg-orange-100 text-orange-800'
	if (s === 'Cold') return 'bg-blue-100 text-blue-800'
	if (s === 'Negative') return 'bg-red-100 text-red-800'
	return 'bg-gray-100 text-gray-800'
}

function getCallBadgeClasses(status) {
	const s = (status || '').trim()
	if (s === 'Completed') return 'bg-green-100 text-green-800'
	if (s === 'Failed') return 'bg-red-100 text-red-800'
	if (s === 'Initiated') return 'bg-blue-100 text-blue-800'
	if (s === 'No Answer') return 'bg-orange-100 text-orange-800'
	return 'bg-gray-100 text-gray-800'
}

function renderMarkdown(text) {
	if (!text) return '<span class="text-gray-400 italic">No data available.</span>'

	let html = text
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/\n/g, '<br>')
		.replace(/\*\*(.*?)\*\*/g, '<strong class="text-gray-900 font-bold">$1</strong>')
		// CHANGE 7: AI Prefix uses Accent Color
		.replace(/(Alex \(AI\):)/g, '<span class="text-[#4318FF] font-medium">$1</span>')
		.replace(/^- (.*)/gm, '<li class="ml-4 list-disc">$1</li>')

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
		alert('Failed to save log.')
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
		alert('Failed to delete log.')
	} finally {
		deleting.value = false
	}
}
</script>
