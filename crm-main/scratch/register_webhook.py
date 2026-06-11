import sys
import os
os.chdir('/home/frappe/frappe-bench')

sys.path.insert(0, '/home/frappe/frappe-bench/apps/frappe')
sys.path.insert(0, '/home/frappe/frappe-bench/apps/crm')
import frappe
import requests

frappe.init(site='crm.localhost', sites_path='/home/frappe/frappe-bench/sites')
frappe.connect()

doc = frappe.get_single('CRM Vobiz Settings')
auth_id = doc.auth_id
api_password = doc.get_password('api_password')
app_id = doc.app_id

webhook_url = 'https://240560eca66d0b71-183-82-122-17.serveousercontent.com/api/method/crm.integrations.vobiz.api.voice'
hangup_url = 'https://240560eca66d0b71-183-82-122-17.serveousercontent.com/api/method/crm.integrations.vobiz.api.hangup'

url = f'https://api.vobiz.ai/api/v1/Account/{auth_id}/Application/{app_id}/'
headers = {
    'X-Auth-ID': auth_id,
    'X-Auth-Token': api_password,
    'Content-Type': 'application/json'
}
payload = {
    'answer_url': webhook_url,
    'answer_method': 'POST',
    'hangup_url': hangup_url,
    'hangup_method': 'POST'
}

print('Sending request to Vobiz API...')
res = requests.post(url, headers=headers, json=payload, timeout=10)
res.raise_for_status()

doc.db_set('registered_webhook_url', webhook_url)
frappe.db.commit()
print('SUCCESSALLY REGISTERED:', webhook_url)
