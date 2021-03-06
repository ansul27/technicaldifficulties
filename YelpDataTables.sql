--This file creates all Tables and Stored Procedures in the Yelpdata Database
--USE yelpdata
--USE is commented out, cannot change databases with Azure (in SSMS, change database manually)

--Drops all tables, in an order that does not violate key constraints
DROP TABLE IF EXISTS users
DROP TABLE IF EXISTS reviews
DROP TABLE IF EXISTS resHours
DROP TABLE IF EXISTS restaurantCategories
DROP TABLE IF EXISTS categories
DROP TABLE IF EXISTS restaurantData

--Drops all Stored Procedures
DROP PROC IF EXISTS addReviews
DROP PROC IF EXISTS addHours
DROP PROC IF EXISTS addRestaurants

CREATE TABLE restaurantData (
	resId int IDENTITY(1,1) PRIMARY KEY,
	resName VARCHAR(4096) NOT NULL,
	numReviews VARCHAR(4096),
	resAddress VARCHAR(4096),
	yelpUrl VARCHAR(4096),
	rating DECIMAL(3,2)
)
Go

IF OBJECT_ID ( 'addRestaurants', 'P' ) IS NOT NULL   
    DROP PROCEDURE addRestaurants;  
GO

Create PROCEDURE addRestaurants
@resName VARCHAR(4096),
@numReviews VARCHAR(4096),
@resAddress VARCHAR(4096),
@yelpUrl VARCHAR(4096),
@rating DECIMAL(3,2)
AS
IF @resName IS NULL
BEGIN
PRINT 'parameters must have a value'
RAISERROR ('parameters cannot be NULL', 11, 1) 
RETURN
END

BEGIN TRAN R1 
INSERT INTO restaurantData(resName, numReviews, resAddress, yelpUrl, rating) 
VALUES (@resName, @numReviews, @resAddress, @yelpUrl, @rating)

IF @@ERROR <> 0 
	ROLLBACK TRAN R1
ELSE 
	COMMIT TRAN R1
	PRINT 'inserted'
GO 

CREATE TABLE reviews (
	reviewId int IDENTITY(1,1) PRIMARY KEY,
	resId int FOREIGN KEY REFERENCES restaurantData NOT NULL,
	review VARCHAR(4096),
	stars int,
	reviewDate VARCHAR(4096)
)
Go

IF OBJECT_ID ( 'addReviews', 'P' ) IS NOT NULL   
    DROP PROCEDURE addReviews;  
GO

Create PROCEDURE addReviews
@resId int,
@review VARCHAR(4096),
@stars int,
@reviewDate VARCHAR(4096)
AS

IF @resId IS NULL
BEGIN
PRINT 'parameters must have a value'
RAISERROR ('parameters cannot be NULL', 11, 1) 
RETURN
END

BEGIN TRAN T1 
INSERT INTO reviews(resId, review, stars, reviewDate) 
VALUES (@resId, @review, @stars, @reviewDate)

IF @@ERROR <> 0 
	ROLLBACK TRAN T1
ELSE 
	COMMIT TRAN T1
	PRINT 'inserted'
GO 

CREATE TABLE categories(
	catId int IDENTITY(1,1) PRIMARY KEY,
	catName VARCHAR(4096)
)

CREATE TABLE restaurantCategories(
	resCatID int IDENTITY(1,1) PRIMARY KEY,
	resId int FOREIGN KEY REFERENCES restaurantData,
	catId int FOREIGN KEY REFERENCES categories
)

CREATE TABLE resHours (
	hourId int IDENTITY(1,1) PRIMARY KEY,
	resId int FOREIGN KEY REFERENCES restaurantData NOT NULL,
	dayOfWeek VARCHAR(4096),
	openTime TIME,
	closeTime TIME,
	hoursOpen AS DATEDIFF(MINUTE, openTime, closeTime)/60.0
)
Go

IF OBJECT_ID ( 'addHours', 'P' ) IS NOT NULL   
    DROP PROCEDURE addHours;  
GO

Create PROCEDURE addHours
@resId int,
@dayOfWeek VARCHAR(4096),
@openTime TIME,
@closeTime TIME
AS
IF @resId IS NULL
BEGIN
PRINT 'parameters must have a value'
RAISERROR ('parameters cannot be NULL', 11, 1) 
RETURN
END

BEGIN TRAN L1 
INSERT INTO resHours(resId, dayOfWeek, openTime, closeTime) 
VALUES (@resId, @dayOfWeek, @openTime, @closeTime)

IF @@ERROR <> 0 
	ROLLBACK TRAN L1
ELSE 
	COMMIT TRAN L1
	PRINT 'inserted'
GO 