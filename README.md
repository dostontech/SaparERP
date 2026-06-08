<div align="center">
  <h1>SaparERP</h1>
  <p>O'zbekiston uchun moslashtirilgan ERP tizimi — Frappe / ERPNext asosida</p>
  <p>
    <img src="https://img.shields.io/badge/ERPNext-v16-blue" alt="ERPNext v16" />
    <img src="https://img.shields.io/badge/Frappe-v16-green" alt="Frappe v16" />
    <img src="https://img.shields.io/badge/HRMS-v16-orange" alt="HRMS v16" />
    <img src="https://img.shields.io/badge/Docker-ready-2496ED" alt="Docker" />
    <img src="https://img.shields.io/badge/Lang-UZ%20%7C%20RU%20%7C%20EN-yellow" alt="Languages" />
  </p>
</div>

---

## Nima bu?

**SaparERP** — bu ERPNext va Frappe HR platformalari asosida O'zbekiston uchun maxsus sozlangan ERP tizimi.

### Asosiy imkoniyatlar

| Xususiyat | Tavsif |
|---|---|
| **O'zbek tili** | To'liq UZ interfeysi (463+ tarjima) |
| **Rus tili** | To'liq RU interfeysi (16 000+ tarjima PO fayllaridan) |
| **Til almashtirgich** | Navbar'da EN / O'Z / RU tugmalar |
| **SaparERP brendingi** | ERPNext → SaparERP, Frappe HR → Sapar HR |
| **Tarjima muharriri** | Jamoa uchun inline tarjima sahifasi |
| **Demo ma'lumotlar** | Kichik va yirik kompaniya uchun tayyor test data |
| **Docker Compose** | Lokal va Railway cloud deployment |

---

## Tez boshlash (Local)

### Talablar

- Docker Desktop (Windows/Mac) yoki Docker Engine (Linux)
- 8 GB RAM (minimum), 16 GB tavsiya etiladi
- 20 GB bo'sh disk

### 1. Repo'ni klonlash

```bash
git clone https://github.com/dostontech/SaparERP.git
cd SaparERP
```

### 2. Asosiy obrazni qurish

```bash
# Birinchi marta: asosiy obraz (frappe + erpnext + hrms)
docker build \
  --build-arg=FRAPPE_PATH=https://github.com/frappe/frappe \
  --build-arg=FRAPPE_BRANCH=version-16 \
  --build-arg=APPS_JSON_BASE64=$(base64 -w 0 apps-uz.json) \
  --tag=erpnext-uz:latest \
  --file=images/layered/Dockerfile .
```

> Bu jarayon 20-30 daqiqa oladi. Faqat bir marta bajarish kerak.

### 3. SaparERP obrazini qurish

```bash
docker build -f Dockerfile.uz -t erpnext-uz-fixed:latest .
```

### 4. Stackni ishga tushirish

```bash
docker compose -f compose-uz.yml up
```

### 5. Brauzerda ochish

```
http://localhost:8080
Login: Administrator / admin
```

---

## Demo ma'lumotlarini yuklash

Stack ishga tushgandan keyin (birinchi marta ~10-15 daqiqa):

```bash
# Ikkala kompaniya uchun
docker compose -f compose-uz.yml exec backend bash -c \
  "cd /home/frappe/frappe-bench/sites && \
   /home/frappe/frappe-bench/env/bin/python /home/frappe/setup_demo_data.py --company both"
```

```bash
# Faqat kichik kompaniya
docker compose -f compose-uz.yml exec backend bash -c \
  "cd /home/frappe/frappe-bench/sites && \
   /home/frappe/frappe-bench/env/bin/python /home/frappe/setup_demo_data.py --company small"

# Faqat yirik kompaniya
docker compose -f compose-uz.yml exec backend bash -c \
  "cd /home/frappe/frappe-bench/sites && \
   /home/frappe/frappe-bench/env/bin/python /home/frappe/setup_demo_data.py --company large"
```

### Demo kompaniyalar

