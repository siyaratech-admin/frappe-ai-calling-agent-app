<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Header -->
    <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Bulk Calling</h1>
        <p class="text-sm text-gray-500 mt-1">Organize contacts into groups and launch AI calling campaigns.</p>
      </div>
      <div>
        <Button
          v-if="groups.data && groups.data.length > 0"
          variant="solid"
          class="!bg-primary-600 hover:!bg-primary-700 !text-white !rounded-xl shadow-lg shadow-primary-500/20"
          @click="openCreateDialog"
        >
          <template #prefix><FeatherIcon name="plus" class="h-4 w-4" /></template>
          Create New Group
        </Button>
      </div>
    </header>

    <!-- Loading State -->
    <div v-if="groups.loading" class="grid grid-cols-1 md:grid-cols-3 gap-6">
       <div v-for="i in 3" :key="i" class="h-48 bg-white rounded-2xl border border-gray-100 shadow-sm animate-pulse"></div>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="!groups.data || groups.data.length === 0"
      class="flex flex-col items-center justify-center text-center py-20 bg-white rounded-2xl border border-gray-200 shadow-sm"
    >
      <div class="w-20 h-20 bg-primary-50 rounded-full flex items-center justify-center mb-6">
        <FeatherIcon name="layers" class="h-10 w-10 text-primary-300" />
      </div>
      <h3 class="text-xl font-bold text-gray-900">No Groups Created Yet</h3>
      <p class="text-gray-500 max-w-sm mt-2 mb-8 mx-auto">
        Groups allow you to target specific segments of your contacts for bulk calling.
      </p>
      <Button
        variant="solid"
        size="lg"
        class="!bg-primary-600 hover:!bg-primary-700 !text-white !rounded-xl shadow-lg shadow-primary-500/30"
        @click="openCreateDialog"
      >
        <template #prefix><FeatherIcon name="plus" class="h-4 w-4" /></template>
        Create Your First Group
      </Button>
    </div>

    <!-- Groups Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="group in groups.data"
        :key="group.name"
        class="group bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg hover:border-primary-200 hover:-translate-y-1 transition-all duration-300 cursor-pointer flex flex-col justify-between relative overflow-hidden"
        @click="openGroupDetails(group)"
      >
         <div class="absolute top-0 right-0 w-24 h-24 bg-primary-50 rounded-bl-full -mr-6 -mt-6 transition-transform group-hover:scale-110"></div>
         
        <div class="relative z-10">
          <div class="flex justify-between items-start mb-4">
             <div class="p-2.5 bg-gray-50 rounded-xl group-hover:bg-white group-hover:shadow-sm transition-all text-gray-500 group-hover:text-primary-600">
                <FeatherIcon name="folder" class="h-5 w-5" />
             </div>
          </div>
          
          <h3 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 transition-colors mb-1 truncate pr-4">
            {{ group.title }}
          </h3>
          <p class="text-xs text-gray-400 font-medium">
            Created {{ formatDate(group.creation) }}
          </p>

          <div class="mt-6 flex items-center gap-4">
             <div class="flex -space-x-3 overflow-hidden">
                <div class="w-8 h-8 rounded-full border-2 border-white bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-400">#1</div>
                <div class="w-8 h-8 rounded-full border-2 border-white bg-gray-200 flex items-center justify-center text-xs font-bold text-gray-500">#2</div>
                 <div class="w-8 h-8 rounded-full border-2 border-white bg-primary-100 flex items-center justify-center text-xs font-bold text-primary-600">
                    <FeatherIcon name="users" class="w-3 h-3" />
                 </div>
             </div>
             <span class="text-xs font-semibold text-gray-500 group-hover:text-primary-600 transition-colors">View Members</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Group Wizard -->
    <Dialog v-model="showCreateDialog" :options="{ size: 'xl' }">
      <template #body-title>
        <div class="flex items-center gap-3">
           <div class="flex items-center justify-center w-8 h-8 rounded-full bg-primary-100 text-primary-600 font-bold text-sm border-2 border-white shadow-sm">
              {{ createStep }}
           </div>
           <h3 class="text-xl font-bold text-gray-900">
              {{ createStep === 1 ? 'Name Your Group' : 'Add Members' }}
           </h3>
        </div>
      </template>
      <template #body-content>
        <div class="mt-6 min-h-[400px]">
           <!-- Step 1: Naming -->
          <div v-if="createStep === 1" class="flex flex-col items-center justify-center h-full py-12">
             <div class="w-16 h-16 bg-gradient-to-br from-primary-100 to-indigo-50 rounded-2xl flex items-center justify-center mb-6 shadow-inner">
                <FeatherIcon name="edit-3" class="w-8 h-8 text-primary-600" />
             </div>
            <div class="w-full max-w-md space-y-4">
              <label class="block text-sm font-bold text-gray-700 text-center uppercase tracking-wider">Group Title</label>
              <input
                v-model="newGroupTitle"
                type="text"
                placeholder="e.g. Q4 Sales Outreach"
                class="block w-full rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 text-lg py-3 px-4 text-center transition-shadow"
                autofocus
                @keydown.enter="createStep = 2"
              />
              <p class="text-xs text-gray-400 text-center">Give your group a descriptive name to easily identify it later.</p>
            </div>
          </div>

          <!-- Step 2: Selection -->
          <div v-if="createStep === 2" class="flex flex-col h-[500px]">
            <div class="mb-4 relative">
               <FeatherIcon name="search" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                v-model="contactSearch"
                type="text"
                placeholder="Search by name or phone..."
                class="block w-full pl-9 pr-4 py-2.5 rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm transition-shadow"
              />
            </div>

            <div class="flex-1 overflow-hidden border border-gray-200 rounded-xl bg-white flex flex-col">
              <div v-if="contacts.loading" class="p-8 text-center text-gray-500">
                <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600 mx-auto mb-2"></div>
                Loading contacts...
              </div>
              <div
                v-else-if="filteredContacts.length === 0"
                class="flex-1 flex flex-col items-center justify-center text-gray-400 p-8"
              >
                <FeatherIcon name="users" class="w-8 h-8 mb-2 opacity-50" />
                No contacts found matching your search.
              </div>

              <div v-else class="flex-1 overflow-y-auto custom-scrollbar">
                <table class="min-w-full divide-y divide-gray-100">
                  <thead class="bg-gray-50 sticky top-0 z-10">
                    <tr>
                      <th scope="col" class="px-6 py-3 text-left w-10 bg-gray-50">
                        <input
                          type="checkbox"
                          :checked="isAllSelected"
                          @change="toggleAllSelection"
                          class="rounded border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
                        />
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50">Name</th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50">Phone</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-100">
                    <tr
                      v-for="contact in filteredContacts"
                      :key="contact.name"
                      class="hover:bg-gray-50 cursor-pointer transition-colors"
                      @click="toggleSelection(contact)"
                    >
                      <td class="px-6 py-4 whitespace-nowrap">
                        <input
                          type="checkbox"
                          :checked="selectedContacts.has(contact.name)"
                          class="rounded border-gray-300 text-primary-600 focus:ring-primary-500 pointer-events-none"
                        />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                         <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-500">
                               {{ getInitials(contact.first_name) }}
                            </div>
                            <div class="font-medium text-gray-900">{{ contact.first_name }} {{ contact.last_name }}</div>
                         </div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">
                        {{ contact.mobile_no || contact.phone }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="mt-3 flex justify-between items-center text-sm">
               <span class="text-gray-500">Select contacts to include in this group.</span>
               <span class="font-bold text-primary-600 bg-primary-50 px-3 py-1 rounded-full border border-primary-100">
                  {{ selectedContacts.size }} Selected
               </span>
            </div>
          </div>
        </div>
      </template>
      <template #actions>
        <div class="flex w-full justify-between items-center">
          <div>
            <Button v-if="createStep === 2" variant="outline" @click="createStep = 1">Back</Button>
          </div>
          <div class="flex items-center gap-3">
            <Button
              v-if="createStep === 1"
              variant="solid"
              class="!bg-primary-600 hover:!bg-primary-700 !text-white !rounded-lg px-6"
              :disabled="!newGroupTitle"
              @click="createStep = 2"
            >
               <div class="flex items-center gap-2">
                  Next Step <FeatherIcon name="arrow-right" class="w-4 h-4" />
               </div>
            </Button>
            <Button
              v-if="createStep === 2"
              variant="solid"
              class="!bg-primary-600 hover:!bg-primary-700 !text-white !rounded-lg px-6"
              :disabled="selectedContacts.size === 0"
              :loading="creating"
              @click="createGroup"
            >
               <div class="flex items-center gap-2">
                  Create Group <FeatherIcon name="check" class="w-4 h-4" />
               </div>
            </Button>
            <Button variant="subtle" @click="closeCreateDialog" class="hover:bg-gray-200">Cancel</Button>
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Group Details & Action Modal -->
    <Dialog v-model="showDetailsDialog" :options="{ size: '2xl' }">
      <template #body-title>
         <div class="flex items-center gap-3">
            <div class="p-2 bg-primary-50 text-primary-600 rounded-lg">
               <FeatherIcon name="folder" class="w-5 h-5" />
            </div>
            <div>
               <h3 class="text-xl font-bold text-gray-900">{{ selectedGroup?.title }}</h3>
               <p class="text-xs text-gray-500 font-normal mt-0.5">{{ groupMembers.length }} Members</p>
            </div>
         </div>
      </template>
      <template #body-content>
        <div class="mt-6 flex flex-col h-[500px]">
           
           <div class="bg-blue-50 border border-blue-100 rounded-xl p-4 mb-4 flex items-start gap-3">
              <FeatherIcon name="info" class="w-5 h-5 text-blue-600 mt-0.5 shrink-0" />
              <div>
                 <h4 class="font-bold text-blue-900 text-sm">Target Audience</h4>
                 <p class="text-sm text-blue-700 mt-1">Review the list below. Clicking "Start Bulk Calling" will queue calls for all valid numbers in this group.</p>
              </div>
           </div>

          <div class="flex-1 overflow-hidden border border-gray-200 rounded-xl bg-white flex flex-col">
            <div v-if="detailsLoading" class="p-8 text-center text-gray-500 flex flex-col items-center justify-center h-full">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mb-2"></div>
              Loading members...
            </div>
             
             <div v-else class="flex-1 overflow-y-auto overflow-x-auto custom-scrollbar">
                <table class="min-w-full divide-y divide-gray-100">
                  <thead class="bg-gray-50 sticky top-0">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Contact Name</th>
                      <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Phone</th>
                      <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-100">
                    <tr v-for="member in groupMembers" :key="member.name" class="hover:bg-gray-50">
                      <td class="px-6 py-4 text-sm font-medium text-gray-900">
                         <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-500 border border-white shadow-sm">
                               {{ getInitials(member.contact_name) }}
                            </div>
                            {{ member.contact_name }}
                         </div>
                      </td>
                      <td class="px-6 py-4 text-sm text-gray-500 font-mono">{{ member.phone_number }}</td>
                      <td class="px-6 py-4 text-sm">
                        <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-gray-100 text-gray-600">Pending</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
             </div>
          </div>
        </div>
      </template>
      <template #actions>
        <div class="flex w-full justify-between items-center bg-white pt-2">
          <Button
            variant="ghost"
            theme="red"
            class="text-red-600 hover:bg-red-50 hover:border-red-100 border border-transparent"
            @click="deleteGroup"
          >
           <template #prefix><FeatherIcon name="trash-2" class="h-4 w-4" /></template>
            Delete Group
          </Button>

          <div class="flex gap-3">
            <Button variant="subtle" @click="showDetailsDialog = false">Close</Button>
            <Button
              variant="solid"
              class="!bg-primary-600 hover:!bg-primary-700 !text-white !rounded-lg shadow-lg shadow-primary-500/30 pl-4 pr-5"
              :loading="triggering"
              @click="startBulkCall"
            >
              <template #prefix><FeatherIcon name="phone-call" class="h-4 w-4" /></template>
              Start Bulk Calling
            </Button>
          </div>
        </div>
      </template>
    </Dialog>
    <!-- Notification Toast -->
    <transition name="slide-fade">
      <div
        v-if="toast.show"
        class="fixed bottom-6 right-6 z-50 flex items-center gap-4 px-5 py-4 bg-white rounded-xl shadow-2xl border border-gray-100 max-w-md transform transition-all"
        :class="toast.type === 'success' ? 'border-l-4 border-l-green-500' : 'border-l-4 border-l-red-500'"
      >
        <div
          class="flex items-center justify-center w-10 h-10 rounded-full shrink-0"
          :class="toast.type === 'success' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'"
        >
          <FeatherIcon :name="toast.type === 'success' ? 'check' : 'alert-circle'" class="h-5 w-5" />
        </div>
        <div>
          <h4 class="text-sm font-bold text-gray-900">{{ toast.title }}</h4>
          <p class="text-xs text-gray-500 mt-0.5 leading-relaxed">{{ toast.message }}</p>
        </div>
        <button @click="toast.show = false" class="text-gray-400 hover:text-gray-600 ml-2">
           <FeatherIcon name="x" class="w-4 h-4" />
        </button>
      </div>
    </transition>
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

// Toast State
const toast = ref({
	show: false,
	title: '',
	message: '',
	type: 'success', // 'success' or 'error'
})

// --- RESOURCES ---
const groups = createResource({
	url: 'ai_calling_agent.api.get_call_groups',
	auto: true,
})

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

// --- ACTIONS ---

function showToast(title, message, type = 'success') {
	toast.value = { show: true, title, message, type }
	setTimeout(() => {
		toast.value.show = false
	}, 4000)
}

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

function getInitials(name) {
   if(!name) return '?'
   return name.substring(0, 1).toUpperCase()
}

function formatDate(dateStr) {
	if (!dateStr) return ''
	return new Date(dateStr).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
   })
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
         showToast('Success', 'Call Group created successfully!', 'success')
		} else {
			showToast('Error', data.message || 'Error creating group', 'error')
		}
	} catch (e) {
		console.error(e)
		showToast('Error', 'Failed to create group', 'error')
	} finally {
		creating.value = false
	}
}

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
        showToast('Error', 'Failed to load group details', 'error')
	} finally {
		detailsLoading.value = false
	}
}

