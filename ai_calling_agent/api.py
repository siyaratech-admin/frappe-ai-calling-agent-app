import frappe
import os
import asyncio
import uuid
import json
import requests
from livekit import api  # The library we installed
import time

# This is the async helper function that does the real work.
# We need this because Frappe's main hooks are synchronous, 
# but the livekit-api library is asynchronous (async/await).
async def _initiate_livekit_call(phone_number, contact_docname, agent_name, room_name, outbound_trunk_id, metadata_json, lk_url, lk_api_key, lk_api_secret):
    """
    Uses the LiveKit API to create a room, dispatch an agent,
    and start an outbound SIP call.
    """
    
    # The LiveKitAPI client reads credentials from environment variables by default.
    # We set them temporarily for this process using the values passed from the main function.
    os.environ["LIVEKIT_URL"] = lk_url
    os.environ["LIVEKIT_API_KEY"] = lk_api_key
    os.environ["LIVEKIT_API_SECRET"] = lk_api_secret

    # Use 'async with' to manage the client's lifecycle
    async with api.LiveKitAPI() as lkapi:
        # 1. Create a new, unique room for this call
        await lkapi.room.create_room(
            api.CreateRoomRequest(
                name=room_name,
                empty_timeout=10  # Close room 10s after last participant leaves
            )
        )

        # 2. Dispatch your agent to the room.
        # We pass the contact_docname as metadata so the agent knows
        # which Frappe record to write back to (Flow 2)
        await lkapi.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                agent_name=agent_name,
                room=room_name,
                metadata=metadata_json
            )
        )
        
        # 3. Start the outbound SIP call to the user's phone
        # This connects the phone call to the room where the agent is waiting.
        await lkapi.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                sip_trunk_id=outbound_trunk_id,
                room_name=room_name,
                sip_call_to=phone_number,
                participant_identity=f"pstn_{contact_docname}" # A unique ID for the call
            )
        )

# This is the main function our frontend will call
# The @frappe.whitelist() decorator makes it a public API endpoint
@frappe.whitelist()
def start_ai_call(phone_number=None, contact_docname=None, party_type="Contact"):
    """
    A whitelisted Frappe API endpoint to trigger an AI sales call.
    Compatible with both Frontend API calls and Backend Bulk Queues.
    """
    try:
        # 1. Validate Inputs
        if not phone_number:
            frappe.throw("Phone number is required to start a call.")
        if not contact_docname:
            frappe.throw("Contact Name/ID is required to link the call.")

        # ---------------------------------------------------------------
        # FIX: Smart ID Lookup
        # If the contact_docname provided is not a valid ID (e.g. it's "Manas Patil"),
        # try to find the real ID using the phone number.
        # ---------------------------------------------------------------
        if party_type == "Contact" and not frappe.db.exists("Contact", contact_docname):
            # Try finding contact by Mobile Number
            found_contact = frappe.db.get_value("Contact", {"mobile_no": phone_number}, "name")
            
            # Try finding contact by Phone Number field
            if not found_contact:
                found_contact = frappe.db.get_value("Contact", {"phone": phone_number}, "name")
            
            # If found, swap the name for the real ID
            if found_contact:
                contact_docname = found_contact
            else:
                # Optional: If contact doesn't exist, create a Lead or fail gracefully
                # For now, we will proceed, but it might fail if strict validation is on.
                frappe.log_error(f"Could not find Contact ID for {contact_docname} ({phone_number})", "AI Call Warning")

        # ---------------------------------------------------------------
        # UPDATED: Fetch Credentials from 'AI Agent Settings' DocType
        # ---------------------------------------------------------------
        settings = frappe.get_single("AI Agent Settings")
        
        lk_url = settings.livekit_url
        lk_api_key = settings.livekit_api_key
        lk_api_secret = settings.get_password("livekit_api_secret")
        outbound_trunk_id = settings.livekit_outbound_trunk_id

        # Validate that settings exist
        if not all([lk_url, lk_api_key, lk_api_secret, outbound_trunk_id]):
            frappe.throw("LiveKit credentials are missing. Please configure them in 'AI Agent Settings'.")

        agent_name = "sales-sdr-agent" # You could also make this configurable if you want
        room_name = f"frappe-call-{uuid.uuid4()}"

        # Create a new "AI Call Log" document
        new_log = frappe.new_doc("AI Call Log")
        new_log.party_type = party_type
        new_log.party = contact_docname # Now holds the correct ID
        new_log.phone_number = phone_number
        new_log.call_status = "Initiated"
        new_log.livekit_room = room_name
        
        # Save the log
        new_log.insert(ignore_permissions=True) 

        call_log_docname = new_log.name

        metadata_to_pass = json.dumps({
            "call_log_docname": call_log_docname 
        })

        asyncio.run(_initiate_livekit_call(
            phone_number=phone_number,
            contact_docname=contact_docname,
            agent_name=agent_name,
            room_name=room_name,
            outbound_trunk_id=outbound_trunk_id,
            metadata_json=metadata_to_pass,
            lk_url=lk_url,               # Passed down
            lk_api_key=lk_api_key,       # Passed down
            lk_api_secret=lk_api_secret  # Passed down
        ))

        return {
            "status": "success",
            "message": f"Placing call to {phone_number}. Log created: {call_log_docname}",
            "call_log_id": call_log_docname
        }

    except Exception as e:
        error_msg = f"Failed to initiate AI call to {phone_number}: {str(e)}"
        frappe.log_error(error_msg, "AI Call Start Error")
        return {
            "status": "error",
            "message": error_msg
        }

