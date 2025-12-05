from flask import Flask, render_template_string, jsonify
import redis
import os

app = Flask(__name__)

# Redis connection
redis_host = os.environ.get("REDIS_HOST", "redis")
r = redis.StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Voting Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: white;
            padding: 40px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
            width: 350px;
        }
        h2 {
            margin-bottom: 20px;
        }
        .result {
            font-size: 24px;
            margin: 10px 0;
            font-weight: bold;
        }
        .reset-btn {
            margin-top: 20px;
            padding: 12px 20px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            background-color: #e74c3c;
            color: white;
            transition: 0.2s;
        }
        .reset-btn:hover {
            background-color: #c0392b;
            transform: scale(1.05);
        }
    </style>

    <script>
        async function updateCounts() {
            const res = await fetch('/counts');
            const data = await res.json();
            document.getElementById('cats').innerText = data.cats;
            document.getElementById('dogs').innerText = data.dogs;
        }

        async function resetCounts() {
            await fetch('/reset');
            updateCounts(); // Refresh immediately
        }

        setInterval(updateCounts, 1000); // Update every second
        window.onload = updateCounts;
    </script>
</head>
<body>
    <div class="card">
        <h2>Voting Results</h2>

        <div class="result">Cats: <span id="cats">0</span></div>
        <div class="result">Dogs: <span id="dogs">0</span></div>

        <button class="reset-btn" onclick="resetCounts()">Reset Counts</button>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(html)

@app.route("/counts")
def counts():
    cats = int(r.get("cats") or 0)
    dogs = int(r.get("dogs") or 0)
    return jsonify({"cats": cats, "dogs": dogs})

@app.route("/reset")
def reset():
    r.delete("cats")
    r.delete("dogs")
    r.delete("votes")
    return jsonify({"status": "reset"})
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)