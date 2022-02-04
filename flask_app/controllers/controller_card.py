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

from flask_app.models.model_card import Card


MODEL = model_card.Card


test_Data = {'data': [{'id': 91152256, 'name': 'Celtic Guardian', 'type': 'Normal Monster', 'desc': 'An elf who learned to wield a sword, he baffles enemies with lightning-swift attacks.', 'atk': 1400, 'def': 1200, 'level': 4, 'race': 'Warrior', 'attribute': 'EARTH', 'archetype': 'Celtic Guard', 
                            'card_images': [{'id': 91152256, 'image_url': 'https://storage.googleapis.com/ygoprodeck.com/pics/91152256.jpg', 'image_url_small': 'https://storage.googleapis.com/ygoprodeck.com/pics_small/91152256.jpg'}, 
                                            {'id': 91152257, 'image_url': 'https://storage.googleapis.com/ygoprodeck.com/pics/91152257.jpg', 'image_url_small': 'https://storage.googleapis.com/ygoprodeck.com/pics_small/91152257.jpg'}, 
                                            {'id': 91152258, 'image_url': 'https://storage.googleapis.com/ygoprodeck.com/pics/91152258.jpg', 'image_url_small': 'https://storage.googleapis.com/ygoprodeck.com/pics_small/91152258.jpg'}]},
                        {"id":53129443,"name":"Dark Hole","type":"Spell Card","desc":"Destroy all monsters on the field.","race":"Normal","archetype":"Hole", 
                            "card_images": [{"id":53129443,"image_url":"https://storage.googleapis.com/ygoprodeck.com/pics/53129443.jpg","image_url_small":"https://storage.googleapis.com/ygoprodeck.com/pics_small/53129443.jpg"}]
                        },
                        {"id":84013237,"name":"Number 39: Utopia","type":"XYZ Monster","desc":"2 Level 4 monsters\r\nWhen a monster declares an attack: You can detach 1 material from this card; negate the attack. If this card is targeted for an attack, while it has no material: Destroy this card.","atk":2500,"def":2000,"level":4,"race":"Warrior","attribute":"LIGHT","archetype":"Utopia",
                            "card_images": [{"id":84013237,"image_url":"https://storage.googleapis.com/ygoprodeck.com/pics/84013237.jpg","image_url_small":"https://storage.googleapis.com/ygoprodeck.com/pics_small/84013237.jpg"}]
                        },
                        {"id":1861629,"name":"Decode Talker","type":"Link Monster","desc":"2+ Effect Monsters\r\nGains 500 ATK for each monster it points to. When your opponent activates a card or effect that targets a card(s) you control (Quick Effect): You can Tribute 1 monster this card points to; negate the activation, and if you do, destroy that card.","atk":2300,"race":"Cyberse","attribute":"DARK","archetype":"Code Talker","linkval":3,"linkmarkers":["Top","Bottom-Left","Bottom-Right"],
                            "card_images":[{"id":1861629,"image_url":"https://storage.googleapis.com/ygoprodeck.com/pics/1861629.jpg","image_url_small":"https://storage.googleapis.com/ygoprodeck.com/pics_small/1861629.jpg"},{"id":1861630,"image_url":"https://storage.googleapis.com/ygoprodeck.com/pics/1861630.jpg","image_url_small":"https://storage.googleapis.com/ygoprodeck.com/pics_small/1861630.jpg"}]
                        }
            ]}

# test_error = {"error": "Cards not Found Try a valid query"}

