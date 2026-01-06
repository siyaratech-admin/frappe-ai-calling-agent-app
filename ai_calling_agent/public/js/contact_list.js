frappe.listview_settings['Contact'] = {
  formatters: {
    // This function will run for every row's 'phone' column
    phone: function (value, field, doc) {
      if (!value) {
        return ""; // If no phone number, show nothing
      }

      // Get the data we need from the row
      let contact_docname = doc.name;
      let phone_number = value; // 'value' is the phone number string

      // Create the HTML for our clickable icon
      // We use a <a> tag and classes to make it easy to click
      let call_btn_html = `
                <a class="ai-call-list-btn"
                   data-phone="${phone_number}"
                   data-docname="${contact_docname}"
                   title="Start AI Call"
                   style="margin-right: 10px; cursor: pointer;">
                   <i class="fa fa-phone" style="font-size: 14px;"></i>
                </a>
            `;

      // Return our button HTML + the original phone number
      return call_btn_html + value;
    }
  },
  // This 'onload' function runs after the list is rendered
  onload: function (listview) {
    // We add a single click listener to the list wrapper
    // This is more efficient and handles clicks on our button
    listview.wrapper.on('click', '.ai-call-list-btn', function (e) {
      e.preventDefault();    // Stop the browser from following the <a> tag
      e.stopPropagation(); // Stop the click from opening the Contact

      // Get the data we stored on the button
      let $btn = $(this);
      let phone = $btn.data('phone');
      let docname = $btn.data('docname');

      // --- This is our E.164 (country code) fix ---
      if (phone && !phone.startsWith('+')) {
        phone = '+91' + phone;
      }

      // Show a "working..." message
      frappe.show_alert({
        message: __(`Placing AI call to ${docname}...`),
        indicator: 'blue'
      }, 5);

      // --- This is the same frappe.call as our other button ---
      frappe.call({
        method: 'ai_calling_agent.api.start_ai_call',
        args: {
          'phone_number': phone,
          'contact_docname': docname
        },
        callback: function (response) {
          if (response.message && response.message.status === 'success') {
            frappe.show_alert({
              message: __("Call placed successfully!"),
              indicator: 'green'
            }, 5);
          } else {
            frappe.show_alert({
              message: __("Failed to place call."),
              indicator: 'red'
            }, 5);
          }
        },
        error: function (err) {
          console.error("Frappe Call Failed:", err);
          frappe.msgprint(__("Error: Could not contact server. Check F12 console."));
        }
      });
    });
  }
};