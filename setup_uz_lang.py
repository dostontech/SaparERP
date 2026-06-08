#!/usr/bin/env python3
"""
Uzbek branding + translation setup for SaparERP.
Run inside bench container:
  /home/frappe/frappe-bench/env/bin/python /home/frappe/setup_uz_lang.py
"""
import os
import sys

os.chdir("/home/frappe/frappe-bench/sites")
sys.path.insert(0, "/home/frappe/frappe-bench/apps/frappe")

import frappe

SITE = "frontend"
SITES_PATH = "/home/frappe/frappe-bench/sites"

# ── Comprehensive Uzbek translations ──────────────────────────────────────────
# Format: (source_text, translated_text)
UZ_TRANSLATIONS = [
    # Actions
    ("Save", "Saqlash"),
    ("Submit", "Tasdiqlash"),
    ("Cancel", "Bekor qilish"),
    ("Delete", "O'chirish"),
    ("Add", "Qo'shish"),
    ("Edit", "Tahrirlash"),
    ("Update", "Yangilash"),
    ("Create", "Yaratish"),
    ("New", "Yangi"),
    ("Close", "Yopish"),
    ("Back", "Orqaga"),
    ("Next", "Keyingisi"),
    ("Previous", "Oldingi"),
    ("Search", "Qidirish"),
    ("Filter", "Filtr"),
    ("Apply", "Qo'llash"),
    ("Clear", "Tozalash"),
    ("Reset", "Qayta o'rnatish"),
    ("Refresh", "Yangilash"),
    ("Print", "Chop etish"),
    ("Download", "Yuklab olish"),
    ("Upload", "Yuklash"),
    ("Import", "Import"),
    ("Export", "Eksport"),
    ("Copy", "Nusxa"),
    ("Duplicate", "Nusxalash"),
    ("Rename", "Qayta nomlash"),
    ("Merge", "Birlashtirish"),
    ("Confirm", "Tasdiqlash"),
    ("OK", "OK"),
    ("Done", "Tayyor"),
    ("Finish", "Tugatish"),
    ("Continue", "Davom etish"),
    ("Skip", "O'tkazib yuborish"),
    ("Share", "Ulashish"),
    ("Assign", "Tayinlash"),
    ("Amend", "Tuzatish"),
    ("Discard", "Bekor qilish"),
    ("Archive", "Arxivlash"),
    ("Restore", "Tiklash"),
    ("Send", "Yuborish"),
    ("Reply", "Javob berish"),
    ("Forward", "Yo'naltirish"),
    ("Attach", "Biriktirish"),
    ("Remove", "Olib tashlash"),
    ("Set", "O'rnatish"),
    ("Get", "Olish"),
    ("Go", "O'tish"),
    ("Open", "Ochish"),
    ("View", "Ko'rish"),
    ("Expand", "Kengaytirish"),
    ("Collapse", "Yig'ish"),
    ("Select", "Tanlash"),
    ("Deselect", "Tanlovni bekor qilish"),
    ("Check", "Belgilash"),
    ("Uncheck", "Belgini olib tashlash"),
    ("Enable", "Yoqish"),
    ("Disable", "O'chirish"),
    ("Activate", "Faollashtirish"),
    ("Deactivate", "Faolsizlashtirish"),
    ("Lock", "Qulflash"),
    ("Unlock", "Qulfni ochish"),

    # Navigation / Layout
    ("Home", "Bosh sahifa"),
    ("Dashboard", "Boshqaruv paneli"),
    ("Settings", "Sozlamalar"),
    ("Profile", "Profil"),
    ("Logout", "Chiqish"),
    ("Login", "Kirish"),
    ("Help", "Yordam"),
    ("About", "Haqida"),
    ("Reports", "Hisobotlar"),
    ("Report", "Hisobot"),
    ("List", "Ro'yxat"),
    ("Form", "Forma"),
    ("Table", "Jadval"),
    ("Chart", "Grafik"),
    ("Calendar", "Taqvim"),
    ("Map", "Xarita"),
    ("Kanban", "Kanban"),
    ("Gallery", "Galereya"),
    ("Tree", "Daraxt"),
    ("Details", "Tafsilotlar"),
    ("Summary", "Qisqacha"),
    ("Overview", "Umumiy ko'rinish"),
    ("Timeline", "Vaqt chizig'i"),
    ("Activity", "Faoliyat"),
    ("Log", "Jurnal"),
    ("History", "Tarix"),
    ("Attachments", "Qo'shimchalar"),
    ("Comments", "Izohlar"),
    ("Notes", "Eslatmalar"),
    ("Notifications", "Bildirishnomalar"),
    ("Bookmarks", "Xatcholar"),
    ("Shortcuts", "Yorliqlar"),
    ("Workspace", "Ish maydoni"),
    ("Modules", "Modullar"),
    ("Apps", "Ilovalar"),
    ("Tools", "Asboblar"),

    # Status
    ("Draft", "Qoralama"),
    ("Submitted", "Tasdiqlangan"),
    ("Cancelled", "Bekor qilingan"),
    ("Pending", "Kutilmoqda"),
    ("Approved", "Tasdiqlangan"),
    ("Rejected", "Rad etilgan"),
    ("Active", "Faol"),
    ("Inactive", "Faol emas"),
    ("Enabled", "Yoqilgan"),
    ("Disabled", "O'chirilgan"),
    ("Open", "Ochiq"),
    ("Closed", "Yopilgan"),
    ("Completed", "Tugallangan"),
    ("In Progress", "Bajarilmoqda"),
    ("Overdue", "Muddati o'tgan"),
    ("On Hold", "To'xtatilgan"),
    ("Partially Paid", "Qisman to'langan"),
    ("Paid", "To'langan"),
    ("Unpaid", "To'lanmagan"),
    ("Return", "Qaytarish"),
    ("Debit", "Debet"),
    ("Credit", "Kredit"),
    ("Yes", "Ha"),
    ("No", "Yo'q"),
    ("True", "To'g'ri"),
    ("False", "Noto'g'ri"),
    ("None", "Yo'q"),

    # Fields / Data
    ("Name", "Nomi"),
    ("Title", "Sarlavha"),
    ("Description", "Tavsif"),
    ("Date", "Sana"),
    ("Time", "Vaqt"),
    ("From Date", "Boshlanish sanasi"),
    ("To Date", "Tugash sanasi"),
    ("Start Date", "Boshlanish sanasi"),
    ("End Date", "Tugash sanasi"),
    ("Due Date", "Muddat sanasi"),
    ("Posting Date", "Kiritish sanasi"),
    ("Created On", "Yaratilgan"),
    ("Modified On", "O'zgartirilgan"),
    ("Created By", "Yaratuvchi"),
    ("Modified By", "O'zgartiruvchi"),
    ("Amount", "Miqdor"),
    ("Total Amount", "Jami miqdor"),
    ("Grand Total", "Umumiy jami"),
    ("Net Total", "Sof jami"),
    ("Total", "Jami"),
    ("Subtotal", "Oraliq jami"),
    ("Quantity", "Miqdori"),
    ("Rate", "Narx"),
    ("Price", "Narx"),
    ("Unit Price", "Birlik narxi"),
    ("Discount", "Chegirma"),
    ("Discount %", "Chegirma %"),
    ("Tax", "Soliq"),
    ("Tax Amount", "Soliq miqdori"),
    ("Tax Rate", "Soliq stavkasi"),
    ("Currency", "Valyuta"),
    ("Exchange Rate", "Almashuv kursi"),
    ("Balance", "Qoldiq"),
    ("Outstanding Amount", "To'lanmagan miqdor"),
    ("Paid Amount", "To'langan miqdor"),
    ("Remarks", "Izohlar"),
    ("Reference", "Havola"),
    ("Reference No", "Havola raqami"),
    ("Reference Date", "Havola sanasi"),
    ("Serial No", "Seriya raqami"),
    ("Batch No", "Partiya raqami"),
    ("UOM", "O'lchov birligi"),
    ("Unit of Measure", "O'lchov birligi"),
    ("Address", "Manzil"),
    ("Phone", "Telefon"),
    ("Mobile", "Mobil"),
    ("Email", "Elektron pochta"),
    ("Website", "Veb-sayt"),
    ("Country", "Davlat"),
    ("City", "Shahar"),
    ("State", "Viloyat"),
    ("Postal Code", "Pochta indeksi"),
    ("Territory", "Hudud"),
    ("Type", "Tur"),
    ("Category", "Kategoriya"),
    ("Group", "Guruh"),
    ("Code", "Kod"),
    ("Number", "Raqam"),
    ("ID", "ID"),
    ("Owner", "Egasi"),
    ("Assigned To", "Tayinlangan"),
    ("Priority", "Muhimlik"),
    ("Image", "Rasm"),
    ("Document", "Hujjat"),
    ("File", "Fayl"),
    ("Folder", "Papka"),
    ("Tag", "Teg"),
    ("Color", "Rang"),
    ("Size", "Hajm"),
    ("Weight", "Og'irlik"),

    # ERPNext Modules
    ("Accounts", "Buxgalteriya"),
    ("Accounting", "Buxgalteriya"),
    ("Human Resources", "Kadrlar bo'limi"),
    ("HR", "Kadrlar"),
    ("Payroll", "Ish haqi"),
    ("Stock", "Ombor"),
    ("Inventory", "Inventarizatsiya"),
    ("Purchase", "Xarid"),
    ("Buying", "Xarid qilish"),
    ("Sales", "Sotish"),
    ("Selling", "Sotish"),
    ("Manufacturing", "Ishlab chiqarish"),
    ("Projects", "Loyihalar"),
    ("Assets", "Aktivlar"),
    ("CRM", "Mijozlar bilan munosabat"),
    ("Support", "Qo'llab-quvvatlash"),
    ("Quality", "Sifat"),
    ("Retail", "Chakana savdo"),
    ("Website", "Veb-sayt"),
    ("Integrations", "Integratsiyalar"),
    ("Customization", "Moslash"),
    ("Setup", "Sozlash"),
    ("Core", "Asosiy"),
    ("Desk", "Ish stoli"),
    ("Email", "Elektron pochta"),

    # ERPNext Core Doctypes
    ("Customer", "Mijoz"),
    ("Customers", "Mijozlar"),
    ("Supplier", "Ta'minotchi"),
    ("Suppliers", "Ta'minotchilar"),
    ("Employee", "Xodim"),
    ("Employees", "Xodimlar"),
    ("Item", "Mahsulot"),
    ("Items", "Mahsulotlar"),
    ("Company", "Kompaniya"),
    ("Companies", "Kompaniyalar"),
    ("Department", "Bo'lim"),
    ("Departments", "Bo'limlar"),
    ("Designation", "Lavozim"),
    ("Branch", "Filial"),
    ("Territory", "Hudud"),
    ("Warehouse", "Ombor"),
    ("Warehouses", "Omborlar"),
    ("Account", "Hisob"),
    ("Cost Center", "Xarajat markazi"),
    ("Project", "Loyiha"),
    ("Task", "Vazifa"),
    ("Lead", "Potensial mijoz"),
    ("Opportunity", "Imkoniyat"),
    ("Contact", "Kontakt"),
    ("Address", "Manzil"),
    ("User", "Foydalanuvchi"),
    ("Users", "Foydalanuvchilar"),
    ("Role", "Rol"),
    ("Permission", "Ruxsat"),
    ("Workflow", "Ish jarayoni"),
    ("Print Format", "Chop etish formati"),
    ("Email Template", "Elektron pochta shabloni"),
    ("Custom Field", "Maxsus maydon"),
    ("Custom Script", "Maxsus skript"),

    # Accounting Doctypes
    ("Sales Invoice", "Sotish hisob-fakturasi"),
    ("Purchase Invoice", "Xarid hisob-fakturasi"),
    ("Payment Entry", "To'lov"),
    ("Journal Entry", "Jurnal yozuvi"),
    ("Sales Order", "Sotish buyurtmasi"),
    ("Purchase Order", "Xarid buyurtmasi"),
    ("Delivery Note", "Yetkazib berish xati"),
    ("Purchase Receipt", "Xarid kvitansiyasi"),
    ("Quotation", "Taklif"),
    ("Expense Claim", "Xarajat talabi"),
    ("Budget", "Byudjet"),
    ("Bank Account", "Bank hisobi"),
    ("Bank Statement", "Bank ko'chirmasi"),
    ("Bank Reconciliation", "Bank yarashtirish"),
    ("Payment Request", "To'lov talabi"),
    ("Payment Schedule", "To'lov jadvali"),
    ("Payment Term", "To'lov muddati"),
    ("Price List", "Narxlar ro'yxati"),
    ("Tax Rule", "Soliq qoidasi"),
    ("Fiscal Year", "Moliya yili"),
    ("Period Closing Voucher", "Davr yopish vaucheri"),
    ("Chart of Accounts", "Hisoblar rejasi"),
    ("GL Entry", "Bosh kitob yozuvi"),
    ("Stock Ledger Entry", "Ombor kitobi yozuvi"),
    ("Balance Sheet", "Balans hisoboti"),
    ("Profit and Loss Statement", "Daromad va zararlar hisoboti"),
    ("Trial Balance", "Umumiy balans"),
    ("Cash Flow Statement", "Pul oqimi hisoboti"),

    # HR & Payroll Doctypes
    ("Salary Slip", "Ish haqi varaqasi"),
    ("Salary Structure", "Ish haqi strukturasi"),
    ("Salary Component", "Ish haqi komponenti"),
    ("Salary Structure Assignment", "Ish haqi strukturasi tayinlash"),
    ("Leave Application", "Ta'til arizasi"),
    ("Leave Type", "Ta'til turi"),
    ("Leave Allocation", "Ta'til taqsimlash"),
    ("Leave Balance", "Ta'til qoldig'i"),
    ("Leave Policy", "Ta'til siyosati"),
    ("Attendance", "Davomat"),
    ("Attendance Request", "Davomat talabi"),
    ("Shift Type", "Smenа turi"),
    ("Employee Checkin", "Xodim kirish vaqti"),
    ("Appraisal", "Baholash"),
    ("Training Program", "O'quv dasturi"),
    ("Training Event", "O'quv tadbiri"),
    ("Job Opening", "Bo'sh ish o'rni"),
    ("Job Applicant", "Nomzod"),
    ("Offer Letter", "Taklif xati"),
    ("Employee Grade", "Xodim darajasi"),
    ("Employee Group", "Xodimlar guruhi"),
    ("Employee Transfer", "Xodimni ko'chirish"),
    ("Employee Promotion", "Xodimni lavozimga ko'tarish"),
    ("Loan", "Qarz"),
    ("Loan Application", "Qarz arizasi"),
    ("Provident Fund", "Pensiya jamg'arma"),
    ("Gratuity", "Mukofot"),
    ("Employee Benefit Application", "Xodim imtiyozlari arizasi"),

    # Stock Doctypes
    ("Stock Entry", "Ombor harakati"),
    ("Material Request", "Mahsulot talabi"),
    ("Item Group", "Mahsulot guruhi"),
    ("Item Category", "Mahsulot kategoriyasi"),
    ("Item Variant", "Mahsulot varianti"),
    ("Stock Reconciliation", "Ombor yarashtirish"),
    ("Delivery Trip", "Yetkazib berish sayohati"),
    ("Packing Slip", "Qadoqlash varaqasi"),
    ("Quality Inspection", "Sifat tekshiruvi"),
    ("Batch", "Partiya"),
    ("Serial No", "Seriya raqami"),
    ("Stock Balance", "Ombor qoldig'i"),
    ("Valuation Rate", "Baholash stavkasi"),

    # Messages / Notifications
    ("Loading...", "Yuklanmoqda..."),
    ("Please wait...", "Iltimos, kuting..."),
    ("No data found", "Ma'lumot topilmadi"),
    ("Record not found", "Yozuv topilmadi"),
    ("Successfully saved", "Muvaffaqiyatli saqlandi"),
    ("Successfully submitted", "Muvaffaqiyatli tasdiqlandi"),
    ("Successfully cancelled", "Muvaffaqiyatli bekor qilindi"),
    ("Successfully deleted", "Muvaffaqiyatli o'chirildi"),
    ("Are you sure?", "Ishonchingiz komilmi?"),
    ("This action cannot be undone", "Bu amalni bekor qilib bo'lmaydi"),
    ("Required fields are missing", "Majburiy maydonlar to'ldirilmagan"),
    ("Invalid value", "Noto'g'ri qiymat"),
    ("Duplicate entry", "Takroriy yozuv"),
    ("Permission denied", "Ruxsat berilmagan"),
    ("Not authorized", "Avtorizatsiya qilinmagan"),
    ("Session expired", "Sessiya muddati tugadi"),
    ("Connection error", "Ulanish xatosi"),
    ("Server error", "Server xatosi"),
    ("Validation error", "Tekshiruv xatosi"),
    ("Changes saved", "O'zgarishlar saqlandi"),
    ("Unsaved changes", "Saqlanmagan o'zgarishlar"),
    ("Do you want to save changes?", "O'zgarishlarni saqlashni xohlaysizmi?"),
    ("Document has been saved", "Hujjat saqlandi"),
    ("Document has been submitted", "Hujjat tasdiqlandi"),
    ("Document has been cancelled", "Hujjat bekor qilindi"),
    ("Document has been deleted", "Hujjat o'chirildi"),
    ("Select a row first", "Avval qatorni tanlang"),
    ("No rows selected", "Hech qanday qator tanlanmagan"),
    ("Add Row", "Qator qo'shish"),
    ("Delete Row", "Qatorni o'chirish"),
    ("Move Up", "Yuqoriga ko'chirish"),
    ("Move Down", "Pastga ko'chirish"),
    ("Bulk Edit", "Ko'plab tahrirlash"),
    ("Bulk Delete", "Ko'plab o'chirish"),
    ("Bulk Submit", "Ko'plab tasdiqlash"),

    # Company / Finance
    ("Fiscal Year", "Moliya yili"),
    ("Accounting Year", "Buxgalteriya yili"),
    ("Opening Balance", "Kirish qoldig'i"),
    ("Closing Balance", "Yopish qoldig'i"),
    ("Debit", "Debet"),
    ("Credit", "Kredit"),
    ("Net", "Sof"),
    ("Gross", "Yalpi"),
    ("VAT", "QQS"),
    ("GST", "GST"),
    ("Income Tax", "Daromad solig'i"),
    ("Withholding Tax", "Manba solig'i"),
    ("Asset", "Aktiv"),
    ("Liability", "Majburiyat"),
    ("Equity", "Kapital"),
    ("Revenue", "Daromad"),
    ("Expense", "Xarajat"),
    ("Profit", "Foyda"),
    ("Loss", "Zarar"),
    ("Cash", "Naqd pul"),
    ("Bank", "Bank"),
    ("Receivable", "Debitorlik"),
    ("Payable", "Kreditorlik"),
    ("Fixed Asset", "Asosiy vosita"),
    ("Depreciation", "Amortizatsiya"),
    ("Write Off", "Hisobdan chiqarish"),
    ("Provision", "Zaxira"),
    ("Accrual", "Hisoblash"),

    # Uzbekistan specific
    ("INN", "INN"),
    ("PINFL", "PINFL"),
    ("INPS Account", "INPS hisobi"),
    ("Tax Resident", "Soliq rezidenti"),
    ("Basic Salary UZ", "Asosiy ish haqi (O'z)"),
    ("INPS Pension UZ", "INPS pensiya (O'z)"),
    ("Personal Income Tax UZ", "JSHIR (O'z)"),
    ("UST Employer UZ", "YaST (O'z)"),
    ("PIT Payable", "JSHIR to'lash"),
    ("UST Payable", "YaST to'lash"),
    ("INPS Payable", "INPS to'lash"),
    ("Salaries Payable", "Ish haqi to'lash"),

    # Login / Auth
    ("Sign In", "Kirish"),
    ("Sign Out", "Chiqish"),
    ("Sign Up", "Ro'yxatdan o'tish"),
    ("Register", "Ro'yxatdan o'tish"),
    ("Forgot Password?", "Parolni unutdingizmi?"),
    ("Reset Password", "Parolni tiklash"),
    ("Change Password", "Parolni o'zgartirish"),
    ("New Password", "Yangi parol"),
    ("Confirm Password", "Parolni tasdiqlash"),
    ("Current Password", "Joriy parol"),
    ("Remember Me", "Eslab qolish"),
    ("Two Factor Authentication", "Ikki faktorli autentifikatsiya"),

    # Time
    ("Today", "Bugun"),
    ("Yesterday", "Kecha"),
    ("Tomorrow", "Ertaga"),
    ("This Week", "Bu hafta"),
    ("Last Week", "O'tgan hafta"),
    ("This Month", "Bu oy"),
    ("Last Month", "O'tgan oy"),
    ("This Quarter", "Bu chorak"),
    ("This Year", "Bu yil"),
    ("Last Year", "O'tgan yil"),
    ("January", "Yanvar"),
    ("February", "Fevral"),
    ("March", "Mart"),
    ("April", "Aprel"),
    ("May", "May"),
    ("June", "Iyun"),
    ("July", "Iyul"),
    ("August", "Avgust"),
    ("September", "Sentabr"),
    ("October", "Oktabr"),
    ("November", "Noyabr"),
    ("December", "Dekabr"),
    ("Monday", "Dushanba"),
    ("Tuesday", "Seshanba"),
    ("Wednesday", "Chorshanba"),
    ("Thursday", "Payshanba"),
    ("Friday", "Juma"),
    ("Saturday", "Shanba"),
    ("Sunday", "Yakshanba"),
    ("Hour", "Soat"),
    ("Hours", "Soat"),
    ("Minute", "Daqiqa"),
    ("Minutes", "Daqiqa"),
    ("Second", "Soniya"),
    ("Day", "Kun"),
    ("Days", "Kun"),
    ("Week", "Hafta"),
    ("Month", "Oy"),
    ("Quarter", "Chorak"),
    ("Year", "Yil"),

    # Numbers
    ("Zero", "Nol"),
    ("First", "Birinchi"),
    ("Second", "Ikkinchi"),
    ("Third", "Uchinchi"),
    ("Total", "Jami"),
    ("Count", "Soni"),
    ("Percentage", "Foiz"),
    ("Average", "O'rtacha"),
    ("Maximum", "Maksimal"),
    ("Minimum", "Minimal"),

    # Sapar rebranding — rename ERPNext strings to SaparERP
    ("ERPNext Settings", "SaparERP Sozlamalari"),
    ("ERPNext", "SaparERP"),

    # App name overrides
    ("Frappe HR", "Sapar HR"),
]

