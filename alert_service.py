import requests
from twilio.rest import Client

# ===============================
# CONFIGURATION (EDIT THESE)
# ===============================

# ---- Twilio WhatsApp ----
TWILIO_ACCOUNT_SID = "ACbd9535efc5dad240213608c1c6431aed"
TWILIO_AUTH_TOKEN = "4aa92b5aab60519dbe6472915bc67acc"
TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"   # Twilio sandbox
TWILIO_WHATSAPP_TO = "whatsapp:+918778075696"   # YOUR verified number

# ---- Fast2SMS ----
FAST2SMS_API_KEY = "F41EHbOtRcfsmX7CNiqLo0MJ5rj23TK86gdywzlPhAUk9apSQY1JvpZe0Q6aCAjbyIVxfnsBPY3GXE2g"
SMS_NUMBERS = "8124800419,8778075696"  # Comma-separated list of numbers


# ===============================
# WhatsApp Alert (Single Number)
# ===============================
def send_whatsapp_alert(message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_FROM,
            to=TWILIO_WHATSAPP_TO
        )

        print("✅ WhatsApp alert sent")

    except Exception as e:
        print("❌ WhatsApp alert failed:", e)


# ===============================
# SMS Alert (Multiple Numbers)
# ===============================
def send_sms_alert(message):
    try:
        url = "https://www.fast2sms.com/dev/bulkV2"

        payload = {
            "route": "v3",
            "sender_id": "TXTIND",
            "message": message,
            "language": "english",
            "numbers": SMS_NUMBERS
        }

        headers = {
            "authorization": FAST2SMS_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            print("✅ SMS alerts sent")
        else:
            print("❌ SMS failed:", response.text)

    except Exception as e:
        print("❌ SMS error:", e)
