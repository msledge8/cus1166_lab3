import sys
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import *

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

#courses = [("CUS 1166", 12345),("CHE 2240", 23456),("CHE 2241L", 34567),("CUS 1165",45678),("CUS 1186",56789),("NET 1001",67890)]

@app.route("/")
def index():
    courses = Course.query.all()
    return render_template("index.html", courses=courses)


@app.route("/add_course", methods=["post"])
def add():
    course_number = request.form.get("Course Number")
    course_name = request.form.get("Course Name")
    courses = Course(course_number=course_number, course_name=course_name)
    db.session.add(courses)
    db.session.commit()

    courses = Course.query.all()
    return render_template('index.html', courses=courses)


@app.route("/register_student", methods=["GET", "POST"])
def register(course_id):
    courses = Course.query.get(course_id)
    if request.method == 'POST':
        course_name =  request.form.get("Course Name")
        grade = request.form.get("Grade")
    courses.add_student(course_name, grade)
    student = courses.student
    return render_template("course_details.html",courses=courses, student=student)

def main():
    if (len(sys.argv)==2):
        print(sys.argv)
    if sys.argv[1] == 'createdb':
        db.create_all()
    else:
        print("Run app using 'flask run' . To create a database use 'python app.py createdb' ")
