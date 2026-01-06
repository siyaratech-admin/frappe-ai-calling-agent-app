<template>
	<div class="flex flex-col h-full">
		<div class="px-8 py-6 border-b border-gray-100 bg-white">
			<h1 class="text-2xl font-bold text-gray-900">Lead Generator</h1>
			<p class="text-sm text-gray-500 mt-1">
				Search millions of verified B2B contacts using Apollo.io integration.
			</p>
		</div>

		<div class="flex flex-1 overflow-hidden bg-gray-50">
			<div class="w-80 bg-white border-r border-gray-200 flex flex-col overflow-y-auto p-6">
				<div class="flex items-center justify-between mb-6">
					<h2 class="font-semibold text-gray-900">Filters</h2>
					<Button
						v-if="hasFilters"
						variant="ghost"
						class="text-xs text-[#4318FF] hover:text-[#3311CC]"
						@click="clearFilters"
					>
						Clear All
					</Button>
				</div>

				<div class="space-y-6">
					<Input
						label="Job Title"
						v-model="filters.job_title"
						type="text"
						placeholder="e.g. CEO, Marketing Manager"
						:disabled="leads.loading"
					/>

					<Input
						label="Location"
						v-model="filters.location"
						type="text"
						placeholder="e.g. Mumbai, New York"
						:disabled="leads.loading"
					/>

					<Input
						label="Industry / Keywords"
						v-model="filters.industry"
						type="text"
						placeholder="e.g. Software, Healthcare"
						:disabled="leads.loading"
					/>

					<div class="pt-4">
						<Button
							variant="solid"
							class="w-full justify-center py-2 !bg-[#4318FF] hover:!bg-[#3311CC] !text-white border-transparent transition-colors"
							size="lg"
							:loading="leads.loading"
							@click="searchLeads"
						>
							<template #prefix>
								<FeatherIcon name="search" class="h-4 w-4" />
							</template>
							Find Leads
						</Button>
					</div>
				</div>
			</div>

			<div class="flex-1 overflow-y-auto p-8 relative">
				<div
					v-if="!leads.data && !leads.loading"
					class="h-full flex flex-col items-center justify-center text-center opacity-60"
				>
					<div class="bg-white p-4 rounded-full shadow-sm mb-4">
						<FeatherIcon name="users" class="h-8 w-8 text-gray-400" />
					</div>
					<h3 class="text-lg font-medium text-gray-900">No leads to show</h3>
					<p class="text-gray-500 max-w-sm mt-2">
						Enter your target criteria in the filters panel to start searching.
					</p>
				</div>

				<div v-else-if="leads.loading" class="space-y-4">
					<div
						v-for="i in 3"
						:key="i"
						class="bg-white p-6 rounded-lg border border-gray-100 shadow-sm animate-pulse"
					>
						<div class="flex items-center gap-4">
							<div class="h-12 w-12 bg-gray-200 rounded-full"></div>
							<div class="space-y-2 flex-1">
								<div class="h-4 bg-gray-200 rounded w-1/4"></div>
								<div class="h-3 bg-gray-200 rounded w-1/3"></div>
							</div>
						</div>
					</div>
				</div>

				<div v-else class="flex flex-col h-full">
					<div class="flex justify-between items-center mb-4">
						<h3 class="font-bold text-gray-800">
							Search Results
							<span
								class="ml-2 px-2 py-0.5 bg-gray-200 text-gray-600 rounded-full text-xs"
							>
								Page {{ currentPage }}
							</span>
						</h3>

						<div class="flex items-center gap-2">
							<Button
								variant="outline"
								size="sm"
								:disabled="currentPage === 1 || leads.loading"
								@click="changePage(-1)"
							>
								<FeatherIcon name="chevron-left" class="h-4 w-4" />
							</Button>
							<span class="text-sm text-gray-500">Page {{ currentPage }}</span>
							<Button
								variant="outline"
								size="sm"
								:disabled="!leads.data || leads.data.length < 10 || leads.loading"
								@click="changePage(1)"
							>
								<FeatherIcon name="chevron-right" class="h-4 w-4" />
							</Button>
						</div>
					</div>

					<div class="space-y-4 pb-20">
						<div
							v-for="lead in leads.data"
							:key="lead.id"
							@click="openLeadDetails(lead)"
							class="group bg-white p-5 rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-[#4318FF]/30 transition-all duration-200 cursor-pointer"
						>
							<div class="flex justify-between items-start">
								<div class="flex gap-4">
									<div
										class="h-12 w-12 rounded-full bg-[#4318FF]/10 flex items-center justify-center text-[#4318FF] font-bold text-lg"
									>
										{{ getInitials(lead.name) }}
									</div>

									<div>
										<div class="flex items-center gap-2">
											<h4
												class="font-bold text-gray-900 text-lg group-hover:text-[#4318FF] transition-colors"
											>
												{{ lead.name }}
											</h4>
											<Badge
												v-if="lead.is_saved"
												theme="green"
												variant="subtle"
												>Saved</Badge
											>
										</div>

										<div class="text-gray-600 font-medium mt-0.5">
											{{ lead.title || 'No Title' }}
										</div>

										<div
											class="flex items-center gap-4 mt-3 text-sm text-gray-500"
										>
											<div
												class="flex items-center gap-1.5"
												v-if="lead.company"
											>
												<FeatherIcon
													name="briefcase"
													class="h-3.5 w-3.5"
												/>
												{{ lead.company }}
											</div>
											<div
												class="flex items-center gap-1.5"
												v-if="lead.location"
											>
												<FeatherIcon name="map-pin" class="h-3.5 w-3.5" />
												{{ lead.location }}
											</div>
										</div>
									</div>
								</div>

								<FeatherIcon
									name="chevron-right"
									class="text-gray-300 group-hover:text-[#4318FF] h-5 w-5 mt-4"
								/>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<Dialog v-model="showDetailsDialog" :options="{ size: 'xl' }">
			<template #body-title>
				<h3 class="text-xl font-bold">Lead Details</h3>
			</template>
			<template #body-content>
				<div v-if="selectedLead" class="mt-4">
					<div class="flex items-center gap-4 mb-6">
						<div
							class="h-16 w-16 rounded-full bg-[#4318FF]/10 flex items-center justify-center text-[#4318FF] text-2xl font-bold"
						>
							{{ getInitials(selectedLead.name) }}
						</div>
						<div>
							<h2 class="text-2xl font-bold text-gray-900">
								{{ selectedLead.name }}
							</h2>
							<p class="text-lg text-gray-600">{{ selectedLead.title }}</p>
						</div>
					</div>

					<div
						class="grid grid-cols-2 gap-6 bg-gray-50 p-6 rounded-lg border border-gray-100"
					>
						<div>
							<label class="text-xs font-bold text-gray-500 uppercase"
								>Company</label
							>
							<div class="text-gray-900 font-medium mt-1">
								{{ selectedLead.company || 'N/A' }}
							</div>
						</div>
						<div>
							<label class="text-xs font-bold text-gray-500 uppercase"
								>Location</label
							>
							<div class="text-gray-900 font-medium mt-1">
								{{ selectedLead.location || 'N/A' }}
							</div>
						</div>
					</div>

					<div
						class="mt-6 p-4 bg-[#4318FF]/5 border border-[#4318FF]/10 rounded text-sm text-[#4318FF] flex items-start gap-2"
					>
						<FeatherIcon name="info" class="h-4 w-4 mt-0.5 flex-shrink-0" />
						<span
							>Clicking "Reveal & Save" will use 1 credit to fetch verified contact
							info and add this person to your CRM.</span
						>
					</div>
				</div>
			</template>
			<template #actions>
				<Button variant="subtle" @click="showDetailsDialog = false">Close</Button>
				<Button
					v-if="!selectedLead?.is_saved"
					variant="solid"
					class="!bg-[#4318FF] hover:!bg-[#3311CC] !text-white border-transparent"
					:loading="savingId === selectedLead?.id"
					@click="saveLead(selectedLead)"
				>
					Reveal & Save
				</Button>
				<Button v-else variant="outline" theme="green" disabled>
					<template #prefix><FeatherIcon name="check" class="h-4 w-4" /></template>
					Already Saved
				</Button>
			</template>
		</Dialog>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { createResource, Input, Button, Badge, FeatherIcon, Dialog } from 'frappe-ui'

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
