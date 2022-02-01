from functools import cached_property
from importlib.resources import path
import urllib.response, requests, os
# from numpy import image
from flask_app import app
from flask import jsonify, redirect, render_template, request 
# import PIL
from PIL import Image
from pathlib import Path

from flask_app.models import model_card, model_query, model_archetype, model_attribute, model_race, model_type

# EXAMPLE DATA
data ={'data': 
    [{  'id': 91152256, 
        'name': 'Celtic Guardian', 
        'type': 'Normal Monster', 
        'desc': 'An elf who learned to wield a sword, he baffles enemies with lightning-swift attacks.', 
        'atk': 1400, 
        'def': 1200, 
        'level': 4, 
        'race': 'Warrior', 
        'attribute': 'EARTH', 
        'archetype': 'Celtic Guard', 
            'card_images': [{
                'id': 91152256, 
                'image_url': 'https://storage.googleapis.com/ygoprodeck.com/pics/91152256.jpg', 
                'image_url_small': 'https://storage.googleapis.com/ygoprodeck.com/pics_small/91152256.jpg'}, 
                {'id': 91152257, 
                'image_url': 'https://storage.googleapis.com/ygoprodeck.com/pics/91152257.jpg',
                'image_url_small': 'https://storage.googleapis.com/ygoprodeck.com/pics_small/91152257.jpg'}, 
                {'id': 91152258, 'image_url': 'https://storage.googleapis.com/ygoprodeck.com/pics/91152258.jpg', 
                'image_url_small': 'https://storage.googleapis.com/ygoprodeck.com/pics_small/91152258.jpg'
                }]
        }]}

data2 = {
    'card_image': [{
        'id' : 91152256,
        'image_url' : 'E:/Applications/SourceTree/_test/image/91152256.jpg',
        'image_url_small' : 'E:/Applications/SourceTree/_test/image_small/91152256.jpg'
    },]
}
                        # 'card_prices': 
                        # [{'cardmarket_price': '0.07', 'tcgplayer_price': '0.25', 'ebay_price': '999.99', 'amazon_price': '1.68', 'coolstuffinc_price': '11.99'}]}
                        # ]}


def save_image(path, source):
    print(app.static_folder)
    print(source)
    print(str(path))
    urllib.request.urlretrieve(source,str(path))
    # image = Image.open("gfg.png")
    # image = image.save(path)#app.static_folder+ f"\img\card_image\{id}.jpg")
    # image_list = data['card_image'] #simulate the handing in of the list of objects

    


@app.route('/api/ygo/search', methods=['POST'])
def search_card_api():
    print(request.form['query'])
    r = model_query.Query.get_one_with_query({"query" : request.form['query']})
    if not r:
        r =  {'data':   [{'id': 91152256, 'name': 'Celtic Guardian', 'type': 'Normal Monster', 'desc': 'An elf who learned to wield a sword, he baffles enemies with lightning-swift attacks.', 'atk': 1400, 'def': 1200, 'level': 4, 'race': 'Warrior', 'attribute': 'EARTH', 'archetype': 'Celtic Guard', 
                            'card_images': [{'id': 91152256, 'image_url': 'https://storage.googleapis.com/ygoprodeck.com/pics/91152256.jpg', 'image_url_small': 'https://storage.googleapis.com/ygoprodeck.com/pics_small/91152256.jpg'}, 
                                            {'id': 91152257, 'image_url': 'https://storage.googleapis.com/ygoprodeck.com/pics/91152257.jpg', 'image_url_small': 'https://storage.googleapis.com/ygoprodeck.com/pics_small/91152257.jpg'}, 
                                            {'id': 91152258, 'image_url': 'https://storage.googleapis.com/ygoprodeck.com/pics/91152258.jpg', 'image_url_small': 'https://storage.googleapis.com/ygoprodeck.com/pics_small/91152258.jpg'}]
                        },
                        {"id":53129443,"name":"Dark Hole","type":"Spell Card","desc":"Destroy all monsters on the field.","race":"Normal","archetype":"Hole", 
                            "card_images": [{"id":53129443,"image_url":"https://storage.googleapis.com/ygoprodeck.com/pics/53129443.jpg","image_url_small":"https://storage.googleapis.com/ygoprodeck.com/pics_small/53129443.jpg"}]
                        }
            ]}


        #requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?fname={request.form['query']}")
        #card_query = MODEL
        #prpare the data to set IDs
        attributes = model_attribute.Attribute.json_all_name_id()
        races = model_race.Race.json_all_name_id()
        archetypes = model_archetype.Archetype.json_all_name_id()
        types = model_type.Type.json_all_name_id()

        # cards = model_card.Card.get_all_with_name()
        #print(response.json())
        resJson = r#.json()
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


    # cards = model_card.Card.get_all_with_name({"name": request.form['query']})
    # # we must keep in line with JSON format.
    # # requests has a method to convert the data coming back into JSON.
    # print(cards)
    # cardsJson = {}
    # i = 0
    # for item in cards:
    #     cardsJson[i] = {
    #             "card_id" : item.card_id, 
    #             "name" : item.name, 
    #             "description" : item.description, 
    #             "attack" : item.attack, 
    #             "defense": item.defense, 
    #             "level": item.level, 
    #             "attribute_id": item.attribute_id, 
    #             "race_id": item.race_id, 
    #             "archetype_id": item.archetype_id,
    #             "type_id": item.type_id
    #     }
    #     i = i + 1
    # print(cardsJson)
    return "HONK" #jsonify(cardsJson)


@app.route("/all/tags")
def all_tags_test():
    # Send this to the client when they're searching cards...
    # There's going to be another one for card packs 
    res = { "attributes" : model_attribute.Attribute.json_all_name_id(),
            "archetypes" : model_archetype.Archetype.json_all_name_id(),
            "type":model_type.Type.json_all_name_id(),
            "race":model_race.Race.json_all_name_id()
            }

    return res 
# no route... this is called after the card search


@app.route("/archetypes/setup")
def setup_archetypes():
    
    response = requests.get(f"https://db.ygoprodeck.com/api/v7/archetypes.php")
    model_archetype.Archetype.create_many(response)
    
    return "Nothing"
