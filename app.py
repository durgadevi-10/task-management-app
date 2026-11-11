
from flask import Flask, render_template, request, redirect
from database import get_db_connection, create_table

app = Flask(__name__)

create_table()


@app.route("/")
def home():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    description = request.form["description"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (title, description)
    )
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    status = request.form["status"]

    conn = get_db_connection()
    conn.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
