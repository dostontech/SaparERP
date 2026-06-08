# SaparERP — Free 30-Day Demo Deployment

## Option 1: Railway (Recommended — Docker Compose support)

Railway gives $5 free credit/month — enough for a small demo.

### Steps

1. Push your repo to GitHub (private is fine):
   ```
   git init
   git add .
   git commit -m "SaparERP demo"
   gh repo create saparerp-demo --private --push --source .
   ```

2. Go to https://railway.app → New Project → Deploy from GitHub repo

3. Railway will detect `compose-uz.yml`. Set it as the compose file in settings.

4. Add these environment variables in Railway dashboard:
   ```
   DB_PASSWORD=your_secure_password
   ADMIN_PASSWORD=admin123
   ```

5. Railway gives a public URL like `https://saparerp-demo.up.railway.app`

---

## Option 2: Render (Free tier, sleeps after 15 min idle)

Not ideal for demos — services sleep. Use Railway instead.

---

## Option 3: VPS (Best — €4/month Hetzner, always on)

Best for a real showcase. Hetzner CX11 is cheapest (2GB RAM, €4/month).

### Steps

1. Create a Hetzner account → New Server → CX11 → Ubuntu 22.04

2. SSH in and install Docker:
   ```bash
   curl -fsSL https://get.docker.com | sh
   apt-get install -y docker-compose-plugin git
   ```

3. Clone your repo:
   ```bash
   git clone https://github.com/yourname/saparerp-demo.git
   cd saparerp-demo/frappe_docker
   ```

4. Build and start:
   ```bash
   docker build -f Dockerfile.uz -t erpnext-uz:latest ../erpnext-uz/ 2>/dev/null || true
   docker build -f Dockerfile.uz -t erpnext-uz-fixed:latest .
   docker compose -f compose-uz.yml up -d
   ```

5. Access at `http://YOUR_SERVER_IP:8080`

6. Optional — add domain + HTTPS:
   ```bash
   apt-get install -y certbot nginx
   # Add nginx reverse proxy + certbot
   ```

---

## Option 4: ngrok (Instant — expose localhost to internet, FREE)

If your machine is on 24/7, this is the fastest option.

1. Download ngrok: https://ngrok.com/download

2. Get free account → copy authtoken

3. Run:
   ```bash
   ngrok config add-authtoken YOUR_TOKEN
   ngrok http 8080
   ```

4. You get a URL like `https://abc123.ngrok-free.app` — share this.

Free plan: 1 tunnel, random URL changes on restart. 
Paid plan ($8/month): static URL, never expires.

---

## After deployment — load demo data

SSH into backend container and run:

```bash
# Small company only
docker compose -f compose-uz.yml exec backend bash -c \
  "cd /home/frappe/frappe-bench/sites && \
   /home/frappe/frappe-bench/env/bin/python /home/frappe/setup_demo_data.py --company small"

# Large company only
docker compose -f compose-uz.yml exec backend bash -c \
  "cd /home/frappe/frappe-bench/sites && \
   /home/frappe/frappe-bench/env/bin/python /home/frappe/setup_demo_data.py --company large"

# Both companies
docker compose -f compose-uz.yml exec backend bash -c \
  "cd /home/frappe/frappe-bench/sites && \
   /home/frappe/frappe-bench/env/bin/python /home/frappe/setup_demo_data.py --company both"
```

---

## Demo credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | Administrator | admin |

---

## Demo company overview

### Small — Nur Savdo MChJ (Textile shop)
- 5 employees
- 8 customers, 5 suppliers
- 10 items (clothing & accessories)
- ~10 purchase + ~15 sales invoices

### Large — Sapar Holding AJ (Electronics corp)
- 33 employees across 7 departments
- 20 customers, 15 suppliers
- 25 items (electronics & furniture)
- ~30 purchase + ~50 sales invoices
- 3 warehouses (Toshkent, Samarqand, Namangan)
