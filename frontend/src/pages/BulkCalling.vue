<template>
	<div class="p-8 max-w-7xl mx-auto h-full flex flex-col">
		<div class="flex justify-between items-center mb-8">
			<div>
				<h1 class="text-3xl font-bold text-gray-900">Bulk Calling</h1>
				<p class="text-gray-600 mt-1">Create groups and trigger AI campaigns</p>
			</div>
			<Button
				v-if="groups.data && groups.data.length > 0"
				variant="solid"
				class="!bg-[#4318FF] hover:!bg-[#3311CC] !text-white border-transparent"
				@click="openCreateDialog"
			>
				<template #prefix><FeatherIcon name="plus" class="h-4 w-4" /></template>
				New Group
			</Button>
		</div>

		<div v-if="groups.loading" class="flex-1 flex items-center justify-center">
			<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[#4318FF]"></div>
		</div>

		<div
			v-else-if="!groups.data || groups.data.length === 0"
			class="flex-1 flex flex-col items-center justify-center text-center opacity-80"
		>
			<div class="bg-gray-50 p-6 rounded-full mb-4">
				<FeatherIcon name="layers" class="h-10 w-10 text-gray-400" />
			</div>
			<h3 class="text-xl font-bold text-gray-900">No groups found</h3>
			<p class="text-gray-500 max-w-sm mt-2 mb-6">
				Create your first contact group to start a bulk calling campaign.
			</p>
			<Button
				variant="solid"
				size="lg"
				class="!bg-[#4318FF] hover:!bg-[#3311CC] !text-white border-transparent"
				@click="openCreateDialog"
			>
				<template #prefix><FeatherIcon name="plus" class="h-4 w-4" /></template>
				Create Group
			</Button>
		</div>

		<div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
			<div
				v-for="group in groups.data"
				:key="group.name"
				class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all flex flex-col justify-between group cursor-pointer"
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

					<div class="mt-4 flex -space-x-2 overflow-hidden">
						<div
							class="inline-block h-8 w-8 rounded-full ring-2 ring-white bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-500"
						>
							#
						</div>
						<div
							class="inline-block h-8 w-8 rounded-full ring-2 ring-white bg-[#4318FF]/10 flex items-center justify-center text-xs font-bold text-[#4318FF]"
						>
							AI
						</div>
						<div
							class="inline-block h-8 w-8 rounded-full ring-2 ring-white bg-gray-50 flex items-center justify-center text-xs text-gray-400"
						>
							<FeatherIcon name="users" class="h-3 w-3" />
						</div>
					</div>
				</div>

				<div class="mt-6 flex items-center justify-between border-t border-gray-100 pt-4">
					<span class="text-xs font-semibold text-gray-500">Click to view details</span>
					<FeatherIcon
						name="arrow-right"
						class="h-4 w-4 text-[#4318FF] opacity-0 group-hover:opacity-100 transition-opacity"
					/>
				</div>
			</div>
		</div>

		<Dialog v-model="showCreateDialog" :options="{ size: 'xl' }">
			<template #body-title>
				<h3 class="text-xl font-bold">
					{{ createStep === 1 ? 'Name Your Group' : 'Add Members' }}
				</h3>
			</template>
			<template #body-content>
				<div v-if="createStep === 1" class="mt-4 space-y-4">
					<p class="text-sm text-gray-600">Give your new contact group a clear name.</p>
					<div class="space-y-1">
						<label class="block text-sm font-medium text-gray-700">Group Title</label>
						<input
							v-model="newGroupTitle"
							type="text"
							placeholder="e.g. Real Estate Leads - Oct"
							class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#4318FF] focus:ring-[#4318FF] sm:text-sm px-3 py-2 border"
						/>
					</div>
				</div>

				<div v-if="createStep === 2" class="mt-4 flex flex-col h-[50vh]">
					<div class="mb-4">
						<input
							v-model="contactSearch"
							type="text"
							placeholder="Search contacts..."
							class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#4318FF] focus:ring-[#4318FF] sm:text-sm px-3 py-2 border"
						/>
					</div>

					<div class="flex-1 overflow-y-auto border border-gray-200 rounded-lg">
						<div v-if="contacts.loading" class="p-4 text-center text-gray-500">
							Loading contacts...
						</div>
						<div
							v-else-if="filteredContacts.length === 0"
							class="p-4 text-center text-gray-500"
						>
							No contacts found
						</div>

						<table v-else class="min-w-full divide-y divide-gray-200">
							<thead class="bg-gray-50 sticky top-0">
								<tr>
									<th
										scope="col"
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-10"
									>
										<input
											type="checkbox"
											:checked="isAllSelected"
											@change="toggleAllSelection"
											class="rounded border-gray-300 text-[#4318FF] focus:ring-[#4318FF]"
										/>
									</th>
									<th
										scope="col"
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Name
									</th>
									<th
										scope="col"
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										Phone
									</th>
								</tr>
							</thead>
							<tbody class="bg-white divide-y divide-gray-200">
								<tr
									v-for="contact in filteredContacts"
									:key="contact.name"
									class="hover:bg-gray-50 cursor-pointer"
									@click="toggleSelection(contact)"
								>
									<td class="px-6 py-4 whitespace-nowrap">
										<input
											type="checkbox"
											:checked="selectedContacts.has(contact.name)"
											class="rounded border-gray-300 text-[#4318FF] focus:ring-[#4318FF] pointer-events-none"
										/>
									</td>
									<td
										class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
									>
										{{ contact.first_name }} {{ contact.last_name }}
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
										{{ contact.mobile_no || contact.phone }}
									</td>
								</tr>
							</tbody>
						</table>
					</div>
					<div class="mt-2 text-sm text-gray-500 text-right">
						{{ selectedContacts.size }} contacts selected
					</div>
				</div>
			</template>
			<template #actions>
				<div class="flex w-full justify-between">
					<Button variant="subtle" @click="closeCreateDialog">Cancel</Button>
					<div class="flex gap-2">
						<Button v-if="createStep === 2" variant="outline" @click="createStep = 1"
							>Back</Button
						>
						<Button
							v-if="createStep === 1"
							variant="solid"
							class="!bg-[#4318FF] !text-white"
							:disabled="!newGroupTitle"
							@click="createStep = 2"
						>
							Next
						</Button>
						<Button
							v-if="createStep === 2"
							variant="solid"
							class="!bg-[#4318FF] !text-white"
							:disabled="selectedContacts.size === 0"
							:loading="creating"
							@click="createGroup"
						>
							Create Group
						</Button>
					</div>
				</div>
			</template>
		</Dialog>

		<Dialog v-model="showDetailsDialog" :options="{ size: '2xl' }">
			<template #body-title>
				<div class="flex justify-between items-center w-full pr-8">
					<h3 class="text-xl font-bold">{{ selectedGroup?.title }}</h3>
					<Badge theme="gray" size="lg">{{ groupMembers.length }} Members</Badge>
				</div>
			</template>
			<template #body-content>
				<div class="mt-4 h-[50vh] flex flex-col">
					<div class="flex-1 overflow-y-auto border border-gray-200 rounded-lg">
						<div v-if="detailsLoading" class="p-6 text-center text-gray-500">
							Loading members...
						</div>
						<table v-else class="min-w-full divide-y divide-gray-200">
							<thead class="bg-gray-50 sticky top-0">
								<tr>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
									>
										Contact Name
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
									>
										Phone
									</th>
									<th
										class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
									>
										Status
									</th>
								</tr>
							</thead>
							<tbody class="bg-white divide-y divide-gray-200">
								<tr v-for="member in groupMembers" :key="member.name">
									<td class="px-6 py-4 text-sm font-medium text-gray-900">
										{{ member.contact_name }}
									</td>
									<td class="px-6 py-4 text-sm text-gray-500 font-mono">
										{{ member.phone_number }}
									</td>
									<td class="px-6 py-4 text-sm text-gray-500">
										<Badge theme="gray">Pending</Badge>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</template>
			<template #actions>
				<div class="flex w-full justify-between items-center">
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
							:loading="triggering"
							@click="startBulkCall"
						>
							<template #prefix
								><FeatherIcon name="phone-call" class="h-4 w-4"
							/></template>
							Start Bulk Calling
						</Button>
					</div>
				</div>
			</template>
		</Dialog>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { createResource, Button, Dialog, FeatherIcon, Badge } from 'frappe-ui'

// --- STATE ---
const showCreateDialog = ref(false)
const createStep = ref(1)
const newGroupTitle = ref('')
const contactSearch = ref('')
const selectedContacts = ref(new Set())
const creating = ref(false)

const showDetailsDialog = ref(false)
const selectedGroup = ref(null)
const groupMembers = ref([])
const detailsLoading = ref(false)
const triggering = ref(false)

// --- RESOURCES ---

// 1. Fetch Groups (FIXED: Uses single path)
const groups = createResource({
	url: 'ai_calling_agent.api.get_call_groups',
	auto: true,
})

// 2. Fetch Contacts
const contacts = createResource({
	url: 'frappe.client.get_list',
	makeParams() {
		return {
			doctype: 'Contact',
			fields: ['name', 'first_name', 'last_name', 'mobile_no', 'phone'],
			limit: 1000,
		}
	},
})

// --- COMPUTED ---

const filteredContacts = computed(() => {
	if (!contacts.data) return []
	const search = contactSearch.value.toLowerCase()
	return contacts.data.filter((c) => {
		const hasPhone = c.mobile_no || c.phone
		if (!hasPhone) return false

		const name = `${c.first_name || ''} ${c.last_name || ''}`.toLowerCase()
		const phone = (c.mobile_no || c.phone || '').toLowerCase()
		return name.includes(search) || phone.includes(search)
	})
})

const isAllSelected = computed(() => {
	return (
		filteredContacts.value.length > 0 &&
		filteredContacts.value.every((c) => selectedContacts.value.has(c.name))
	)
})

// --- ACTIONS: CREATE GROUP ---

function openCreateDialog() {
	newGroupTitle.value = ''
	selectedContacts.value.clear()
	createStep.value = 1
	contacts.fetch()
	showCreateDialog.value = true
}

function closeCreateDialog() {
	showCreateDialog.value = false
}

function toggleSelection(contact) {
	if (selectedContacts.value.has(contact.name)) {
		selectedContacts.value.delete(contact.name)
	} else {
		selectedContacts.value.add(contact.name)
	}
}

function toggleAllSelection() {
	if (isAllSelected.value) {
		filteredContacts.value.forEach((c) => selectedContacts.value.delete(c.name))
	} else {
		filteredContacts.value.forEach((c) => selectedContacts.value.add(c.name))
	}
}

async function createGroup() {
	creating.value = true

	const memberList = []
	selectedContacts.value.forEach((docName) => {
		const contact = contacts.data.find((c) => c.name === docName)
		if (contact) {
			memberList.push({
				name: `${contact.first_name || ''} ${contact.last_name || ''}`.trim(),
				phone: contact.mobile_no || contact.phone,
			})
		}
	})

	try {
		// FIXED: Uses single path
		const res = await fetch('/api/method/ai_calling_agent.api.create_call_group', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				title: newGroupTitle.value,
				members: JSON.stringify(memberList),
			}),
		})

		const data = await res.json()
		if (res.ok) {
			groups.fetch()
			showCreateDialog.value = false
		} else {
			alert(data.message || 'Error creating group')
		}
	} catch (e) {
		console.error(e)
		alert('Failed to create group')
	} finally {
		creating.value = false
	}
}

