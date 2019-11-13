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
    EXECUTE [insert_simkota]
    @resName = ?, 
    @numReviews = ?,
    @resAddress = ?,
    @resCat = ?
    """
    print("start to import")
    for i in all:
        # in this case, I can just do cursor.execute(insertBook, params),
        # but doing this is just to make sure my my tuple elements are in right order
        resName = i[0]
        numReviews = i[1]
        resAddress = i[2]
        resCat = i[3]
        params = (resName, numReviews, resAddress, resCat)
        #just for debugging
        print(i)
        cursor.execute(insertRes, params)
    #commit your transaction when finished
    cursor.commit()
    #close the connection and cursor
    cursor.close()
    mydb.close()





if __name__ == '__main__':

    # get our pages that we wish to scrape
    links = processLink(1, 2)
    # get list of url of each individual restaurant
    finalLink = getWebLinks(links)

    # set the empty list for each column
    names = []
    reviews = []
    locations = []
    categories = []

    # for all the links we got, append the title, price, desc, and genres into a list
    for i in finalLink:
        restaurant = getHTML(i)
        names.append(restaurant.find('h1').text)
        reviews.append(restaurant.find('p', class_ = 'lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--mid__373c0__3G312 text-align--left__373c0__2pnx_ text-size--large__373c0__1568g').text)
        locations.append(restaurant.find('p', class_ = 'lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_').text)
        categories.append(restaurant.find('a', class_ = 'lemon--a__373c0__IEZFH link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--inherit__373c0__2JXk5').text)
    # zip the book with their information into tuples, and put them in a list
    allRes = list(zip(names, reviews, locations, categories))
    #connect to our database
    mydb = conenctToDB()
    # insert your data into the table you created
    insertRestaurants(allRes, mydb)