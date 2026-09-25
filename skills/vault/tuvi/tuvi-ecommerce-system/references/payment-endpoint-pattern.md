# Payment Endpoint Pattern — Momo & VNPay

> Created: 20/07/2026 Phase 2 | File: `backend/main.py`

## Architecture

### 3 payment endpoints (all in main.py)

| Endpoint | Method | Purpose | Request Body |
|----------|--------|---------|--------------|
| `/api/payment/momo` | POST | Direct Momo payment | `PaymentRequest` |
| `/api/payment/vnpay` | POST | Direct VNPay payment | `PaymentRequest` |
| `/api/order/create` | POST | Unified order (frontend picks method) | `OrderRequest` (includes `payment_method`) |

### `PaymentRequest` schema

```python
class PaymentRequest(BaseModel):
    product_id: str
    customer_name: str
    customer_phone: str
    customer_email: str = ""
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour: int = 0
    gender: str
```

### `OrderRequest` schema (unified)

```python
class OrderRequest(BaseModel):
    product_id: str
    customer_name: str
    customer_phone: str
    customer_email: str = ""
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour: int = 0
    gender: str
    payment_method: str  # "momo" or "vnpay"
```

## Flow

```
Frontend                   Backend                          Momo/VNPay
   │                          │                                │
   ├── POST /api/payment/momo─┼──→ create Order (pending) ────┤
   │◄─ {order_id, payment_url}┼──→ 302 redirect ──────────────┼──→ User pays
   │                          │                                │
   │                          │◄─ IPN callback ───────────────┼──→ update status
   │                          │                                │
   │                          │ User redirected back ─────────┼──→ /api/order/{id}
   │◄─ {status, order} ──────┼──→ frontend shows result       │
```

## ⚠️ Critical: Product Lookup

The most common bug: **Product ID field mismatch.**

- Products stored in DB with `product_id` = "PDF01", "PDF02", etc.
- Frontend sends `product_id: "PDF01"` — but `id` column (primary key auto-increment) is NOT the same as `product_id` column

**ALWAYS use this safe lookup pattern on ALL 3 payment endpoints:**

```python
def _find_product(db, product_id):
    product = db.query(Product).filter(
        (Product.product_id == product_id) |
        (Product.product_id == f"TV-{product_id}") |
        (Product.id == product_id)
    ).first()
    if not product:
        product = db.query(Product).filter(Product.product_id == product_id).first()
    return product
```

## Momo Signature

```python
import hashlib, hmac

def create_momo_payment(order_id, amount, order_info):
    partner_code = "MOMO"
    access_key = "F8BBA842ECF85"
    secret_key = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    redirect_url = f"{BASE_URL}/api/order/momo-return"
    ipn_url = f"{BASE_URL}/api/order/momo-ipn"
    request_id = order_id
    request_type = "captureWallet"
    extra_data = ""
    
    raw_sign = f"accessKey={access_key}&amount={int(amount)}&extraData={extra_data}&ipnUrl={ipn_url}&orderId={order_id}&orderInfo={order_info}&partnerCode={partner_code}&redirectUrl={redirect_url}&requestId={request_id}&requestType={request_type}"
    signature = hmac.new(secret_key.encode(), raw_sign.encode(), hashlib.sha256).hexdigest()
    
    payload = {
        "partnerCode": partner_code,
        "accessKey": access_key,
        "requestId": request_id,
        "amount": int(amount),
        "orderId": order_id,
        "orderInfo": order_info,
        "redirectUrl": redirect_url,
        "ipnUrl": ipn_url,
        "extraData": extra_data,
        "requestType": request_type,
        "signature": signature
    }
    
    resp = requests.post("https://test-payment.momo.vn/v2/gateway/api/create", json=payload, timeout=10)
    return resp.json().get("payUrl", "")
```

## VNPay Signature

```python
import hashlib
from urllib.parse import urlencode

def create_vnpay_payment(order_id, amount, order_info):
    tmn_code = "2QXU4R4K"
    hash_secret = "HDVWDWYRHOFJJXKELNCVPEWRTFPUEWCH"
    return_url = f"{BASE_URL}/api/order/vnpay-return"
    
    params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": tmn_code,
        "vnp_Amount": int(amount * 100),
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": order_id,
        "vnp_OrderInfo": order_info[:255],
        "vnp_OrderType": "other",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": return_url,
        "vnp_IpAddr": "127.0.0.1",
        "vnp_CreateDate": datetime.now().strftime("%Y%m%d%H%M%S"),
    }
    
    # Sort params alphabetically
    sorted_params = dict(sorted(params.items()))
    sign_data = urlencode(sorted_params)
    secure_hash = hashlib.sha512(hash_secret.encode() + b'?' + sign_data.encode()).hexdigest()
    params["vnp_SecureHash"] = secure_hash
    
    return "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html?" + urlencode(params)
```
