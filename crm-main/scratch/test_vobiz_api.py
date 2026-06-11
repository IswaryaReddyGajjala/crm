import requests
import json
import sys
sys.path.extend(["/home/frappe/frappe-bench/apps/frappe", "/home/frappe/frappe-bench/apps/crm"])
import frappe

def run():
    frappe.init(site="crm.localhost", sites_path="/home/frappe/frappe-bench/sites")
    frappe.connect()
    
    settings = frappe.get_single("CRM Vobiz Settings")
    auth_id = settings.auth_id
    api_password = settings.get_password("api_password")
    
    if not auth_id or not api_password:
        print("Auth ID or API Password not set!")
        return
        
    print(f"Testing connection with Auth ID: {auth_id}")
    
    # 1. Fetch applications
    url = f"https://api.vobiz.ai/api/v1/Account/{auth_id}/Application/"
    headers = {
        "X-Auth-ID": auth_id,
        "X-Auth-Token": api_password,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Applications status: {response.status_code}")
        print(f"Applications response: {response.text}")
    except Exception as e:
        print(f"Error fetching applications: {e}")
        
    # 2. Fetch endpoints
    # Let's try /api/v1/Account/{auth_id}/Endpoint/
    url2 = f"https://api.vobiz.ai/api/v1/Account/{auth_id}/Endpoint/"
    try:
        response2 = requests.get(url2, headers=headers, timeout=10)
        print(f"Endpoints status: {response2.status_code}")
        print(f"Endpoints response: {response2.text}")
    except Exception as e:
        print(f"Error fetching endpoints: {e}")

if __name__ == "__main__":
    run()
