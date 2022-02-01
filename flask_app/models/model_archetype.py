#Get the connection 
from lib2to3.refactor import get_all_fix_names
from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import DATABASE_SCHEMA
# DATABASE = 'CHANGE DATABASE'
#REMEMBER TO REPLACE THE TABLE



class Archetype:
    def __init__(self,data): #DON'T FORGET TO INITIALIZE EVERY FIELD YOU USE
        self.id = data['id']
        self.name = data['name']
        
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']
    
    #get_all
    #get_one
    #create / save
    #update_one
    #delete_one

    #if you use data then remember to match up the %(same_key)s 

    # C
    @classmethod #ONLY CALL THIS IF THE ARCHETYPE ISN'T FOUND!
    def create(cls,data:dict) -> int: #The expected return is int
        query = "INSERT INTO archetypes (name) VALUES (%(name)s)"
        user_id = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return user_id


    @classmethod #ONLY CALL THIS IF THERE IS A LARGE LIST THAT NEEDS TO BE ADDED
    def create_many(cls,data:list) -> int: #The expected return is int
        print("attempting to create many!")
        current = cls.get_all()
        current_list = []
        for item in current:
            current_list.append(item.name)
        print(current_list)
        print(data.json())
        query = "INSERT INTO archetypes (name) VALUES (%(archetype_name)s);"
        user_id = 0
        for item in data.json():
            if not current_list or item["archetype_name"] not in current_list:
                print(item['archetype_name'] + " is not currently listed")
                user_id = connectToMySQL(DATABASE_SCHEMA).query_db(query,item )

        return user_id
    # R
    @classmethod
    def json_all_id_name(cls):
        archetypes = cls.get_all()
        # print(archetypes)
        data = {}
        for item in archetypes:
            data[item.id] = item.name  
        return data
    @classmethod
    def json_all_name_id(cls):
        archetypes = cls.get_all()
        # print(archetypes)
        data = {}
        for item in archetypes:
            data[item.name] = item.id  
        return data

    @classmethod
    def get_all(cls) -> list: #This is a get all and will return a list of dictionaries
        query = "SELECT * FROM archetypes;"
        results_from_db =  connectToMySQL(DATABASE_SCHEMA).query_db(query) #Gets a list of dictionaries....
        to_object =[] 
        if results_from_db:
            for values in results_from_db :  #turn those dictionaries into objects
                to_object.append(cls(values))
            return to_object
        else : return []
    

    @classmethod
    def get_one(cls, data) -> list: #this is the same
        query = "SELECT * FROM archetypes WHERE id= %(id)s "
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        to_object = []
        if results_from_db:
            return cls(results_from_db[0])
        else : return []

    @classmethod #use this to get the id
    def get_one_with_name(cls, data) -> list: #this is the same
        query = "SELECT * FROM archetypes WHERE name = %(name)s "
        results_from_db = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        to_object = []
        if results_from_db:
            return cls(results_from_db[0])
        else : return []
            
    # U
    @classmethod 
    def update(cls,data): #RETURNS NOTHING
        query = "UPDATE archetypes SET name=%(name)s WHERE id=%(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

    # D
    @classmethod  #Shouldn't have a way to actually call this....
    def delete(cls,data): #RETURNS NOTHING
        query = "DELETE FROM archetypes WHERE id=%(id)s;"
        # This would target a field and flag is as disabled so we get to keep the data.
        # query = "UPDATE {TABLE} SET account_disabled=true WHERE id = %(id)s"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