#### Nur Savdo MChJ — Kichik biznes
- 5 xodim (direktor, buxgalter, sotuvchilar, omborchi)
- 8 mijoz, 5 ta'minotchi
- 10 mahsulot (kiyim-kechak va aksessuarlar)
- 1 ombor
- ~25 hujjat (xarid + sotuv fakturalari)

#### Sapar Holding AJ — Yirik korporatsiya
- 33 xodim, 7 bo'lim (Boshqaruv, Moliya, Sotish, IT, HR, Xarid, Ombor)
- 20 mijoz, 15 ta'minotchi
- 25 mahsulot (elektronika va mebel)
- 3 ombor (Toshkent, Samarqand, Namangan)
- ~80 hujjat

---

## Tarjima muharriri

Jamoa uchun inline tarjima sahifasi ikki xil usulda ochiladi:

**1. Desk sahifasi:**
```
http://localhost:8080/desk#sapar-translate
```

**2. Alohida sahifa (tavsiya etiladi):**
```
http://localhost:8080/assets/frappe/html/sapar-translate.html
```

**Imkoniyatlar:**
- Til tanlash: UZ / RU / EN
- Filter: Hammasi / Tarjima qilinmaganlar / Tarjima qilinganlar
- Qidiruv
- Inline tahrirlash (qatorni bosing va yozing)
- Ommaviy saqlash
- Yangi tarjima qo'shish
- O'chirish

---

## Railway'ga joylash (bepul 30 kun)

### 1. Docker Hub'ga obrazni push qilish

```bash
docker login
docker tag erpnext-uz-fixed:latest dostontech/saparerp:latest
docker push dostontech/saparerp:latest
```

### 2. Railway'da sozlash

1. [railway.app](https://railway.app) → GitHub bilan kirish
2. **New Project** → **Deploy from GitHub repo** → `SaparERP`
3. Compose fayl: `compose.railway.yml`
4. Environment variables:

| O'zgaruvchi | Qiymat |
|---|---|
| `SAPAR_IMAGE` | `dostontech/saparerp:latest` |
| `DB_ROOT_PASSWORD` | `SaparDemo2024!` |
| `ADMIN_PASSWORD` | `admin` |

Batafsil ko'rsatmalar: [DEPLOY.md](DEPLOY.md)

---

## Fayl tuzilmasi

```
SaparERP/
├── Dockerfile.uz              # SaparERP maxsus obrazi
├── compose-uz.yml             # Lokal ishlab chiqish stacki
├── compose.railway.yml        # Railway cloud deployment
├── apps-uz.json               # O'rnatiladigan ilovalar ro'yxati
│
├── setup_uz.py                # Sayt sozlamalari (kompaniya, valyuta)
├── setup_uz_lang.py           # Til, tarjimalar, brendlash, ish stoli
├── setup_demo_data.py         # Test ma'lumotlar (2 kompaniya)
│
├── sapar_lang_switch.js       # EN/O'Z/RU til almashtirgich
├── sapar_translate.html       # Tarjima muharriri (standalone HTML)
├── sapar_translate_page.js    # Tarjima muharriri (desk sahifasi JS)
├── sapar_translate_page.py    # Tarjima muharriri (API metodlar)
│
└── DEPLOY.md                  # Deployment ko'rsatmalar
```

---

## Qayta tiklash

```bash
# Hamma ma'lumotlarni o'chirish va qaytadan boshlash
docker compose -f compose-uz.yml down -v
docker compose -f compose-uz.yml up
```

---

## Texnik ma'lumotlar

| Komponent | Versiya |
|---|---|
| Frappe Framework | v16.20.0 |
| ERPNext | v16.21.1 |
| Frappe HRMS | v16.8.0 |
| MariaDB | 11.8 |
| Redis | 6.2 |
| Python | 3.14 |
| Node.js | 22 |

---

## Litsenziya

Ushbu loyiha [MIT litsenziyasi](LICENSE) ostida tarqatiladi.  
Asosiy [frappe/frappe_docker](https://github.com/frappe/frappe_docker) loyihasiga asoslangan.

---

<div align="center">
  <p>SaparERP — O'zbekiston biznes tizimi</p>
</div>
