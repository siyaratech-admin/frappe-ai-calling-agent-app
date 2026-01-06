<template>
	<div class="p-8 max-w-7xl mx-auto relative">
		<div class="flex justify-between items-center mb-6">
			<div>
				<h1 class="text-2xl font-bold text-gray-900">Contacts</h1>
				<p class="text-sm text-gray-500 mt-1">Synced with Frappe CRM</p>
			</div>
			<Button
				variant="solid"
				size="md"
				class="!bg-[#4318FF] hover:!bg-[#3311CC] !text-white border-transparent"
				@click="openCRMAddContact"
			>
				<template #prefix>
					<FeatherIcon name="plus" class="h-4 w-4" />
				</template>
				Add Contact (CRM)
			</Button>
		</div>

		<div class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
			<table class="w-full text-left text-sm">
				<thead class="bg-gray-50 border-b border-gray-200 text-gray-500 font-medium">
					<tr>
						<th class="px-6 py-3">Name & Designation</th>
						<th class="px-6 py-3">Status</th>
						<th class="px-6 py-3">Contact Info</th>
						<th class="px-6 py-3">Company</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-100">
					<tr v-if="contacts.loading">
						<td colspan="4" class="p-6 text-center text-gray-500">
							Loading contacts...
						</td>
					</tr>
					<tr v-else-if="!contacts.data || contacts.data.length === 0">
						<td colspan="4" class="p-6 text-center text-gray-500">
							No contacts found.
						</td>
					</tr>
					<tr
						v-else
						v-for="contact in contacts.data"
						:key="contact.name"
						@click="openDetails(contact)"
						class="hover:bg-gray-50 transition-colors cursor-pointer group"
					>
						<td class="px-6 py-4">
							<div
								class="font-medium text-gray-900 group-hover:text-[#4318FF] transition-colors"
							>
								{{ contact.first_name }} {{ contact.last_name }}
							</div>
							<div class="text-xs text-gray-400 mt-0.5">
								{{ contact.designation || 'No Designation' }}
							</div>
						</td>
						<td class="px-6 py-4">
							<Badge :theme="getStatusColor(contact.status)">
								{{ contact.status }}
							</Badge>
						</td>
						<td class="px-6 py-4">
							<div class="text-gray-900">{{ contact.email_id || '-' }}</div>
							<div class="text-gray-500 mt-0.5">
								{{ contact.mobile_no || contact.phone || '-' }}
							</div>
						</td>
						<td class="px-6 py-4 text-gray-600">
							{{ contact.company_name || '-' }}
						</td>
					</tr>
				</tbody>
			</table>
		</div>

		<Dialog v-model="showDetailsDialog" :options="{ size: 'xl' }">
			<template #body-title>
				<h3 class="text-xl font-bold">Contact Details</h3>
			</template>
			<template #body-content>
				<div v-if="selectedContact" class="mt-6 space-y-6">
					<div class="flex items-start justify-between border-b border-gray-100 pb-6">
						<div class="flex gap-4">
							<div
								class="h-16 w-16 rounded-full bg-[#4318FF]/10 flex items-center justify-center text-2xl font-bold text-[#4318FF]"
							>
								{{ getInitials(selectedContact) }}
							</div>
							<div>
								<h2 class="text-2xl font-bold text-gray-900">
									{{
										selectedContact.salutation
											? selectedContact.salutation + ' '
											: ''
									}}
									{{ selectedContact.first_name }}
									{{ selectedContact.last_name }}
								</h2>
								<div class="text-gray-500">{{ selectedContact.designation }}</div>
								<div class="mt-2">
									<Badge
										:theme="getStatusColor(selectedContact.status)"
										size="lg"
									>
										{{ selectedContact.status }}
									</Badge>
								</div>
							</div>
						</div>
					</div>

					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<div class="space-y-1">
							<div class="text-xs font-semibold text-gray-500 uppercase">
								Contact Info
							</div>
							<div class="flex items-center gap-2 text-gray-700">
								<FeatherIcon name="mail" class="h-4 w-4 text-[#4318FF]" />
								{{ selectedContact.email_id || 'No Email' }}
							</div>
							<div class="flex items-center gap-2 text-gray-700">
								<FeatherIcon name="phone" class="h-4 w-4 text-[#4318FF]" />
								{{
									selectedContact.mobile_no ||
									selectedContact.phone ||
									'No Phone'
								}}
							</div>
						</div>

						<div class="space-y-1">
							<div class="text-xs font-semibold text-gray-500 uppercase">
								Professional
							</div>
							<div class="flex items-center gap-2 text-gray-700">
								<FeatherIcon name="briefcase" class="h-4 w-4 text-[#4318FF]" />
								{{ selectedContact.company_name || 'No Company' }}
							</div>
							<div class="flex items-center gap-2 text-gray-700">
								<FeatherIcon name="user" class="h-4 w-4 text-[#4318FF]" />
								{{ selectedContact.gender || 'Gender Not Specified' }}
							</div>
						</div>
					</div>

					<div class="bg-gray-50 p-4 rounded-lg flex items-center justify-between mt-4">
						<div class="text-sm text-gray-600">
							<span v-if="getPhoneNumber(selectedContact)">
								Ready to call
								<strong>{{ getPhoneNumber(selectedContact) }}</strong>
							</span>
							<span v-else class="text-red-500">No phone number available.</span>
						</div>

						<Button
							variant="solid"
							class="!bg-[#4318FF] hover:!bg-[#3311CC] !text-white border-transparent"
							:loading="callLoading"
							:disabled="!getPhoneNumber(selectedContact)"
							@click="initiateCall"
						>
							<template #prefix>
								<FeatherIcon name="phone-call" class="h-4 w-4" />
							</template>
							Start AI Call
						</Button>
					</div>
				</div>
			</template>
			<template #actions>
				<Button variant="subtle" @click="showDetailsDialog = false">Close</Button>
				<Button variant="outline" @click="openInDesk">Open in Desk</Button>
			</template>
		</Dialog>

		<transition name="fade">
			<div
				v-if="toast.show"
				class="fixed bottom-6 right-6 z-50 flex items-center gap-3 px-4 py-3 bg-white rounded-lg shadow-lg border border-gray-100 max-w-sm"
			>
				<div
					class="flex items-center justify-center w-8 h-8 rounded-full"
					:class="
						toast.type === 'success'
							? 'bg-green-100 text-green-600'
							: 'bg-red-100 text-red-600'
					"
				>
					<FeatherIcon
						:name="toast.type === 'success' ? 'check' : 'alert-circle'"
						class="h-5 w-5"
					/>
				</div>
				<div>
					<h4 class="text-sm font-semibold text-gray-900">{{ toast.title }}</h4>
					<p class="text-xs text-gray-500">{{ toast.message }}</p>
				</div>
			</div>
		</transition>
	</div>
