from flask import Flask, request, redirect, render_template
import sqlite3
import string
import random
import re
import os

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT,
            short_code TEXT UNIQUE,
            clicks INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def valid_url(url):
    pattern = re.compile(
        r'^(http|https)://'
    )
    return re.match(pattern, url)


@app.route("/", methods=["GET", "POST"])
def index():

    short_url = None
    error = None

    if request.method == "POST":

        original_url = request.form["url"]

        if not valid_url(original_url):
            error = "Please enter a valid URL starting with http:// or https://"
            return render_template("index.html", error=error)

        conn = sqlite3.connect("urls.db")
        c = conn.cursor()

        while True:
            code = generate_code()

            c.execute(
                "SELECT id FROM urls WHERE short_code=?",
                (code,)
            )

            if not c.fetchone():
                break

        c.execute(
            "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
            (original_url, code)
        )

        conn.commit()
        conn.close()

        short_url = request.host_url + "s/" + code

    return render_template("index.html", short_url=short_url, error=error)


@app.route("/s/<code>")
def redirect_to_url(code):

    conn = sqlite3.connect("urls.db")
    c = conn.cursor()

    c.execute(
        "SELECT original_url, clicks FROM urls WHERE short_code=?",
        (code,)
    )

    result = c.fetchone()

    if result:

        original_url, clicks = result

        c.execute(
            "UPDATE urls SET clicks=? WHERE short_code=?",
            (clicks + 1, code)
        )

        conn.commit()
        conn.close()

        return redirect(original_url)

    conn.close()

    return "URL not found", 404

@app.route("/delete/<code>")
def delete_link(code):

    conn = sqlite3.connect("urls.db")
    c = conn.cursor()

    c.execute(
        "DELETE FROM urls WHERE short_code=?",
        (code,)
    )

    conn.commit()
    conn.close()

    return redirect("/links")


@app.route("/links")
def links():

    conn = sqlite3.connect("urls.db")
    c = conn.cursor()

    c.execute(
        "SELECT original_url, short_code, clicks FROM urls ORDER BY id DESC"
    )

    rows = c.fetchall()

    conn.close()

    return render_template("links.html", rows=rows)


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)