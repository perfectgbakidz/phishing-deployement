from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('phishing_links.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phishing_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT NOT NULL,
            username TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('phishing_links.db')
    cursor = conn.cursor()
    cursor.execute('SELECT link, username FROM phishing_links')
    links = cursor.fetchall()
    conn.close()
    return render_template('index.html', links=links)

@app.route('/report', methods=['POST'])
def report():
    data = request.get_json()
    link = data.get('link')
    username = data.get('username')

    if link and username:
        conn = sqlite3.connect('phishing_links.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO phishing_links (link, username)
            VALUES (?, ?)
        ''', (link, username))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Link reported successfully'}), 200
    else:
        return jsonify({'message': 'Invalid data'}), 400

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
