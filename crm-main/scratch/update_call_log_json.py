import json

path = '/home/satheesh/aiprof_crm/crm/fcrm/doctype/crm_call_log/crm_call_log.json'
with open(path, 'r') as f:
    dt = json.load(f)

new_fields = [
  {
   "fieldname": "column_break_for_lead",
   "fieldtype": "Column Break"
  },
  {
   "fieldname": "lead_name",
   "fieldtype": "Data",
   "label": "Lead Name",
   "read_only": 1
  },
  {
   "fieldname": "organization",
   "fieldtype": "Data",
   "label": "Organization",
   "read_only": 1
  },
  {
   "fieldname": "mobile_no",
   "fieldtype": "Data",
   "label": "Mobile No.",
   "options": "Phone",
   "read_only": 1
  },
  {
   "fieldname": "direction",
   "fieldtype": "Select",
   "label": "Direction",
   "options": "\ninbound\noutbound"
  },
  {
   "fieldname": "call_date",
   "fieldtype": "Date",
   "label": "Date"
  },
  {
   "fieldname": "call_time",
   "fieldtype": "Time",
   "label": "Time"
  },
  {
   "fieldname": "call_flag",
   "fieldtype": "Data",
   "label": "Flags"
  }
]

existing = [f['fieldname'] for f in dt['fields']]
for nf in new_fields:
    if nf['fieldname'] not in existing:
        dt['fields'].append(nf)
        dt['field_order'].append(nf['fieldname'])

with open(path, 'w') as f:
    json.dump(dt, f, indent=1)

print("Updated crm_call_log.json")
