#import the app
from flask_app import app
#Then import the important flask responses
from flask import render_template,redirect,request,session,flash,jsonify
#then import the SAME relative file
from flask_app.models.model_deck import Deck #Importing the object we're manipulating
from flask_app.models import model_decklist, model_user

import json
MODEL = Deck


#Some of restful Routing
#Path should be '/TABLE_NAME/ID/ACTION'
#/User/new
#/user/create
#/user/<id>/edit
#/user/<id>/update
#/user/<id>/delete

@app.route("/deck/form")        #render route
def get_deck_form():
    return render_template("deck_form.html")

#So this is what happens when the URL reaches that ROUTE
@app.route('/deck/create',methods=['POST']) #action route
def create_deck():
    deckData = json.loads(request.form['deck'])
    deckDetails = request.form

    is_not_valid = Deck.validate(deckDetails)
    if is_not_valid:
        return jsonify({"error": is_not_valid})
    is_not_valid = model_decklist.DeckList.validate(deckData)
    if is_not_valid:
        return jsonify({"error": is_not_valid})

    #At this point the decklisting is valid....

    deckId = Deck.create({"name": request.form['name'], 'description': request.form['playstyle'], "user_id": session['uuid']})
    print("BLAAAAH" + str(deckId))
    for card_pin in deckData['main']:
        model_decklist.DeckList.create({"count":deckData['main'][card_pin] , 'card_pin': card_pin, 'deck_id': deckId})
    for card_pin in deckData['extra']:
        model_decklist.DeckList.create({"count":deckData['extra'][card_pin] , 'card_pin': card_pin, 'deck_id': deckId})
    # user_id = MODEL.create(request.form)
    # for card_pin in deckData['main']:
    #     print(f"{deckData['main'][card_pin]} | {card_pin}")
    # print(deckDetails)

    return redirect(f'/deck/{deckId}')


@app.route('/deck/<int:id>')
def get_deck(id):

    deck = Deck.get_one({"id": id})
    context ={
        "deckList": model_decklist.DeckList.get_one_with_deck_id({'id': id}),
        "deck": deck,
        "creator": model_user.User.get_one_with_uuid({'uuid': deck.user_id})
    }
    
    return render_template("deck_view.html", **context)

@app.route('/deck/<int:id>/edit')
def edit_deck(id):
    deck = Deck.get_one({"id": id})
    if 'uuid' not in session:
        return redirect(f"/deck/{id}")
    elif deck.user_id != session['uuid']:
        return redirect(f"/deck/{id}")
    return render_template("deck_edit.html")

@app.route('/deck/<int:id>/update', methods=['POST'])
def update_deck(id):
    deckData = json.loads(request.form['deck'])
    deckDetails = request.form

    is_not_valid = Deck.validate(deckDetails)
    if is_not_valid:
        return jsonify({"error": is_not_valid})
    is_not_valid = model_decklist.DeckList.validate(deckData)
    if is_not_valid:
        return jsonify({"error": is_not_valid})

    #If it's valid Then Delete our current listing for it...
    Deck.update({"name": deckDetails['name'], "description": deckDetails['playstyle'], "id": id})
    model_decklist.DeckList.delete({"deck_id": id})
    #Then populate a new set for it.... 
    for card_pin in deckData['main']:
        model_decklist.DeckList.create({"count":deckData['main'][card_pin] , 'card_pin': card_pin, 'deck_id': id})
    for card_pin in deckData['extra']:
        model_decklist.DeckList.create({"count":deckData['extra'][card_pin] , 'card_pin': card_pin, 'deck_id': id})
 # user_id = MODEL.create(request.form)
    # for card_pin in deckData['main']:
    #     print(f"{deckData['main'][card_pin]} | {card_pin}")
    print(deckDetails)

    return redirect(f"/deck/{id}")

@app.route('/deck/<int:id>/json')
def get_deck_list(id):
    data = model_decklist.DeckList.get_one_with_deck_id({"deck_id": id})
    dataJSON = {"deck":{} , "details": {}}
    for key in data:
        dataJSON['deck'][key.card_pin] = key.count
   
    deck = Deck.get_one({"id": id})
    dataJSON["details"]["name"] = deck.name
    dataJSON['details']["description"] = deck.description
    dataJSON['details']["creator_uuid"] = deck.user_id
    return jsonify(dataJSON)


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