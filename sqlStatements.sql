USE yelpdata

DROP TABLE IF EXISTS restaurantData

-- Create table for Book
CREATE TABLE restaurantData (
	resId int IDENTITY(1,1) PRIMARY KEY,
	resName VARCHAR(4096) NOT NULL,
	numReviews VARCHAR(4096),
	resAddress VARCHAR(4096),
	resCat VARCHAR(4096),
	yelpUrl VARCHAR(4096),
	rating int
)
Go

IF OBJECT_ID ( 'addRestaurants', 'P' ) IS NOT NULL   
    DROP PROCEDURE addRestaurants;  
GO

-- Create stored procedure for inserting two tables
Create PROCEDURE addRestaurants
@resName VARCHAR(4096),
@numReviews VARCHAR(4096),
@resAddress VARCHAR(4096),
@resCat VARCHAR(4096),
@yelpUrl VARCHAR(4096),
@rating INT
AS
-- check if any parameter is null
IF @resName IS NULL
BEGIN
PRINT 'parameters must have a value'
RAISERROR ('parameters cannot be NULL', 11, 1) 
RETURN
END

BEGIN TRAN R1 
INSERT INTO restaurantData(resName, numReviews, resAddress, resCat, yelpUrl, rating) 
VALUES (@resName, @numReviews, @resAddress, @resCat, @yelpUrl, @rating)

IF @@ERROR <> 0 
	ROLLBACK TRAN R1
ELSE 
	COMMIT TRAN R1
	PRINT 'inserted'
GO 

DROP TABLE IF EXISTS users

-- Create table for Book
CREATE TABLE users (
	UserID int IDENTITY(1,1) PRIMARY KEY,
	name VARCHAR(4096)
)
Go

DROP TABLE IF EXISTS reviews

-- Create table for Book
CREATE TABLE reviews (
	reviewId int IDENTITY(1,1) PRIMARY KEY,
	resId int FOREIGN KEY REFERENCES restaurantData NOT NULL,
	review VARCHAR(4096),
	reviewerId int FOREIGN KEY REFERENCES users NOT NULL,
	stars int,
	reviewDate VARCHAR(4096)
)
Go

IF OBJECT_ID ( 'addReviews', 'P' ) IS NOT NULL   
    DROP PROCEDURE addReviews;  
GO

-- Create stored procedure for inserting two tables
Create PROCEDURE addReviews
@resId int,
@review VARCHAR(4096),
@reviewerId int,
@stars int,
@reviewDate VARCHAR(4096)
AS
-- check if any parameter is null
IF @resId IS NULL
BEGIN
PRINT 'parameters must have a value'
RAISERROR ('parameters cannot be NULL', 11, 1) 
RETURN
END

BEGIN TRAN T1 
INSERT INTO reviews(resId, review, reviewerId, stars, reviewDate) 
VALUES (@resId, @review, @reviewerId, @stars, @reviewDate)

IF @@ERROR <> 0 
	ROLLBACK TRAN T1
ELSE 
	COMMIT TRAN T1
	PRINT 'inserted'
GO 