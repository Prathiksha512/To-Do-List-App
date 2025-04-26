from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default="Pending")

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('task')
    if content:
        new_task = Task(content=content)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get(task_id)
    if request.method == 'POST':
        task.content = request.form.get('task')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

@app.route('/complete/<int:task_id>')
def complete(task_id):
    task = Task.query.get(task_id)
    task.status = 'Completed'
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/processing/<int:task_id>')
def processing(task_id):
    task = Task.query.get(task_id)
    task.status = 'Processing'
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
