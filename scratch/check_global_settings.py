import sys
sys.path.extend(["/home/frappe/frappe-bench/apps/frappe", "/home/frappe/frappe-bench/apps/crm"])
import frappe

def run():
    frappe.init(site="crm.localhost", sites_path=".")
    frappe.connect()
    
    lead_settings = frappe.db.get_value("CRM Global Settings", {"dt": "CRM Lead", "type": "Quick Filters"}, "json")
    print("LEAD QUICK FILTERS:", lead_settings)
    
    call_log_settings = frappe.db.get_value("CRM Global Settings", {"dt": "CRM Call Log", "type": "Quick Filters"}, "json")
    print("CALL LOG QUICK FILTERS:", call_log_settings)

if __name__ == "__main__":
    run()
