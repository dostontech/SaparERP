#!/usr/bin/env python3
"""
SaparERP Demo Data Setup
Creates two showcase companies:
  --company small  → Nur Savdo MChJ   (small textile shop,  ~5 employees)
  --company large  → Sapar Holding AJ (multi-division corp, ~50 employees)

Run:
  python setup_demo_data.py --company small
  python setup_demo_data.py --company large
  python setup_demo_data.py --company both
"""

import os, sys, random, datetime, argparse
from decimal import Decimal

os.chdir("/home/frappe/frappe-bench/sites")
sys.path.insert(0, "/home/frappe/frappe-bench/apps/frappe")
sys.path.insert(0, "/home/frappe/frappe-bench/apps/erpnext")

import frappe
from frappe.utils import today, add_days, add_months, getdate, nowdate

SITE = "frontend"
SITES_PATH = "/home/frappe/frappe-bench/sites"


# ═══════════════════════════════════════════════════════════════════════════
#  SMALL COMPANY CONFIG
# ═══════════════════════════════════════════════════════════════════════════
SMALL = {
    "company_name": "Nur Savdo MChJ",
    "abbr": "NS",
    "country": "Uzbekistan",
    "currency": "UZS",
    "tax_id": "123456789",
    "employees": [
        {"name": "Alisher Karimov",   "designation": "Director",         "dept": "Management",  "salary": 8_000_000},
        {"name": "Zulfiya Yusupova",  "designation": "Accountant",       "dept": "Accounting",  "salary": 5_000_000},
        {"name": "Bobur Toshmatov",   "designation": "Sales Manager",    "dept": "Sales",       "salary": 4_500_000},
        {"name": "Malika Nazarova",   "designation": "Sales Executive",  "dept": "Sales",       "salary": 3_500_000},
        {"name": "Sardor Mirzayev",   "designation": "Storekeeper",      "dept": "Warehouse",   "salary": 3_000_000},
    ],
    "customers": [
        ("Akbar Hasanov",      "Individual", "Toshkent"),
        ("Barno Raximova",     "Individual", "Toshkent"),
        ("Firdavs Usmonov",    "Individual", "Samarqand"),
        ("Gulnora Sobirov",    "Individual", "Toshkent"),
        ("Hamidjon Tursunov",  "Individual", "Farg'ona"),
        ("Iroda Xolmatova",    "Company",    "Toshkent"),
        ("Jasur Qodirov",      "Company",    "Namangan"),
        ("Kamola Yildirim",    "Individual", "Buxoro"),
    ],
    "suppliers": [
        ("Ipak Yo'li Tekstil",  "Company"),
        ("Chinor Fabrikasi",    "Company"),
        ("Asia Import LLC",     "Company"),
        ("Sharq Mato MChJ",     "Company"),
        ("Bahor Textile",       "Company"),
    ],
    "items": [
        ("Ko'ylak erkaklar",    "Products", 85_000,  "dona"),
        ("Ko'ylak ayollar",     "Products", 95_000,  "dona"),
        ("Shim erkaklar",       "Products", 120_000, "dona"),
        ("Shim ayollar",        "Products", 130_000, "dona"),
        ("Futbolka",            "Products", 45_000,  "dona"),
        ("Kurtka",              "Products", 280_000, "dona"),
        ("Poyabzal erkaklar",   "Products", 220_000, "juft"),
        ("Poyabzal ayollar",    "Products", 250_000, "juft"),
        ("Sumka",               "Products", 180_000, "dona"),
        ("Ko'zoynaklar",        "Products", 75_000,  "dona"),
    ],
    "warehouses": ["Nur Savdo Ombori - NS"],
}


