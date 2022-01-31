#import the app
from unicodedata import name
from flask_app import app
#Then import the important flask responses
from flask import render_template,redirect,request,session,flash, jsonify
import requests
#then import the SAME relative file
from flask_app.models import model_query, model_attribute, model_race, model_archetype, model_type, model_card
from PIL import Image
from pathlib import Path
import urllib


MODEL = model_card.Card


def save_image(path, source):
    print(app.static_folder)
    print(source)
    print(str(path))
    urllib.request.urlretrieve(source,str(path))


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

# @app.route("/TABLE/new")        #render route
# def get_form():
#     return render_template("TABLE_form.html")
#So this is what happens when the URL reaches that ROUTE

@app.route('/card/create',methods=['POST']) #action route #This isn't going to be used
def create_card():
    user_id = MODEL.create(request.form)
    return redirect(f'/TABLE/{user_id}')

@app.route('/card/search', methods=['POST'])
def search_card():
    print(request.form['query'])
    #first we check to see if we've searched this before... 
    r = model_query.Query.get_one_with_query({"query" : request.form['query']})
    if not r: #if we did not get a hit then let's ask the API
        print("Card not found")
        r =  {'data': [{'id': 91152256, 'name': 'Celtic Guardian', 'type': 'Normal Monster', 'desc': 'An elf who learned to wield a sword, he baffles enemies with lightning-swift attacks.', 'atk': 1400, 'def': 1200, 'level': 4, 'race': 'Warrior', 'attribute': 'EARTH', 'archetype': 'Celtic Guard', 
                            'card_images': [{'id': 91152256, 'image_url': 'https://storage.googleapis.com/ygoprodeck.com/pics/91152256.jpg', 'image_url_small': 'https://storage.googleapis.com/ygoprodeck.com/pics_small/91152256.jpg'}, 
                                            {'id': 91152257, 'image_url': 'https://storage.googleapis.com/ygoprodeck.com/pics/91152257.jpg', 'image_url_small': 'https://storage.googleapis.com/ygoprodeck.com/pics_small/91152257.jpg'}, 
                                            {'id': 91152258, 'image_url': 'https://storage.googleapis.com/ygoprodeck.com/pics/91152258.jpg', 'image_url_small': 'https://storage.googleapis.com/ygoprodeck.com/pics_small/91152258.jpg'}]
                            }]
                    }
        #requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?fname={request.form['query']}")
        #card_query = MODEL

        #If our query
        if "error" in r:
            return jsonify({'error' : 'Card not found!'})
        
        #prpare the data to set IDs
        attributes = model_attribute.Attribute.json_all_name_id()
        races = model_race.Race.json_all_name_id()
        archetypes = model_archetype.Archetype.json_all_name_id()
        types = model_type.Type.json_all_name_id()

        # cards = model_card.Card.get_all_with_name()
        #print(response.json())
        resJson = r#.json()
        #So then for every item in the piece of data
        for data in resJson['data']:
            print(data)
            # value = [] 
            # value.append(data['id'])
            # value.append(attributes[data['attribute']])
            # value.append(races[data['race']])
            # value.append(archetypes[data['archetype']]) 
            # value.append(types[data['type']])
            # print(value)
            
            item_data = { 
                "card_id" : data['id'],
                "name" : data['name'], 
                "description" : data['desc'], 
                "attack" : data['atk'], 
                "defense": data['def'], 
                "level": data['level'], 
                "attribute_id": attributes[data['attribute']], 
                "race_id": races[data['race']], 
                "archetype_id": archetypes[data['archetype']],
                "type_id":types[data['type']]
                }
            
            #get ALL the card images associated with the card
            for image in data['card_images']:
                if not model_card.Card.get_one({"card_id" : image['id']}):
                    item_data["card_id"] = image['id']
                    filepath = Path(f"{app.static_folder}/img/card_image/{image['id']}.jpg")
                    if not Path.is_file(filepath): 
                        save_image(filepath, image['image_url'])
                    filepath_smoll = Path(f"{app.static_folder}/img/card_image_small/{image['id']}.jpg")
                    if not Path.is_file(filepath_smoll): 
                        save_image(filepath_smoll, image['image_url_small'])
                    model_card.Card.create(item_data)
            # model_card.Card.create(input)
    else: print("Query Already Ran")
    cards = model_card.Card.get_all_with_name({"name": request.form['query']})
    # we must keep in line with JSON format.
    # requests has a method to convert the data coming back into JSON.
    print(cards)
    cardsJson = {}
    i = 0
    for item in cards:
        cardsJson[i] = {
                "card_id" : item.card_id, 
                "name" : item.name, 
                "description" : item.description, 
                "attack" : item.attack, 
                "defense": item.defense, 
                "level": item.level, 
                "attribute_id": item.attribute_id, 
                "race_id": item.race_id, 
                "archetype_id": item.archetype_id,
                "type_id": item.type_id
        }
        i = i + 1
    print(cardsJson)
    return jsonify(cardsJson)


@app.route("/TABLE/<int:id>")
def view(id):
    context = {
        "items" : MODEL.get_one({"id": id})
    }
    return render_template("TABLE_edit.html", **context)


@app.route("/TABLE/<int:id>/edit")
def edit(id):
    context = {
        "items" : MODEL.get_one({"id": id})
    }
    return render_template("TABLE.html", **context)

@app.route("/TABLE/<int:id>/update", methods=['POST'])
def update(id):
    nothing = MODEL.update(request.form)
    return redirect(f"/TABLE/{id}")


@app.route("/TABLE/<int:id>/delete", methods=['POST'])
def delete(id):
    nothing = MODEL.delete({"id":id})
    return redirect("/")  #