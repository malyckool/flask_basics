from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config.update(
    SECRET_KEY='topsecret',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:earths@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

@app.route('/')
@app.route('/index')
def hello_world():
    return 'Hello World!'

@app.route("/new/")
def query_string(greeting="hello"):
    query_val = request.args.get('greeting',greeting)
    return "<h1>the greetin is : {0}</h1>".format(query_val)

@app.route("/user/")
@app.route("/user/<name>")
def no_query_string(name="Malyck"):
    return "<h1>Hello dear {0}</h1>".format(name)

#strings

@app.route("/text/<string:name>")
def working_with_strings(name):
    return "<h1>Here is a string: " + name + "</h1>"

#numbers

@app.route("/number/<int:num>")
def working_with_numbers(num):
    return "<h1>Here is a string: " + str(num) + "</h1>"

@app.route("/add/<int:num1>/<int:num2>")
def adding_integers(num1,num2):
    return "<h1>Here is a string: {}".format(num1+num2) + "</h1>"

#floats
@app.route("/product/<float:num1>/<float:num2>")
def product_two_number(num1,num2):
    return "<h1>Here is a string: {}".format(num1*num2) + "</h1>"

#Using Templates
@app.route("/temp/")
def using_templates():
    return render_template("hello.html")

#Jinja template
@app.route("/watch/")
def movies_2018():
    movie_list=["Avengers: Infinity WarFare",
                "Ocean's 8",
                "Solo : A Star Wars Movie,"
                "Equalizer 2",
                "The big bang Theory"]

    return render_template("movies.html", movies=movie_list, name="Malyck")

@app.route("/tables/")
def movies_plus():
    movie_list={"Avengers: Infinity WarFare":02.50,
                "Ocean's 8":01.37,
                "Solo : A Star Wars Movie":01.50,
                "Equalizer 2":03.51,
                "The big bang Theory":01.45}

    return render_template("table_data.html", movies=movie_list, name="Malyck")

@app.route("/filter/")
def filter_data():
    movie_list = {"Avengers: Infinity WarFare": 02.50,
                  "Ocean's 8": 01.37,
                  "Solo : A Star Wars Movie": 01.50,
                  "Equalizer 2": 03.51,
                  "The big bang Theory": 01.45}

    return render_template("filter_data.html", movies=movie_list, name=None, film="Terminator 3")

@app.route("/macro/")
def jinja_macros():
    movie_list={"Avengers: Infinity WarFare":02.50,
                "Ocean's 8":01.37,
                "Solo : A Star Wars Movie":01.50,
                "Equalizer 2":03.51,
                "The big bang Theory":01.45}

    return render_template("using_macro.html", movies=movie_list)

class Publication(db.Model):
    __tablename__="publication"

    id= db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return "The id is {}, Name is {}".format(self.id,self.name)

class Book(db.Model):
    __tablename__="book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500),nullable=False,index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(50), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    #Relationship
    pub_id = db.Column(db.Integer,db.ForeignKey('publication.id'))

    def __init__(self,title,author,avg_rating,book_format,image,num_pages,pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return "{} by {}".format(self.title,self.author)



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
