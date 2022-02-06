#Get the connection 
from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import DATABASE_SCHEMA
# DATABASE = 'CHANGE DATABASE'
#REMEMBER TO REPLACE THE TABLE

class DeckList:
    def __init__(self,data): #DON'T FORGET TO INITIALIZE EVERY FIELD YOU USE
        self.id = data['card_id']
        self.count = data['count']
        self.card_pin = data['card_pin']
        self.deck_id = data['deck_id']
    
        # self.created_at = data['created_at']
        # self.updated_at = data['updated_at']
    #get_all
    #get_one
    #create / save
    #update_one
    #delete_one

    #if you use data then remember to match up the %(same_key)s 

    # C
    @classmethod
    def create(cls,data:dict) -> int: #The expected return is int Location is a simple 0 1 2 -> Main Extra Side
        print(data)
        query = "INSERT INTO decklists (count, card_pin, deck_id) VALUES (%(count)s, %(card_pin)s, %(deck_id)s)"
        user_id = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return user_id

    # R
    @classmethod
    def get_all(cls) -> list: #This is a get all and will return a list of dictionaries
        query = "SELECT * FROM authors;"
        results_from_db =  connectToMySQL(DATABASE_SCHEMA).query_db(query) #Gets a list of dictionaries....
        to_object =[] 
        if results_from_db:
            for values in results_from_db :  #turn those dictionaries into objects
                to_object.append(cls(values))
            return to_object
        else : return []
        

    @classmethod
    def get_one(cls, data) -> list: #this is the same
        query = "SELECT * FROM decklists WHERE id= %(id)s "
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        to_object = []
        if results_from_db:
            for values in results_from_db :  #turn those dictionaries into objects
                to_object.append(cls(values))
            return to_object
        else : return []
    
    @classmethod
    def get_one_with_deck_id(cls, data) -> list: #This is going to sift through all the connections to find relationships where the deck id is that... That should get us all the cards related to that deck
        query = "SELECT * FROM decklists WHERE deck_id = %(deck_id)s "
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        to_object = []
        if results_from_db:
            for values in results_from_db :  #turn those dictionaries into objects
                to_object.append(cls(values))
            return to_object
        else : return []
            

    # U
    @classmethod
    def save(cls,data): #RETURNS NOTHING
        query = "UPDATE {CLASS} SET value= %(value)s WHERE id=%(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

    # D
    @classmethod 
    def delete(cls,data): #So as it stands this is going to delete the entire deck.... then update it with the new one
        query = "DELETE FROM decklists WHERE deck_id=%(deck_id)s;"
        # This would target a field and flag is as disabled so we get to keep the data.
        # query = "UPDATE {TABLE} SET account_disabled=true WHERE id = %(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
    
    @classmethod
    def validate(cls,data):
        errorMessages = {}
        cardCount = 0
        for item in data['main']:
            cardCount += data['main'][item]
        
        print(f"main Deck {cardCount}")
        if cardCount < 40:
            errorMessages['main_deck_err'] = "Too few Cards in main deck. Main deck Must be between 40 and 60 cards"
        elif cardCount > 60:
            errorMessages['main_deck_err'] = "Too Many Cards in main deck. Main deck must be between 40 and 60 cards"

        cardCount = 0
        for item in data['extra']:
            cardCount += int(data['extra'][item])
            pass
        if(cardCount > 15):
            errorMessages['extra_deck_err'] = "Extra Deck is too large. Extra Deck Must be between 0 and 15 cards"
        print(f"extra Deck {cardCount}")
        return errorMessages