from flask import Flask, render_template , request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, redirect, request, session
from flask_session import Session

import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db=SQLAlchemy(app)
migrate = Migrate(app, db)

class UserTodo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	complete = db.Column(db.Boolean)
	phone = db.Column(db.Integer)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name= db.Column(db.String)
	last_name= db.Column(db.String)
	email= db.Column(db.String)
	phone=db.Column(db.Integer)
	password=db.Column(db.String)


@app.route('/register')
def register():
	return render_template("register.html")

@app.route('/create-user')
def create():
	firstname=request.args.get('first_name')
	lastname=request.args.get('last_name')
	phone=request.args.get('phone_num')
	email=request.args.get('email')
	password=request.args.get('password')

	user_=User(first_name=firstname, last_name=lastname, email=email, phone=phone, password=password)
	db.session.add(user_)
	db.session.commit()

	response = render_template("template.html", phon=phone)
	return response

@app.route('/login')
def login():
	phone = request.args.get('phone_num')
	password= request.args.get('password')
	data = request.cookies.get('shaily')
	user = User.query.filter_by(phone=phone).first()
	if not user:
		return 'User Not found'
	if user.password!= password:
		return 'Incorrect password'
	todos=UserTodo.query.filter_by(phone=phone).all()
	session["user"] = phone
	return render_template("template.html", todo_list=todos, phon=phone, password=password)

@app.route('/logout')
def logout():
	session.pop("user", None)
	return redirect('/')

@app.route('/')
def home():
	return render_template("login.html")



@app.route('/add/<int:ph>/<string:password>', methods=['POST'])
def add(ph, password):
	# user = session["user"]
	# if not user:
	# 	return "Please log in"
	new_title=request.form.get('title')
	todo=UserTodo(title=new_title, complete=False, phone=ph)
	db.session.add(todo)
	db.session.commit()
	return redirect('/login?phone_num='+str(ph)+ '&password=' + password)



@app.route("/update/<int:todo_id>")
def update(todo_id):
	todo=UserTodo.query.filter_by(id=todo_id).first()
	todo.complete= not todo.complete
	db.session.commit()
	return redirect('/login?phone_num='+str(todo.phone))	

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
	todo=UserTodo.query.filter_by(id=todo_id).first()
	db.session.delete(todo)
	db.session.commit()
	return redirect('/login?phone_num='+str(todo.phone))



@app.route('/aboutme')
def about():
	return "<p> My name is Shalini. </p> "

db.create_all()
app.run(debug=True, port=4000)