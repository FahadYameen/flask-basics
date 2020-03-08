from flask import Flask
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.update(
    SECRET_KEY = 'topsecret',
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:incorrect17?@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db= SQLAlchemy(app)

@app.route('/')
def hello_flask():
    return("hello world")

@app.route('/new')
def query_string(greeting='default'):
    greeting_value=request.args.get('greeting',greeting)
    return("the greeting is {}".format(greeting_value))

@app.route('/user/')
@app.route('/user/<name>')
def no_query_string(name='default'):
    return("hello there {}".format(name))

#INTEGERS
@app.route('/integer/<int:number>')
def working_with_integer(number):
    return("The input number is {}".format(number))

#float
@app.route('/float/<float:number>')
def working_with_float(number):
    return("The input number is {}".format(number))

#html_render
@app.route('/temp')
def redirect_to_html_file():
    return(render_template('temp.html'))


#watch movies page
@app.route('/watch')
def watch_movies():
    movie_list=['Money Heist','War','Breaking bad']
    return(render_template('movies.html',movies=movie_list))

@app.route('/movie_details')
def movie_details():
    movie_details_dict={'Money Heist':1.2,'War':3.5,'Breaking bad':5.7}
    return(render_template('movie_table.html',movie_dict=movie_details_dict))

@app.route('/macros')
def jinja_macros():
    movie_details_dict={'Money Heist':1.2,'War':3.5,'Breaking bad':5.7}
    return(render_template('using_macros.html',movie_dict=movie_details_dict))

@app.route('/api')
@app.route('/api/sample')
def return_json():
    movie_details_dict={'Money Heist':1.2,'War':3.5,'Breaking bad':5.7}
    return movie_details_dict


class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable = False)

    def __init__(self,name):

        self.name = name
         
    def __repr__(self):

        return('name is {} '.format(self.name))

class Book(db.Model):

    __table_name__ = 'book'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(500),nullable = False, index = True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100),unique = True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime,default = datetime.utcnow())

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
        
        return('{} by {}'.format(self.title,self.author))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
