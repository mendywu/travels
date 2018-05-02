DROP DATABASE TravelAgency;
CREATE DATABASE TravelAgency;
USE TravelAgency;

CREATE TABLE Passenger (
	Id		INT,
	Age		INT,
	Gender	CHAR(1) CHECK (Gender IN ('F', 'M', 'U')),
    pWord 	VARCHAR(30),
	FName		VARCHAR(40),
	LName		VARCHAR(40),
	CHECK (Id >= 0),
	CHECK (Age >= 0),
PRIMARY KEY (Id)
);

CREATE TABLE Grp (
	Id		INT,
	Size		INT,
	Purpose	VARCHAR(9) CHECK (Purpose IN ('Business', 'P	leasure', 'Education')),
	CHECK (Id >= 0),
	CHECK (Size >= 1),
	PRIMARY KEY (Id)
    );
    
CREATE TABLE Review (
	Id	INT,
	Review VARCHAR(1000),
	Rating	INT,
	CHECK (Id >= 0),
	CHECK (Rating > 0 AND Rating < 6),
	PRIMARY KEY (Id)
);

CREATE TABLE ParticipatesIn (
PassengerId	INT,
GrpId	INT,
ReviewId	INT,
PRIMARY KEY (PassengerId, GrpId),
FOREIGN KEY (GrpId) REFERENCES Grp(Id),
FOREIGN KEY (PassengerId) REFERENCES Passenger(Id),
FOREIGN KEY (ReviewId) REFERENCES Review(Id)
);


CREATE TABLE TransportationMethod (
	Id	INT,
	Cost 	FLOAT(10, 2),
	Type	VARCHAR(6),
	CHECK (Cost >= 0),
	CHECK (Id >= 0),
	CHECK (Type IN ('Flight', 'Car', 'Cruise')),
	PRIMARY KEY (Id)
);
	
CREATE TABLE TravelsBy (
	GrpId		INT,
	TransportationId	INT,
	PRIMARY KEY(GrpId, TransportationId),
	FOREIGN KEY (GrpId) REFERENCES Grp(Id),
	FOREIGN KEY (TransportationId) REFERENCES TransportationMethod(Id)
);




CREATE TABLE Flight (
	Id		INT,
	Depart		DATE,
	Carrier		VARCHAR(30),
	Class		VARCHAR(8),
	CHECK (Class in ('First', 'Business', 'Economy')),
	PRIMARY KEY (Id),
	FOREIGN KEY (Id) REFERENCES TransportationMethod(Id)
);

CREATE TABLE Car (
	Id	INT,
	Type	VARCHAR(30),
	PRIMARY KEY (Id),
FOREIGN KEY (Id) REFERENCES TransportationMethod(Id)
);

CREATE TABLE Cruise (
	Id	INT,
	PRIMARY KEY (Id),
FOREIGN KEY (Id) REFERENCES TransportationMethod(Id)
);

CREATE TABLE Location (
	Id		INT,
	City		VARCHAR(30),
	State		VARCHAR(30),
	Country	VARCHAR(30),
	CHECK (Id >= 0),
	PRIMARY KEY (Id)
);

CREATE TABLE TravelsTo (
	SourceId		INT,
	DestinationId		INT,
	TransportationId	INT,
	PRIMARY KEY (SourceId, DestinationId, TransportationId),
FOREIGN KEY (DestinationId) REFERENCES Location(Id),
FOREIGN KEY (SourceId) REFERENCES Location(Id),
FOREIGN KEY (TransportationId) REFERENCES TransportationMethod(Id)
);

CREATE TABLE Accommodation (
	Id		INT,
    Name	VARCHAR(100),
	Rate		FLOAT(10, 2),
	Discount	FLOAT(2, 2),
	AccommodationType		VARCHAR(30),
    City VARCHAR(30),
	CHECK (Id >= 0),
	CHECK (Rate >= 0),
	PRIMARY KEY (Id)
);

CREATE TABLE StaysIn (
	AccommodationId	INT,
	BookingNumber	INT AUTO_INCREMENT,
    GrpId INT,
	CHECK (BookingNumber >= 0),
	PRIMARY KEY (BookingNumber),
	FOREIGN KEY (AccommodationId) REFERENCES Accommodation(Id),
	FOREIGN KEY (GrpId) REFERENCES Grp(Id)
);

CREATE TABLE Facilities (
	Id	INT,
	Facility	VARCHAR(30),
	PRIMARY KEY (Id, Facility),
	FOREIGN KEY (Id) REFERENCES Accommodation(Id)
);

CREATE TABLE Payment (
	CardNumber	INT,
	Type		VARCHAR(20),
	PassengerId	INT,
	PRIMARY KEY (CardNumber),
	FOREIGN KEY (PassengerId) REFERENCES Passenger(Id)
);
	
