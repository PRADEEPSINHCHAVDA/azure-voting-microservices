from flask import Flask, render_template_string
import redis
import os

app = Flask(__name__)

# Connect to Redis
redis_host = os.environ.get('REDIS', 'redis')
redis_port = 6379
r = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)

# Simple HTML template
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Voting Results</title>
    <style>
        body { font-family: Arial; text-align: center; background-color: #f2f2f2; }
        h1 { color: #333; }
        .result { font-size: 24px; margin: 20px; }
    </style>
</head>
<body>
    <h1>Voting Results</h1>
    <div class="result">Cats: {{ cats }}</div>
    <div class="result">Dogs: {{ dogs }}</div>
</body>
</html>
"""

@app.route("/")
def results():
    cats = r.get("cats") or 0
    dogs = r.get("dogs") or 0
    return render_template_string(html, cats=cats, dogs=dogs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)