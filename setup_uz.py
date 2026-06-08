#!/usr/bin/env python3
"""
Uzbekistan ERPNext setup: UZS currency, salary components, custom Employee fields, GL accounts.
Run inside the bench container: cd /home/frappe/frappe-bench && ./env/bin/python /home/frappe/setup_uz.py
"""
import os
import sys

# CWD must be the sites/ dir so frappe's relative "../logs/" path resolves to bench/logs/
os.chdir("/home/frappe/frappe-bench/sites")
sys.path.insert(0, "/home/frappe/frappe-bench/apps/frappe")

import frappe

SITE = "frontend"
SITES_PATH = "/home/frappe/frappe-bench/sites"


def main():
    frappe.init(site=SITE, sites_path=SITES_PATH)
    frappe.connect()
    print("=== Uzbekistan ERPNext Setup ===\n")
    try:
        r_currency = setup_currency()
        r_components = setup_salary_components()
        r_fields = setup_custom_fields()
        company = ensure_company()
        r_accounts = setup_gl_accounts(company) if company else [("GL Accounts", "SKIPPED — no company")]
        frappe.db.commit()
        print_summary(r_currency, r_components, r_fields, r_accounts)
    finally:
        frappe.destroy()


# ── 1. Currency ────────────────────────────────────────────────────────────────

def setup_currency():
    results = []
    if not frappe.db.exists("Currency", "UZS"):
        try:
            frappe.get_doc({
                "doctype": "Currency",
                "currency_name": "UZS",
                "currency_symbol": "сўм",
                "fraction": "Tiyin",
                "fraction_units": 100,
                "enabled": 1,
                "smallest_currency_fraction_value": 1,
                "number_format": "#,###.##",
            }).insert(ignore_permissions=True)
            results.append(("UZS (сўм)", "CREATED"))
        except Exception as e:
            results.append(("UZS (сўм)", f"ERROR: {e}"))
    else:
        results.append(("UZS (сўм)", "EXISTS"))
    return results


# ── 2. Salary components ───────────────────────────────────────────────────────

def setup_salary_components():
    if not frappe.db.table_exists("Salary Component"):
        return [("Salary Components", "SKIPPED — hrms not installed")]

    items = [
        ("Basic Salary UZ",        "BSU",  "Earning"),
        ("INPS Pension UZ",        "INPS", "Deduction"),
        ("Personal Income Tax UZ", "PIT",  "Deduction"),
        ("UST Employer UZ",        "UST",  "Deduction"),
    ]
    results = []
    for name, abbr, comp_type in items:
        existing = frappe.db.sql(
            "SELECT name FROM `tabSalary Component` WHERE name=%s", (name,), as_list=True
        )
        if not existing:
            try:
                # Use raw SQL because the ORM requires hrms controller to be importable
                frappe.db.sql("""
                    INSERT INTO `tabSalary Component`
                    (name, creation, modified, modified_by, owner, docstatus, idx,
                     salary_component, salary_component_abbr, type)
                    VALUES (%s, NOW(), NOW(), %s, %s, 0, 0, %s, %s, %s)
                """, (name, "Administrator", "Administrator", name, abbr, comp_type))
                results.append((name, "CREATED"))
            except Exception as e:
                results.append((name, f"ERROR: {e}"))
        else:
            results.append((name, "EXISTS"))
    return results


# ── 3. Custom fields on Employee ──────────────────────────────────────────────

def setup_custom_fields():
    fields = [
        {"fieldname": "inn",          "label": "INN",          "fieldtype": "Data",  "insert_after": "employee_name"},
        {"fieldname": "pinfl",        "label": "PINFL",        "fieldtype": "Data",  "insert_after": "inn"},
        {"fieldname": "inps_account", "label": "INPS Account", "fieldtype": "Data",  "insert_after": "pinfl"},
        {"fieldname": "tax_resident", "label": "Tax Resident", "fieldtype": "Check", "insert_after": "inps_account"},
    ]
    results = []
    for f in fields:
        cf_name = f"Employee-{f['fieldname']}"
        if not frappe.db.exists("Custom Field", cf_name):
            try:
                frappe.get_doc({"doctype": "Custom Field", "dt": "Employee", **f}).insert(ignore_permissions=True)
                results.append((f["label"], "CREATED"))
            except Exception as e:
                results.append((f["label"], f"ERROR: {e}"))
        else:
            results.append((f["label"], "EXISTS"))
    return results


# ── 4. Company + GL accounts ──────────────────────────────────────────────────

def ensure_company():
    companies = frappe.get_all("Company", pluck="name")
    if companies:
        print(f"Using existing company: {companies[0]}")
        return companies[0]

    print("No company found — creating 'ERPNext Uzbekistan'...")
    try:
        frappe.get_doc({
            "doctype": "Company",
            "company_name": "ERPNext Uzbekistan",
            "abbr": "EU",
            "default_currency": "UZS",
            "country": "Uzbekistan",
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        # Mark setup wizard complete so the UI doesn't redirect to the wizard
        frappe.db.set_value("System Settings", "System Settings", "setup_complete", 1)
        frappe.db.commit()
        print("Company 'ERPNext Uzbekistan' created.")
        return "ERPNext Uzbekistan"
    except Exception as e:
        print(f"Could not create company: {e}")
        return None


def setup_gl_accounts(company):
    abbr = frappe.db.get_value("Company", company, "abbr")

    # Locate the Accounts Payable group
    parent = None
    for flt in [
        {"company": company, "is_group": 1, "account_type": "Payable"},
        {"company": company, "is_group": 1, "account_name": ["like", "%Payable%"]},
        {"company": company, "is_group": 1, "account_name": ["like", "%Creditor%"]},
    ]:
        rows = frappe.get_all("Account", filters=flt, pluck="name", limit=1)
        if rows:
            parent = rows[0]
            break

    if not parent:
        return [("GL Accounts", "SKIPPED — no Accounts Payable parent found in CoA")]

    accounts = [
        "PIT Payable",
        "UST Payable",
        "INPS Payable",
        "Salaries Payable",
    ]
    results = []
    for acc_name in accounts:
        full_name = f"{acc_name} - {abbr}"
        if not frappe.db.exists("Account", full_name):
            try:
                frappe.get_doc({
                    "doctype": "Account",
                    "account_name": acc_name,
                    "parent_account": parent,
                    "company": company,
                    "account_type": "Payable",
                    "is_group": 0,
                }).insert(ignore_permissions=True)
                results.append((full_name, "CREATED"))
            except Exception as e:
                results.append((full_name, f"ERROR: {e}"))
        else:
            results.append((full_name, "EXISTS"))
    return results


# ── Summary ────────────────────────────────────────────────────────────────────

def print_summary(r_currency, r_components, r_fields, r_accounts):
    sections = [
        ("Currency",          r_currency),
        ("Salary Components", r_components),
        ("Custom Fields",     r_fields),
        ("GL Accounts",       r_accounts),
    ]
    print("\n── Results ───────────────────────────────")
    for section, rows in sections:
        print(f"\n  {section}:")
        for name, status in rows:
            ok = status in ("CREATED", "EXISTS")
            print(f"    {'OK' if ok else 'FAIL'}  {name}: {status}")
    print("\n==========================================")


if __name__ == "__main__":
    main()
