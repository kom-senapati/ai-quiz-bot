import sqlite3
import os

def create_connection():
    conn = None
    try:
        db_path = os.path.abspath(os.getcwd()) + "\\quiz_database.db"
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_quiz(topic, data):
    conn = create_connection()
    cursor = conn.cursor()
    for entry in data:
        cursor.execute('''
            INSERT INTO quiz_table (topic, question, option_a, option_b, option_c, option_d, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (topic, entry['q'], entry['A'], entry['B'], entry['C'], entry['D'], entry['correct']))
    conn.commit()
    conn.close()

def get_quiz(topic):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT question, option_a, option_b, option_c, option_d, correct_answer
        FROM quiz_table
        WHERE topic = ?
    ''', (topic,))
    rows = cursor.fetchall()
    conn.close()
    quiz = []
    for row in rows:
        quiz.append({
            'question': row[0],
            'option_a': row[1],
            'option_b': row[2],
            'option_c': row[3],
            'option_d': row[4],
            'correct_answer': row[5]
        })
    return quiz

def delete_quiz(topic):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM quiz_table
        WHERE topic = ?
    ''', (topic,))
    conn.commit()
    conn.close()

def get_topics():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT topic FROM quiz_table')
    topics = cursor.fetchall()
    conn.commit()
    conn.close()
    return [topic[0] for topic in topics]