def save_image(path, source):
    #print(app.static_folder)
    #print(source)
    #print(str(path))
    urllib.request.urlretrieve(source,str(path))


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
    #first we check to see if we've searched this before... 
    #TODO: STORE THE RESULTS IN THE SESSION CACHE SO IT DOESN'T PING MY SERVER AGAIN
    if len(request.form['query']) < 2:
        return jsonify({"error": "Search must be at least two characters"})
    r = model_query.Query.get_one_with_query({"query" : request.form['query']})
    if not r: #if we did not get a hit then we've never searched this
        print("Quuery not Found Creating query!")
        model_query.Query.create(request.form['query'])
        #add the query to our db so we don't ping them to ask the same thing
        #TODO: Check how old the query is.... If it's too old then Ask the API again and refresh results
        #r =  test_Data
        r =requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?fname={request.form['query']}")
        #If the API hit an error then the card does not exist
        if "error" in r.json():
            return jsonify({'error' : 'Card not found! Search only for card names'})
            #TODO: Eventually add a search descriptions as well

        #otherwise we start preparing to fill in card data
        #prpare the operating table to set ids of external values
        attributes = model_attribute.Attribute.json_all_name_id()
        races = model_race.Race.json_all_name_id()
        archetypes = model_archetype.Archetype.json_all_name_id()
        types = model_type.Type.json_all_name_id()
        #resJson = r#.json()
        #So then for every item in the piece of data
        for data in r.json()['data']:
            #Check to see if we have this
            if not Card.get_one_with_pin({"pin": data["id"]}):
                print("Creating Data For monster Card ",data['name'])
                alternate_pins = ''
                for i in data['card_images']:
                    alternate_pins += str(i['id']) + ','

                card_data = {
                    "pin": data['id'],
                    "alternate_pin": alternate_pins[:-1], #gets all the alternate arts
                    "name" : data['name'], #required....
                    "description" : data['desc'], #required...
                    "attack" : data['atk'] if 'def' in data else None,
                    'defense': data['def'] if 'def' in data else None,
                    'level': data['level'] if 'level' in data else data['linkval'] if 'linkval' in data else None,
                    'link_markers': data['linkmarkers'] if 'linkmarkers' in data else None,
                    'attribute_id': attributes[data['attribute']] if 'attribute' in data else None,
                    'race_id': races[data['race']] if 'race' in data else None,
                    'archetype_id': archetypes[data['archetype']] if 'archetype' in data else None,
                    'type_id': types[data['type']] if 'type' in data else None,
                }
                print(card_data)
                Card.create(card_data)
                for image in data['card_images']:
                    filepath = Path(f"{app.static_folder}/img/card_image/{image['id']}.jpg")
                    if not Path.is_file(filepath): 
                        save_image(filepath, image['image_url'])
                    filepath_smoll = Path(f"{app.static_folder}/img/card_image_small/{image['id']}.jpg")
                    if not Path.is_file(filepath_smoll): 
                        save_image(filepath_smoll, image['image_url_small'])
    else: 
        print("Query Already Ran " + request.form['query'] + " moving onto getting them from our DB...")
    cards = model_card.Card.get_all_with_name(request.form['query'])
    if not cards:
        return jsonify({'error' : 'Card not found! Search only for card names'})
    # we must keep in line with JSON format.
    # requests has a method to convert the data coming back into JSON.
    print(cards)
    cardsJson = {"data" : []}
    if 'cards' not in session:
        session['cards'] = {}

    for item in cards:
        card_data = {}
        cardsJson['data'].append({
                "pin" : item.pin
                # "name" : item.name, 
                # "description" : item.description, 
                # "attack" : item.attack, 
                # "defense": item.defense, 
                # "level": item.level, 
                # "attribute_id": item.attribute_id, 
                # "race_id": item.race_id, 
                # "archetype_id": item.archetype_id,
                # "type_id": item.type_id
        })

    print(cardsJson)
    return jsonify(cardsJson)

@app.route("/card/<int:pin>.json")
def card_json(pin):
    card = Card.get_one_with_pin({"pin": pin})
    cardJSON = {
                "pin" : card.pin, 
                "name" : card.name, 
                "description" : card.description, 
                "attack" : card.attack, 
                "defense": card.defense, 
                "level": card.level, 
                "attribute_id":card.attribute_id,
                "attribute":  model_attribute.Attribute.get_one({"id" : card.attribute_id}).name if card.attribute_id is not None else None, 
                "race_id": card.race_id, 
                "race" :  model_race.Race.get_one({"id" : card.race_id}).name if card.race_id is not None else None, 
                "archetype_id": card.archetype_id,
                "archetype" :  model_archetype.Archetype.get_one({"id" : card.archetype_id}).name if card.archetype_id is not None else None,  
                "type_id": card.type_id,
                "type": model_type.Type.get_one({"id": card.type_id}).name if card.type_id is not None else None,
                "link_markers": card.link_markers if card.link_markers is not None else None
    }
    print (cardJSON)
    return jsonify(cardJSON)


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