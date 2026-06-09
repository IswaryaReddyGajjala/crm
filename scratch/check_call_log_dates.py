import sys
sys.path.extend(["/home/frappe/frappe-bench/apps/frappe", "/home/frappe/frappe-bench/apps/crm"])
import frappe

def run():
    frappe.init(site="crm.localhost", sites_path=".")
    frappe.connect()
    
    meta = frappe.get_meta("CRM Call Log")
    for f in meta.fields:
        if f.fieldname in ['call_date', 'call_time']:
            print(f.fieldname, f.fieldtype)

if __name__ == "__main__":
    run()