# ═══════════════════════════════════════════════════════════════════════════
#  LARGE COMPANY CONFIG
# ═══════════════════════════════════════════════════════════════════════════
LARGE = {
    "company_name": "Sapar Holding AJ",
    "abbr": "SH",
    "country": "Uzbekistan",
    "currency": "UZS",
    "tax_id": "987654321",
    "employees": [
        # Boshqaruv
        {"name": "Nodir Rashidov",      "designation": "CEO",                  "dept": "Management",  "salary": 25_000_000},
        {"name": "Dilnoza Ergasheva",   "designation": "CFO",                  "dept": "Finance",     "salary": 20_000_000},
        {"name": "Ulugbek Xasanov",     "designation": "CTO",                  "dept": "IT",          "salary": 18_000_000},
        {"name": "Nargiza Toshpulatova","designation": "HR Director",          "dept": "HR",          "salary": 15_000_000},
        {"name": "Sherzod Abdullayev",  "designation": "Sales Director",       "dept": "Sales",       "salary": 15_000_000},
        # Moliya
        {"name": "Feruza Qosimova",     "designation": "Chief Accountant",     "dept": "Accounting",  "salary": 12_000_000},
        {"name": "Botir Haydarov",      "designation": "Financial Analyst",    "dept": "Finance",     "salary": 10_000_000},
        {"name": "Ozoda Yunusova",      "designation": "Accountant",           "dept": "Accounting",  "salary": 8_000_000},
        {"name": "Hamza Tursunov",      "designation": "Accountant",           "dept": "Accounting",  "salary": 7_500_000},
        {"name": "Sabohat Razzaqova",   "designation": "Tax Specialist",       "dept": "Accounting",  "salary": 9_000_000},
        # Sotish
        {"name": "Jasur Ismoilov",      "designation": "Regional Manager",     "dept": "Sales",       "salary": 12_000_000},
        {"name": "Lobar Nazarova",      "designation": "Sales Manager",        "dept": "Sales",       "salary": 10_000_000},
        {"name": "Mansur Yo'ldoshev",   "designation": "Sales Manager",        "dept": "Sales",       "salary": 10_000_000},
        {"name": "Nilufar Baxtiyorova", "designation": "Sales Executive",      "dept": "Sales",       "salary": 7_000_000},
        {"name": "Otabek Mirzayev",     "designation": "Sales Executive",      "dept": "Sales",       "salary": 7_000_000},
        {"name": "Parizod Sodiqova",    "designation": "Sales Executive",      "dept": "Sales",       "salary": 6_500_000},
        {"name": "Qodir Yusupov",       "designation": "Sales Executive",      "dept": "Sales",       "salary": 6_500_000},
        {"name": "Rohila Axmedova",     "designation": "Sales Executive",      "dept": "Sales",       "salary": 6_000_000},
        # Ombor / Logistika
        {"name": "Sanjar Karimov",      "designation": "Warehouse Manager",    "dept": "Warehouse",   "salary": 10_000_000},
        {"name": "Tohir Raximov",       "designation": "Logistics Manager",    "dept": "Warehouse",   "salary": 9_000_000},
        {"name": "Umida Sobirov",       "designation": "Storekeeper",          "dept": "Warehouse",   "salary": 6_000_000},
        {"name": "Vohid Holiqov",       "designation": "Storekeeper",          "dept": "Warehouse",   "salary": 5_500_000},
        {"name": "Xurshid Normatov",    "designation": "Driver",               "dept": "Warehouse",   "salary": 5_000_000},
        {"name": "Yulduz Axrorova",     "designation": "Driver",               "dept": "Warehouse",   "salary": 5_000_000},
        # IT
        {"name": "Zafar Mahmudov",      "designation": "Senior Developer",     "dept": "IT",          "salary": 15_000_000},
        {"name": "Aziza Sobirov",       "designation": "Developer",            "dept": "IT",          "salary": 12_000_000},
        {"name": "Bekzod Xoliqov",      "designation": "System Administrator", "dept": "IT",          "salary": 10_000_000},
        # HR
        {"name": "Charos Tursunova",    "designation": "HR Manager",           "dept": "HR",          "salary": 10_000_000},
        {"name": "Doniyor Alimov",      "designation": "HR Specialist",        "dept": "HR",          "salary": 7_000_000},
        # Xarid
        {"name": "Elbek Qodirov",       "designation": "Purchase Manager",     "dept": "Purchase",    "salary": 11_000_000},
        {"name": "Farzona Yusupova",    "designation": "Purchase Executive",   "dept": "Purchase",    "salary": 8_000_000},
        {"name": "Gavhar Nazarova",     "designation": "Purchase Executive",   "dept": "Purchase",    "salary": 7_500_000},
    ],
    "customers": [
        ("Texno Market MChJ",      "Company",    "Toshkent"),
        ("Baraka Savdo AJ",        "Company",    "Toshkent"),
        ("Andijon Trade LLC",      "Company",    "Andijon"),
        ("Samarqand Business",     "Company",    "Samarqand"),
        ("Farg'ona Invest MChJ",   "Company",    "Farg'ona"),
        ("Namangan Group",         "Company",    "Namangan"),
        ("Buxoro Trade Center",    "Company",    "Buxoro"),
        ("Xorazm Commerce MChJ",   "Company",    "Xorazm"),
        ("Qashqadaryo Savdo",      "Company",    "Qashqadaryo"),
        ("Surxondaryo LLC",        "Company",    "Surxondaryo"),
        ("Termiz Export MChJ",     "Company",    "Surxondaryo"),
        ("Jizzax Distribution",    "Company",    "Jizzax"),
        ("Sirdaryo Optima",        "Company",    "Sirdaryo"),
        ("Navoiy Minerals MChJ",   "Company",    "Navoiy"),
        ("Global Toshkent LLC",    "Company",    "Toshkent"),
        ("Premier Electronics",    "Company",    "Toshkent"),
        ("Smart Solutions MChJ",   "Company",    "Toshkent"),
        ("Digital Hub AJ",         "Company",    "Toshkent"),
        ("Metro Cash & Carry UZ",  "Company",    "Toshkent"),
        ("Makro Supermarket",      "Company",    "Toshkent"),
    ],
    "suppliers": [
        ("Samsung Electronics UZ",  "Company"),
        ("LG Electronics Central",  "Company"),
        ("Apple Premium UZ",        "Company"),
        ("Xiaomi Uzbekistan",       "Company"),
        ("Dell Technologies UZ",    "Company"),
        ("HP Inc Uzbekistan",       "Company"),
        ("Lenovo UZ MChJ",          "Company"),
        ("Huawei Central Asia",     "Company"),
        ("Sony UZ Distribution",    "Company"),
        ("Bosch Home Uzbekistan",   "Company"),
        ("Artel Electronics AJ",    "Company"),
        ("Orient Electronics",      "Company"),
        ("China Import LLC",        "Company"),
        ("Korea Tech Import",       "Company"),
        ("EU Electronics MChJ",     "Company"),
    ],
    "items": [
        ("Smartphone Samsung A55",   "Electronics", 4_500_000, "dona"),
        ("Smartphone Xiaomi 14",     "Electronics", 5_200_000, "dona"),
        ("iPhone 15 Pro",            "Electronics", 18_000_000,"dona"),
        ("Laptop Dell Inspiron",     "Electronics", 12_000_000,"dona"),
        ("Laptop Lenovo IdeaPad",    "Electronics", 9_500_000, "dona"),
        ("MacBook Air M2",           "Electronics", 22_000_000,"dona"),
        ("Monitor Samsung 24\"",     "Electronics", 3_200_000, "dona"),
        ("Printer HP LaserJet",      "Electronics", 4_800_000, "dona"),
        ("UPS APC 1200VA",           "Electronics", 1_800_000, "dona"),
        ("Keyboard + Mouse Set",     "Electronics", 450_000,   "to'plam"),
        ("SSD 1TB Samsung",          "Electronics", 1_200_000, "dona"),
        ("RAM 16GB DDR4",            "Electronics", 800_000,   "dona"),
        ("Router WiFi6 Huawei",      "Electronics", 1_500_000, "dona"),
        ("Smart TV 55\" Samsung",    "Electronics", 8_500_000, "dona"),
        ("Refrigerator Artel 260L",  "Electronics", 7_200_000, "dona"),
        ("Washing Machine Bosch 7",  "Electronics", 9_800_000, "dona"),
        ("Air Conditioner 12000",    "Electronics", 6_500_000, "dona"),
        ("Vacuum Cleaner LG",        "Electronics", 2_800_000, "dona"),
        ("Microwave Oven Samsung",   "Electronics", 1_900_000, "dona"),
        ("Coffee Machine Delonghi",  "Electronics", 3_500_000, "dona"),
        ("Office Chair Premium",     "Furniture",   2_200_000, "dona"),
        ("Office Desk 160cm",        "Furniture",   3_800_000, "dona"),
        ("Shelf Unit Steel",         "Furniture",   1_800_000, "dona"),
        ("Filing Cabinet 4-Draw",    "Furniture",   2_500_000, "dona"),
        ("Conference Table 10p",     "Furniture",  18_000_000, "dona"),
    ],
    "warehouses": [
        "Toshkent Asosiy Ombor - SH",
        "Samarqand Ombori - SH",
        "Namangan Ombori - SH",
    ],
}