# English overrides — rename ERPNext → SaparERP and Frappe HR → Sapar HR
EN_OVERRIDES = [
    ("ERPNext Settings", "SaparERP Settings"),
    ("ERPNext", "SaparERP"),
    ("Frappe HR", "Sapar HR"),
]


def main():
    frappe.init(site=SITE, sites_path=SITES_PATH)
    frappe.connect()
    print("=== Sapar Rebranding + Uzbek Language Setup ===\n")
    try:
        rebrand_to_sapar()
        setup_languages()
        import_translations()
        import_russian_translations()
        rename_workspaces()
        fix_desktop_icons()
        setup_translation_page()
        frappe.db.commit()
        print("\n==========================================")
        print("Done. Restart the backend to apply changes:")
        print("  docker compose -f compose-uz.yml restart backend")
    finally:
        frappe.destroy()


def rebrand_to_sapar():
    print("── Rebranding to SaparERP ───────────────")
    changes = [
        ("System Settings", "app_name", "SaparERP"),
        ("Website Settings", "app_name", "SaparERP"),
        ("Website Settings", "title_prefix", "SaparERP"),
        ("Website Settings", "copyright", "SaparERP"),
    ]
    for doctype, field, value in changes:
        frappe.db.set_single_value(doctype, field, value)
        print(f"  OK  {doctype}.{field} = '{value}'")

    # Replace any remaining "ERPNext" text in website footer
    current_footer = frappe.db.get_single_value("Website Settings", "footer_items") or ""
    if "ERPNext" in current_footer:
        frappe.db.set_single_value("Website Settings", "footer_items",
                                   current_footer.replace("ERPNext", "SaparERP"))
        print("  OK  Website Settings.footer_items — ERPNext replaced")


