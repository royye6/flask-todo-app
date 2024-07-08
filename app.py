from flask import Flask, request, render_template
from flask import url_for, redirect
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
    if htmx:
        pass
    else:
        if request.method == 'GET':
            pass
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)