# ═══════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def exists(doctype, name):
    return frappe.db.exists(doctype, name)


def upsert(doctype, filters, values):
    name = frappe.db.get_value(doctype, filters)
    if name:
        doc = frappe.get_doc(doctype, name)
        doc.update(values)
        doc.save(ignore_permissions=True)
        return doc
    else:
        doc = frappe.get_doc({"doctype": doctype, **filters, **values})
        doc.insert(ignore_permissions=True)
        return doc


def rand_date(months_back=6):
    base = getdate(today())
    offset = random.randint(0, months_back * 30)
    return str(add_days(base, -offset))


def rand_date_range(start_months=3, end_months=0):
    base = getdate(today())
    start = add_days(base, -start_months * 30)
    end = add_days(base, -end_months * 30)
    diff = (getdate(end) - getdate(start)).days
    return str(add_days(start, random.randint(0, max(diff, 0))))


# ═══════════════════════════════════════════════════════════════════════════
#  SETUP CURRENCY
# ═══════════════════════════════════════════════════════════════════════════

def ensure_currency():
    if not exists("Currency", "UZS"):
        frappe.get_doc({
            "doctype": "Currency",
            "currency_name": "UZS",
            "symbol": "so'm",
            "fraction": "tiyin",
            "fraction_units": 100,
            "enabled": 1,
        }).insert(ignore_permissions=True)
    else:
        frappe.db.set_value("Currency", "UZS", "enabled", 1)
    print("  OK  Currency UZS")


