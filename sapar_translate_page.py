import frappe


@frappe.whitelist()
def get_translations(language, search="", only_empty=0, only_done=0, page=1, page_length=100):
    filters = [["language", "=", language]]
    if search:
        filters.append(["source_text", "like", f"%{search}%"])
    if frappe.utils.cint(only_empty):
        filters.append(["translated_text", "in", ["", None]])
    elif frappe.utils.cint(only_done):
        filters.append(["translated_text", "not in", ["", None]])

    limit_start = (frappe.utils.cint(page) - 1) * frappe.utils.cint(page_length)

    rows = frappe.get_list(
        "Translation",
        filters=filters,
        fields=["name", "source_text", "translated_text", "context"],
        limit_start=limit_start,
        limit_page_length=frappe.utils.cint(page_length),
        order_by="source_text asc",
    )
    total = frappe.db.count("Translation", filters)
    done = frappe.db.count("Translation", [["language", "=", language], ["translated_text", "not in", ["", None]]])
    total_lang = frappe.db.count("Translation", [["language", "=", language]])
    return {"rows": rows, "total": total, "done": done, "total_lang": total_lang}


@frappe.whitelist()
def save_translation(name, translated_text):
    frappe.db.set_value("Translation", name, "translated_text", translated_text)
    return True


@frappe.whitelist()
def save_batch(updates):
    if isinstance(updates, str):
        import json
        updates = json.loads(updates)
    for item in updates:
        frappe.db.set_value("Translation", item["name"], "translated_text", item["translated_text"])
    frappe.db.commit()
    return len(updates)


@frappe.whitelist()
def add_translation(language, source_text, translated_text="", context=""):
    doc = frappe.get_doc({
        "doctype": "Translation",
        "language": language,
        "source_text": source_text,
        "translated_text": translated_text,
        "context": context,
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.as_dict()


@frappe.whitelist()
def delete_translation(name):
    frappe.delete_doc("Translation", name, ignore_permissions=True)
    frappe.db.commit()
    return True
