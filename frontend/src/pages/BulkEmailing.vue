<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Header -->
    <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Bulk Emailing</h1>
        <p class="text-sm text-gray-500 mt-1">Manage email lists and send targeted campaigns.</p>
      </div>
      <div class="flex gap-3">
        <Button variant="outline" @click="openImportDialog" class="bg-white hover:bg-gray-50">
          <template #prefix><FeatherIcon name="download-cloud" class="h-4 w-4" /></template>
          Import from Calls
        </Button>
        <Button
          variant="solid"
          class="!bg-primary-600 hover:!bg-primary-700 !text-white !rounded-xl shadow-lg shadow-primary-500/20"
          @click="openCreateDialog"
        >
          <template #prefix><FeatherIcon name="plus" class="h-4 w-4" /></template>
          Create Email Group
        </Button>
      </div>
    </header>

    <!-- Loading State -->
    <div v-if="emailGroups.loading" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="i in 3" :key="i" class="h-48 bg-white rounded-2xl border border-gray-100 shadow-sm animate-pulse"></div>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="!emailGroups.data || emailGroups.data.length === 0"
      class="flex flex-col items-center justify-center text-center py-20 bg-white rounded-2xl border border-gray-200 shadow-sm"
    >
      <div class="w-20 h-20 bg-primary-50 rounded-full flex items-center justify-center mb-6">
        <FeatherIcon name="mail" class="h-10 w-10 text-primary-300" />
      </div>
      <h3 class="text-xl font-bold text-gray-900">No Email Lists Found</h3>
      <p class="text-gray-500 max-w-sm mt-2 mb-8 mx-auto">
        Create a new group or import contacts from your call logs to start sending emails.
      </p>
      <div class="flex gap-3 justify-center">
         <Button
           variant="outline"
           @click="openImportDialog"
         >
           Import Existing Group
         </Button>
         <Button
           variant="solid"
           class="!bg-primary-600 hover:!bg-primary-700 !text-white"
           @click="openCreateDialog"
         >
           Create New Group
         </Button>
      </div>
    </div>

    <!-- Email Groups Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="group in emailGroups.data"
        :key="group.name"
        class="group bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg hover:border-primary-200 hover:-translate-y-1 transition-all duration-300 cursor-pointer flex flex-col justify-between relative overflow-hidden"
        @click="openGroupDetails(group)"
      >
        <div class="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-bl-full -mr-6 -mt-6 transition-transform group-hover:scale-110"></div>
        
        <div class="relative z-10">
          <div class="flex justify-between items-start mb-4">
             <div class="p-2.5 bg-gray-50 rounded-xl group-hover:bg-white group-hover:shadow-sm transition-all text-gray-500 group-hover:text-primary-600">
                <FeatherIcon name="mail" class="h-5 w-5" />
             </div>
          </div>

          <h3 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 transition-colors mb-1 truncate pr-4">
            {{ group.title }}
          </h3>
          <p class="text-xs text-gray-400 font-medium">
             Created {{ formatDate(group.creation) }}
          </p>
          
           <div class="mt-6 flex items-center justify-between">
              <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-green-50 text-green-700 border border-green-100">
                 <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span> Ready
              </span>
              <div class="flex items-center gap-1 text-xs font-medium text-gray-400 group-hover:text-primary-600 transition-colors">
                 <span>Manage Campaign</span>
                 <FeatherIcon name="arrow-right" class="w-3 h-3" />
              </div>
           </div>
        </div>
      </div>
    </div>

    <!-- Import Dialog -->
    <Dialog v-model="showImportDialog">
      <template #body-title>
         <div class="flex items-center gap-2">
            <div class="p-1.5 bg-indigo-100 rounded text-indigo-600"><FeatherIcon name="download-cloud" class="w-4 h-4" /></div>
            <h3 class="text-lg font-bold">Import from Call Group</h3>
         </div>
      </template>
      <template #body-content>
        <div class="mt-4 space-y-5">
           <div class="bg-indigo-50 border border-indigo-100 rounded-lg p-3 text-sm text-indigo-700 flex gap-2">
              <FeatherIcon name="info" class="w-4 h-4 mt-0.5 shrink-0" />
              <p>We'll automatically extract valid email addresses from the members of the selected call group.</p>
           </div>
           
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1.5">Source Call Group</label>
            <select
              v-model="selectedCallGroup"
              class="block w-full rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm py-2.5"
            >
              <option disabled value="">-- Select Group --</option>
              <option v-for="cg in callGroups.data" :key="cg.name" :value="cg.name">
                {{ cg.title }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1.5">New List Name</label>
            <input
              v-model="importName"
              type="text"
              placeholder="e.g. Q3 Leads - Email Followup"
              class="block w-full rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm py-2.5"
            />
          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="subtle" @click="showImportDialog = false">Cancel</Button>
        <Button
          variant="solid"
          class="!bg-primary-600 hover:!bg-primary-700 !text-white"
          :loading="importing"
          :disabled="!selectedCallGroup || !importName"
          @click="importGroup"
        >
          Start Import
        </Button>
      </template>
    </Dialog>

    <!-- Create Group Wizard -->
    <Dialog v-model="showCreateDialog" :options="{ size: 'xl' }">
      <template #body-title>
        <h3 class="text-xl font-bold flex items-center gap-2">
           <div class="p-1.5 bg-primary-100 text-primary-600 rounded-lg"><FeatherIcon name="user-plus" class="w-5 h-5" /></div>
           Create Email Group
        </h3>
      </template>
      <template #body-content>
        <div class="mt-6 flex flex-col h-[600px] space-y-6">
          
          <!-- Title Input -->
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1.5">Group Title</label>
            <input
              v-model="newGroupTitle"
              type="text"
              placeholder="e.g. Newsletter Subscribers"
              class="block w-full rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 text-lg py-3 px-4"
            />
          </div>

          <!-- Manual Entry Box -->
          <div class="bg-gray-50 p-5 rounded-xl border border-gray-200">
            <label class="block text-sm font-bold text-gray-900 mb-2 flex items-center gap-2">
               <FeatherIcon name="edit-2" class="w-4 h-4 text-gray-500" /> Manually Add Emails
            </label>
            <div class="flex gap-2 mb-3">
              <input
                v-model="manualEmailInput"
                @keyup.enter="addManualEmail"
                type="email"
                placeholder="Enter email address..."
                class="block flex-1 rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              />
              <Button variant="outline" @click="addManualEmail" class="bg-white">Add</Button>
            </div>

            <div
              v-if="manualEmails.length > 0"
              class="flex flex-wrap gap-2 max-h-24 overflow-y-auto custom-scrollbar p-1"
            >
              <div
                v-for="(email, idx) in manualEmails"
                :key="idx"
                class="bg-white border border-gray-200 text-gray-700 px-2.5 py-1 rounded-md text-xs font-medium flex items-center gap-2 shadow-sm"
              >
                <span>{{ email }}</span>
                <button
                  @click="removeManualEmail(idx)"
                  class="text-gray-400 hover:text-red-500 transition-colors"
                >
                  <FeatherIcon name="x" class="h-3 w-3" />
                </button>
              </div>
            </div>
            <div v-else class="text-xs text-gray-400 italic">
               No manual emails added yet. Type an email above and press Enter.
            </div>
          </div>

          <!-- Contact Selection -->
          <div class="flex-1 flex flex-col min-h-0 border border-gray-200 rounded-xl bg-white overflow-hidden">
            <div class="bg-gray-50 px-4 py-3 border-b border-gray-100 flex justify-between items-center">
              <span class="text-sm font-bold text-gray-700 flex items-center gap-2">
                 <FeatherIcon name="users" class="w-4 h-4 text-gray-400" /> Select From Contacts
              </span>
              <span class="text-xs font-medium bg-white px-2 py-1 rounded border border-gray-200 text-gray-600">
                 {{ selectedContactsManual.length }} selected
              </span>
            </div>

            <div v-if="contacts.loading" class="p-8 text-center text-gray-500">
               <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600 mx-auto mb-2"></div>
              Loading contacts...
            </div>
            
            <div v-else class="flex-1 overflow-y-auto custom-scrollbar">
              <table class="min-w-full divide-y divide-gray-100">
                <thead class="bg-gray-50 sticky top-0">
                  <tr>
                    <th class="px-6 py-3 w-10">
                      <input
                        type="checkbox"
                        @change="toggleAllManual"
                        :checked="isAllManualSelected"
                        class="rounded border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
                      />
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Name</th>
                    <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Email Address</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 bg-white">
                  <tr
                    v-for="c in contactsWithEmails"
                    :key="c.name"
                    class="hover:bg-gray-50 cursor-pointer transition-colors"
                  >
                    <td class="px-6 py-3">
                      <input
                        type="checkbox"
                        :value="c.name"
                        v-model="selectedContactsManual"
                        class="rounded border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
                      />
                    </td>
                    <td class="px-6 py-3 text-sm font-medium text-gray-900">
                      {{ c.first_name }} {{ c.last_name }}
                    </td>
                    <td class="px-6 py-3 text-sm text-gray-500">
                      {{ c.email_id }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="flex justify-between items-center px-2">
             <div class="text-xs text-gray-400">
                You can add both existing contacts and manual emails.
             </div>
             <div class="text-sm font-medium text-gray-900">
               Total Recipients: <span class="text-primary-600 font-bold ml-1 text-lg">{{ totalRecipients }}</span>
             </div>
          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="subtle" @click="showCreateDialog = false">Cancel</Button>
        <Button
          variant="solid"
          class="!bg-primary-600 hover:!bg-primary-700 !text-white !rounded-lg px-6"
          :loading="creating"
          :disabled="!newGroupTitle || totalRecipients === 0"
          @click="createManualGroup"
        >
          Create Group
        </Button>
      </template>
    </Dialog>

    <!-- Details & Campaign Launcher -->
    <Dialog v-model="showDetailsDialog" :options="{ size: 'xl' }">
      <template #body-title>
         <div class="flex justify-between items-center w-full pr-8">
            <div class="flex items-center gap-3">
               <div class="p-2 bg-indigo-50 text-indigo-600 rounded-lg"><FeatherIcon name="send" class="w-5 h-5" /></div>
               <h3 class="text-xl font-bold">{{ selectedGroup?.title }}</h3>
            </div>
         </div>
      </template>
      <template #body-content>
        <div class="mt-6 space-y-6">
           <!-- Info Banner -->
          <div class="bg-indigo-50 border border-indigo-100 text-indigo-900 px-4 py-3 rounded-xl flex items-center justify-between">
             <div class="flex items-center gap-2 font-medium">
                <FeatherIcon name="users" class="h-4 w-4" />
                <span>Recipients: <strong>{{ currentGroupMembers.length }}</strong></span>
             </div>
             <button @click="deleteGroup" class="text-xs text-red-600 hover:text-red-800 font-semibold hover:underline">
                Delete Group
             </button>
          </div>

          <!-- Preview List of Emails -->
          <div class="border border-gray-200 rounded-xl overflow-hidden">
             <div class="bg-gray-50 px-4 py-2 border-b border-gray-200 text-xs font-bold text-gray-500 uppercase">Recipient Preview</div>
              <div class="max-h-32 overflow-y-auto overflow-x-auto p-2 bg-white space-y-1">
               <div
                 v-for="m in currentGroupMembers"
                 :key="m.email"
                 class="flex justify-between px-3 py-1.5 hover:bg-gray-50 rounded text-sm group"
               >
                 <span class="text-gray-900 font-medium">{{ m.contact_name || 'Guest User' }}</span>
                 <span class="text-gray-500 group-hover:text-gray-900 font-mono text-xs">{{ m.email }}</span>
               </div>
             </div>
          </div>

          <!-- Campaign Form -->
          <div class="space-y-4 pt-2">
            <div>
              <label class="block text-xs font-bold text-gray-500 uppercase mb-1.5 ml-1">Email Subject</label>
              <input
                v-model="emailSubject"
                type="text"
                placeholder="e.g. Exclusive Invitation: AI Calling Agent Demo"
                class="block w-full rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 py-3 px-4 font-medium"
              />
            </div>

            <div>
              <label class="block text-xs font-bold text-gray-500 uppercase mb-1.5 ml-1">Message Content</label>
              <textarea
                v-model="emailBody"
                rows="8"
                placeholder="Write your email content here..."
                class="block w-full rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 p-4"
              ></textarea>
            </div>
          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="subtle" @click="showDetailsDialog = false">Cancel</Button>
        <Button
          variant="solid"
          class="!bg-primary-600 hover:!bg-primary-700 !text-white !rounded-lg px-6 shadow-lg shadow-primary-500/20"
          :loading="sending"
          :disabled="!emailSubject || !emailBody"
          @click="sendCampaign"
        >
          <template #prefix><FeatherIcon name="send" class="h-4 w-4" /></template>
          Send Campaign Now
        </Button>
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
import { createResource, Button, Dialog, FeatherIcon } from 'frappe-ui'

// --- RESOURCES ---
const emailGroups = createResource({
	url: 'ai_calling_agent.api.get_email_groups',
	auto: true,
})

const callGroups = createResource({
	url: 'ai_calling_agent.api.get_call_groups',
})

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

// Toast State
const toast = ref({
	show: false,
	title: '',
	message: '',
	type: 'success', // 'success' or 'error'
})

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

function showToast(title, message, type = 'success') {
	toast.value = { show: true, title, message, type }
	setTimeout(() => {
		toast.value.show = false
	}, 4000)
}

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
			showToast('Success', data.message || 'Group imported successfully', 'success')
			emailGroups.fetch()
			showImportDialog.value = false
		} else {
			showToast('Error', data.message || 'Import Failed', 'error')
		}
	} catch (e) {
		console.error(e)
        showToast('Error', 'An error occurred during import', 'error')
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
		showToast('Invalid Email', 'Please enter a valid email address.', 'error')
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
        showToast('Success', 'Email group created successfully', 'success')
	} catch (e) {
		console.error(e)
        showToast('Error', 'Failed to create group', 'error')
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
        showToast('Error', 'Failed to load group details', 'error')
	}
}

async function sendCampaign() {
	if (!selectedGroup.value) return
	sending.value = true
	try {
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
			showToast('Campaign Sent', data.message || 'Emails sent successfully', 'success')
			showDetailsDialog.value = false
		} else {
			showToast('Error', data.message || 'Failed', 'error')
		}
	} catch (e) {
		console.error(e)
		showToast('Error', 'Failed to start campaign', 'error')
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
        showToast('Deleted', 'Group deleted successfully', 'success')
	} catch (e) {
		console.error(e)
		showToast('Error', 'Failed to delete', 'error')
	}
}

function formatDate(d) {
	if (!d) return ''
	return new Date(d).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
   })
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