# ═══════════════════════════════════════════════════════════════════════════
#  CREATE COMPANY
# ═══════════════════════════════════════════════════════════════════════════

def create_company(cfg):
    cname = cfg["company_name"]
    if exists("Company", cname):
        print(f"  OK  Company '{cname}' already exists")
        return
    doc = frappe.get_doc({
        "doctype": "Company",
        "company_name": cname,
        "abbr": cfg["abbr"],
        "country": cfg["country"],
        "default_currency": cfg["currency"],
        "tax_id": cfg["tax_id"],
        "create_chart_of_accounts_based_on": "Standard Template",
        "chart_of_accounts": "Standard",
        "date_of_establishment": add_months(today(), -24),
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  OK  Company '{cname}' created")


# ═══════════════════════════════════════════════════════════════════════════
#  SETUP MASTERS
# ═══════════════════════════════════════════════════════════════════════════

def setup_territories():
    regions = [
        ("Toshkent", "All Territories"),
        ("Samarqand", "All Territories"),
        ("Farg'ona", "All Territories"),
        ("Andijon", "All Territories"),
        ("Namangan", "All Territories"),
        ("Buxoro", "All Territories"),
        ("Xorazm", "All Territories"),
        ("Qashqadaryo", "All Territories"),
        ("Surxondaryo", "All Territories"),
        ("Jizzax", "All Territories"),
        ("Sirdaryo", "All Territories"),
        ("Navoiy", "All Territories"),
    ]
    for name, parent in regions:
        if not exists("Territory", name):
            frappe.get_doc({
                "doctype": "Territory",
                "territory_name": name,
                "parent_territory": parent,
            }).insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  OK  {len(regions)} territories ensured")


def setup_item_groups(cfg):
    groups = set(item[1] for item in cfg["items"])
    for g in groups:
        if not exists("Item Group", g):
            frappe.get_doc({
                "doctype": "Item Group",
                "item_group_name": g,
                "parent_item_group": "All Item Groups",
            }).insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  OK  Item groups: {', '.join(groups)}")


def setup_departments(cfg, company):
    root = f"All Departments - {cfg['abbr']}"
    if not frappe.db.exists("Department", root):
        frappe.get_doc({
            "doctype": "Department",
            "department_name": "All Departments",
            "company": company,
            "is_group": 1,
        }).insert(ignore_permissions=True)
        frappe.db.commit()

    depts = set(e["dept"] for e in cfg["employees"])
    for d in depts:
        if not exists("Department", f"{d} - {cfg['abbr']}"):
            frappe.get_doc({
                "doctype": "Department",
                "department_name": d,
                "company": company,
                "parent_department": root,
            }).insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  OK  Departments: {', '.join(depts)}")


def setup_designations(cfg):
    desigs = set(e["designation"] for e in cfg["employees"])
    for d in desigs:
        if not exists("Designation", d):
            frappe.get_doc({
                "doctype": "Designation",
                "designation_name": d,
            }).insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  OK  {len(desigs)} designations")


def setup_warehouses(cfg):
    company = cfg["company_name"]
    abbr = cfg["abbr"]
    for wh_name in cfg["warehouses"]:
        if not exists("Warehouse", wh_name):
            frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": wh_name.replace(f" - {abbr}", ""),
                "company": company,
            }).insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  OK  {len(cfg['warehouses'])} warehouse(s)")


