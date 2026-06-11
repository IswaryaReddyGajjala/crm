import sys
sys.path.extend(["/home/frappe/frappe-bench/apps/frappe", "/home/frappe/frappe-bench/apps/crm"])
import frappe
import json

def run():
    frappe.init(site="crm.localhost", sites_path=".")
    frappe.connect()
    
    lead_settings_name = frappe.db.exists("CRM Global Settings", {"dt": "CRM Lead", "type": "Quick Filters"})
    call_log_settings_name = frappe.db.exists("CRM Global Settings", {"dt": "CRM Call Log", "type": "Quick Filters"})
    
    if lead_settings_name:
        lead_json = frappe.db.get_value("CRM Global Settings", lead_settings_name, "json")
        
        # We need to change lead_name, email, organization, status, source
        # Call Log has: lead_name, organization, direction, call_flag, duration
        # Or let's just make Call Log Quick Filters exactly what the Lead has, but appropriate for Call Log.
        # Wait, the user said "once see leads list page how olters and sort by is there in ui like that only implemnt in call logs page"
        # The Leads page has "Quick Filters" for: Name, Email, Organization, Status, Source.
        # So Call Logs should have: Name, Organization, Direction, Call Flag, etc.?
        # Or I can just set Call Logs Quick Filters to the columns it has.
        
        new_filters = ["lead_name", "organization", "direction", "call_flag"]
        
        if call_log_settings_name:
            frappe.db.set_value("CRM Global Settings", call_log_settings_name, "json", json.dumps(new_filters))
        else:
            doc = frappe.new_doc("CRM Global Settings")
            doc.dt = "CRM Call Log"
            doc.type = "Quick Filters"
            doc.json = json.dumps(new_filters)
            doc.insert(ignore_permissions=True)
            
        frappe.db.commit()
        print("Synced Call Log Quick Filters")
    else:
        print("No Lead Quick Filters found.")

if __name__ == "__main__":
    run()