# --- APOLLO LEAD FINDER INTEGRATION ---

@frappe.whitelist()
def search_apollo_leads(job_title=None, location=None, industry=None, page=1, per_page=10):
    """
    Searches Apollo.io using the 'mixed_people/api_search' endpoint.
    Fetches API Key securely from 'AI Agent Settings'.
    """
    try:
        # 1. Get API Key securely
        settings = frappe.get_single("AI Agent Settings")
        api_key = settings.get_password("apollo_api_key")
        
        if not api_key:
            frappe.throw("Please set the Apollo API Key in 'AI Agent Settings' doctype.")

        # 2. UPDATE: Use the 'api_search' endpoint as requested by the error
        url = "https://api.apollo.io/v1/mixed_people/api_search"
        
        headers = {
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "X-Api-Key": api_key
        }
        
        # 3. Payload
        payload = {
            "page": int(page),
            "per_page": int(per_page),
            "person_titles": [job_title] if job_title else [],
            "person_locations": [location] if location else [],
            "q_keywords": industry if industry else None,
            "person_has_phone_number": True, 
        }

        # 4. Call Apollo
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            error_msg = response.json().get('error_message') or response.json().get('error') or response.text
            frappe.log_error(f"Apollo API Error: {error_msg}", "Apollo Integration")
            frappe.throw(f"Apollo Error ({response.status_code}): {error_msg}")

        data = response.json()
        
        # 5. Structure data
        clean_leads = []
        for person in data.get("people", []):
            clean_leads.append({
                "id": person.get("id"),
                "name": f"{person.get('first_name', '')} {person.get('last_name', '')}".strip(),
                "title": person.get("title"),
                "company": person.get("organization", {}).get("name"),
                "location": person.get("city") or person.get("country"),
                "linkedin_url": person.get("linkedin_url"),
                "email": person.get("email"),
                "phone_numbers": person.get("phone_numbers", []),
                "has_mobile": True 
            })
            
        return clean_leads

    except Exception as e:
        frappe.log_error(f"Apollo Search Failed: {str(e)}", "Apollo Integration")
        return []

