USE yelpdata

DROP TABLE IF EXISTS tblRes_simkota

-- Create table for Book
CREATE TABLE tblRes_simkota (
	resId int IDENTITY(1,1) PRIMARY KEY,
	resName VARCHAR(4096) NOT NULL,
	numReviews VARCHAR(4096),
	resAddress VARCHAR(4096),
	resCat VARCHAR(4096)
)
Go

IF OBJECT_ID ( 'insert_simkota', 'P' ) IS NOT NULL   
    DROP PROCEDURE insert_simkota;  
GO

-- Create stored procedure for inserting two tables
Create PROCEDURE insert_simkota
@resName VARCHAR(4096),
@numReviews VARCHAR(4096),
@resAddress VARCHAR(4096),
@resCat VARCHAR(4096)
AS
-- check if any parameter is null
IF @resName IS NULL
BEGIN
PRINT 'parameters must have a value'
RAISERROR ('parameters cannot be NULL', 11, 1) 
RETURN
END

BEGIN TRAN R1 
INSERT INTO tblRes_simkota(resName, numReviews, resAddress, resCat) 
VALUES (@resName, @numReviews, @resAddress, @resCat)

IF @@ERROR <> 0 
	ROLLBACK TRAN R1
ELSE 
	COMMIT TRAN R1
	PRINT 'inserted'
GO 
