<template>
	<div class="p-8 max-w-7xl mx-auto h-full flex flex-col">
		<div class="flex justify-between items-center mb-8">
			<div>
				<h1 class="text-3xl font-bold text-gray-900">Bulk Emailing</h1>
				<p class="text-gray-600 mt-1">Manage email groups and campaigns</p>
			</div>
			<div class="flex gap-2">
				<Button variant="outline" @click="openImportDialog">
					<template #prefix><FeatherIcon name="download" class="h-4 w-4" /></template>
					Import from Call Group
				</Button>
				<Button
					variant="solid"
					class="!bg-[#4318FF] hover:!bg-[#3311CC] !text-white border-transparent"
					@click="openCreateDialog"
				>
					<template #prefix><FeatherIcon name="plus" class="h-4 w-4" /></template>
					New Group
				</Button>
			</div>
		</div>

		<div v-if="emailGroups.loading" class="flex-1 flex items-center justify-center">
			<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[#4318FF]"></div>
		</div>

		<div
			v-else-if="!emailGroups.data || emailGroups.data.length === 0"
			class="flex-1 flex flex-col items-center justify-center text-center opacity-80"
		>
			<div class="bg-gray-50 p-6 rounded-full mb-4">
				<FeatherIcon name="mail" class="h-10 w-10 text-gray-400" />
			</div>
			<h3 class="text-xl font-bold text-gray-900">No Email Groups</h3>
			<p class="text-gray-500 max-w-sm mt-2 mb-6">
				Import contacts from your call lists or create a new email group.
			</p>
		</div>

		<div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
			<div
				v-for="group in emailGroups.data"
				:key="group.name"
				class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all cursor-pointer group flex flex-col justify-between"
				@click="openGroupDetails(group)"
			>
				<div>
					<div class="flex justify-between items-start mb-2">
						<h3
							class="font-bold text-lg text-gray-900 group-hover:text-[#4318FF] transition-colors"
						>
							{{ group.title }}
						</h3>
						<FeatherIcon name="more-horizontal" class="h-5 w-5 text-gray-400" />
					</div>
					<p class="text-xs text-gray-500 font-medium">
						Created on {{ formatDate(group.creation) }}
					</p>
				</div>
				<div
					class="mt-4 flex items-center gap-2 text-sm text-gray-600 bg-gray-50 p-2 rounded"
				>
					<FeatherIcon name="mail" class="h-4 w-4 text-[#4318FF]" />
					<span>Ready to send</span>
				</div>
			</div>
		</div>

		<Dialog v-model="showImportDialog">
			<template #body-title>
				<h3 class="text-xl font-bold">Import from Call Group</h3>
			</template>
			<template #body-content>
				<div class="mt-4 space-y-4">
					<p class="text-sm text-gray-600">
						Select an existing Call Group. We will automatically fetch the email
						addresses for its members.
					</p>
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-1"
							>Select Source Group</label
						>
						<select
							v-model="selectedCallGroup"
							class="w-full rounded-md border-gray-300 shadow-sm focus:border-[#4318FF] focus:ring-[#4318FF] sm:text-sm px-3 py-2 border"
						>
							<option disabled value="">-- Select a Call Group --</option>
							<option v-for="cg in callGroups.data" :key="cg.name" :value="cg.name">
								{{ cg.title }}
							</option>
						</select>
					</div>
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-1"
							>New Email Group Name</label
						>
						<input
							v-model="importName"
							type="text"
							placeholder="e.g. Follow-up Campaign A"
							class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#4318FF] focus:ring-[#4318FF] sm:text-sm px-3 py-2 border"
						/>
					</div>
				</div>
			</template>
			<template #actions>
				<Button variant="subtle" @click="showImportDialog = false">Cancel</Button>
				<Button
					variant="solid"
					class="!bg-[#4318FF] hover:!bg-[#3311CC] !text-white border-transparent"
					:loading="importing"
					:disabled="!selectedCallGroup || !importName"
					@click="importGroup"
				>
					Import & Create
				</Button>
			</template>
		</Dialog>

		<Dialog v-model="showCreateDialog" :options="{ size: 'xl' }">
			<template #body-title>
				<h3 class="text-xl font-bold">Create New Email Group</h3>
			</template>
			<template #body-content>
				<div class="mt-4 h-[70vh] flex flex-col space-y-4">
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-1"
							>Group Title</label
						>
						<input
							v-model="newGroupTitle"
							type="text"
							placeholder="e.g. Newsletter Subscribers"
							class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#4318FF] focus:ring-[#4318FF] sm:text-sm px-3 py-2 border"
						/>
					</div>

					<div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
						<label class="block text-sm font-bold text-gray-700 mb-2"
							>Add Emails Manually</label
						>
						<div class="flex gap-2 mb-3">
							<input
								v-model="manualEmailInput"
								@keyup.enter="addManualEmail"
								type="email"
								placeholder="Enter email address (e.g. client@gmail.com)"
								class="block flex-1 rounded-md border-gray-300 shadow-sm focus:border-[#4318FF] focus:ring-[#4318FF] sm:text-sm px-3 py-2 border"
							/>
							<Button variant="outline" @click="addManualEmail">Add</Button>
						</div>

						<div
							v-if="manualEmails.length > 0"
							class="flex flex-wrap gap-2 max-h-24 overflow-y-auto"
						>
							<div
								v-for="(email, idx) in manualEmails"
								:key="idx"
								class="bg-white border border-gray-300 text-gray-700 px-2 py-1 rounded-md text-xs flex items-center gap-2"
							>
								<span>{{ email }}</span>
								<button
									@click="removeManualEmail(idx)"
									class="text-red-500 hover:text-red-700"
								>
									<FeatherIcon name="x" class="h-3 w-3" />
								</button>
							</div>
						</div>
						<div v-else class="text-xs text-gray-400 italic">
							No manual emails added yet.
						</div>
					</div>

					<div class="flex-1 flex flex-col min-h-0 border border-gray-200 rounded-lg">
						<div
							class="bg-gray-100 p-2 border-b border-gray-200 flex justify-between items-center"
						>
							<span class="text-sm font-bold text-gray-700"
								>Select from Contacts</span
							>
							<span class="text-xs text-gray-500"
								>{{ selectedContactsManual.length }} selected</span
							>
						</div>

						<div v-if="contacts.loading" class="p-4 text-center">
							Loading contacts...
						</div>
						<div v-else class="flex-1 overflow-y-auto bg-white">
							<table class="min-w-full divide-y divide-gray-200">
								<thead class="bg-gray-50 sticky top-0">
									<tr>
										<th class="px-4 py-2 w-10">
											<input
												type="checkbox"
												@change="toggleAllManual"
												:checked="isAllManualSelected"
												class="rounded text-[#4318FF] focus:ring-[#4318FF]"
											/>
										</th>
										<th
											class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
										>
											Name
										</th>
										<th
											class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
										>
											Email
										</th>
									</tr>
								</thead>
								<tbody class="divide-y divide-gray-200">
									<tr
										v-for="c in contactsWithEmails"
										:key="c.name"
										class="hover:bg-gray-50"
									>
										<td class="px-4 py-2">
											<input
												type="checkbox"
												:value="c.name"
												v-model="selectedContactsManual"
												class="rounded text-[#4318FF] focus:ring-[#4318FF]"
											/>
										</td>
										<td class="px-4 py-2 text-sm font-medium text-gray-900">
											{{ c.first_name }} {{ c.last_name }}
										</td>
										<td class="px-4 py-2 text-sm text-gray-500">
											{{ c.email_id }}
										</td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>

					<div class="text-right text-sm text-gray-600">
						Total Recipients: <strong>{{ totalRecipients }}</strong> ({{
							selectedContactsManual.length
						}}
						Contacts + {{ manualEmails.length }} Manual)
					</div>
				</div>
			</template>
			<template #actions>
				<Button variant="subtle" @click="showCreateDialog = false">Cancel</Button>
				<Button
					variant="solid"
					class="!bg-[#4318FF] hover:!bg-[#3311CC] !text-white border-transparent"
					:loading="creating"
					:disabled="!newGroupTitle || totalRecipients === 0"
					@click="createManualGroup"
				>
					Create Group
				</Button>
			</template>
		</Dialog>

		<Dialog v-model="showDetailsDialog" :options="{ size: 'xl' }">
			<template #body-title>
				<h3 class="text-xl font-bold">{{ selectedGroup?.title }}</h3>
			</template>
			<template #body-content>
				<div class="mt-4 space-y-4">
					<div
						class="bg-blue-50 border border-blue-100 text-blue-700 px-4 py-3 rounded-md text-sm flex items-center gap-2"
					>
						<FeatherIcon name="info" class="h-4 w-4" />
						<span
							>This group contains
							<strong>{{ currentGroupMembers.length }}</strong> members.</span
						>
					</div>

					<div
						class="max-h-32 overflow-y-auto border border-gray-200 rounded p-2 text-xs text-gray-600"
					>
						<div
							v-for="m in currentGroupMembers"
							:key="m.email"
							class="flex justify-between py-1 border-b border-gray-100 last:border-0"
						>
							<span>{{ m.contact_name || 'Guest' }}</span>
							<span class="font-mono">{{ m.email }}</span>
						</div>
					</div>

					<div>
						<label class="block text-sm font-medium text-gray-700 mb-1"
							>Email Subject</label
						>
						<input
							v-model="emailSubject"
							type="text"
							placeholder="e.g. Exclusive Offer for You"
							class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#4318FF] focus:ring-[#4318FF] sm:text-sm px-3 py-2 border"
						/>
					</div>

					<div>
						<label class="block text-sm font-medium text-gray-700 mb-1"
							>Email Content</label
						>
						<textarea
							v-model="emailBody"
							rows="6"
							placeholder="Type your message here..."
							class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#4318FF] focus:ring-[#4318FF] sm:text-sm px-3 py-2 border"
						></textarea>
					</div>
				</div>
			</template>
			<template #actions>
				<div class="flex justify-between w-full items-center">
					<Button
						variant="ghost"
						theme="red"
						class="text-red-600 hover:bg-red-50"
						@click="deleteGroup"
					>
						<template #prefix><FeatherIcon name="trash-2" class="h-4 w-4" /></template>
						Delete Group
					</Button>

					<div class="flex gap-2">
						<Button variant="subtle" @click="showDetailsDialog = false">Close</Button>
						<Button
							variant="solid"
							class="!bg-[#4318FF] hover:!bg-[#3311CC] !text-white border-transparent"
							:loading="sending"
							:disabled="!emailSubject || !emailBody"
							@click="sendCampaign"
						>
							<template #prefix
								><FeatherIcon name="send" class="h-4 w-4"
							/></template>
							Send Campaign
						</Button>
					</div>
				</div>
			</template>
		</Dialog>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { createResource, Button, Dialog, FeatherIcon } from 'frappe-ui'

// --- FIXED PATHS (Single Path) ---
const emailGroups = createResource({
	url: 'ai_calling_agent.api.get_email_groups',
	auto: true,
})

const callGroups = createResource({
	url: 'ai_calling_agent.api.get_call_groups',
})

// --- FIXED SYNTAX: makeParams -> params ---
const contacts = createResource({
	url: 'frappe.client.get_list',
	params: {
		doctype: 'Contact',
		fields: ['name', 'first_name', 'last_name', 'email_id'],
		limit: 1000,
	},
})

// --- STATE ---
const showImportDialog = ref(false)
const showCreateDialog = ref(false)
const showDetailsDialog = ref(false)

const selectedCallGroup = ref('')
const importName = ref('')
const importing = ref(false)

const newGroupTitle = ref('')
const selectedContactsManual = ref([])
const manualEmailInput = ref('')
const manualEmails = ref([])
const creating = ref(false)

const selectedGroup = ref(null)
const currentGroupMembers = ref([])
const emailSubject = ref('')
const emailBody = ref('')
const sending = ref(false)

// --- COMPUTED ---
const contactsWithEmails = computed(() => {
	return (contacts.data || []).filter((c) => c.email_id)
})

const isAllManualSelected = computed(() => {
	return (
		contactsWithEmails.value.length > 0 &&
		contactsWithEmails.value.every((c) => selectedContactsManual.value.includes(c.name))
	)
})

const totalRecipients = computed(() => {
	return selectedContactsManual.value.length + manualEmails.value.length
})

// --- ACTIONS ---

function openImportDialog() {
	callGroups.fetch()
	selectedCallGroup.value = ''
	importName.value = ''
	showImportDialog.value = true
}

async function importGroup() {
	if (!selectedCallGroup.value || !importName.value) return
	importing.value = true
	try {
		// FIXED PATH
		const res = await fetch('/api/method/ai_calling_agent.api.import_call_group_to_email', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				call_group_name: selectedCallGroup.value,
				new_title: importName.value,
			}),
		})
		const data = await res.json()
		if (res.ok) {
			alert(data.message)
			emailGroups.fetch()
			showImportDialog.value = false
		} else {
			alert(data.message || 'Import Failed')
		}
	} catch (e) {
		console.error(e)
	} finally {
		importing.value = false
	}
}