@frappe.whitelist()
def save_apollo_lead(apollo_id):
    """
    Reveals and Saves an Apollo Lead to Frappe Contacts.
    Tries 'people/match' first, falls back to 'people/{id}' if needed.
    """
    try:
        # 1. Get API Key
        settings = frappe.get_single("AI Agent Settings")
        api_key = settings.get_password("apollo_api_key")
        
        if not api_key:
            frappe.throw("Apollo API Key is missing in settings.")

        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": api_key
        }

        # 2. Try 'people/match' (The standard Reveal Endpoint)
        url = "https://api.apollo.io/v1/people/match"
        payload = {
            "id": apollo_id,
            "reveal_personal_emails": True,
            "reveal_phone_number": True
        }
        
        response = requests.post(url, headers=headers, json=payload)
        person_data = {}

        # 3. Handle Response & Fallback
        if response.status_code == 200:
            data = response.json()
            person_data = data.get('person') or {}
        else:
            # Fallback: Try fetching by ID directly (GET request)
            # This often works if 'match' returns 400 due to reveal restrictions
            frappe.log_error(f"Apollo Match Failed ({response.status_code}), trying Fallback ID fetch.", "Apollo Import")
            
            fallback_url = f"https://api.apollo.io/v1/people/{apollo_id}"
            fallback_res = requests.get(fallback_url, headers=headers)
            
            if fallback_res.status_code == 200:
                data = fallback_res.json()
                person_data = data.get('person') or {}
            else:
                # If both fail, throw the error
                error_msg = response.json().get('error', 'Unknown Error')
                frappe.throw(f"Apollo Import Failed ({response.status_code}): {error_msg}")

        if not person_data:
             frappe.throw("No person data returned from Apollo.")

        # 4. Check if Contact already exists
        email = person_data.get('email')
        if email and frappe.db.exists("Contact", {"email_id": email}):
            return {"status": "exists", "message": f"Contact {email} already exists."}

        # 5. Create Frappe Contact
        contact = frappe.new_doc("Contact")
        contact.first_name = person_data.get('first_name')
        contact.last_name = person_data.get('last_name')
        contact.designation = person_data.get('title')
        contact.company_name = person_data.get('organization', {}).get('name')
        
        # Add Email
        if email:
            contact.append("email_ids", {
                "email_id": email,
                "is_primary": 1
            })
            
        # Add Phone (Mobile)
        # Check 'phone_numbers' list first, then flat fields
        phone = None
        phone_numbers = person_data.get('phone_numbers') or []
        if phone_numbers:
            # Prefer mobile, then any
            mobile = next((p['sanitized_number'] for p in phone_numbers if p['type'] == 'mobile'), None)
            phone = mobile or phone_numbers[0].get('sanitized_number')
        
        # Fallback to direct fields
        if not phone:
             phone = person_data.get('mobile_number') or person_data.get('phone_number')

        if phone:
            contact.append("phone_nos", {
                "phone": phone,
                "is_primary_mobile_no": 1
            })
            contact.mobile_no = phone # Set main field too

        # Add Location to a custom field or description if you want
        location = person_data.get('city') or person_data.get('country')
        if location:
            # You can append this to notes or a custom field
            contact.add_comment("Info", f"Location: {location}")

        contact.insert(ignore_permissions=True)
        
        return {"status": "success", "message": f"Saved {contact.first_name} {contact.last_name}"}

    except Exception as e:
        frappe.log_error(f"Apollo Import Error: {str(e)}", "Apollo Import")
        frappe.throw(f"Lead Import Failed: {str(e)}")

@frappe.whitelist()
def get_dashboard_metrics():
    """
    Returns metrics for the dashboard:
    - Total Calls Made
    - Hot Leads (Lead Status = 'Hot')
    - Average Duration
    """
    total_calls = frappe.db.count("AI Call Log")
    
    hot_leads = frappe.db.count("AI Call Log", {"lead_status": "Hot"})
    
    # Calculate average duration
    avg_duration_result = frappe.db.sql("""
        SELECT AVG(duration) as avg_duration 
        FROM `tabAI Call Log` 
        WHERE duration > 0
    """, as_dict=True)
    
    avg_duration = 0
    if avg_duration_result and avg_duration_result[0].avg_duration:
        avg_duration = float(avg_duration_result[0].avg_duration)

    return {
        "total_calls": total_calls,
        "hot_leads": hot_leads,
        "avg_duration": avg_duration
    }

