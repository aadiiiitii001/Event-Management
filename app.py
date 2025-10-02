from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      event_name TEXT,
                      event_date TEXT,
                      location TEXT,
                      description TEXT)''')
    conn.commit()
    conn.close()

init_db()

users = {
    "test@example.com": "password123"
}


# Home Page - Display all events
@app.route('/')
def home():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    conn.close()
    return render_template('home.html', events=events)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session.permanent = True
            session['user'] = email
            return redirect(url_for('create_event'))
        else:
            return "Incorrect email or password. Please try again."
    return render_template('login.html')

# Create Event Page
@app.route('/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        location = request.form['location']
        description = request.form['description']
        
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (event_name, event_date, location, description) VALUES (?, ?, ?, ?)",
                       (event_name, event_date, location, description))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    
    return render_template('create_event.html')

# Event Details Page
@app.route('/event/<int:event_id>')
def event_details(event_id):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()
    conn.close()
    return render_template('event_details.html', event=event)

# Edit Event Page
@app.route('/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        location = request.form['location']
        description = request.form['description']
        
        cursor.execute("UPDATE events SET event_name = ?, event_date = ?, location = ?, description = ? WHERE id = ?",
                       (event_name, event_date, location, description, event_id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()
    conn.close()
    return render_template('edit_event.html', event=event)

# Delete Event
@app.route('/delete/<int:event_id>')
def delete_event(event_id):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