# ═══════════════════════════════════════════════════════════════════════════
#  ITEMS
# ═══════════════════════════════════════════════════════════════════════════

def create_items(cfg):
    created = 0
    for item_name, group, rate, uom in cfg["items"]:
        if exists("Item", item_name):
            continue
        # Ensure UOM
        if not exists("UOM", uom):
            frappe.get_doc({"doctype": "UOM", "uom_name": uom}).insert(ignore_permissions=True)
        doc = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_name,
            "item_name": item_name,
            "item_group": group,
            "stock_uom": uom,
            "is_stock_item": 1,
            "standard_rate": rate,
            "valuation_rate": rate * 0.7,
        })
        doc.insert(ignore_permissions=True)
        # Set item price
        frappe.get_doc({
            "doctype": "Item Price",
            "item_code": item_name,
            "price_list": "Standard Selling",
            "currency": "UZS",
            "price_list_rate": rate,
            "buying": 0,
            "selling": 1,
        }).insert(ignore_permissions=True)
        frappe.get_doc({
            "doctype": "Item Price",
            "item_code": item_name,
            "price_list": "Standard Buying",
            "currency": "UZS",
            "price_list_rate": rate * 0.65,
            "buying": 1,
            "selling": 0,
        }).insert(ignore_permissions=True)
        created += 1
    frappe.db.commit()
    print(f"  OK  {created} items created")


# ═══════════════════════════════════════════════════════════════════════════
#  CUSTOMERS & SUPPLIERS
# ═══════════════════════════════════════════════════════════════════════════

