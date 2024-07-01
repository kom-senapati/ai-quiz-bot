from flask import Flask, render_template, request, redirect, url_for, session
import db
from main import generate_quiz

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quizzes')
def quizzes():
    topics = db.get_topics()
    return render_template('quizzes.html', topics=topics)

@app.route('/quiz/<topic>', methods=['GET', 'POST'])
def quiz(topic):
    questions = db.get_quiz(topic)
    if request.method == 'POST':
        answers = request.form.to_dict()
        session['answers'] = answers
        return redirect(url_for('quiz_summary', topic=topic))
    if questions:
        return render_template('quiz.html', topic=topic, questions=questions)
    else:
        return render_template('create_quiz.html', topic=topic)

@app.route('/delete_quiz/<topic>')
def delete_quiz(topic):
    db.delete_quiz(topic)
    return redirect(url_for('quizzes'))

@app.route('/create_quiz/<topic>', methods=['POST'])
def create_quiz(topic):
    new_topic = request.form['new_topic']
    quiz_data = generate_quiz(new_topic)
    db.create_quiz(new_topic, quiz_data)
    return redirect(url_for('quizzes'))

@app.route('/quiz_summary/<topic>')
def quiz_summary(topic):
    questions = db.get_quiz(topic)
    answers = session.get('answers', {})
    correct_count = 0
    total_questions = len(questions)
    for i, question in enumerate(questions):
        correct_answer = question['correct_answer']
        user_answer = answers.get(f'question{i+1}')
        if user_answer == correct_answer:
            correct_count += 1
    percentage = (correct_count / total_questions) * 100
    return render_template('quiz_summary.html', topic=topic, questions=questions, answers=answers, correct_count=correct_count, percentage=percentage)


if __name__ == '__main__':
    app.run(debug=True)