@frappe.whitelist(allow_guest=True)
def get_logged_user():
    if frappe.session.user == "Guest":
        return None
    
    return frappe.db.get_value("User", frappe.session.user, 
        ["name", "first_name", "last_name", "email", "user_image"], 
        as_dict=1
    )

# -------------------------
# GROUP MANAGEMENT APIS
# -------------------------

@frappe.whitelist()
def create_call_group(title, members):
    """
    Creates a new Call Group with members.
    members should be a list of dicts: [{'name': 'John', 'phone': '+123...'}]
    """
    try:
        # Create the parent DocType
        doc = frappe.get_doc({
            "doctype": "Call Group",
            "title": title,
            "members": []
        })

        # Parse the members list (passed as string/JSON from frontend)
        import json
        if isinstance(members, str):
            members = json.loads(members)

        # Add rows to child table
        for m in members:
            doc.append("members", {
                "contact_name": m.get("name"),
                "phone_number": m.get("phone")
            })
        
        doc.insert()
        return {"status": "success", "message": f"Group '{title}' created with {len(members)} members."}
    except Exception as e:
        frappe.log_error(f"Error creating group: {str(e)}")
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def get_call_groups():
    """Fetches all groups for the sidebar list"""
    return frappe.get_all("Call Group", fields=["name", "title", "creation"])

# -------------------------
# BULK CALLING LOGIC
# -------------------------