def create_customers(cfg):
    created = 0
    for cname, ctype, territory in cfg["customers"]:
        if exists("Customer", cname):
            continue
        frappe.get_doc({
            "doctype": "Customer",
            "customer_name": cname,
            "customer_type": ctype,
            "customer_group": "Commercial" if ctype == "Company" else "Individual",
            "territory": territory if exists("Territory", territory) else "All Territories",
        }).insert(ignore_permissions=True)
        created += 1
    frappe.db.commit()
    print(f"  OK  {created} customers created")


def create_suppliers(cfg):
    created = 0
    for sname, stype in cfg["suppliers"]:
        if exists("Supplier", sname):
            continue
        frappe.get_doc({
            "doctype": "Supplier",
            "supplier_name": sname,
            "supplier_type": stype,
            "supplier_group": "All Supplier Groups",
        }).insert(ignore_permissions=True)
        created += 1
    frappe.db.commit()
    print(f"  OK  {created} suppliers created")


# ═══════════════════════════════════════════════════════════════════════════
#  EMPLOYEES
# ═══════════════════════════════════════════════════════════════════════════

def create_employees(cfg):
    company = cfg["company_name"]
    abbr = cfg["abbr"]
    created = 0
    emp_map = {}  # name → employee docname

    for e in cfg["employees"]:
        fname, lname = e["name"].split(" ", 1)
        dept_key = f"{e['dept']} - {abbr}"
        if not exists("Department", dept_key):
            dept_key = e["dept"]

        # Check by name
        existing = frappe.db.get_value("Employee", {"employee_name": e["name"], "company": company})
        if existing:
            emp_map[e["name"]] = existing
            continue

        doc = frappe.get_doc({
            "doctype": "Employee",
            "first_name": fname,
            "last_name": lname,
            "employee_name": e["name"],
            "company": company,
            "department": dept_key,
            "designation": e["designation"],
            "date_of_joining": str(add_months(today(), -random.randint(3, 36))),
            "date_of_birth": str(add_days(today(), -random.randint(25*365, 45*365))),
            "gender": "Female" if any(x in fname for x in ["Zulfiya","Malika","Dilnoza","Nargiza","Feruza","Ozoda","Sabohat","Lobar","Nilufar","Parizod","Rohila","Umida","Yulduz","Aziza","Charos","Farzona","Gavhar","Nodira","Ozoda","Sabohat"]) else "Male",
            "status": "Active",
            "employment_type": "Regular",
            "cell_number": f"+998 9{random.randint(0,9)} {random.randint(100,999)} {random.randint(10,99)} {random.randint(10,99)}",
        })
        doc.insert(ignore_permissions=True)
        emp_map[e["name"]] = doc.name
        created += 1

    frappe.db.commit()
    print(f"  OK  {created} employees created")
    return emp_map


def create_salary_structures(cfg, emp_map):
    company = cfg["company_name"]
    abbr = cfg["abbr"]

    # Ensure salary components exist
    for comp_name, comp_type in [
        ("Basic Salary UZ", "Earning"),
        ("INPS Pension UZ", "Deduction"),
        ("Personal Income Tax UZ", "Deduction"),
    ]:
        if not exists("Salary Component", comp_name):
            frappe.get_doc({
                "doctype": "Salary Component",
                "salary_component": comp_name,
                "salary_component_abbr": comp_name[:4],
                "type": comp_type,
                "is_tax_applicable": 1 if comp_type == "Deduction" else 0,
            }).insert(ignore_permissions=True)

    # One structure per unique salary
    salary_levels = {}
    for e in cfg["employees"]:
        salary_levels[e["salary"]] = True

    struct_map = {}
    for salary in salary_levels:
        struct_name = f"SS-{abbr}-{salary}"
        if not exists("Salary Structure", struct_name):
            doc = frappe.get_doc({
                "doctype": "Salary Structure",
                "name": struct_name,
                "company": company,
                "currency": "UZS",
                "payroll_frequency": "Monthly",
                "is_active": "Yes",
                "earnings": [{"salary_component": "Basic Salary UZ", "amount": salary}],
                "deductions": [
                    {"salary_component": "INPS Pension UZ",      "amount": salary * 0.01},
                    {"salary_component": "Personal Income Tax UZ","amount": salary * 0.12},
                ],
            })
            doc.insert(ignore_permissions=True)
        struct_map[salary] = struct_name

    # Assign structures to employees
    assigned = 0
    for e in cfg["employees"]:
        emp_name = emp_map.get(e["name"])
        if not emp_name:
            continue
        if frappe.db.exists("Salary Structure Assignment", {"employee": emp_name, "salary_structure": struct_map[e["salary"]]}):
            continue
        frappe.get_doc({
            "doctype": "Salary Structure Assignment",
            "employee": emp_name,
            "salary_structure": struct_map[e["salary"]],
            "from_date": add_months(today(), -6),
            "base": e["salary"],
            "company": company,
        }).insert(ignore_permissions=True)
        assigned += 1

    frappe.db.commit()
    print(f"  OK  Salary structures assigned for {assigned} employee(s)")