function openCreateDialog() {
	contacts.fetch()
	newGroupTitle.value = ''
	selectedContactsManual.value = []
	manualEmails.value = []
	manualEmailInput.value = ''
	showCreateDialog.value = true
}

function addManualEmail() {
	const email = manualEmailInput.value.trim()
	if (!email) return
	if (!email.includes('@') || !email.includes('.')) {
		alert('Please enter a valid email address.')
		return
	}
	if (!manualEmails.value.includes(email)) {
		manualEmails.value.push(email)
	}
	manualEmailInput.value = ''
}

function removeManualEmail(index) {
	manualEmails.value.splice(index, 1)
}

function toggleAllManual() {
	if (isAllManualSelected.value) {
		selectedContactsManual.value = []
	} else {
		selectedContactsManual.value = contactsWithEmails.value.map((c) => c.name)
	}
}

async function createManualGroup() {
	if (!newGroupTitle.value || totalRecipients.value === 0) return
	creating.value = true

	const contactMembers = selectedContactsManual.value.map((id) => {
		const c = contacts.data.find((x) => x.name === id)
		return { name: c.name, email: c.email_id }
	})

	const manualMembers = manualEmails.value.map((email) => {
		return { name: 'External', email: email }
	})

	const allMembers = [...contactMembers, ...manualMembers]

	try {
		// FIXED PATH
		await fetch('/api/method/ai_calling_agent.api.create_email_group', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				title: newGroupTitle.value,
				members: JSON.stringify(allMembers),
			}),
		})
		emailGroups.fetch()
		showCreateDialog.value = false
	} catch (e) {
		console.error(e)
	} finally {
		creating.value = false
	}
}

