import sys
sys.path.extend(["/home/frappe/frappe-bench/apps/frappe", "/home/frappe/frappe-bench/apps/crm"])
import frappe

def run():
    frappe.init(site="crm.localhost", sites_path=".")
    frappe.connect()
    
    lead_view = frappe.get_doc("CRM View Settings", {"dt": "CRM Lead", "type": "list"})
    call_log_view_name = frappe.db.get_value("CRM View Settings", {"dt": "CRM Call Log", "type": "list"}, "name")
    
    if call_log_view_name:
        doc = frappe.get_doc("CRM View Settings", call_log_view_name)
        
        doc.filters = lead_view.filters
        doc.order_by = lead_view.order_by
            
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Synced filters and order_by to CRM Call Log.")
    else:
        print("No view settings found for CRM Call Log.")

if __name__ == "__main__":
    run()