async function startBulkCall() {
	if (!selectedGroup.value) return
	if (!confirm(`Are you sure you want to call all ${groupMembers.value.length} members in this group?`)) return

	triggering.value = true
	try {
		const res = await fetch('/api/method/ai_calling_agent.api.trigger_bulk_call', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ group_name: selectedGroup.value.name }),
		})

		const data = await res.json()
		if (res.ok) {
			showToast('Campaign Started', 'Bulk call campaign started successfully! Logs will appear in the dashboard.', 'success')
			showDetailsDialog.value = false
		} else {
			showToast('Error', data.message || 'Failed to start bulk call', 'error')
		}
	} catch (e) {
		console.error(e)
		showToast('Error', 'An error occurred', 'error')
	} finally {
		triggering.value = false
	}
}

async function deleteGroup() {
	if (!confirm('Are you sure you want to delete this group? This action cannot be undone.')) return
	try {
		await fetch(`/api/resource/Call Group/${selectedGroup.value.name}`, { method: 'DELETE' })
		groups.fetch()
		showDetailsDialog.value = false
        showToast('Deleted', 'Group deleted successfully', 'success')
	} catch (e) {
		console.error(e)
		showToast('Error', 'Failed to delete group', 'error')
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
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(20px);
  opacity: 0;
}
</style>
