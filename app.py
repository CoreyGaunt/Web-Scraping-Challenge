from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)
conn = 'mongodb://localhost:27017'
mongo = pymongo.MongoClient(conn)
db = mongo.mars_db
collection = db.mars_info


@app.route("/")
def index():
   mars = collection.find_one()
   return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = collection
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)