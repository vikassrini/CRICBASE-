from flask import Flask, render_template
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__,template_folder='./static')

def connect_to_database():
    try:
        cnx = mysql.connector.connect(host = "localhost", user = "root", password = "root123", database='CRICBASE')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return cnx

@app.route('/')
def index():
    cnx = connect_to_database()
    cursor = cnx.cursor()

    query = "DESC TOURNAMENT"
    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    cnx.close()

    return render_template('index.html', rows=rows)

if __name__ == '_main_':
    app.run()