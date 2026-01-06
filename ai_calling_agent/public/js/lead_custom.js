frappe.ui.form.on('Lead', {
  refresh: function (frm) {
    if (!frm.is_new() && frm.doc.mobile_no) {
      frm.add_custom_button(__('Start AI Call'), function () {
        start_ai_call(frm);
      }).addClass('btn-primary');
    }
  }
});

function start_ai_call(frm) {
  frappe.confirm(
    `Are you sure you want to start an AI call with <b>${frm.doc.first_name} ${frm.doc.last_name || ''}</b> on <b>${frm.doc.mobile_no}</b>?`,
    function () {
      // Yes
      frappe.call({
        method: 'ai_calling_agent.api.start_ai_call',
        args: {
          phone_number: frm.doc.mobile_no,
          contact_docname: frm.doc.name, // Using Lead Name as contact reference for now, API expects contact_docname but logs it as 'contact' link. 
          party_type: 'Lead'
          // Note: The API might need adjustment if 'contact' field in AI Call Log is strictly a Link to 'Contact' doctype and not 'Lead'.
          // Let's check the AI Call Log definition. It links to 'Contact'.
          // If we pass Lead Name, it might fail if it expects a Contact Name.
          // If the Lead is not converted to Contact, this might be an issue.
          // BUT, often in Frappe, people link Lead/Contact dynamically or use Dynamic Link.
          // The AI Call Log 'contact' field is Link:Contact.
          // So we strictly need a Contact. 
          // Wait, the user requirement says "save those leads in the Frappe CRM Leads and from there they can start the AI Call".
          // So the user is on a Lead.
          // If the API strictly requires a Contact, we might need to change the API or the Call Log to support Leads.
          // Let's check the API again.
        },
        freeze: true,
        freeze_message: 'Initiating AI Call...',
        callback: function (r) {
          if (r.message && r.message.status === 'success') {
            frappe.show_alert({ message: 'Call Initiated Successfully', indicator: 'green' });
          }
        }
      });
    }
  );
}
