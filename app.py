from flask import Flask, render_template, json, request, redirect, url_for
from flask.ext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cse305'
app.config['MYSQL_DATABASE_DB'] = 'bucketlist'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

curID = 0
source = 'New York City'
dest = 'Boston'

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/transportation")
def transportation():
    return render_template('transportation.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showLoc')
def getLoc():
    cursor.execute('SELECT city, state, country FROM location')
    data = cursor.fetchall() # returns list of tuples
    return render_template('loc.html',data = data)

@app.route('/srcdst', methods=['POST'])
def setSourceDest():
    source = request.form['source']
    dest = request.form['dest']
    return render_template('srcdst.html',src=source, dst=dest)

@app.route('/signUp', methods=['POST'])
def signUp():
    # create user code will be here !!
    # read the posted values from the UI
    _FName = request.form['inputFName']
    _LName = request.form['inputLName']
    _ID = request.form['inputID']
    curID = _ID
    _password = request.form['inputPassword']
    _Age = request.form['inputAge']
    query = ('INSERT INTO Passenger (Id, Age, FName, LName, pWord)' 'VALUES (%s,%s,%s,%s,%s)')
    data = (_ID, _Age, _FName, _LName, _password);
    try:
        cursor.execute(query,data)
        conn.commit();
    except:
        return render_template('signup.html', error='Sign Up Error: ID# already in use')

    return render_template('index.html', nameNew=_FName)

@app.route('/signIn', methods=['POST'])
def signIn():
    _ID = request.form['inputID']
    curID = _ID
    _password = request.form['inputPassword']
    query = ('SELECT Passenger.Id FROM Passenger WHERE Passenger.Id = %s AND Passenger.pWord = %s')
    data = (_ID, _password);
    cursor.execute(query,data)

    ID = cursor.fetchone();
    if ID is not None:
        query = ('SELECT Passenger.FName FROM Passenger WHERE Passenger.Id = %s')
        data = (_ID);
        cursor.execute(query, data)
        Name = cursor.fetchone()[0];
        return render_template('index.html', name=Name)

    return render_template('signup.html', error='Sign In Error: invalid ID or password')

@app.route('/signInFail')
def signInFail():
    return render_template('signupFail.html', error='true')

@app.route('/searchTransportation', methods=['POST'])
def searchTransportation():
    query = ('SELECT Location.Id FROM Location WHERE Location.City = %s')
    data = (source);
    cursor.execute(query, data)
    sourceID = cursor.fetchone()[0];

    query = ('SELECT Location.Id FROM Location WHERE Location.City = %s')
    data = (dest);
    cursor.execute(query, data)
    destID = cursor.fetchone()[0];
    query = ('SELECT TransportationMethod.Id, TransportationMethod.Cost, TransportationMethod.Type FROM TransportationMethod, TravelsTo WHERE TransportationMethod.Id = TravelsTo.TransportationId AND TravelsTo.SourceId = %s AND TravelsTo.DestinationId = %s')
    data = (sourceID, destID)
    cursor.execute(query, data)

    options = cursor.fetchall();

    return json.dumps({'options':options, 'source':source, 'dest':dest})


if __name__ == "__main__":
    app.run()
