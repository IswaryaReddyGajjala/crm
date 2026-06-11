import sys
sys.path.extend(["/home/frappe/frappe-bench/apps/frappe", "/home/frappe/frappe-bench/apps/crm"])
import frappe

def run():
    frappe.init(site="crm.localhost", sites_path="/home/frappe/frappe-bench/sites")
    frappe.connect()
    
    agents = frappe.get_all("CRM Telephony Agent", fields=["name", "vobiz_username", "vobiz_number"])
    print("AGENTS LIST:")
    for a in agents:
        doc = frappe.get_doc("CRM Telephony Agent", a.name)
        pw = doc.get_password("vobiz_password")
        print(f"Agent: {doc.name}")
        print(f"  vobiz_username: {doc.vobiz_username}")
        print(f"  vobiz_number: {doc.vobiz_number}")
        print(f"  password_length: {len(pw) if pw else 0}")
        print(f"  password_value: {pw}")
        
    settings = frappe.get_single("CRM Vobiz Settings")
    print("\nVOBIZ SETTINGS:")
    print(f"  enabled: {settings.enabled}")
    print(f"  auth_id: {settings.auth_id}")
    print(f"  app_id: {settings.app_id}")
    print(f"  api_password (api_key): {settings.get_password('api_password')}")
    print(f"  websocket_url_override: {settings.websocket_url_override}")

if __name__ == "__main__":
    run()
