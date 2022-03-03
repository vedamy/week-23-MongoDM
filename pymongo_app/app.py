from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)

#setup mongo connection with database
app.config['MONGO_URI']="mongodb://localhost:27017/shows_db"
mongo = PyMongo(app)

#connect to collection
tv_shows = mongo.db.tv_shows

#READ
@app.route("/")
def index():
    #find all items in db and save to a variable
    
    all_shows = list(tv_shows.find())

    return render_template('index.html',data=all_shows)

#CREATE
@app.route("/create", methods=["POST", "GET"])

def create_func():
    if request.method=="POST":
        create_data = request.form 

        post_create = {'name':create_data['name'], 
                     'seasons': create_data['seasons'], 
                     'duration': create_data['duration'], 
                     'year': create_data['year'], 
                     'date_added':datetime.datetime.utcnow()}

        tv_shows.insert_one(post_create)

        return "<p>Document Created Successfully.</p>"
    else:
        return render_template("create_form.html")
    

#UPDATE
@app.route("/update", methods=["POST", "GET"])

def update_func():
    if request.method=="POST":
        update_data = request.form 

        to_update = {'name':update_data['to_update']}

        post_update = {"$set":{'name':update_data['name'], 
                               'seasons': update_data['seasons'], 
                               'duration': update_data['duration'], 
                               'year': update_data['year']}}

        tv_shows.update_one(to_update, post_update)

        return "<p>Document Updated Successfully.</p>"

    else:
        return render_template("update_form.html")

#DELETE
@app.route("/delete", methods=["POST", "GET"])

def delete_func():
    if request.method=="POST":
        delete_data = request.form
        
        post_delete = {'name':delete_data['to_delete']}

        tv_shows.delete_one(post_delete)

        return "<p>Document Deleted Successfully.</p>"
    
    else:
        return render_template("delete_form.html")

if __name__ == "__main__":
    app.run(debug=True)