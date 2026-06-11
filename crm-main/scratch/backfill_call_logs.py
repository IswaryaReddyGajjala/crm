import sys
sys.path.extend(["/home/frappe/frappe-bench/apps/frappe", "/home/frappe/frappe-bench/apps/crm"])
import frappe

def run():
    frappe.init(site="crm.localhost", sites_path=".")
    frappe.connect()
    call_logs = frappe.get_all("CRM Call Log", fields=["name"])
    print(f"Backfilling {len(call_logs)} call logs...")
    
    for cl in call_logs:
        doc = frappe.get_doc("CRM Call Log", cl.name)
        doc.save(ignore_permissions=True)
        
    frappe.db.commit()
    print("Done backfilling.")

if __name__ == "__main__":
    run()