def setup_languages():
    print("\n── Languages (EN / UZ / RU) ─────────────")
    langs = [
        ("en", "English"),
        ("uz", "O'zbekcha"),
        ("ru", "Русский"),
    ]
    for code, name in langs:
        if not frappe.db.exists("Language", code):
            frappe.get_doc({
                "doctype": "Language",
                "name": code,
                "language_name": name,
                "enabled": 1,
            }).insert(ignore_permissions=True)
            print(f"  OK  Language '{code}' ({name}) created")
        else:
            frappe.db.set_value("Language", code, {"enabled": 1, "language_name": name})
            print(f"  OK  Language '{code}' ({name}) enabled")


def import_russian_translations():
    import os, datetime
    print("\n── Russian Translations (from PO files) ─")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    po_files = []
    for app in ["frappe", "erpnext", "hrms"]:
        p = f"/home/frappe/frappe-bench/apps/{app}/{app}/locale/ru.po"
        if os.path.exists(p):
            po_files.append(p)

    if not po_files:
        print("  SKIP  No ru.po files found")
        return

    total_ins = 0
    total_skip = 0
    for po_path in po_files:
        try:
            with open(po_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Parse PO format: msgid / msgstr pairs
            import re
            pairs = re.findall(
                r'msgid\s+"((?:[^"\\]|\\.)*)"\s+msgstr\s+"((?:[^"\\]|\\.)*)"',
                content)
            for src, tgt in pairs:
                src = src.replace('\\n', '\n').replace('\\"', '"')
                tgt = tgt.replace('\\n', '\n').replace('\\"', '"')
                if not src or not tgt or src == tgt:
                    continue
                exists = frappe.db.sql(
                    "SELECT name FROM tabTranslation WHERE language='ru' AND source_text=%s",
                    (src,), as_list=True)
                if not exists:
                    frappe.db.sql("""INSERT INTO tabTranslation
                        (name,creation,modified,modified_by,owner,docstatus,idx,
                         language,source_text,translated_text)
                        VALUES (UUID(),%s,%s,'Administrator','Administrator',0,0,'ru',%s,%s)""",
                        (now, now, src, tgt))
                    total_ins += 1
                else:
                    total_skip += 1
            print(f"  OK  {po_path} processed")
        except Exception as e:
            print(f"  ERR {po_path}: {e}")

    frappe.db.commit()
    print(f"  OK  {total_ins} inserted, {total_skip} already exist")


def import_translations():
    print("\n── Uzbek Translations ───────────────────")
    lang = "uz"
    inserted = 0
    updated = 0
    skipped = 0

    for source, target in UZ_TRANSLATIONS:
        existing = frappe.db.sql(
            "SELECT name FROM `tabTranslation` WHERE language=%s AND source_text=%s",
            (lang, source), as_list=True
        )
        if existing:
            frappe.db.sql(
                "UPDATE `tabTranslation` SET translated_text=%s, modified=NOW() "
                "WHERE language=%s AND source_text=%s",
                (target, lang, source)
            )
            updated += 1
        else:
            frappe.db.sql("""
                INSERT INTO `tabTranslation`
                  (name, creation, modified, modified_by, owner, docstatus, idx,
                   language, source_text, translated_text)
                VALUES (UUID(), NOW(), NOW(), 'Administrator', 'Administrator',
                        0, 0, %s, %s, %s)
            """, (lang, source, target))
            inserted += 1

    print(f"  OK  {inserted} inserted, {updated} updated, {skipped} skipped")
    print(f"      Total uz translations: {len(UZ_TRANSLATIONS)}")

    # English overrides (rename ERPNext → SaparERP in English UI)
    en_ins = 0
    for source, target in EN_OVERRIDES:
        existing = frappe.db.sql(
            "SELECT name FROM `tabTranslation` WHERE language='en' AND source_text=%s",
            (source,), as_list=True
        )
        if existing:
            frappe.db.sql(
                "UPDATE `tabTranslation` SET translated_text=%s, modified=NOW() "
                "WHERE language='en' AND source_text=%s",
                (target, source)
            )
        else:
            frappe.db.sql("""
                INSERT INTO `tabTranslation`
                  (name, creation, modified, modified_by, owner, docstatus, idx,
                   language, source_text, translated_text)
                VALUES (UUID(), NOW(), NOW(), 'Administrator', 'Administrator',
                        0, 0, 'en', %s, %s)
            """, (source, target))
            en_ins += 1
    print(f"  OK  {en_ins} English overrides applied")


def fix_desktop_icons():
    print("\n── Desktop Icon Fixes ───────────────────")
    # Rename erpnext app icon label from 'ERPNext' → 'SaparERP'
    frappe.db.sql(
        "UPDATE `tabDesktop Icon` SET label='SaparERP' WHERE name='ERPNext' AND icon_type='App'"
    )
    frappe.db.sql(
        "UPDATE `tabDesktop Icon` SET label='SaparERP Settings', link_to='ERPNext Settings' "
        "WHERE name='ERPNext Settings' AND icon_type='Link'"
    )
    # Fix parent_icon references: ERPNext → SaparERP
    affected = frappe.db.sql(
        "SELECT COUNT(*) FROM `tabDesktop Icon` WHERE parent_icon='ERPNext'",
        as_list=True
    )[0][0]
    frappe.db.sql(
        "UPDATE `tabDesktop Icon` SET parent_icon='SaparERP' WHERE parent_icon='ERPNext'"
    )
    print(f"  OK  {affected} child icon(s) re-parented ERPNext → SaparERP")
    # Unhide CRM and Support (visible by default in standard nav)
    for label in ['CRM', 'Support']:
        frappe.db.sql(
            "UPDATE `tabDesktop Icon` SET hidden=0 WHERE label=%s AND app='erpnext'",
            (label,)
        )
    print("  OK  CRM, Support unhidden")


def setup_translation_page():
    print("\n── Translation Tool Page ────────────────")
    page_name = "sapar-translate"
    exists = frappe.db.sql(
        "SELECT name FROM `tabPage` WHERE name=%s", (page_name,), as_list=True
    )
    if exists:
        frappe.db.sql(
            "UPDATE `tabPage` SET title='Translation Tool', icon='fa fa-language', "
            "modified=NOW() WHERE name=%s",
            (page_name,)
        )
        print(f"  OK  Page '{page_name}' updated")
    else:
        frappe.db.sql("""
            INSERT INTO `tabPage`
              (name, creation, modified, modified_by, owner, docstatus, idx,
               system_page, page_name, title, icon, module, standard)
            VALUES (%s, NOW(), NOW(), 'Administrator', 'Administrator',
                    0, 0, 0, %s, 'Translation Tool', 'fa fa-language', 'Core', 'Yes')
        """, (page_name, page_name))
        print(f"  OK  Page '{page_name}' created")


def rename_workspaces():
    print("\n── Workspace Rename ─────────────────────")
    frappe.db.sql("""
        UPDATE tabWorkspace
        SET title='SaparERP Settings', label='SaparERP Settings'
        WHERE name='ERPNext Settings'
    """)
    frappe.db.sql("""
        UPDATE `tabWorkspace Sidebar`
        SET title='SaparERP Settings'
        WHERE name='ERPNext Settings'
    """)
    print("  OK  ERPNext Settings workspace -> SaparERP Settings")


if __name__ == "__main__":
    main()
