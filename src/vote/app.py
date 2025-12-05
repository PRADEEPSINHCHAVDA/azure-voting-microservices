from flask import Flask, request, redirect
import os, redis

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

CHOICE_A = os.getenv("CHOICE_A", "Cats")
CHOICE_B = os.getenv("CHOICE_B", "Dogs")
TITLE = os.getenv("TITLE", "Vote!")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        vote = request.form["vote"]
        r.rpush("votes", vote)
        return redirect("/")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{TITLE}</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
                width: 350px;
            }}
            h2 {{
                margin-bottom: 20px;
                color: #444;
            }}
            button {{
                width: 100%;
                padding: 15px;
                margin-top: 15px;
                font-size: 18px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: 0.2s;
            }}
            .btn-a {{
                background-color: #4CAF50;
                color: white;
            }}
            .btn-b {{
                background-color: #2196F3;
                color: white;
            }}
            button:hover {{
                transform: scale(1.05);
                opacity: 0.9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>{TITLE}</h2>
            <form method="POST">
                <button class="btn-a" name="vote" value="A">{CHOICE_A}</button>
                <button class="btn-b" name="vote" value="B">{CHOICE_B}</button>
            </form>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)