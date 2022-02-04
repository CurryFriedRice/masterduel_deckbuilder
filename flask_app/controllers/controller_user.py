from flask_app import app
#Then import the important flask responses
from flask import render_template,redirect,request,session,flash, jsonify
from flask_bcrypt import Bcrypt
import requests

#then import the SAME relative file
from flask_app.models.model_user import User #Importing the object we're manipulating
from flask_app.models import model_deck
bcrypt = Bcrypt(app)
MODEL = User

@app.route('/')
def to_dashboard():
    return redirect("/dashboard")


@app.route('/dashboard')
def get_form():
    session['cards'] = {}
    # if 'uuid' in session:
    #     return redirect("/dashboard")
    # #REMOVE THIS!
    context = {
        "decks" : model_deck.Deck.get_all(),
        "users" : User.get_all()
    } 
    return render_template("index.html", **context)


#Some of restful Routing
#Path should be '/TABLE_NAME/ID/ACTION'
#/User/new
#/user/create 
#/user/<id>/edit
#/user/<id>/update
#/user/<id>/delete
@app.route("/account/form")
def get_Login():
    if "uuid" in session:
        return redirect("/dashboard")
    return render_template("login_form.html")

@app.route("/account/logout")
def logout():
    session.pop('uuid',0)
    flash("User Successfully Logged Out", "account_session_clear")
    return redirect("/")


@app.route("/account/login", methods=['POST'])
def login():
    user_in_db = MODEL.get_one_with_email({"email" :request.form['email']})

    if not user_in_db:
        return jsonify({"error": {'login_err': "Invalid Email/Password"}})

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        return jsonify({"error": {'login_err': "Invalid Email/Password"}})
    
    session['uuid'] = user_in_db.uuid
    session['username'] = user_in_db.username
    return redirect("/dashboard")


@app.route('/account/create',methods=['POST']) #action route
def create():
    if MODEL.validate(request.form):
        return jsonify({"error" : MODEL.validate(request.form)})
    #make and format the data
    form_dict = dict(request.form)
    form_dict['password'] = bcrypt.generate_password_hash(request.form['password'])
    #add the entry
    form_dict['uuid'] = requests.get("https://www.uuidtools.com/api/generate/v4").json()[0]
    user_id = MODEL.create(form_dict)
    #get the entry
    session['uuid'] = form_dict['uuid'] #this is so we don't use t he UUID
    session['username'] = form_dict['username']
    return  redirect("/dashboard")

@app.route('/user/<string:uuid>')
def user_decks(uuid):
    context = {
        "decks" : model_deck.Deck.get_all_with_uuid({"uuid": uuid}),
        "users" : User.get_all()
    }
    return render_template("index.html", ** context)


# #we aren't doing editing....
# @app.route("/account/edit")
# def edit():
#     if 'uuid' not in session:
#         return redirect("/account")

#     context = {
#         "accounts" : MODEL.get_one_with_uuid({"uuid": session['id']})
#     }
#     return render_template("account_edit.html", **context)

# @app.route("/account/update", methods=['POST'])
# def update():
#     if 'uuid' not in session:
#         return redirect("/account")
#     user_in_db = MODEL.get_one_with_uuid({'uuid': session['uuid']})
#     if not user_in_db:
#         flash("Attempting to edit Wrong account", "account_edit_err")
#         return redirect("/")
#     nothing = MODEL.update(request.form)
#     flash("Update successful", "account_edit_success")
#     return redirect("/account/edit")


# @app.route("/account/delete", methods=['POST'])
# def delete(id):
#     #nothing = MODEL.delete({"id":id})
#     return redirect("/")  


# @app.route("/account/logout")
# def clear_uuid():
#     session.pop("uuid",0)
#     return redirect('/dashboard')

# @app.route('/account/session/cards')
# def get_session_cards():
#     return session['cards']