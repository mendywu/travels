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
curID = 1111          # the PassengerID who is logged in
name = "Mendy"           # the name of Passenger that is logged in
grp = 1121             # group selected
source = ""         # source location
destId = 0
dest = ""           # destination location

@app.route("/")
def main():
    return render_template('index.html', name=name)

@app.route("/home")
def home():
    return render_template('index.html', name=name)

@app.route("/transportation")
def transportation():
    return render_template('transportation.html')

@app.route("/payment")
def payment():
    return render_template('payment.html')

############  SIGN IN/SIGN UP TRANSACTIONS  ######################
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    # create user code will be here !!
    # read the posted values from the UI
    _FName = request.form['inputFName']
    _LName = request.form['inputLName']
    _ID = request.form['inputID']
    global curID
    curID = int(_ID)
    _password = request.form['inputPassword']
    _Age = request.form['inputAge']
    query = ('INSERT INTO Passenger (Id, Age, FName, LName, pWord)' 'VALUES (%s,%s,%s,%s,%s)')
    data = (_ID, _Age, _FName, _LName, _password);
    try:
        cursor.execute(query,data)
        conn.commit();
    except:
        return render_template('signup.html', error='Sign Up Error: ID# already in use')

    global name
    name = _FName
    return render_template('index.html', nameNew=_FName)

@app.route('/signIn', methods=['POST'])
def signIn():
    _ID = request.form['inputID']
    global curID
    curID = int(_ID)
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

        global name
        name = Name
        return render_template('index.html', name=Name)

    return render_template('signup.html', error='Sign In Error: invalid ID or password')

@app.route('/signInFail')
def signInFail():
    return render_template('signupFail.html', error='true')

@app.route('/signOut')
def signOut():
    global name
    name = ""
    global curID
    curID = 0
    return render_template('index.html', name=name)

############  GROUP TRANSACTIONS  ######################
@app.route('/joinGroup')
def joinGroup():
    return render_template('group.html',name=name)

@app.route('/selectGroup',methods=['POST'])
def selectGroup():
    global grp
    grp = request.form['grpID']
    return json.dumps({'result':grp})

@app.route('/searchGroup',methods=['POST'])
def checkGroup():
    if curID is 0:
        return json.dumps({'result': 0})

    grp_id = request.form['grpID']
    query = ('SELECT PassengerId FROM ParticipatesIn WHERE GrpId=%s')
    cursor.execute(query,grp_id)
    result = cursor.fetchall()
    if len(result) is 0:
        return json.dumps({'result':-1})
    passengers = []
    inGroup = 0
    for id in result:
        passenger_id = id[0]
        query = ('SELECT * FROM Passenger WHERE Id=%s')
        cursor.execute(query,passenger_id)
        passengers += cursor.fetchall()
        if passenger_id == curID:
            inGroup = 1

    query = ('SELECT Size FROM Grp WHERE Id=%s')
    cursor.execute(query,grp_id)
    size = cursor.fetchall()

    query = ('SELECT TransportationId FROM TravelsBy WHERE GrpId=%s')
    cursor.execute(query,grp_id)
    transport = cursor.fetchall()
    transportationId = 0
    if len(transport) != 0:
        transportationId = transport[0][0]
    else:
        return json.dumps({'result':1,'GrpID':grp_id,'GrpSize':size[0],'Passengers':passengers,'inGroup':inGroup,'Transport':0})

    query = ('SELECT Type, Cost FROM TransportationMethod WHERE Id=%s')
    cursor.execute(query,transportationId)
    transport = cursor.fetchall()
    transportationMethod = 0
    cost = 0
    if len(transport) != 0:
        transportationMethod = transport[0][0]
        cost = transport[0][1]

    date = 0
    if transportationMethod == 'Flight':
        query = ('SELECT Date FROM Flight WHERE Id=%s')
        cursor.execute(query,transportationId)
        transport = cursor.fetchall()
        if len(transport) != 0:
            date = transport[0][0]

    accomName = "None"
    query = ('SELECT AccommodationId FROM StaysIn WHERE GrpId =%s')
    cursor.execute(query,grp_id)
    AccomID = cursor.fetchone()
    if AccomID:
        query = ('SELECT Name,Rate FROM Accommodation WHERE Id =%s')
        cursor.execute(query,AccomID)
        result = cursor.fetchone()
        if result:
            cost += result[1]
            accomName = result[0]

    query = ('SELECT SourceId, DestinationId FROM TravelsTo WHERE TransportationId =%s')
    cursor.execute(query,transportationId)
    location = cursor.fetchall()
    srcId = location[0][0]
    destId = location[0][1]

    query = ('SELECT City FROM Location WHERE Id =%s')
    cursor.execute(query,srcId)
    src_location = cursor.fetchall()
    src = src_location[0][0]

    query = ('SELECT City FROM Location WHERE Id =%s')
    cursor.execute(query,destId)
    dest_location = cursor.fetchall()
    dest_ = dest_location[0][0]

    return json.dumps({'result':1,'GrpID':grp_id,'GrpSize':size[0],'Passengers':passengers,
    'Date':date,'inGroup':inGroup,'Cost':cost,'Transport':transportationMethod,'Location':[src,dest_],'Accom':accomName})