# ═══════════════════════════════════════════════════════════════════════════
#  TRANSACTIONS
# ═══════════════════════════════════════════════════════════════════════════

def create_purchase_invoices(cfg, count=10):
    company = cfg["company_name"]
    abbr = cfg["abbr"]
    wh = cfg["warehouses"][0]
    items = cfg["items"]
    suppliers = [s[0] for s in cfg["suppliers"]]
    created = 0

    for i in range(count):
        supplier = random.choice(suppliers)
        if not exists("Supplier", supplier):
            continue
        posting_date = rand_date_range(5, 1)
        n_items = random.randint(2, 5)
        sel_items = random.sample(items, min(n_items, len(items)))

        inv_items = []
        for iname, grp, rate, uom in sel_items:
            if not exists("Item", iname):
                continue
            qty = random.randint(5, 50)
            inv_items.append({
                "item_code": iname,
                "qty": qty,
                "rate": rate * 0.65,
                "uom": uom,
                "warehouse": wh,
            })

        if not inv_items:
            continue

        try:
            doc = frappe.get_doc({
                "doctype": "Purchase Invoice",
                "company": company,
                "supplier": supplier,
                "posting_date": posting_date,
                "bill_date": posting_date,
                "bill_no": f"SUP-{i+1:03d}",
                "currency": "UZS",
                "buying_price_list": "Standard Buying",
                "update_stock": 1,
                "items": inv_items,
            })
            doc.insert(ignore_permissions=True)
            doc.submit()
            created += 1
        except Exception as e:
            pass  # skip if validation fails

    frappe.db.commit()
    print(f"  OK  {created}/{count} purchase invoices created & submitted")


def create_sales_invoices(cfg, count=15):
    company = cfg["company_name"]
    wh = cfg["warehouses"][0]
    items = cfg["items"]
    customers = [c[0] for c in cfg["customers"]]
    created = 0

    for i in range(count):
        customer = random.choice(customers)
        if not exists("Customer", customer):
            continue
        posting_date = rand_date_range(4, 0)
        n_items = random.randint(1, 4)
        sel_items = random.sample(items, min(n_items, len(items)))

        inv_items = []
        for iname, grp, rate, uom in sel_items:
            if not exists("Item", iname):
                continue
            qty = random.randint(1, 10)
            inv_items.append({
                "item_code": iname,
                "qty": qty,
                "rate": rate,
                "uom": uom,
                "warehouse": wh,
            })

        if not inv_items:
            continue

        try:
            doc = frappe.get_doc({
                "doctype": "Sales Invoice",
                "company": company,
                "customer": customer,
                "posting_date": posting_date,
                "currency": "UZS",
                "selling_price_list": "Standard Selling",
                "update_stock": 1,
                "items": inv_items,
            })
            doc.insert(ignore_permissions=True)
            doc.submit()
            created += 1
        except Exception as e:
            pass

    frappe.db.commit()
    print(f"  OK  {created}/{count} sales invoices created & submitted")


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════

