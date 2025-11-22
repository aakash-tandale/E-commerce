📌 Overview

This project implements a Coupons Management API for an e-commerce platform.  
It supports:

- Cart-wise coupons
- Product-wise coupons
- BxGy (Buy X Get Y) coupons
- Coupon CRUD
- Fetching applicable coupons
- Applying a specific coupon on a given cart

The objective is to build an extensible system that can support new coupon types in the future while clearly documenting all cases, assumptions, and limitations, as required in the assignment.

---

### Features Implemented

✔️ **1. Create Coupon (POST /coupons)**  
- Strict validation using Pydantic  
- Raw SQL insert  
- JSON stored using SQLAlchemy JSON type  

✔️ **2. Get All Coupons (GET /coupons)**  
- Returns list of all coupons  
- Includes parsed JSON details  

✔️ **3. Get Coupon By ID (GET /coupons/{id})**  

✔️ **4. Update Coupon (PUT /coupons/{id})**  
- Strict validation  
- Full overwrite of type + details  

✔️ **5. Delete Coupon (DELETE /coupons/{id})**  

✔️ **6. POST /applicable-coupons**  
- Returns only those coupons that apply to the given cart along with the computed discount.  

**Supported calculation logic:**  
- **Cart-wise**  
    - Applies percentage discount if cart total ≥ threshold.  
- **Product-wise**  
    - Applies percentage discount only to matching product(s).  
- **BxGy**  
    - Handles:  
        - Multiple buy groups  
        - Multiple get groups  
        - Repetition limit  
        - Partial applicability (e.g., buy 6 → apply twice)  
    - Returns monetary discount equal to the price of free products.  

✔️ **7. POST /apply-coupon/{id}**  
- Applies the selected coupon to the cart and returns:  
    - Updated items  
    - `total_price`  
    - `total_discount`  
    - `final_price`  
- **BxGy** also modifies quantities by adding free products.  

---

### Project Structure

```
app/
│── main.py
│── db.py                 # SQLite in-memory shared DB
│── models.py             # Coupon models
│── models_cart.py        # Cart models
│── routers/
│     └── coupons.py      # All endpoints
│── services/
            └── coupon_logic.py # Calculation and application logic
README.md
requirements.txt
```

---

### Tech Stack

- Python 3.12  
- FastAPI  
- SQLite (in-memory, shared DB mode)  
- Raw SQL (no ORM)  
- SQLAlchemy (engine only, JSON field type)  
- Pydantic v2  

---

### How to Run

1. **Create virtual environment**  
     ```bash
     python3.12 -m venv venv
     source venv/bin/activate
     ```

2. **Install dependencies**  
     ```bash
     pip install -r requirements.txt
     ```

3. **Start server**  
     ```bash
     uvicorn app.main:app --reload
     ```

4. **Open Swagger UI**  
     [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Example Payloads

1️⃣ **Cart-wise**  
```json
{
    "type": "cart-wise",
    "details": { "threshold": 100, "discount": 10 }
}
```

2️⃣ **Product-wise**  
```json
{
    "type": "product-wise",
    "details": { "product_id": 1, "discount": 20 }
}
```

3️⃣ **BxGy**  
```json
{
    "type": "bxgy",
    "details": {
        "buy_products": [{ "product_id": 1, "quantity": 3 }],
        "get_products": [{ "product_id": 3, "quantity": 1 }],
        "repition_limit": 2
    }
}
```

---

### Use Cases Considered 
  
Below are all cases I identified (implemented + unimplemented).

#### Implemented Use Cases

**Cart-wise**  
- Apply % discount on entire cart  
- Only when threshold exceeded  
- Handles any cart size  
- Ignores negative or zero totals  

**Product-wise**  
- Apply % discount only on target product  
- Supports multiple quantities  
- Supports any product price  
- No discount if product missing  

**BxGy**  
- Buy product(s) from a set  
- Get product(s) from a set  
- Handles:  
    - Multiple buy products  
    - Multiple get products  
    - Repetition limit  
    - Missing buy items → coupon not applicable  
    - Free products added to cart  
    - Price-based discount calculation  

---

#### Unimplemented (But Identified) Cases

**Cart-wise Unimplemented Cases**  
- Different discount types (flat ₹ off)  
- Tiered discounts (e.g., 10% above 100, 20% above 500)  

**Product-wise Unimplemented**  
- Multi-product discount sets  
- Category-based discounts  
- Price caps (max ₹100 off)  

**BxGy Unimplemented Cases**  
- Buy X of category A → get Y of category B  
- Free items with different price rules (e.g., cheapest free)  
- Free item selection when multiple items are available  
- Combining BxGy with product-wise  
- Minimum cart value for BxGy to activate  
- BxGy stacking with cart-wise  

**Cross-Coupon Cases (Unimplemented)**  
- Applying multiple coupons together  
- Prioritization (which coupon to pick first)  
- Selecting best discount automatically  
- Coupon exclusivity tags  

**Operational Unimplemented**  
- Coupon usage limits (per user, per day)  
- Coupon expiration (bonus feature)  
- Multi-currency support  
- Percentage + fixed discount combinations  
- Inventory-aware discounts  

---

### ⚙️ Assumptions

- All prices are in INR (₹).  
- Input cart items always include `product_id`, `quantity`, and `price`.  
- **BxGy** free products use the cart price if present; else assumed price 0.  
- Discounts always apply once per request (no global usage tracking).  
- Coupons do not interfere with each other (single apply at a time).  
- Coupon IDs are auto-incremented integers.  
- Invalid JSON structures are strictly rejected.  

---

### 🔍 Limitations

- In-memory SQLite DB resets on server restart.  
- **BxGy** cannot determine price for `get_products` not present in cart.  
- No persistent user or product catalog implemented.  
- No coupon expiry feature included.  
- No rate limiting, authentication, or user scope.  
- No partial return logic for free products.  

---

### 🧪 Testing

Use Swagger UI (`/docs`) or tools like Postman.  
You can test:  

- Create coupon  
- Update coupon  
- Delete coupon  
- Fetch all coupons  
- Identify applicable coupons  
- Apply coupon and verify final cart  

All calculations are deterministic and validated.  

---

🏁 Conclusion

The system implements all required API endpoints and core coupon logic as specified.
The codebase is structured for clarity, extensibility, and ease of review.
All necessary use cases, assumptions, and limitations have been documented.