from flask import Flask, render_template, redirect, request
from flask_app import app
from flask_app.controllers import controller_ygo_api, controller_user, controller_archetype, controller_attributes, controller_races

if __name__=="__main__":
    app.run(debug=True)