@app.route('/createGroup',methods=['POST'])
def createGroup():
    if name == "":
        return json.dumps({'message':0})

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
    data = (curID,_id)
    cursor.execute(query,data)
    conn.commit()

    return json.dumps({'message':"added successfully"})
    #return render_template('signup.html')

@app.route('/joinGroupOfficially',methods=['POST'])
def joinGroupOfficially():

    group_id = request.form['grpID']

    query = ('SELECT PassengerID FROM ParticipatesIn WHERE GrpId = %s AND PassengerID=%s')
    cursor.execute(query,(group_id,curID))
    result = cursor.fetchall()
    if len(result) != 0:
        return json.dumps({'message':-1})

    query = ('SELECT PassengerId FROM ParticipatesIn WHERE GrpId=%s')
    cursor.execute(query,group_id)
    result = cursor.fetchall()
    passengers = []
    inGroup = 0
    for id in result:
        passenger_id = id[0]
        query = ('SELECT * FROM Passenger WHERE Id=%s')
        cursor.execute(query,passenger_id)
        passengers += cursor.fetchall()

    query = ('SELECT Size FROM Grp WHERE Id=%s')
    cursor.execute(query,group_id)
    result = cursor.fetchall()
    size = 0
    for i in result:
        size = i[0]

    if len(passengers) >= size:
        return json.dumps({'message':0})

    query = ('INSERT INTO ParticipatesIn (PassengerId,GrpId)' 'VALUES (%s,%s)')
    data = (curID,group_id)
    cursor.execute(query,data)
    conn.commit()

    return json.dumps({'message':1})

@app.route('/leaveGroup',methods=['POST'])
def leaveGroup():
    group_id = request.form['grpID']

    query = ('DELETE FROM ParticipatesIn WHERE GrpId = %s AND PassengerID=%s')
    cursor.execute(query,(group_id,curID))

    query = ('SELECT PassengerId FROM ParticipatesIn WHERE GrpId = %s')
    cursor.execute(query,(group_id))
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.execute(('DELETE FROM Grp WHERE Id = %s'),(group_id))
    conn.commit()

    return json.dumps({'message':1})

############  ACCOMMODATION TRANSACTIONS  ######################
@app.route('/accommodation')
def accommodations():
    global dest
    city = dest.split(",")[0]
    cursor.execute('SELECT Id, Name, Rate, AccommodationType,City from Accommodation where City=%s',(city))
    options = cursor.fetchall()
    return render_template('accommodation.html',name=name, options=options)

@app.route('/selectAccom', methods=['POST'])
def selectAccom():
    accomId = request.form['accomSelect']
    global grp
    cursor.execute('INSERT INTO StaysIn (AccommodationId, GrpId)' 'VALUES (%s,%s)',(accomId,grp))
    conn.commit()
    return json.dumps({'message':1})

############  LOCATION TRANSACTIONS  ######################
@app.route('/showLoc')
def getLoc():
    cursor.execute('SELECT city, state, country FROM location')
    data = cursor.fetchall() # returns list of tuples
    return render_template('loc.html',data = data, name=name)