def setup_company(cfg, label):
    print(f"\n{'='*55}")
    print(f"  Setting up: {cfg['company_name']} ({label})")
    print(f"{'='*55}")

    ensure_currency()
    create_company(cfg)
    frappe.db.commit()

    print("\n── Masters ───────────────────────────────────")
    setup_territories()
    setup_item_groups(cfg)
    setup_departments(cfg, cfg["company_name"])
    setup_designations(cfg)
    setup_warehouses(cfg)

    print("\n── Items ─────────────────────────────────────")
    create_items(cfg)

    print("\n── Customers & Suppliers ─────────────────────")
    create_customers(cfg)
    create_suppliers(cfg)

    print("\n── Employees ─────────────────────────────────")
    emp_map = create_employees(cfg)
    create_salary_structures(cfg, emp_map)

    # Transactions: more for large
    is_large = len(cfg["employees"]) > 10
    pi_count = 30 if is_large else 10
    si_count = 50 if is_large else 15

    print("\n── Transactions ──────────────────────────────")
    create_purchase_invoices(cfg, pi_count)
    create_sales_invoices(cfg, si_count)

    frappe.db.commit()
    print(f"\n  ✓  {cfg['company_name']} setup complete!\n")


def ensure_prerequisites():
    # Warehouse Types
    for wt in ["Stores", "Transit", "Manufacturing", "Fixed Asset"]:
        if not frappe.db.exists("Warehouse Type", wt):
            frappe.get_doc({"doctype": "Warehouse Type", "name": wt}).insert(ignore_permissions=True)

    # Root Territory
    if not frappe.db.exists("Territory", "All Territories"):
        frappe.get_doc({
            "doctype": "Territory",
            "territory_name": "All Territories",
            "is_group": 1,
        }).insert(ignore_permissions=True)

    # Root Customer Group
    if not frappe.db.exists("Customer Group", "All Customer Groups"):
        frappe.get_doc({
            "doctype": "Customer Group",
            "customer_group_name": "All Customer Groups",
            "is_group": 1,
        }).insert(ignore_permissions=True)

    # Root Supplier Group
    if not frappe.db.exists("Supplier Group", "All Supplier Groups"):
        frappe.get_doc({
            "doctype": "Supplier Group",
            "supplier_group_name": "All Supplier Groups",
            "is_group": 1,
        }).insert(ignore_permissions=True)

    # Root Item Group
    if not frappe.db.exists("Item Group", "All Item Groups"):
        frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": "All Item Groups",
            "is_group": 1,
        }).insert(ignore_permissions=True)

    # Price Lists
    for pl_name, buying, selling in [("Standard Selling", 0, 1), ("Standard Buying", 1, 0)]:
        if not frappe.db.exists("Price List", pl_name):
            frappe.get_doc({
                "doctype": "Price List",
                "price_list_name": pl_name,
                "currency": "UZS",
                "buying": buying,
                "selling": selling,
                "enabled": 1,
            }).insert(ignore_permissions=True)

    frappe.db.commit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", choices=["small", "large", "both"], default="both")
    args = parser.parse_args()

    frappe.init(site=SITE, sites_path=SITES_PATH)
    frappe.connect()
    frappe.set_user("Administrator")

    try:
        ensure_prerequisites()
        if args.company in ("small", "both"):
            setup_company(SMALL, "Small Company")
        if args.company in ("large", "both"):
            setup_company(LARGE, "Large Company")
        frappe.db.commit()
        print("=" * 55)
        print("  Demo data setup complete!")
        print("  Login: http://localhost:8080  admin / admin")
        print("=" * 55)
    except Exception:
        frappe.db.rollback()
        raise
    finally:
        frappe.destroy()


if __name__ == "__main__":
    main()
