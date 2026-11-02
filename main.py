from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


app = Flask(__name__)

# Configureer database
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]


with app.app_context():
    db.create_all()


@app.route("/plants")
def plants():
    return render_template('plants.html', test="HBV")


@app.route("/")
def home():
    return render_template('Home.html', test="HBV")


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
