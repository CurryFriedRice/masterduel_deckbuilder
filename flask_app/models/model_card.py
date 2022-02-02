#Get the connection 
from contextlib import nullcontext
from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import DATABASE_SCHEMA, app
from PIL import Image
import os

# DATABASE = 'CHANGE DATABASE'
#REMEMBER TO REPLACE THE TABLE

class Card:
    def __init__(self,data): #DON'T FORGET TO INITIALIZE EVERY FIELD YOU USE
        self.id = data['id']
        self.pin = data['pin']   # the 8 digit combination        
        self.alternate_pin = data['alternate_pin'] #strings separated by commas

        self.name = data['name']    # This will never be null
        self.description = data['description']  # This will never be null
        self.attack = data['attack'] # this is a minimum of 0
        self.defense = data['defense']# this is a minimum of 0
        self.level = data['level']  # this has a minimum of 0
                                    # This is also used for: RANK, and LINK VALUE

        self.race_id = data['race_id']  # Race 0 is 'NONE' items that have NONE Should be spells or traps
        self.archetype_id = data['archetype_id'] # What Group this card belongs
        self.attribute_id = data['attribute_id'] # So this determins
        self.type_id = data['type_id'] # So this helps determine how a card is laid out
        self.link_markers =  data['link_markers'].split(',') if data['link_markers'] is not None else None # so this is going to be stored as a string.that's going to be split up into an array

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #get_all
    #get_one
    #create / save
    #update_one
    #delete_one

    #if you use data then remember to match up the %(same_key)s 

    def save_image(self, data):
        print(app.static_folder)
        image_list = data['card_image'] #simulate the handing in of the list of objects
        

        for img in image_list:
            image = Image.open(img['image_url'])
            image = image.save(app.static_folder+ f"\img\card_image\{img['id']}.jpg")
            
            image_small = Image.open(img['image_url_small'])
            image_small = image_small.save(app.static_folder+ f"\img\card_image_small\{img['id']}.jpg")
            

        return "uh oh...."

    # C
    @classmethod #We should never really be using this. it fills out EVERY piece of data about a card typically this will be a monster card
    def create(cls,data:dict) -> int: #The expected return is int
        query = "INSERT INTO cards (pin, alternate_pin, name, description, attack, defense, level, link_markers, attribute_id, race_id, archetype_id, type_id) " 
        query +="VALUES (%(pin)s, %(alternate_pin)s, %(name)s, %(description)s, %(attack)s, %(defense)s, %(level)s, %(link_markers)s, %(attribute_id)s, %(race_id)s, %(archetype_id)s, %(type_id)s);"
        user_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return user_id

    @classmethod
    def create_support(cls,data:dict) -> int:
        query = "INSERT INTO cards (pin, alternate_pin, name, description, attribute_id, race_id, archetype_id, type_id) " 
        query +="VALUES (%(pin)s, %(alternate_pin)s, %(name)s, %(description)s, %(attribute_id)s,%(race_id)s, %(archetype_id)s, %(type_id)s);"
        user_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return user_id

    # R
    @classmethod
    def get_all(cls) -> list: #This is a get all and will return a list of dictionaries
        query = "SELECT * FROM cards;"
        results_from_db =  connectToMySQL(DATABASE_SCHEMA).query_db(query) #Gets a list of dictionaries....
        to_object =[] 
        if results_from_db:
            for values in results_from_db :  #turn those dictionaries into objects
                to_object.append(cls(values))
            return to_object
        else : return []

    @classmethod
    def get_all_with_name(cls, data) -> list: #This is a get all and will return a list of dictionaries
        #print("%"+data['name']+"%")
        query = "SELECT * FROM cards WHERE name LIKE '%%%s%%'" % (data)
        results_from_db =  connectToMySQL(DATABASE_SCHEMA).query_db(query) #Gets a list of dictionaries....
        to_object =[] 
        if results_from_db:
            for values in results_from_db :  #turn those dictionaries into objects
                to_object.append(cls(values))
            return to_object
        else : return []
        

    @classmethod
    def get_one(cls, data) -> list: #this is the same
        query = "SELECT * FROM cards WHERE id= %(id)s "
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        to_object = []
        if results_from_db:
            return cls(results_from_db[0])
        else : return []
    
    @classmethod
    def get_one_with_pin(cls, data) -> list: #this is the same
        query = "SELECT * FROM cards WHERE pin= %(pin)s "
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        to_object = []
        if results_from_db:
            return cls(results_from_db[0])
        else : return []
            

    # U
    @classmethod
    def save(cls,data): #RETURNS NOTHING
        query = "UPDATE {CLASS} SET value= %(value)s pin id=%(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

    # D
    @classmethod 
    def delete(cls,data): #RETURNS NOTHING
        query = "DELETE FROM {TABLE} WHERE id=%(id)s;"
        # This would target a field and flag is as disabled so we get to keep the data.
        # query = "UPDATE {TABLE} SET account_disabled=true WHERE id = %(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

