from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        location TEXT NOT NULL,
        description TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        description = request.form['description']
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()
        c.execute("INSERT INTO jobs (title, company, location, description) VALUES (?, ?, ?, ?)", (title, company, location, description))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('post_job.html')

@app.route('/view_jobs')
def view_jobs():
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    jobs = c.fetchall()
    conn.close()
    return render_template('view_jobs.html', jobs=jobs)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
