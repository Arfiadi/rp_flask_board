from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)
from board.database import get_pg_db_conn
import psycopg2

bp = Blueprint("posts", __name__)

@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        author = request.form["author"] or "Anonymous"
        message = request.form["message"]

        if message:
            conn = get_pg_db_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO post (author, message) VALUES (%s, %s)",
                (author, message),
            )
            conn.commit()
            cur.close()
            return redirect(url_for("posts.posts"))

    return render_template("posts/create.html")

@bp.route("/posts")
def posts():
    conn = get_pg_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT author, message, created FROM post ORDER BY created DESC")
    posts = cur.fetchall()
    cur.close()
    return render_template("posts/posts.html", posts=posts)
