frappe.pages['AI Calling Dashboard'].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: 'AI Calling Dashboard',
    single_column: true
  });

  // Load CSS
  frappe.require("ai_calling_dashboard.css");

  // Render Dashboard Layout with Tabs
  $(wrapper).find('.layout-main-section').append(`
        <div class="ai-calling-dashboard">
            <div class="dashboard-tabs">
                <div class="dashboard-tab active" data-tab="overview">Overview</div>
                <div class="dashboard-tab" data-tab="apollo">Apollo Search</div>
                <div class="dashboard-tab" data-tab="history">Call History</div>
            </div>

            <div class="tab-content active" id="tab-overview">
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-icon"><i class="fa fa-phone"></i></div>
                        <div class="metric-title">Total Calls Made</div>
                        <div class="metric-value" id="metric-total-calls">-</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon"><i class="fa fa-fire"></i></div>
                        <div class="metric-title">Hot Leads</div>
                        <div class="metric-value" id="metric-hot-leads">-</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon"><i class="fa fa-clock-o"></i></div>
                        <div class="metric-title">Avg Duration</div>
                        <div class="metric-value" id="metric-avg-duration">-</div>
                    </div>
                </div>
            </div>

            <div class="tab-content" id="tab-apollo">
                <div class="dashboard-section" id="apollo-search-section">
                    <h3>Apollo.io Lead Finder</h3>
                    <div class="apollo-search-filters">
                        <div class="form-group">
                            <label>Job Title</label>
                            <input type="text" id="search-job-title" placeholder="e.g. CEO, Sales Manager">
                        </div>
                        <div class="form-group">
                            <label>Location</label>
                            <input type="text" id="search-location" placeholder="e.g. San Francisco, London">
                        </div>
                        <div class="form-group">
                            <label>Industry (Keywords)</label>
                            <input type="text" id="search-industry" placeholder="e.g. Technology, Finance">
                        </div>
                    </div>
                    <div class="search-actions">
                        <button class="btn btn-primary" id="btn-search-leads">Search Leads</button>
                    </div>
                    <div class="results-table-container" id="apollo-results-container" style="display:none;">
                        <table class="results-table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Title</th>
                                    <th>Company</th>
                                    <th>Location</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody id="apollo-results-body"></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="tab-content" id="tab-history">
                <div class="dashboard-section" id="recent-calls-section">
                    <h3>AI Call History</h3>
                    <div class="recent-calls-list" id="recent-calls-list">
                        <div class="text-center p-3">Loading...</div>
                    </div>
                </div>
            </div>
        </div>
    `);

  // Tab Switching Logic
  $('.dashboard-tab').on('click', function () {
    const tab = $(this).data('tab');

    // Update Tabs UI
    $('.dashboard-tab').removeClass('active');
    $(this).addClass('active');

    // Update Content UI
    $('.tab-content').removeClass('active');
    $(`#tab-${tab}`).addClass('active');

    // Load data if needed
    if (tab === 'overview') {
      load_overview_metrics();
    } else if (tab === 'history') {
      load_recent_calls();
    }
  });

  // Attach Apollo Event Listeners
  page.wrapper.find('#btn-search-leads').on('click', function () {
    search_apollo_leads();
  });

  // Initial Load
  load_overview_metrics();
}

function load_overview_metrics() {
  frappe.call({
    method: 'ai_calling_agent.api.get_dashboard_metrics',
    callback: function (r) {
      if (r.message) {
        $('#metric-total-calls').text(r.message.total_calls);
        $('#metric-hot-leads').text(r.message.hot_leads);

        const avg = r.message.avg_duration || 0;
        $('#metric-avg-duration').text(format_duration(avg));
      }
    }
  });
}

