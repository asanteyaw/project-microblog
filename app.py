import os, datetime
from flask import Flask, render_template, request
from pymongo import MongoClient   # allows to open a client side session to MongoDB
from dotenv import load_dotenv

load_dotenv()  # populate our environment variable from a file called .env

def create_app():  # app factory which prevent issues in deployment. Function name must be "create_app"
  app = Flask(__name__)
  # client = MongoClient("mongodb+srv://asanteyaw:HYJTDwIuQ07Dpg3i@blogapp.jd8c8.mongodb.net/")
  client = MongoClient(os.getenv("MONGODB_URI"))
  app.db = client.microblog   # stores the database in our flask app. To access collections in the db, do app.db.<collection_name>

  # will store the contents of the form
  # entries = []

  @app.route("/", methods=["GET", "POST"])
  def home():
    # .find with an empty dictionary grabs everything there is to fetch in the database
    # entries is the name of our collection in the microblog database
    # so we're basically retrieving data from our database and printing to screen  
    if request.method == "POST":
      """request.form is a dictionary and we call the .get method of the dictionary.
        The "content" is the value we gave to the "name" attribute of the textarea in home.htm
      """
      # datetime object prints a very long date, so we wanna format it to year-month-day
      formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
      entry_content = request.form.get("content")
      # entries.append((entry_content, formatted_date))
      # persistence by storing data in database instead of appending to list like previously
      app.db.entries.insert_one({
          "content": entry_content,
          "date": formatted_date
      })
      
    content = [(
        entry["content"], 
        entry["date"], 
        datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
      ) for entry in app.db.entries.find({})]
    return render_template("home.htm", entries=content)
  
  return app

# HYJTDwIuQ07Dpg3i - mongo db password?
