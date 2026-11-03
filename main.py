from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import pickle
from datetime import datetime
from plantcare_fetcher import fetch_all_plants
import json


class Base(DeclarativeBase):
    pass


app = Flask(__name__)

# Configureer database
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)


class PlantCare(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column()
    image_path: Mapped[str] = mapped_column(nullable=True)


with app.app_context():
    db.create_all()


def db_recently_updated() -> bool:
    """ Return whether database was updated in the last 3 days """
    try:
        last_db_update_timestamp = pickle.load(open('last_db_update', 'rb'))
    except FileNotFoundError:
        return False

    timedelta = last_db_update_timestamp - datetime.now()
    if timedelta.days < 3:
        return True
    else:
        return False


def update_db(tries=3):
    """Upload all .json plant information to the database"""
    if tries <= 0:
        exit()

    try:
        plants_index = json.load(open('plants/index.json', 'r'))
    except FileNotFoundError:
        fetch_all_plants()
        update_db(tries=tries-1)

    with app.app_context():
        for plant in plants_index:
            file_path = plant['file_path']
            try:
                plant_info = json.load(open(file_path, 'r'))
                print(file_path)
            except FileNotFoundError:
                continue
            plant = PlantCare(
                id=plant_info['id'], name=plant_info['commonName'], image_path=plant_info.get('featuredImage', None))
            db.session.merge(plant)
        db.session.commit()

@app.route("/plants")
def plants():
    return render_template('plants.html', plants=[])


@app.route("/")
def home():
    return render_template('home.html', test="HBV")


@app.route("/settings")
def settings():
    return render_template('settings.html', test="HBV")


def main():
    # Check if db was recently updated
    if not db_recently_updated():
        print("Plant data hasn't been updated recently, updating...")
        fetch_all_plants()

    update_db()

    app.run(debug=True)


if __name__ == "__main__":
    main()