@frappe.whitelist()
def trigger_bulk_call(group_name):
    """
    The Main Trigger.
    1. Fetches the group.
    2. Enqueues a background job to process the list.
    """
    try:
        group = frappe.get_doc("Call Group", group_name)
        
        if not group.members:
            return {"status": "error", "message": "This group has no members."}

        # We pass the list of numbers to a background worker
        # queue='long' is important so it doesn't time out
        frappe.enqueue(
            method=process_bulk_queue,
            queue='long',
            timeout=3000, 
            member_list=[m.as_dict() for m in group.members]
        )

        return {
            "status": "success", 
            "message": f"Bulk call initiated for {len(group.members)} contacts. Calls will happen in the background."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def process_bulk_queue(member_list):
    """
    This runs in the BACKGROUND.
    It loops through numbers and triggers the single call function.
    """
    from ai_calling_agent.api import start_ai_call # Import your existing function
    
    success_count = 0
    
    for member in member_list:
        phone = member.get('phone_number')
        name = member.get('contact_name')
        
        if not phone:
            continue
            
        try:
            # We assume start_ai_call exists in your api.py
            # We call it internally (not via HTTP request)
            
            # NOTE: We artificially slow it down slightly to prevent 
            # hitting API rate limits of your AI provider (Bland/Vapi/etc)
            time.sleep(2) 
            
            # Trigger the actual call
            # We must pass arguments directly to start_ai_call now
            frappe.call('ai_calling_agent.api.start_ai_call', 
                        phone_number=phone, 
                        contact_docname=name) 
            
            success_count += 1
            
        except Exception as e:
            frappe.log_error(f"Bulk Call Failed for {phone}: {str(e)}")
            
    # Optional: Send a System Notification to the user when done
    frappe.publish_realtime(
        event='msgprint',
        message=f'Bulk Calling Completed. {success_count} calls initiated.',
        user=frappe.session.user
    )

# -------------------------
# EMAIL GROUP MANAGEMENT
# -------------------------

@frappe.whitelist()
def get_email_groups():
    """Fetches the list of email groups for the frontend."""
    # UPDATED: Fetching 'AI Email Group' instead of 'Email Group'
    return frappe.get_all("AI Email Group", fields=["name", "title", "creation"])

@frappe.whitelist()
def create_email_group(title, members):
    """
    Creates a new Email Group manually from a list of contacts.
    """
    try:
        # UPDATED: Creating 'AI Email Group'
        doc = frappe.new_doc("AI Email Group")
        doc.title = title
        
        import json
        if isinstance(members, str):
            members = json.loads(members)
            
        for m in members:
            if m.get("email"):
                # UPDATED: Appending to 'members' child table
                doc.append("members", {
                    "contact_name": m.get("name"),
                    "email": m.get("email"),
                    "status": "Pending"
                })
            
        doc.insert()
        return {"status": "success", "message": f"Created group '{title}'"}
    except Exception as e:
        frappe.log_error(f"Create Group Error: {str(e)}")
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def import_call_group_to_email(call_group_name, new_title):
    """
    Creates a new AI Email Group by importing members from an existing Call Group.
    """
    try:
        if not frappe.db.exists("Call Group", call_group_name):
            frappe.throw("Call Group not found")
            
        call_group = frappe.get_doc("Call Group", call_group_name)
        
        # UPDATED: Creating 'AI Email Group'
        new_doc = frappe.new_doc("AI Email Group")
        new_doc.title = new_title
        
        added_count = 0
        
        for member in call_group.members:
            email = None
            
            # Lookup logic (same as before)
            if member.contact_name:
                email = frappe.db.get_value("Contact", member.contact_name, "email_id")
            
            if not email and member.phone_number:
                 email = frappe.db.get_value("Contact", {"mobile_no": member.phone_number}, "email_id")
                 if not email:
                     email = frappe.db.get_value("Contact", {"phone": member.phone_number}, "email_id")
            
            if email:
                new_doc.append("members", {
                    "contact_name": member.contact_name or "Unknown",
                    "email": email,
                    "status": "Pending"
                })
                added_count += 1
                
        if added_count == 0:
            frappe.throw("No valid email addresses found in this Call Group.")
            
        new_doc.insert()
        return {"status": "success", "message": f"Imported {added_count} contacts into '{new_title}'."}
        
    except Exception as e:
        frappe.log_error(f"Import Error: {str(e)}")
        return {"status": "error", "message": str(e)}

# -------------------------
# BULK EMAIL TRIGGER
# -------------------------

@frappe.whitelist()
def trigger_email_campaign(group_name, subject, message):
    try:
        # UPDATED: Fetching 'AI Email Group'
        group = frappe.get_doc("AI Email Group", group_name)
        
        if not group.members:
            return {"status": "error", "message": "Group is empty."}

        frappe.enqueue(
            method=process_email_queue,
            queue='long',
            timeout=3000,
            member_list=[m.as_dict() for m in group.members],
            subject=subject,
            message=message
        )
        return {"status": "success", "message": "Campaign started in background."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def process_email_queue(member_list, subject, message):
    import time
    success_count = 0
    
    for member in member_list:
        email = member.get('email')
        if not email: continue
        
        try:
            frappe.sendmail(
                recipients=[email],
                subject=subject,
                message=message,
                reference_doctype="Contact", 
                reference_name=member.get('contact_name')
            )
            time.sleep(1) 
            success_count += 1
        except Exception as e:
            frappe.log_error(f"Email Failed to {email}: {str(e)}", "Bulk Email Error")
            
    frappe.publish_realtime(
        event='msgprint',
        message=f'Email Campaign Finished. Sent {success_count} emails.',
        user=frappe.session.user
    )

@frappe.whitelist()
def get_agent_settings():
    """
    Fetches settings for the frontend. 
    Intentionally returns empty strings for passwords to ensure security.
    """
    try:
        doc = frappe.get_single("AI Agent Settings")
        return {
            "livekit_url": doc.livekit_url,
            "livekit_api_key": doc.livekit_api_key,
            "livekit_outbound_trunk_id": doc.livekit_outbound_trunk_id,
            # We do NOT send the actual secret hashes to the frontend
            "livekit_api_secret": "", 
            "apollo_api_key": ""
        }
    except Exception as e:
        frappe.log_error(f"Error fetching settings: {str(e)}")
        return {}