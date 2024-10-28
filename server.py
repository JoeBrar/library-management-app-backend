from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
from blueprints.books import books
from blueprints.members import members
from blueprints.transactions import transactions
from blueprints.default import default
from dotenv import load_dotenv
import requests
import os

load_dotenv()
app=Flask(__name__)
CORS(app)
tmp=os.getenv('db_url')
app.config['MYSQL_HOST']=os.getenv('MYSQL_HOST')
app.config['MYSQL_PORT']=int(os.getenv('MYSQL_PORT'))
app.config['MYSQL_USER']=os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD']=os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB']=os.getenv('MYSQL_DB')
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql=MySQL(app)
app.config['mysql']=mysql

app.register_blueprint(books,url_prefix='/')
app.register_blueprint(members,url_prefix='/')
app.register_blueprint(transactions,url_prefix='/')
app.register_blueprint(default,url_prefix='/')

@app.route('/test')
def test():
    print("Server working")
    return "<h3>Server working</h3>"


if __name__=="__main__":
    app.run(debug=True)

    