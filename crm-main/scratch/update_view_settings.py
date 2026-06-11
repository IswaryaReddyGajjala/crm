import sys
sys.path.extend(["/home/frappe/frappe-bench/apps/frappe", "/home/frappe/frappe-bench/apps/crm"])
import frappe

def run():
    frappe.init(site="crm.localhost", sites_path=".")
    frappe.connect()
    
    lead_cols = frappe.db.get_value("CRM View Settings", {"dt": "CRM Lead", "type": "list"}, "columns")
    
    # Check if CRM Call Log view settings exist
    view_name = frappe.db.get_value("CRM View Settings", {"dt": "CRM Call Log", "type": "list"}, "name")
    
    if view_name:
        doc = frappe.get_doc("CRM View Settings", view_name)
        doc.columns = lead_cols
        doc.save(ignore_permissions=True)
        print("Updated existing view settings.")
    else:
        # Create it if it doesn't exist
        doc = frappe.new_doc("CRM View Settings")
        doc.dt = "CRM Call Log"
        doc.type = "list"
        doc.columns = lead_cols
        doc.save(ignore_permissions=True)
        print("Created new view settings.")
        
    frappe.db.commit()

if __name__ == "__main__":
    run()
