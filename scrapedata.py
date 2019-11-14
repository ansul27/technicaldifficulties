import pyodbc
import requests as r
from bs4 import BeautifulSoup as bs

#Connect to our database, and return our database connection
def conenctToDB():
    print("Connecting to database")
    mydb = pyodbc.connect('''DRIVER={ODBC Driver 17 for SQL Server};
        SERVER=info-430-au19.database.windows.net;
        DATABASE=yelpdata;
        UID=simkota;
        PWD=h3ll0fr!3nd$''')
    print("Done connecting")
    return mydb
#Take in the string of a web address, and retun HTML elements of the page
def getHTML(domain):
    frontPage = r.get(domain)
    return bs(frontPage.content, 'html.parser')

#Takes in starting page and ending page
#Return list of pages's url that we will use
def processLink(start, end):
    pages = []
    for i in range(start, end + 1):
        pages.append("https://www.yelp.com/search?cflt=restaurants&find_loc=University%20District%2C%20Seattle%2C%20WA&start=" + str(i * 30))
    return pages

#takes in a list of url that we will use
#Return a list of all url from the <a> tag in the "image_container", which is the url for each individual book
def getWebLinks(pages):
    linkElement = []
    for i in pages:
        temp = getHTML(i)
        title = temp.findAll('h3', class_="lemon--h3__373c0__sQmiG heading--h3__373c0__1n4Of alternate__373c0__1uacp")
        for c in title:
            linkElement.extend(c.findAll('a', href = True))

    final_res = []
    for i in linkElement:
        if (i['href'][:8] != '/adredir'):
            final_res.append("http://yelp.com" + i['href'])
    return final_res

# Execute our stored procedure to insert our data
# takes in a list and
def insertRestaurants(all, mydb):
    cursor = mydb.cursor()
    # insert data into our database
    insertRes = """
    SET NOCOUNT ON; 
    EXECUTE [addRestaurants]
    @resName = ?, 
    @numReviews = ?,
    @resAddress = ?,
    @resCat = ?,
    @yelpUrl = ?,
    @rating = ?
    """
    print("start to import")
    for i in all:
        # in this case, I can just do cursor.execute(insertBook, params),
        # but doing this is just to make sure my my tuple elements are in right order
        resName = i[0]
        numReviews = i[1]
        resAddress = i[2]
        resCat = i[3]
        yelpUrl = i[4]
        rating = i[5]
        params = (resName, numReviews, resAddress, resCat, yelpUrl, rating)
        #just for debugging
        print(i)
        cursor.execute(insertRes, params)
    #commit your transaction when finished
    cursor.commit()
    #close the connection and cursor
    cursor.close()

def getReviews(mydb):
    cursor = mydb.cursor()
    getRestaurants = '''
        SELECT resId, yelpUrl
        FROM restaurantData
    '''
    resIds = []
    reviews = []
    # reviewerIds = []
    stars = []
    dates = []
    cursor.execute(getRestaurants)
    for row in cursor.fetchall():
        restaurant = getHTML(row[1])
        resReviews = restaurant.findAll('li', class_='lemon--li__373c0__1r9wz u-space-b3 u-padding-b3 border--bottom__373c0__uPbXS border-color--default__373c0__2oFDT')
        for review in resReviews:
            reviews.append(review.find('p', class_='lemon--p__373c0__3Qnnj text__373c0__2pB8f comment__373c0__3EKjH text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_').text)
            resIds.append(row[0])
            # reviewerChunk = review.find('div', class_='lemon--div__373c0__1mboc sidebar__373c0__2uR52 arrange-unit__373c0__1piwO border-color--default__373c0__2oFDT')
            # reviewer = reviewerChunk.find('span', class_='lemon--span__373c0__3997G text__373c0__2pB8f fs-block text-color--inherit__373c0__w_15m text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa')
            # reviewer = (review.find('a', class_='lemon--a__373c0__IEZFH link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--default__373c0__1skgq').text)
            # matches = cursor.execute("SELECT UserID FROM Users WHERE name = ?", reviewer)
            # if matches == 0:
            #     cursor.execute("INSERT INTO Users Values (%s)", reviewer)
            #     cursor.execute("SELECT UserID FROM Users WHERE name = ?", reviewer)
            # for uid in cursor.fetchall():
            #     reviewerIds.append(uid[0])
            stars.append(int(review.find('div', class_=lambda class_:class_ and class_.startswith("lemon--div__373c0__1mboc i-stars__373c0__Y2F3O"))["aria-label"][:1]))
            dates.append(review.find('span', class_="lemon--span__373c0__3997G text__373c0__2pB8f text-color--mid__373c0__3G312 text-align--left__373c0__2pnx_").text)
        # zip the book with their information into tuples, and put them in a list
    allReviews = list(zip(resIds, reviews, stars, dates))
    # insert your data into the table you created
    insertReviews(allReviews, mydb, cursor)

def insertReviews(all, mydb, cursor):
    # insert data into our database
    insertReview = """
    SET NOCOUNT ON; 
    EXECUTE [addReviews]
    @resId = ?, 
    @review = ?,
    @stars = ?,
    @reviewDate = ?
    """
    print("start to import")
    for i in all:
        # in this case, I can just do cursor.execute(insertBook, params),
        # but doing this is just to make sure my my tuple elements are in right order
        resId = i[0]
        review = i[1]
        # reviewerId = i[2]
        stars = i[2]
        date = i[3]
        params = (resId, review, stars, date)
        #just for debugging
        print(i)
        cursor.execute(insertReview, params)
    #commit your transaction when finished
    cursor.commit()
    #close the connection and cursor
    cursor.close()

if __name__ == '__main__':

    # get our pages that we wish to scrape
    links = processLink(0, 1)
    # get list of url of each individual restaurant
    finalLink = getWebLinks(links)

    # set the empty list for each column
    names = []
    reviews = []
    locations = []
    categories = []
    ratings = []

    # for all the links we got, append the title, price, desc, and genres into a list
    for i in finalLink:
        restaurant = getHTML(i)
        names.append(restaurant.find('h1').text)
        reviews.append(restaurant.find('p', class_ = 'lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--mid__373c0__3G312 text-align--left__373c0__2pnx_ text-size--large__373c0__1568g').text)
        locations.append(restaurant.find('p', class_ = 'lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa').text)
        categories.append(restaurant.find('a', class_ = 'lemon--a__373c0__IEZFH link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--inherit__373c0__2JXk5').text)
        ratings.append(int(restaurant.find('div', class_=lambda class_:class_ and class_.startswith("lemon--div__373c0__1mboc i-stars__373c0__Y2F3O"))["aria-label"][:1]))
    # zip the book with their information into tuples, and put them in a list
    allRes = list(zip(names, reviews, locations, categories, finalLink, ratings))
    #connect to our database
    mydb = conenctToDB()
    # insert your data into the table you created
    insertRestaurants(allRes, mydb)
    getReviews(mydb)
    mydb.close()