// --- ACTIONS: DETAILS & BULK CALL ---

async function openGroupDetails(group) {
	selectedGroup.value = group
	showDetailsDialog.value = true
	detailsLoading.value = true
	groupMembers.value = []

	try {
		const res = await fetch(`/api/resource/Call Group/${group.name}`)
		const data = await res.json()
		if (data.data) {
			groupMembers.value = data.data.members || []
		}
	} catch (e) {
		console.error(e)
	} finally {
		detailsLoading.value = false
	}
}

async function startBulkCall() {
	if (!selectedGroup.value) return

	if (
		!confirm(
			`Are you sure you want to call all ${groupMembers.value.length} members in this group?`
		)
	)
		return

	triggering.value = true
	try {
		// FIXED: Uses single path
		const res = await fetch('/api/method/ai_calling_agent.api.trigger_bulk_call', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				group_name: selectedGroup.value.name,
			}),
		})

		const data = await res.json()
		if (res.ok) {
			alert('Bulk call campaign started successfully! Logs will appear in the dashboard.')
			showDetailsDialog.value = false
		} else {
			alert(data.message || 'Failed to start bulk call')
		}
	} catch (e) {
		console.error(e)
		alert('An error occurred')
	} finally {
		triggering.value = false
	}
}

async function deleteGroup() {
	if (!confirm('Are you sure you want to delete this group? This action cannot be undone.'))
		return

	try {
		await fetch(`/api/resource/Call Group/${selectedGroup.value.name}`, {
			method: 'DELETE',
		})
		groups.fetch()
		showDetailsDialog.value = false
	} catch (e) {
		console.error(e)
		alert('Failed to delete group')
	}
}

// --- HELPER ---
function formatDate(dateStr) {
	if (!dateStr) return ''
	return new Date(dateStr).toLocaleDateString()
}
</script>