function search_apollo_leads() {
  const job_title = $('#search-job-title').val();
  const location = $('#search-location').val();
  const industry = $('#search-industry').val();

  if (!job_title && !location && !industry) {
    frappe.msgprint('Please enter at least one search criteria.');
    return;
  }

  frappe.call({
    method: 'ai_calling_agent.api.search_apollo_leads',
    args: {
      job_title: job_title,
      location: location,
      industry: industry
    },
    freeze: true,
    freeze_message: 'Searching Apollo.io...',
    callback: function (r) {
      if (r.message) {
        render_apollo_results(r.message);
      } else {
        $('#apollo-results-container').show();
        $('#apollo-results-body').html('<tr><td colspan="5" class="text-center">No leads found.</td></tr>');
      }
    }
  });
}

function render_apollo_results(leads) {
  const tbody = $('#apollo-results-body');
  tbody.empty();

  if (leads.length === 0) {
    tbody.html('<tr><td colspan="5" class="text-center">No leads found.</td></tr>');
  } else {
    leads.forEach(lead => {
      const row = `
                <tr>
                    <td>${lead.name}</td>
                    <td>${lead.title || '-'}</td>
                    <td>${lead.company || '-'}</td>
                    <td>${lead.location || '-'}</td>
                    <td>
                        <button class="btn btn-xs btn-default btn-save-lead" data-id="${lead.id}">
                            Save to CRM
                        </button>
                    </td>
                </tr>
            `;
      tbody.append(row);
    });

    // Attach save handlers
    $('.btn-save-lead').on('click', function () {
      const btn = $(this);
      const apollo_id = btn.data('id');
      save_apollo_lead(apollo_id, btn);
    });
  }

  $('#apollo-results-container').show();
}

function save_apollo_lead(apollo_id, btn_element) {
  frappe.call({
    method: 'ai_calling_agent.api.save_apollo_lead',
    args: {
      apollo_id: apollo_id
    },
    freeze: true,
    freeze_message: 'Saving Lead...',
    callback: function (r) {
      if (r.message && r.message.status === 'success') {
        frappe.show_alert({ message: 'Lead saved successfully!', indicator: 'green' });
        btn_element.text('Saved').attr('disabled', true).removeClass('btn-default').addClass('btn-success');
      }
    }
  });
}

function load_recent_calls() {
  frappe.call({
    method: 'frappe.client.get_list',
    args: {
      doctype: 'AI Call Log',
      fields: ['name', 'party', 'party_type', 'phone_number', 'call_status', 'duration', 'ai_summary', 'creation'],
      order_by: 'creation desc',
      limit_page_length: 20
    },
    callback: function (r) {
      const container = $('#recent-calls-list');
      container.empty();

      if (r.message && r.message.length > 0) {
        r.message.forEach(log => {
          const statusClass = `status-${log.call_status.toLowerCase().replace(' ', '-')}`;
          const summary = log.ai_summary || 'No summary available yet.';
          const duration = log.duration ? format_duration(log.duration) : '-';

          const card = `
                        <div class="call-card" onclick="frappe.set_route('Form', 'AI Call Log', '${log.name}')" style="cursor: pointer;">
                            <div class="call-info">
                                <h4>${log.party || log.phone_number} <span class="call-status ${statusClass}">${log.call_status}</span></h4>
                                <div class="call-meta">
                                    <span><i class="fa fa-phone"></i> ${log.phone_number}</span>
                                    <span><i class="fa fa-clock-o"></i> ${duration}</span>
                                    <span><i class="fa fa-calendar"></i> ${frappe.datetime.comment_when(log.creation)}</span>
                                </div>
                                <div class="call-summary">
                                    ${summary}
                                </div>
                            </div>
                            <div class="call-action">
                                <i class="fa fa-chevron-right text-muted"></i>
                            </div>
                        </div>
                    `;
          container.append(card);
        });
      } else {
        container.html('<div class="no-results">No recent calls found.</div>');
      }
    }
  });
}

function format_duration(seconds) {
  if (!seconds) return '0s';
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}m ${s}s`;
}
