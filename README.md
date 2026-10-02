<div align="center">

# ⌚ Luxury Watch Store API

### A fully optimized Django REST Framework + PostgreSQL backend for a luxury watch store

![Django](https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.18-A30000?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

A class exercise focused on **deep ORM optimization** — every endpoint is built to avoid the classic **N+1 query problem**, verified live with Django Debug Toolbar. 🚀

</div>

---

## 📖 About

This project implements a complete e-commerce-style data model for a watch store (brands, categories, products, images, colors, customers, wishlists, comments) and exposes it through a small set of read APIs, each one deliberately engineered around a specific ORM optimization technique: `select_related`, `prefetch_related`, `F()` expressions, and SQL **window functions**.

## ✨ Highlights

| Feature                  | How it's done                                                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| 🏷️ 8 relational models   | `Brand`, `Category`, `Product`, `ProductImage`, `ProductColor`, `Customer`, `WishList`, `Comment`                   |
| 🧬 Shared base behaviour | Abstract `BaseModel` (timestamps) and `SluggedMixinModel` (unique slugs), inherited by `Product`                    |
| ⚡ Zero N+1 queries      | Verified with `CaptureQueriesContext` — query count stays constant no matter how many related rows exist            |
| 🖱️ Atomic click counter  | `Product.objects.filter(...).update(click_count=F("click_count") + 1)` — one query, race-condition free             |
| 📊 DB-level aggregation  | `Window(expression=Avg("price"))` computes the average luxury price per row, in the same query, no extra round-trip |
| 🔐 Per-user wishlist     | Authenticated endpoint, fully isolated between users, `unique_together` prevents duplicate wishlist entries         |
| 🛠️ Admin panel           | All 8 models registered, with inline editing for product images & colors                                            |
| 🐘 PostgreSQL via `.env` | Configuration loaded with `python-decouple`, no secrets hardcoded                                                   |
| 🔍 Django Debug Toolbar  | Live SQL panel to confirm query counts on every page                                                                |

## 🗂️ Project structure

```
Luxury_Watch_Store/
├── config/                 # Django project settings & root URLs
│   ├── settings.py
│   └── urls.py
├── shop/                   # Main application
│   ├── models.py           # 8 models + BaseModel / SluggedMixinModel
│   ├── serializers.py      # One serializer per API shape
│   ├── views.py            # 4 optimized APIView endpoints
│   ├── urls.py
│   └── admin.py
├── requirements.txt
├── .env.example
└── README.md
```

## 🔌 API Endpoints

| Method | Endpoint                | Description                                                                                    |
| ------ | ----------------------- | ---------------------------------------------------------------------------------------------- |
| `GET`  | `/api/products/`        | List of products with brand & category                                                         |
| `GET`  | `/api/products/<slug>/` | Full product detail + images + colors + comments; increments `click_count`                     |
| `GET`  | `/api/luxury-special/`  | Special + luxury + available products, with their average price computed at the database level |
| `GET`  | `/api/me/wishlist/`     | The authenticated user's wishlist (requires login)                                             |

<details>
<summary><b>Example response — <code>GET /api/products/</code></b></summary>

```json
[
  {
    "id": 1,
    "title": "Rolex Submariner",
    "slug": "rolex-submariner",
    "price": "15000.00",
    "brand": { "id": 1, "name": "Rolex" },
    "category": { "id": 1, "title": "Luxury Watches" },
    "is_available": true,
    "stash": 3
  }
]
```

</details>

<details>
<summary><b>Example response — <code>GET /api/luxury-special/</code></b></summary>

```json
[
  {
    "title": "Rolex Daytona",
    "price": "20000.00",
    "gender": "men",
    "strap_matterial": "metal",
    "engine": "automatic",
    "avg_luxury_price": "17500.00"
  }
]
```

</details>

## 🚀 Getting started

### 1. Clone & enter the project

```bash
git clone https://github.com/saeidha92/Luxury_Watch_Store.git
cd Luxury_Watch_Store
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Then edit `.env` with your own values:

```env
SECRET_KEY=your-random-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=luxury_watch_store
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Create the PostgreSQL database

```bash
psql -U postgres -c "CREATE DATABASE luxury_watch_store;"
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create an admin account

```bash
python manage.py createsuperuser
```

### 8. Run the server

```bash
python manage.py runserver
```

- 🛍️ Products API: `http://127.0.0.1:8000/api/products/`
- 🛠️ Admin panel: `http://127.0.0.1:8000/admin/`
- 🔍 Debug Toolbar: appears automatically on any HTML/browsable page while `DEBUG=True`

## 🧪 Verifying there's no N+1 query problem

Open any endpoint directly in a browser (not Postman/curl, so DRF's browsable HTML view loads) and check the **SQL** panel in Django Debug Toolbar — the query count should stay low and constant regardless of how many products, images, colors or comments exist.

## 📄 License

Released under the [MIT License](LICENSE).

---

<div align="center">
Built as a Django ORM optimization exercise.
</div>
