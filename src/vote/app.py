from flask import Flask, request, redirect
import os, redis

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

CHOICE_A = os.getenv("CHOICE_A", "Cats")
CHOICE_B = os.getenv("CHOICE_B", "Dogs")
TITLE = os.getenv("TITLE", "Vote!")

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        vote = request.form["vote"]
        r.rpush("votes", vote)
        return redirect("/")
    return f"""
    <html><head><title>{TITLE}</title></head>
    <body>
      <h2>{TITLE}</h2>
      <form method="POST">
        <button name="vote" value="A">{CHOICE_A}</button>
        <button name="vote" value="B">{CHOICE_B}</button>
      </form>
    </body></html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)