from flask import Flask, request, render_template
from flask import url_for, redirect, abort
from flask_htmx import HTMX
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from datetime import datetime


app = Flask(__name__)
htmx = HTMX(app)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.sqlite3'
db=SQLAlchemy(model_class=Base)

db.init_app(app)

# models

class Todos(db.Model):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(300), nullable=False)
    task: Mapped[str] = mapped_column(db.String(500), nullable=False)
    is_complete: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def mark_complete(self):
        self.is_complete = True
        db.session.commit()

    def mark_incomplete(self):
        self.is_complete = False
        db.session.commit()

    def update(self, new_title, new_task):
        self.title = new_title
        self.task = new_task
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# routes

@app.route("/", methods=['POST', 'GET'])
def index():
    todos = Todos.query.order_by(Todos.created_at.desc()).all()

    if request.method == 'POST':
        title = request.form['title']
        task = request.form['task']
        if title != '' and task != '':
            new_task = Todos(title=title, task=task)
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        else:
            return redirect('/')
        
    if htmx == 'GET':
        edit()

    return render_template('index.html', todos=todos)


@app.route("/display/<int:todo_id>/", methods=['GET', 'PUT'])
def display(todo_id):
    todo = Todos.query.get(todo_id)

    if todo is None:
        return abort(404)
    
    return render_template('display.html', todo=todo)


@app.route("/edit/<int:todo_id>/", methods=['GET', 'PUT', 'DELETE'])
def edit(todo_id):
    todo = Todos.query.get(todo_id)

    if todo is None:
        print('error: todo not found')
        return abort(404)
    
    if request.method == 'PUT':
        new_title = request.form.get('ntitle')
        new_task = request.form.get('ntask')
        status = request.form.get('completed', False)
        todo.update(new_title, new_task)
        if status:
            todo.mark_complete()
        else:
            todo.is_complete = False
            db.session.commit()
        print('success: todo updated successfully!')
        return display(todo_id)

    if request.method == 'DELETE':
        todo.delete()
        db.session.commit()
        return ''
    return render_template('edit.html', todo=todo)


if __name__ == '__main__':
    app.run(debug=True)