async function openGroupDetails(group) {
	selectedGroup.value = group
	currentGroupMembers.value = []
	emailSubject.value = ''
	emailBody.value = ''

	try {
		const res = await fetch(`/api/resource/AI Email Group/${group.name}`)
		const d = await res.json()
		if (d.data && d.data.members) {
			currentGroupMembers.value = d.data.members
		}
		showDetailsDialog.value = true
	} catch (e) {
		console.error(e)
	}
}

async function sendCampaign() {
	if (!selectedGroup.value) return
	sending.value = true
	try {
		// FIXED PATH
		const res = await fetch('/api/method/ai_calling_agent.api.trigger_email_campaign', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				group_name: selectedGroup.value.name,
				subject: emailSubject.value,
				message: emailBody.value,
			}),
		})
		const data = await res.json()
		if (res.ok) {
			alert(data.message)
			showDetailsDialog.value = false
		} else {
			alert(data.message || 'Failed')
		}
	} catch (e) {
		console.error(e)
		alert('Failed to start campaign')
	} finally {
		sending.value = false
	}
}

async function deleteGroup() {
	if (!confirm('Are you sure you want to delete this email group?')) return
	try {
		await fetch(`/api/resource/AI Email Group/${selectedGroup.value.name}`, {
			method: 'DELETE',
		})
		emailGroups.fetch()
		showDetailsDialog.value = false
	} catch (e) {
		console.error(e)
		alert('Failed to delete')
	}
}

function formatDate(d) {
	if (!d) return ''
	return new Date(d).toLocaleDateString()
}
</script>
