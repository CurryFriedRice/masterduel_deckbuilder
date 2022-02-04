#Get the connection 
from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import DATABASE_SCHEMA
# DATABASE = 'CHANGE DATABASE'
#REMEMBER TO REPLACE THE TABLE

class Deck:
    def __init__(self,data): #DON'T FORGET TO INITIALIZE EVERY FIELD YOU USE
        self.id = data['id']
        self.name= data['name']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    #get_all
    #get_one
    #create / save
    #update_one
    #delete_one

    #if you use data then remember to match up the %(same_key)s 

    # C
    @classmethod
    def create(cls,data:dict) -> int: #The expected return is int
        query = "INSERT INTO decks (name, description, user_id) VALUES (%(name)s, %(description)s, %(user_id)s)"
        user_id = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return user_id

    # R
    @classmethod
    def get_all(cls) -> list: #This is a get all and will return a list of dictionaries
        query = "SELECT * FROM decks ORDER BY updated_at DESC;"
        results_from_db =  connectToMySQL(DATABASE_SCHEMA).query_db(query) #Gets a list of dictionaries....
        to_object =[] 
        if results_from_db:
            for values in results_from_db :  #turn those dictionaries into objects
                to_object.append(cls(values))
            return to_object
        else : return []
    @classmethod
    def get_all_with_name(cls, data) -> list: #This is a get all and will return a list of dictionaries
        query = "SELECT * FROM decks WHERE name LIKE %(name)%;"
        results_from_db =  connectToMySQL(DATABASE_SCHEMA).query_db(query) #Gets a list of dictionaries....
        to_object =[] 
        if results_from_db:
            for values in results_from_db :  #turn those dictionaries into objects
                to_object.append(cls(values))
            return to_object
        else : return []
    
    @classmethod
    def get_all_with_uuid(cls, data) -> list: #This is a get all and will return a list of dictionaries
        query = "SELECT * FROM decks WHERE user_id=%(uuid)s ORDER BY updated_at DESC"
        results_from_db =  connectToMySQL(DATABASE_SCHEMA).query_db(query,data) #Gets a list of dictionaries....
        to_object =[] 
        if results_from_db:
            for values in results_from_db :  #turn those dictionaries into objects
                to_object.append(cls(values))
            return to_object
        else : return []
        

    @classmethod
    def get_one(cls, data) -> list: #this is the same
        query = "SELECT * FROM decks WHERE id= %(id)s "
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        to_object = []
        if results_from_db:
            return cls(results_from_db[0])
            for values in results_from_db :  #turn those dictionaries into objects
                to_object.append(cls(values))
            return to_object
        else : return []

    @classmethod
    def get_one_with_uuid(cls, data) -> list: #this is the same
        query = "SELECT * FROM decks user_id= %(user_id)s;"
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        to_object = []
        if results_from_db:
            return cls(results_from_db[0])
            for values in results_from_db :  #turn those dictionaries into objects
                to_object.append(cls(values))
            return to_object
        else : return []
    # U
    @classmethod
    def update(cls,data): #RETURNS NOTHING
        query = "UPDATE decks SET name=%(name)s, description=%(description)s WHERE id=%(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

    # D
    @classmethod 
    def delete(cls,data): #RETURNS NOTHING
        query = "DELETE FROM {TABLE} WHERE id=%(id)s;"
        # This would target a field and flag is as disabled so we get to keep the data.
        # query = "UPDATE {TABLE} SET account_disabled=true WHERE id = %(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)


    @classmethod
    def validate(cls, data):
        errorMessages = {}
        print(data)
        if not data['name']:    
            errorMessages['deck_name_err'] = "You must enter a deck name"
        elif len(data['name']) < 3:
            errorMessages['deck_name_err'] = "Your deck name must be at least 3 characters long"
        
        return errorMessages