CREATE TABLE MakesPayment (
	PassengerId	INT,
	GrpId	INT,
	CardNumber	INT,
	Amount	FLOAT(10, 2),
	PRIMARY KEY(PassengerId, GrpId),
	FOREIGN KEY (PassengerId) REFERENCES Passenger(Id),
	FOREIGN KEY (GrpId) REFERENCES Grp(Id),
	FOREIGN KEY (CardNumber) REFERENCES Payment(CardNumber)
);



CREATE TABLE Employee (
	Id	INT,
	SupervisorId	INT,
	DateJoined	DATE,
	Role		VARCHAR(30),
	CHECK (Id >= 0),
	PRIMARY KEY (Id),
	FOREIGN KEY (SupervisorId) REFERENCES Employee(Id)
);

INSERT INTO Passenger(Id, Age, Gender, FName, LName, pWord)
VALUES ('1111', '20', 'F', 'Mendy', 'Wu','mendy');
INSERT INTO Passenger(Id, Age, Gender, FName, LName, pWord)
VALUES ('1112', '19', 'F', 'Dorothy', 'Shek','dorothy');
INSERT INTO Passenger(Id, Age, Gender, FName, LName, pWord)
VALUES ('1113', '20', 'F', 'Samantha','Belliveau','samantha');
INSERT INTO Passenger(Id, Age, Gender, FName, LName, pWord)
VALUES ('1115', '21', 'M', 'John','Doe','john');
INSERT INTO Passenger(Id, Age, Gender, FName, LName, pWord)
VALUES ('1116', '32', 'F', 'Jane', 'Doe','jane');

INSERT INTO Grp (Id, Size, Purpose)
VALUES ('1121', '5', 'Pleasure');
INSERT INTO Grp (Id, Size, Purpose)
VALUES ('1122', '2', 'Education');

INSERT INTO TransportationMethod (Id, Cost, Type)
VALUES ('1131', '100.00', 'Flight');
INSERT INTO TransportationMethod (Id, Cost, Type)
VALUES ('1132', '100.00', 'Flight');

INSERT INTO Flight (Id, Depart, Carrier, Class)
VALUES('1131','2018-5-4','DELTA','Economy');
INSERT INTO Flight (Id, Depart, Carrier, Class)
VALUES('1132','2018-5-4','DELTA','Economy');

INSERT INTO Location (Id, City, State, Country)
VALUES ('1141', 'New York City', 'New York','United States of America	');
INSERT INTO Location (Id, City, State, Country)
VALUES (3, 'Albany', 'New York', 'United States of America');
INSERT INTO Location (Id, City, State, Country)
VALUES ('1142', 'San Francisco', 'CA','United States of America');
INSERT INTO Location (Id, City, State, Country)
VALUES (5, 'Atlanta', 'Georgia', 'United States of America');
INSERT INTO Accommodation(Id, Rate, Name, AccommodationType, City)
VALUES (1, '320.70', 'Fairfield Inn & Suites','Hotel', 'New York City');
INSERT INTO Accommodation(Id, Rate,Name, AccommodationType, City)
VALUES (2, '120.56', 'New York Hilton Midtown','Hotel', 'New York City');
INSERT INTO Accommodation(Id, Rate,Name, AccommodationType, City)
VALUES (3, '20.56', 'The House of Susie','AirBnb', 'New York City');
INSERT INTO Accommodation(Id, Rate,Name, AccommodationType, City)
VALUES (4, '400.00', 'DoubleTree by Hilton','Hotel', 'San Francisco');
INSERT INTO Accommodation(Id, Rate,Name, AccommodationType, City)
VALUES (5, '450.52', 'DoubleTree by Hilton','Hotel', 'Georgia');
INSERT INTO Accommodation(Id, Rate,Name, AccommodationType, City)
VALUES (6, '450.52', 'DoubleTree by Hilton','Hotel', 'Albany');

INSERT INTO StaysIn (AccommodationId, GrpId)
VALUES (4, 1121);

INSERT INTO TravelsTo (SourceId, DestinationId, TransportationId)
VALUES ('1141', '1142', '1131');
INSERT INTO TravelsTo (SourceId, DestinationId, TransportationId)
VALUES ('1142', '1141', '1132');

INSERT INTO ParticipatesIn (PassengerId, GrpId)
VALUES ('1111', '1121');
INSERT INTO ParticipatesIn (PassengerId, GrpId)
VALUES ('1112', '1121');
INSERT INTO ParticipatesIn (PassengerId, GrpId)
VALUES ('1115', '1121');
INSERT INTO ParticipatesIn (PassengerId, GrpId)
VALUES ('1116', '1122');


