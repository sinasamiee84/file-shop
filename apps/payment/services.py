import requests
from django.conf import settings

# در حالت Sandbox از آدرس‌های تستی زرین‌پال استفاده می‌کنیم
# برای حالت واقعی (Production)، آدرس‌ها از zarinpal.com خواهند بود
ZARINPAL_SANDBOX = getattr(settings, "ZARINPAL_SANDBOX", True)

if ZARINPAL_SANDBOX:
    REQ_URL = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    PAY_URL = "https://sandbox.zarinpal.com/pg/StartPay/"
    VERIFY_URL = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
else:
    REQ_URL = "https://api.zarinpal.com/pg/v4/payment/request.json"
    PAY_URL = "https://www.zarinpal.com/pg/StartPay/"
    VERIFY_URL = "https://api.zarinpal.com/pg/v4/payment/verify.json"


def send_zarinpal_request(amount, description, callback_url):
    """ارسال درخواست پرداخت به زرین‌پال و دریافت Authority"""
    amount = amount * 10
    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": amount,
        # به تومان (یا ریال بسته به تنظیمات زرین‌پال، نسخه v4 تومان را پشتیبانی می‌کند اگر تنظیم شود یا ریال باشد)
        "description": description,
        "callback_url": callback_url,
    }
    headers = {"accept": "application/json", "content-type": "application/json"}

    try:
        response = requests.post(REQ_URL, json=data, headers=headers, timeout=10)
        res_data = response.json()
        if res_data.get("data", {}).get("code") == 100:
            authority = res_data["data"]["authority"]
            return True, authority, f"{PAY_URL}{authority}"
        return False, res_data.get("errors"), None
    except Exception as e:
        return False, str(e), None


def verify_zarinpal_payment(amount, authority):
    """تایید تراکنش پس از بازگشت کاربر از بانک"""
    amount = amount * 10
    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": amount,
        "authority": authority,
    }
    headers = {"accept": "application/json", "content-type": "application/json"}

    try:
        response = requests.post(VERIFY_URL, json=data, headers=headers, timeout=10)
        res_data = response.json()
        code = res_data.get("data", {}).get("code")
        # کد 100 به معنی موفقیت، کد 101 به معنی این است که قبلاً تایید شده است
        if code in [100, 101]:
            ref_id = res_data["data"]["ref_id"]
            return True, ref_id
        return False, res_data.get("errors")
    except Exception as e:
        return False, str(e)
