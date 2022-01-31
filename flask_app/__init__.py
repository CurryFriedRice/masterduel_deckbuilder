from flask import Flask
app = Flask(__name__)
app.secret_key ='&AC9xXMjyEhBMh'
# so what I want to do is img.save(app.static_folder+"/"+cardId+".jpg")



if __name__=="main":
    app.run(debug=True)

DATABASE_SCHEMA='masterduel'

