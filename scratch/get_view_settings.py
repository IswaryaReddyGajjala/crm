import frappe
import json

def run():
    frappe.init(site="aiprof_crm")
    frappe.connect()
    try:
        lead_view = frappe.db.get_value("CRM View Settings", {"reference_doctype": "CRM Lead", "view_type": "list"}, "columns")
        call_view = frappe.db.get_value("CRM View Settings", {"reference_doctype": "CRM Call Log", "view_type": "list"}, "columns")
        print("Lead list columns:", lead_view)
        print("Call Log list columns:", call_view)
    finally:
        frappe.destroy()

if __name__ == "__main__":
    run()
