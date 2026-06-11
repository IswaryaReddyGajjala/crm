import sys
sys.path.extend(["/home/frappe/frappe-bench/apps/frappe", "/home/frappe/frappe-bench/apps/crm"])
import frappe
import json

def run():
    frappe.init(site="crm.localhost", sites_path=".")
    frappe.connect()
    
    view_name = frappe.db.get_value("CRM View Settings", {"dt": "CRM Call Log", "type": "list"}, "name")
    
    if view_name:
        doc = frappe.get_doc("CRM View Settings", view_name)
        cols = json.loads(doc.columns)
        for col in cols:
            if col.get("key") == "call_duration" or col.get("fieldname") == "call_duration":
                col["key"] = "duration"
                if "fieldname" in col:
                    col["fieldname"] = "duration"
        doc.columns = json.dumps(cols)
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Fixed CRM Call Log view settings.")
    else:
        print("No view settings found for CRM Call Log.")

if __name__ == "__main__":
    run()
