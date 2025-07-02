from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'comments.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            comment TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rezaayat')
def rezaayat():
    return render_template('rezaayat.html')

@app.route('/get-comments')
def get_comments():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT name, comment FROM comments ORDER BY id DESC')
    comments = [{'name': row[0], 'comment': row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(comments)

@app.route('/add-comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    name = data.get('name')
    comment = data.get('comment')
    if not name or not comment:
        return jsonify({'success': False}), 400
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO comments (name, comment) VALUES (?, ?)', (name, comment))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
