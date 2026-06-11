import frappe

def run():
    frappe.init(site='crm.localhost')
    frappe.connect()
    doc = frappe.get_doc('FCRM Settings')
    print("BRAND NAME:", doc.brand_name)
    print("DROPDOWN ITEMS:")
    for item in doc.dropdown_items:
        print(f"  - {item.label}: hidden={item.hidden}, name1={item.name1}")

if __name__ == '__main__':
    run()
