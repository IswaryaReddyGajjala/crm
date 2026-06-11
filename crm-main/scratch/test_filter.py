import frappe
frappe.init(site="crm")
frappe.connect()

logs_incoming = frappe.get_list('CRM Call Log', filters={'type': 'Incoming'})
logs_outgoing = frappe.get_list('CRM Call Log', filters={'type': 'Outgoing'})

print(f"Incoming calls: {len(logs_incoming)}")
print(f"Outgoing calls: {len(logs_outgoing)}")

logs_inbound = frappe.get_list('CRM Call Log', filters={'direction': 'inbound'})
logs_outbound = frappe.get_list('CRM Call Log', filters={'direction': 'outbound'})

print(f"Inbound calls (direction): {len(logs_inbound)}")
print(f"Outbound calls (direction): {len(logs_outbound)}")
