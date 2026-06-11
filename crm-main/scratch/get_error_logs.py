import frappe
import json

def run():
    frappe.init(site="crm.localhost")
    frappe.connect()
    logs = frappe.get_all("Error Log", fields=["name", "method", "title", "message", "creation"], order_by="creation desc", limit=20)
    print(json.dumps(logs, indent=2, default=str))

run()
