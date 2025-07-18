import time
import requests
import json
from config import INTERVAL_SECONDS, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

RPC_ENDPOINT = "https://api.mainnet-beta.solana.com"

last_slot = None

def get_current_slot():
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSlot"
        }
        response = requests.post(RPC_ENDPOINT, json=payload, timeout=10)
        return response.json().get("result", None)
    except Exception as e:
        send_alert(f"❌ Error fetching slot: {e}")
        return None

def send_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending alert: {e}")

def monitor():
    global last_slot
    while True:
        current_slot = get_current_slot()
        if current_slot is None:
            time.sleep(INTERVAL_SECONDS)
            continue

        if last_slot is not None and current_slot == last_slot:
            send_alert(f"🚨 Slot stagnation detected! Last slot: {last_slot}")
        else:
            print(f"Slot updated: {current_slot}")

        last_slot = current_slot
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    send_alert("🟢 MEV Shield Bot Started Monitoring Solana RPC")
    monitor()
