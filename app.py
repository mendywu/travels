from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cse305'
app.config['MYSQL_DATABASE_DB'] = 'TravelAgency'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
session = 1113 # holds the PassengerID who is logged in
grp = []

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    # create user code will be here !!
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _email and _password:
        #return json.dumps({'html':'<span>All fields good !!</span>'})
        cursor.callproc('sp_createUser',(_name,_email,_password))

        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
            return json.dumps({'error':str(data[0])})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/joinGroup')
def joinGroup():
    return render_template('group.html')

@app.route('/searchGroup',methods=['POST'])
def checkGroup():
    if session is -1:
        return json.dumps({'result': 0})

    grp_id = request.form['grpID']
    query = ('SELECT PassengerId FROM ParticipatesIn WHERE GrpId=%s')

    cursor.execute(query,grp_id)
    result = cursor.fetchall()
    passengers = []
    inGroup = 0
    for id in result:
        passenger_id = id[0]
        query = ('SELECT * FROM Passenger WHERE Id=%s')
        cursor.execute(query,passenger_id)
        passengers += cursor.fetchall()
        if passenger_id == session:
            inGroup = 1

    if len(result) is 0:
        return json.dumps({'result':-1})
    else:
        return json.dumps({'result':1,'GrpID':grp_id, 'Passengers':passengers,'inGroup':inGroup})

@app.route('/createGroup',methods=['POST'])
def createGroup():

    _id = request.form['inputGrpID']
    _size = request.form['inputGrpSize']
    _purpose = request.form['inputGrpPurpose']

    #return json.dumps({'message':_id, 'size':_size, 'purpose':_purpose})
    query = ('SELECT PassengerId FROM ParticipatesIn WHERE GrpId=%s')
    cursor.execute(query,_id)
    result = cursor.fetchall()
    if len(result) != 0:
        return json.dumps({'message':-1})

    query = ('INSERT INTO Grp (Id,Size,Purpose)' 'VALUES (%s,%s,%s)')
    data = (int(_id), int(_size), _purpose)
    cursor.execute(query,data)

    query = ('INSERT INTO ParticipatesIn (PassengerId,GrpId)' 'VALUES (%s,%s)')
    data = (session,_id)
    cursor.execute(query,data)
    conn.commit()

    return json.dumps({'message':"added successfully"})
    #return render_template('signup.html')

@app.route('/joinGroupOfficially',methods=['POST'])
def joinGroupOfficially():

    group_id = request.form['grpID']

    query = ('SELECT PassengerID FROM ParticipatesIn WHERE GrpId = %s AND PassengerID=%s')
    cursor.execute(query,(group_id,session))
    result = cursor.fetchall()
    if len(result) != 0:
        return json.dumps({'message':-1})

    query = ('INSERT INTO ParticipatesIn (PassengerId,GrpId)' 'VALUES (%s,%s)')
    data = (session,group_id)
    cursor.execute(query,data)
    conn.commit()

    return json.dumps({'message':1})

@app.route('/leaveGroup',methods=['POST'])
def leaveGroup():
    group_id = request.form['grpID']

    query = ('DELETE FROM ParticipatesIn WHERE GrpId = %s AND PassengerID=%s')
    cursor.execute(query,(group_id,session))

    query = ('SELECT PassengerId FROM ParticipatesIn WHERE GrpId = %s')
    cursor.execute(query,(group_id))
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.execute(('DELETE FROM Grp WHERE Id = %s'),(group_id))
    conn.commit()

    return json.dumps({'message':1})

if __name__ == "__main__":
    app.run()
