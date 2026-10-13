# VIKMO DealerDesk — Take-Home Assignment

**Track: AI / ML**  
Candidate Role: AI / ML Intern  
Technology Stack: Python 3.11+, Django 5.2, Django REST Framework, PostgreSQL, Scikit-Learn, Groq / Gemini LLM

---

## 1. Overview

DealerDesk is an AI-native distribution backend for automotive spare parts. This project implements:
1. **Priority A (Backend Core):** REST API for Products, Inventory, Dealers, and Draft Orders backed by PostgreSQL, with exact 2-decimal money representation, 18% GST line calculations, unique order sequence generation (`ORD-YYYYMMDD-NNNN`), and idempotent data seeding.
2. **Priority B (Dealer Assistant):** Conversational AI parts assistant (`POST /api/assistant/chat/`) with tool calling (`search_parts`, `check_stock`, `create_draft_order`), conversation memory per `session_id`, runtime database grounding, and untrusted data protection.
3. **Priority C (Forecasting & Reorder):** Chronological, leakage-free 4-week demand forecasting for 40 SKUs (`ml/forecast.csv`, 160 rows) outperforming historical baselines by 18.1%, with dynamic safety stock and reorder suggestions (`GET /api/reorder-suggestions/`, `GET /api/forecast/{sku}/`).
4. **Decisions & Architecture:** Comprehensive documentation answering all evaluation questions in [`DECISIONS.md`](file:///c:/Users/HP/Downloads/VIKMO_DealerDesk_Assignment%20%281%29/DECISIONS.md).

---

## 2. Setup & Installation

### Requirements
- Python 3.11 or newer
- PostgreSQL database (local or hosted e.g. Neon/Supabase)

### Step 1: Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env            # Windows: copy .env.example .env
```

Configure your PostgreSQL connection in `.env`:
```env
DATABASE_URL=postgres://postgres:root@localhost:5432/dealerdesk
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 3: Run Database Migrations & Seed Data
```bash
python manage.py migrate --noinput
python manage.py seed_data
python manage.py seed_data      # Running twice is safe and idempotent
```

### Step 4: Start Development Server
```bash
python manage.py runserver 0.0.0.0:8000 --noreload
```

---

## 3. Running Verification & Smoke Tests

### Run Automated Smoke Test (AI/ML Track)
```bash
python smoke_test.py --base-url http://localhost:8000 --track aiml
```
*Expected Output: 10/10 checks passed.*

### Run Django Unit & Integration Test Suite
```bash
python manage.py test
```

### Run Model Evaluation & Baseline Comparison
```bash
python ml/train_and_evaluate.py
```

### Regenerate Forecast CSV
```bash
python ml/generate_forecast.py
```

---

## 4. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health/` | Health check (`{"status": "ok"}`) |
| `GET` | `/api/products/` | Paginated product list with `search`, `category`, `vehicle` filters |
| `POST` | `/api/products/` | Create new product (initial stock 0) |
| `GET` | `/api/products/{sku}/` | Product detail by SKU |
| `PATCH` | `/api/products/{sku}/` | Partial product update (immutable SKU) |
| `GET` | `/api/inventory/summary/` | Live catalogue inventory aggregation (total units, unique SKUs, stock health, valuation) |
| `PUT` | `/api/inventory/{sku}/` | Update live inventory count |
| `GET` | `/api/dealers/` | Paginated dealer list |
| `POST` | `/api/dealers/` | Create dealer account (unique `dealer_code`) |
| `GET` | `/api/dealers/{id}/` | Dealer detail by ID |
| `POST` | `/api/orders/` | Create DRAFT order with current catalogue prices and 18% GST |
| `GET` | `/api/orders/` | Paginated orders list with `dealer_id`, `status` filters |
| `GET` | `/api/orders/{order_number}/` | Order detail |
| `PUT` | `/api/orders/{order_number}/` | Replace items on DRAFT order |
| `POST` | `/api/orders/{order_number}/confirm/` | Confirm order and deduct stock atomically |
| `POST` | `/api/orders/{order_number}/cancel/` | Cancel order and restore stock |
| `POST` | `/api/assistant/chat/` | Conversational Dealer Assistant with LLM tool calling |
| `GET` | `/api/forecast/{sku}/` | 4-week forecast for target SKU |
| `GET` | `/api/reorder-suggestions/` | Reorder suggestions for all 40 forecast SKUs with live stock |

---

## 5. GenAI Assistant Details

- **Provider:** Groq (`llama-3.3-70b-versatile`) / Google Gemini (`gemini-2.5-flash`).
- **Function Tools Declared:**
  1. `search_parts`: Hybrid retrieval matching vehicle fitment, brand, part name, and category.
  2. `check_stock`: Live database query retrieving exact current stock and price from PostgreSQL.
  3. `create_draft_order`: Server-validated draft order creation through core ordering engine.
- **Safety & Injection Defense:**
  - Product descriptions are marked untrusted in system instructions.
  - LLM cannot execute state changes beyond draft orders.
  - Fallback deterministic router ensures reliable contract compliance when provider API keys are absent or rate-limited.

---

## 6. Demand Forecasting Summary

- **Forecast Horizons:** 4 weeks starting `2026-09-28`, `2026-10-05`, `2026-10-12`, `2026-10-19`.
- **Chronological Validation Benchmark (MAE across 4 sliding historical test windows):**
  - Last Observed Value: `11.671`
  - Same Week Last Year: `11.731`
  - Recent 4-Week Mean: `9.522`
  - Recent 12-Week Mean: `9.074`
  - **Gradient Boosting Hybrid:** `7.434` (18.1% improvement over best baseline).
- **Special Effects Handled:**
  - Moving Diwali effect via Gaussian calendar proximity.
  - Future planned promotions from `promo_calendar.csv`.
  - Cold-start handling for new SKUs (`BRK-1105`, `CHN-1006`).

---

## 7. Submission Artifacts

- Video Walkthrough Link: `https://youtu.be/placeholder-demo` *(To be added by candidate)*
- Detailed decisions and code line citations: [`DECISIONS.md`](file:///c:/Users/HP/Downloads/VIKMO_DealerDesk_Assignment%20%281%29/DECISIONS.md)
