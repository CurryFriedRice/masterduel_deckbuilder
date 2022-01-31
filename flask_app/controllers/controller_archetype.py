#import the app
from flask_app import app
#Then import the important flask responses
from flask import render_template,redirect,request,session,flash, jsonify
#then import the SAME relative file
from flask_app.models.model_archetype import Archetype #Importing the object we're manipulating

MODEL = Archetype

@app.route('/')
def index():
    return render_template("index.html")

#Some of restful Routing
#Path should be '/TABLE_NAME/ID/ACTION'
#/User/new
#/user/create
#/user/<id>/edit
#/user/<id>/update
#/user/<id>/delete
@app.route('/archetypes/')
@app.route("/archetypes")
def get_archetypes():
    archetypes = MODEL.get_all()
    # print(archetypes)
    data = {}
    i = 1
    for item in archetypes:
        data[item.id] = item.name  
        i = i +1
    return jsonify(data) 

@app.route("/potato")
def ptoto():
    return "ptoto"

# @app.route("/TABLE/new")        #render route
# def get_form():
#     return render_template("TABLE_form.html")

# #So this is what happens when the URL reaches that ROUTE
# @app.route('/TABLE/create',methods=['POST']) #action route
# def create():
#     user_id = MODEL.create(request.form)
#     return redirect(f'/TABLE/{user_id}')

# @app.route("/TABLE/<int:id>")
# def view(id):
#     context = {
#         "items" : MODEL.get_one({"id": id})
#     }
#     return render_template("TABLE_edit.html", **context)


# @app.route("/TABLE/<int:id>/edit")
# def edit(id):
#     context = {
#         "items" : MODEL.get_one({"id": id})
#     }
#     return render_template("TABLE.html", **context)

# @app.route("/TABLE/<int:id>/update", methods=['POST'])
# def update(id):
#     nothing = MODEL.update(request.form)
#     return redirect(f"/TABLE/{id}")


# @app.route("/TABLE/<int:id>/delete", methods=['POST'])
# def delete(id):
#     nothing = MODEL.delete({"id":id})
#     return redirect("/")  #