@app.route('/srcdst', methods=['POST'])
def setSourceDest():
    global source
    global dest
    source = request.form['source']
    dest = request.form['dest']
    return render_template('srcdst.html',src=source, dst=dest)

############# TRANSPORTATION TRANSACTIONS ###################
@app.route('/chooseFlight', methods=['POST'])
def selectTransportation():
    global departureFlight
    departureFlight = request.form['departureFlight']
    global returnFlight
    returnFlight = request.form['returnFlight']

    query = ('SELECT TransportationMethod.Id FROM TransportationMethod WHERE TransportationMethod.Id = %s')
    data = (departureFlight)

    cursor.execute(query, data)

    result = cursor.fetchone()

    if result is None:
        return json.dumps({'response':'bad'})

    query = ('SELECT TransportationMethod.Id FROM TransportationMethod WHERE TransportationMethod.Id = %s')
    data = (returnFlight)

    cursor.execute(query, data)

    result = cursor.fetchone()

    if result is None:
            return json.dumps({'response':'bad'})


    return json.dumps({'response':'ok'})

@app.route('/searchTransportation', methods=['POST'])
def searchTransportation():
    departDate = request.form['departureDate']
    returnDate = request.form['returnDate']

    query = ('SELECT Location.Id FROM Location WHERE Location.City = %s')
    data = (source);
    cursor.execute(query, data)
    sourceID = cursor.fetchone()[0];

    query = ('SELECT Location.Id FROM Location WHERE Location.City = %s')
    data = (dest);
    cursor.execute(query, data)
    destID = cursor.fetchone()[0];

    query = ('SELECT TransportationMethod.Id, TransportationMethod.Cost, Flight.Carrier, Flight.Class FROM TransportationMethod, TravelsTo, Flight WHERE TransportationMethod.Id = TravelsTo.TransportationId AND TravelsTo.SourceId = %s AND TravelsTo.DestinationId = %s AND Flight.Depart = %s AND Flight.Id = TransportationMethod.Id')
    data = (sourceID, destID, departDate)
    cursor.execute(query, data)

    departOptions = cursor.fetchall()

    query = ('SELECT TransportationMethod.Id, TransportationMethod.Cost, Flight.Carrier, Flight.Class FROM TransportationMethod, TravelsTo, Flight WHERE TransportationMethod.Id = TravelsTo.TransportationId AND TravelsTo.SourceId = %s AND TravelsTo.DestinationId = %s AND Flight.Depart = %s AND Flight.Id = TransportationMethod.Id')
    data = (destID, sourceID, returnDate)
    cursor.execute(query, data)

    returnOptions = cursor.fetchall()

    return json.dumps({'departOptions':departOptions, 'returnOptions':returnOptions, 'source':source, 'dest':dest, 'departDate':departDate, 'returnDate':returnDate})

################### PAYMENT TRANSACTIONS ############################

@app.route('/addPaymentOptions', methods=['POST'])
def addPaymentOptions():
    cardNum = request.form['cardNumber']
    cardType = request.form['cardType']
    passengerId = curID
    query = ('INSERT INTO Payment (CardNumber, Type, PassengerId)' 'VALUES (%s,%s,%s)')
    data = (cardNum, cardType, passengerId)

    cursor.execute(query, data)
    conn.commit()

    return viewPaymentOptions()

@app.route('/viewPaymentOptions', methods=['POST'])
def viewPaymentOptions():
    query = ('SELECT Payment.CardNumber, Payment.Type FROM Payment WHERE Payment.PassengerId = %s')
    data = (curID)
    cursor.execute(query, data)

    options = cursor.fetchall()

    return json.dumps({'options':options, 'curID': curID})

@app.route('/choosePaymentMethod', methods=['POST'])
def choosePaymentMethod():
    global cardNumber
    cardNumber = request.form['cardNumberSelect']

    query = ('SELECT Payment.CardNumber FROM Payment WHERE Payment.PassengerId = %s AND Payment.CardNumber = %s')
    data = (curID, cardNumber)
    cursor.execute(query, data)

    result = cursor.fetchone()

    if result is None:
        return json.dumps({'response':'bad', 'curID':curID, 'cardNum':cardNumber})

    return json.dumps({'response':'ok'})

if __name__ == "__main__":
    app.run()
