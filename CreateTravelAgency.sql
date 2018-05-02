DROP DATABASE TravelAgency;
CREATE DATABASE TravelAgency;
USE TravelAgency;

CREATE TABLE Passenger (
	Id		INT,
	Age		INT,
	Gender	CHAR(1) CHECK (Gender IN ('F', 'M', 'U')),
	Name		VARCHAR(40),
	CHECK (Id >= 0),
	CHECK (Age >= 0),
PRIMARY KEY (Id)
);

CREATE TABLE Grp (
	Id		INT,
	Size		INT,
	Purpose	VARCHAR(9) CHECK (Purpose IN ('Business', 'Pleasure', 'Education')),
	CHECK (Id >= 0),
	CHECK (Size >= 1),
	PRIMARY KEY (Id)
    );
    
CREATE TABLE Review (
	Id	INT,
	Review VARCHAR(100),
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
	PRIMARY KEY(GrpId),
	FOREIGN KEY (GrpId) REFERENCES Grp(Id),
	FOREIGN KEY (TransportationId) REFERENCES TransportationMethod(Id)
);




CREATE TABLE Flight (
	Id		INT,
	Date		DATE,
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
	Rate		FLOAT(10, 2),
	Discount	FLOAT(2, 2),
	AccommodationType		VARCHAR(30),
CHECK (Id >= 0),
CHECK (Rate >= 0),
PRIMARY KEY (Id)
);

CREATE TABLE StaysIn (
	AccommodationId	INT,
	BookingNumber	INT,
    GrpId INT,
	CHECK (BookingNumber >= 0),
	PRIMARY KEY (AccommodationId, BookingNumber),
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

INSERT INTO Passenger(Id, Age, Gender)
VALUES ('1111', '20', 'F');

