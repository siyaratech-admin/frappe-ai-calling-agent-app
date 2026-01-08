<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Header -->
    <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Contacts</h1>
        <div class="flex items-center gap-2 text-gray-500 mt-1">
           <span class="text-sm">Synced with Frappe CRM</span>
           <span class="w-1 h-1 bg-gray-300 rounded-full"></span>
           <span class="text-sm">{{ contacts.data?.length || 0 }} entries</span>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <div class="relative">
           <FeatherIcon name="search" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
           <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search contacts..." 
              class="pl-9 pr-4 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 w-full sm:w-64 transition-shadow"
           >
        </div>
        <Button
          variant="solid"
          class="!bg-primary-600 hover:!bg-primary-700 !text-white !border-transparent !rounded-xl shadow-md shadow-primary-500/20"
          @click="openCRMAddContact"
        >
          <template #prefix><FeatherIcon name="plus" class="h-4 w-4" /></template>
          Add Contact
        </Button>
      </div>
    </header>

    <!-- Contacts Table -->
    <div class="bg-white rounded-2xl border border-gray-200 shadow-soft overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-gray-50/50 border-b border-gray-200">
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Name & Designation</th>
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Status</th>
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Contact Info</th>
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Company</th>
              <th class="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-if="contacts.loading">
              <td colspan="5" class="px-6 py-12 text-center text-gray-500">
                 <div class="flex flex-col items-center animate-pulse">
                    <div class="h-4 w-32 bg-gray-200 rounded mb-2"></div>
                    <div class="h-3 w-48 bg-gray-100 rounded"></div>
                 </div>
              </td>
            </tr>
            <tr v-else-if="filteredContacts.length === 0">
              <td colspan="5" class="px-6 py-16 text-center text-gray-500">
                 <FeatherIcon name="users" class="w-12 h-12 mx-auto text-gray-300 mb-3" />
                 <p class="font-medium text-gray-900">No contacts found</p>
                 <p class="text-sm mt-1">Get started by adding a new contact from CRM.</p>
              </td>
            </tr>
            <tr
              v-else
              v-for="contact in filteredContacts"
              :key="contact.name"
              @click="openDetails(contact)"
              class="group hover:bg-gray-50/80 transition-colors cursor-pointer"
            >
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-gradient-to-br from-primary-100 to-indigo-100 text-primary-700 flex items-center justify-center font-bold text-sm shadow-sm border border-white">
                     {{ getInitials(contact) }}
                  </div>
                  <div>
                    <div class="font-bold text-gray-900 group-hover:text-primary-600 transition-colors">
                      {{ contact.first_name }} {{ contact.last_name }}
                    </div>
                    <div class="text-xs text-gray-500 flex items-center gap-1">
                      <FeatherIcon name="briefcase" class="w-3 h-3" />
                      {{ contact.designation || 'No Designation' }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold border" :class="getStatusBadgeClasses(contact.status)">
                  {{ contact.status }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex flex-col gap-1">
                   <div class="flex items-center text-sm text-gray-900" v-if="contact.email_id">
                      <FeatherIcon name="mail" class="w-3 h-3 text-gray-400 mr-2" />
                      {{ contact.email_id }}
                   </div>
                   <div class="flex items-center text-sm text-gray-500" v-if="getPhoneNumber(contact)">
                      <FeatherIcon name="phone" class="w-3 h-3 text-gray-400 mr-2" />
                      {{ getPhoneNumber(contact) }}
                   </div>
                   <span v-if="!contact.email_id && !getPhoneNumber(contact)" class="text-xs text-gray-400 italic">No info</span>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600 font-medium">
                {{ contact.company_name || '-' }}
              </td>
               <td class="px-6 py-4 text-right">
                  <FeatherIcon name="chevron-right" class="w-4 h-4 text-gray-300 inline-block group-hover:text-primary-500 transition-colors" />
               </td>
            </tr>
          </tbody>
        </table>
      </div>
      
       <!-- Pagination Placeholder -->
       <div class="px-6 py-4 border-t border-gray-200 flex items-center justify-between bg-gray-50/50">
          <span class="text-xs text-gray-500">Showing top 50 contacts</span>
          <div class="flex gap-2">
             <button class="p-1 rounded hover:bg-white hover:shadow-sm text-gray-400 hover:text-gray-600 disabled:opacity-50" disabled><FeatherIcon name="chevron-left" class="w-4 h-4" /></button>
             <button class="p-1 rounded hover:bg-white hover:shadow-sm text-gray-400 hover:text-gray-600 disabled:opacity-50" disabled><FeatherIcon name="chevron-right" class="w-4 h-4" /></button>
          </div>
       </div>
    </div>

    <!-- Contact Details Modal -->
    <Dialog v-model="showDetailsDialog" :options="{ size: 'xl' }">
      <template #body-title>
         <div class="flex items-center gap-2 text-lg font-bold text-gray-900">
            <FeatherIcon name="user" class="w-5 h-5 text-primary-500" />
            Contact Profile
         </div>
      </template>
      <template #body-content>
        <div v-if="selectedContact" class="mt-6 space-y-8">
          <!-- Profile Header -->
          <div class="flex flex-col sm:flex-row items-center sm:items-start gap-6 bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden">
             <!-- Background decoration -->
             <div class="absolute top-0 right-0 w-32 h-32 bg-primary-50 rounded-bl-full opacity-50 pointer-events-none"></div>
             
            <div class="w-24 h-24 rounded-full bg-gradient-to-br from-primary-500 to-indigo-600 flex items-center justify-center text-3xl font-bold text-white shadow-lg shadow-primary-500/30 flex-shrink-0 border-4 border-white">
               {{ getInitials(selectedContact) }}
            </div>
            
            <div class="text-center sm:text-left flex-1 relative z-10">
              <h2 class="text-2xl font-bold text-gray-900">
                {{ selectedContact.salutation ? selectedContact.salutation + ' ' : '' }}
                {{ selectedContact.first_name }} {{ selectedContact.last_name }}
              </h2>
              <div class="text-gray-500 font-medium text-lg">{{ selectedContact.designation || 'No Designation' }}</div>
               <div class="flex flex-wrap items-center justify-center sm:justify-start gap-3 mt-3">
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold border" :class="getStatusBadgeClasses(selectedContact.status)">
                     {{ selectedContact.status }}
                  </span>
                  <span v-if="selectedContact.company_name" class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600 border border-gray-200">
                     <FeatherIcon name="briefcase" class="w-3 h-3 mr-1.5" />
                     {{ selectedContact.company_name }}
                  </span>
               </div>
            </div>
          </div>

          <!-- Quick Actions & Info -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-4">
               <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-3">Contact Information</h3>
               
               <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-3">
                  <div class="flex items-center gap-3">
                     <div class="p-2 bg-white rounded-lg shadow-sm text-gray-400">
                        <FeatherIcon name="mail" class="w-4 h-4" />
                     </div>
                     <div class="flex-1 overflow-hidden">
                        <div class="text-xs text-gray-500 font-medium uppercase">Email Address</div>
                        <div class="text-sm font-semibold text-gray-900 truncate" :title="selectedContact.email_id">{{ selectedContact.email_id || 'Not provided' }}</div>
                     </div>
                  </div>
                  
                  <div class="flex items-center gap-3">
                     <div class="p-2 bg-white rounded-lg shadow-sm text-gray-400">
                        <FeatherIcon name="phone" class="w-4 h-4" />
                     </div>
                     <div class="flex-1 overflow-hidden">
                        <div class="text-xs text-gray-500 font-medium uppercase">Phone Number</div>
                        <div class="text-sm font-semibold text-gray-900" :title="getPhoneNumber(selectedContact)">{{ getPhoneNumber(selectedContact) || 'Not provided' }}</div>
                     </div>
                  </div>
               </div>
               
               <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mt-6 mb-3">Other Details</h3>
               <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-3">
                   <div class="flex items-center gap-3">
                     <div class="p-2 bg-white rounded-lg shadow-sm text-gray-400">
                        <FeatherIcon name="user" class="w-4 h-4" />
                     </div>
                     <div class="flex-1">
                        <div class="text-xs text-gray-500 font-medium uppercase">Gender</div>
                        <div class="text-sm font-semibold text-gray-900">{{ selectedContact.gender || 'Not specified' }}</div>
                     </div>
                  </div>
               </div>
            </div>

            <div class="flex flex-col h-full">
               <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-3">Actions</h3>
               <div class="flex-1 bg-gradient-to-b from-primary-50 to-white p-6 rounded-2xl border border-primary-100 flex flex-col items-center justify-center text-center space-y-6">
                  
                  <div v-if="getPhoneNumber(selectedContact)">
                     <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-lg shadow-primary-500/20 mb-4 mx-auto animate-pulse">
                        <FeatherIcon name="phone-call" class="w-8 h-8 text-primary-600" />
                     </div>
                     <h4 class="text-lg font-bold text-gray-900">Ready to connect?</h4>
                     <p class="text-sm text-gray-500 mt-1 mb-6 max-w-xs mx-auto">
                        Initiate an AI-powered call with <span class="font-semibold text-gray-900">{{ selectedContact.first_name }}</span> immediately.
                     </p>
                     
                     <Button
                        variant="solid"
                        size="xl"
                        class="w-full !rounded-xl !bg-primary-600 hover:!bg-primary-700 !text-white shadow-xl shadow-primary-500/30 transform hover:-translate-y-1 transition-all"
                        :loading="callLoading"
                        @click="initiateCall"
                     >
                        Start AI Call Now
                     </Button>
                  </div>
                  
                  <div v-else class="text-center py-8">
                      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4 mx-auto">
                        <FeatherIcon name="phone-off" class="w-8 h-8 text-gray-400" />
                     </div>
                     <h4 class="text-lg font-bold text-gray-900">No Phone Number</h4>
                     <p class="text-sm text-gray-500 mt-1 max-w-xs mx-auto">
                        You cannot start a call without a valid phone number. Please update the contact in CRM.
                     </p>
                  </div>
                  
               </div>
            </div>
          </div>
        </div>
      </template>
      <template #actions>
        <div class="flex justify-between w-full">
           <Button variant="outline" class="!border-gray-200 hover:!bg-gray-50" @click="openInDesk">
              <template #prefix><FeatherIcon name="external-link" class="w-4 h-4" /></template>
              View in CRM
           </Button>
           <Button variant="subtle" @click="showDetailsDialog = false">Close</Button>
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
import { createResource, Button, Dialog, Badge, FeatherIcon } from 'frappe-ui'

const showDetailsDialog = ref(false)
const selectedContact = ref(null)
const callLoading = ref(false)
const searchQuery = ref('')

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
		limit: 1000,
	},
	auto: true,
})

const filteredContacts = computed(() => {
	if (!contacts.data) return []
	const query = searchQuery.value.toLowerCase()
	if (!query) return contacts.data
	
	return contacts.data.filter((c) => {
		const name = `${c.first_name || ''} ${c.last_name || ''}`.toLowerCase()
		const email = (c.email_id || '').toLowerCase()
		const phone = (c.mobile_no || c.phone || '').toLowerCase()
		const company = (c.company_name || '').toLowerCase()
		
		return name.includes(query) || email.includes(query) || phone.includes(query) || company.includes(query)
	})
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

function getStatusBadgeClasses(status) {
	if (status === 'Open') return 'bg-green-50 text-green-700 border-green-200'
	if (status === 'Replied') return 'bg-blue-50 text-blue-700 border-blue-200'
	if (status === 'Passive') return 'bg-orange-50 text-orange-700 border-orange-200'
	return 'bg-gray-50 text-gray-600 border-gray-200'
}

function getInitials(contact) {
	const f = contact.first_name ? contact.first_name[0] : ''
	const l = contact.last_name ? contact.last_name[0] : ''
	return (f + l).toUpperCase()
}
</script>

<style scoped>
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
