#Get the connection 
from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import DATABASE_SCHEMA
# DATABASE = 'CHANGE DATABASE'
#REMEMBER TO REPLACE THE TABLE


 # there are only 6... 'dark', 'earth', 'fire', 'light', 'water', 'wind' or 'divine'

class Attribute:
    def __init__(self,data): #DON'T FORGET TO INITIALIZE EVERY FIELD YOU USE
        self.id = data['id']
        self.name = data['name']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    #get_all
    #get_one
    #create / save
    #update_one
    #delete_one

    #if you use data then remember to match up the %(same_key)s 

    # C 
    @classmethod #This should only be called once to setup... Or ya know not at all...
    def create(cls,data:dict) -> int: #The expected return is int
        query = "INSERT INTO attributes (name) VALUES (%(name)s);"
        user_id = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return user_id
   
    # R 
    @classmethod
    def json_all_id_name(cls):
        attributes = cls.get_all()
        # print(archetypes)
        # print(attributes)
        data = {}
        for key in attributes:
            data[key.id] = key.name
        return data
    @classmethod
    def json_all_name_id(cls):
        attributes = cls.get_all()
        # print(archetypes)
        # print(attributes)
        data = {}
        for key in attributes:
            data[key.name] = key.id
        return data


    @classmethod
    def get_all(cls) -> list: #This is a get all and will return a list of dictionaries
        query = "SELECT * FROM attributes;"
        results_from_db =  connectToMySQL(DATABASE_SCHEMA).query_db(query) #Gets a list of dictionaries....
        to_object =[] 
        if results_from_db:
            for values in results_from_db :  #turn those dictionaries into objects
                to_object.append(cls(values))
            return to_object
        else : return []

    @classmethod
    def get_one(cls, data) -> list: #this is the same
        query = "SELECT * FROM attributes WHERE id= %(id)s;"
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        to_object = []
        if results_from_db:
            return cls(results_from_db[0])
        else : return []
    
    @classmethod
    def get_one_with_name(cls, data) -> list: #this is the same
        query = "SELECT * FROM attributes WHERE name= %(name)s;"
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        to_object = []
        if results_from_db:
            return cls(results_from_db[0])
        else : return []
    # U
    @classmethod #this should never be called...
    def update(cls,data): #RETURNS NOTHING
        query = "UPDATE attributes SET name= %(name)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

    # D
    @classmethod 
    def delete(cls,data): #RETURNS NOTHING
        query = "DELETE FROM attributes WHERE id=%(id)s;"
        # This would target a field and flag is as disabled so we get to keep the data.
        # query = "UPDATE {TABLE} SET account_disabled=true WHERE id = %(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