</template>

<script setup>
import { ref } from 'vue'
import { createResource, Button, Dialog, Badge, FeatherIcon } from 'frappe-ui'

const showDetailsDialog = ref(false)
const selectedContact = ref(null)
const callLoading = ref(false)

// Toast State
const toast = ref({
	show: false,
	title: '',
	message: '',
	type: 'success', // 'success' or 'error'
})

// Fetch Contacts Resource
const contacts = createResource({
	url: 'frappe.client.get_list',
	params: {
		doctype: 'Contact',
		fields: [
			'name',
			'first_name',
			'last_name',
			'salutation',
			'email_id',
			'mobile_no',
			'phone',
			'status',
			'designation',
			'company_name',
			'gender',
		],
		order_by: 'creation desc',
		limit: 50,
	},
	auto: true,
})

// --- ACTIONS ---

function openCRMAddContact() {
	window.open('/app/contact/new', '_blank')
}

function openDetails(contact) {
	selectedContact.value = contact
	showDetailsDialog.value = true
}

function openInDesk() {
	if (selectedContact.value) {
		window.open(`/app/contact/${selectedContact.value.name}`, '_blank')
	}
}

function showToast(title, message, type = 'success') {
	toast.value = { show: true, title, message, type }
	setTimeout(() => {
		toast.value.show = false
	}, 4000)
}

async function initiateCall() {
	const contact = selectedContact.value
	const phone = getPhoneNumber(contact)

	if (!phone) {
		showToast('Missing Info', 'No phone number found for this contact.', 'error')
		return
	}

	callLoading.value = true

	try {
		const response = await fetch('/api/method/ai_calling_agent.api.start_ai_call', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				phone_number: `${phone}`, // Ensure proper format or handle dynamic country codes
				contact_docname: contact.name,
			}),
		})

		const data = await response.json()

		if (response.ok) {
			showToast('Call Initiated', 'Connecting agent...', 'success')
			showDetailsDialog.value = false
		} else {
			throw new Error(data.message || 'Server Error')
		}
	} catch (error) {
		console.error(error)
		showToast('Error', `Failed to start call: ${error.message}`, 'error')
	} finally {
		callLoading.value = false
	}
}

// --- HELPERS ---

function getPhoneNumber(contact) {
	return contact.mobile_no || contact.phone || null
}

function getStatusColor(status) {
	if (status === 'Open') return 'green'
	if (status === 'Replied') return 'blue'
	if (status === 'Passive') return 'orange'
	return 'gray'
}

function getInitials(contact) {
	const f = contact.first_name ? contact.first_name[0] : ''
	const l = contact.last_name ? contact.last_name[0] : ''
	return (f + l).toUpperCase()
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
	transform: translateY(10px);
}
</style>
