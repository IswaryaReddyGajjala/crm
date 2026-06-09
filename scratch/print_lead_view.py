import sys
sys.path.extend(["/home/frappe/frappe-bench/apps/frappe", "/home/frappe/frappe-bench/apps/crm"])
import frappe
import json

def run():
    frappe.init(site="crm.localhost", sites_path=".")
    frappe.connect()
    
    doc = frappe.get_doc("CRM View Settings", {"dt": "CRM Lead", "type": "list"})
    print("LEAD FILTERS:", doc.filters)
    print("LEAD SORT:", doc.sort_by)
    
    cdoc = frappe.get_doc("CRM View Settings", {"dt": "CRM Call Log", "type": "list"})
    print("CALL LOG FILTERS:", cdoc.filters)
    print("CALL LOG SORT:", cdoc.sort_by)

if __name__ == "__main__":
    run()
