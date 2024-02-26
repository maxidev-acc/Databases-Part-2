import random, string
import requests
from db_access import registration
import names
"""
newperson = Person(
            svn = '848392493',
            first_name = 'Maximilian',
            email = "newtest@admin.com",
            sex = "m",
                birthDate = '17.04.1999',
                origin = "AT"
                    )
db.session.add(newperson)
db.session.commit()
"""
#flight_data = [{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "AT", "destination": "DE", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}}, {"ID":2,"code": "ER45if", "price": 345.99, "departureDate": "2016/02/11", "origin": "MUA", "destination": "LAX", "emptySeats": 52, "plane": {"type": "Boeing 777", "totalSeats": 300}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}}]
city_names = ["Aberdeen", "Abilene", "Akron", "Albany", "Albuquerque", "Alexandria", "Allentown", "Amarillo", "Anaheim", "Anchorage", "Ann Arbor", "Antioch", "Apple Valley", "Appleton", "Arlington", "Arvada", "Asheville", "Athens", "Atlanta", "Atlantic City", "Augusta", "Aurora", "Austin", "Bakersfield", "Baltimore", "Barnstable", "Baton Rouge", "Beaumont", "Bel Air", "Bellevue", "Berkeley", "Bethlehem", "Billings", "Birmingham", "Bloomington", "Boise", "Boise City", "Bonita Springs", "Boston", "Boulder", "Bradenton", "Bremerton", "Bridgeport", "Brighton", "Brownsville", "Bryan", "Buffalo", "Burbank", "Burlington", "Cambridge", "Canton", "Cape Coral", "Carrollton", "Cary", "Cathedral City", "Cedar Rapids", "Champaign", "Chandler", "Charleston", "Charlotte", "Chattanooga", "Chesapeake", "Chicago", "Chula Vista", "Cincinnati", "Clarke County", "Clarksville", "Clearwater", "Cleveland", "College Station", "Colorado Springs", "Columbia", "Columbus", "Concord", "Coral Springs", "Corona", "Corpus Christi", "Costa Mesa", "Dallas", "Daly City", "Danbury", "Davenport", "Davidson County", "Dayton", "Daytona Beach", "Deltona", "Denton", "Denver", "Des Moines", "Detroit", "Downey", "Duluth", "Durham", "El Monte", "El Paso", "Elizabeth", "Elk Grove", "Elkhart", "Erie", "Escondido", "Eugene", "Evansville", "Fairfield", "Fargo", "Fayetteville", "Fitchburg", "Flint", "Fontana", "Fort Collins", "Fort Lauderdale", "Fort Smith", "Fort Walton Beach", "Fort Wayne", "Fort Worth", "Frederick", "Fremont", "Fresno", "Fullerton", "Gainesville", "Garden Grove", "Garland", "Gastonia", "Gilbert", "Glendale", "Grand Prairie", "Grand Rapids", "Grayslake", "Green Bay", "GreenBay", "Greensboro", "Greenville", "Gulfport-Biloxi", "Hagerstown", "Hampton", "Harlingen", "Harrisburg", "Hartford", "Havre de Grace", "Hayward", "Hemet", "Henderson", "Hesperia", "Hialeah", "Hickory", "High Point", "Hollywood", "Honolulu", "Houma", "Houston", "Howell", "Huntington", "Huntington Beach", "Huntsville", "Independence", "Indianapolis", "Inglewood", "Irvine", "Irving", "Jackson", "Jacksonville", "Jefferson", "Jersey City", "Johnson City", "Joliet", "Kailua", "Kalamazoo", "Kaneohe", "Kansas City", "Kennewick", "Kenosha", "Killeen", "Kissimmee", "Knoxville", "Lacey", "Lafayette", "Lake Charles", "Lakeland", "Lakewood", "Lancaster", "Lansing", "Laredo", "Las Cruces", "Las Vegas", "Layton", "Leominster", "Lewisville", "Lexington", "Lincoln", "Little Rock", "Long Beach", "Lorain", "Los Angeles", "Louisville", "Lowell", "Lubbock", "Macon", "Madison", "Manchester", "Marina", "Marysville", "McAllen", "McHenry", "Medford", "Melbourne", "Memphis", "Merced", "Mesa", "Mesquite", "Miami", "Milwaukee", "Minneapolis", "Miramar", "Mission Viejo", "Mobile", "Modesto", "Monroe", "Monterey", "Montgomery", "Moreno Valley", "Murfreesboro", "Murrieta", "Muskegon", "Myrtle Beach", "Naperville", "Naples", "Nashua", "Nashville", "New Bedford", "New Haven", "New London", "New Orleans", "New York", "New York City", "Newark", "Newburgh", "Newport News", "Norfolk", "Normal", "Norman", "North Charleston", "North Las Vegas", "North Port", "Norwalk", "Norwich", "Oakland", "Ocala", "Oceanside", "Odessa", "Ogden", "Oklahoma City", "Olathe", "Olympia", "Omaha", "Ontario", "Orange", "Orem", "Orlando", "Overland Park", "Oxnard", "Palm Bay", "Palm Springs", "Palmdale", "Panama City", "Pasadena", "Paterson", "Pembroke Pines", "Pensacola", "Peoria", "Philadelphia", "Phoenix", "Pittsburgh", "Plano", "Pomona", "Pompano Beach", "Port Arthur", "Port Orange", "Port Saint Lucie", "Port St. Lucie", "Portland", "Portsmouth", "Poughkeepsie", "Providence", "Provo", "Pueblo", "Punta Gorda", "Racine", "Raleigh", "Rancho Cucamonga", "Reading", "Redding", "Reno", "Richland", "Richmond", "Richmond County", "Riverside", "Roanoke", "Rochester", "Rockford", "Roseville", "Round Lake Beach", "Sacramento", "Saginaw", "Saint Louis", "Saint Paul", "Saint Petersburg", "Salem", "Salinas", "Salt Lake City", "San Antonio", "San Bernardino", "San Buenaventura", "San Diego", "San Francisco", "San Jose", "Santa Ana", "Santa Barbara", "Santa Clara", "Santa Clarita", "Santa Cruz", "Santa Maria", "Santa Rosa", "Sarasota", "Savannah", "Scottsdale", "Scranton", "Seaside", "Seattle", "Sebastian", "Shreveport", "Simi Valley", "Sioux City", "Sioux Falls", "South Bend", "South Lyon", "Spartanburg", "Spokane", "Springdale", "Springfield", "St. Louis", "St. Paul", "St. Petersburg", "Stamford", "Sterling Heights", "Stockton", "Sunnyvale", "Syracuse", "Tacoma", "Tallahassee", "Tampa", "Temecula", "Tempe", "Thornton", "Thousand Oaks", "Toledo", "Topeka", "Torrance", "Trenton", "Tucson", "Tulsa", "Tuscaloosa", "Tyler", "Utica", "Vallejo", "Vancouver", "Vero Beach", "Victorville", "Virginia Beach", "Visalia", "Waco", "Warren", "Washington", "Waterbury", "Waterloo", "West Covina", "West Valley City", "Westminster", "Wichita", "Wilmington", "Winston", "Winter Haven", "Worcester", "Yakima", "Yonkers", "York", "Youngstown"]


def generateshopdata():
    
    lands = ['AT', 'DE', 'AF', 'AO', 'AT', 'AN', 'AQ', 'BR']
    letters = string.ascii_lowercase
    data =[]
    for k in range(1,100):
        sub = {}
        sub['ID'] = k
        result_str = ''.join(random.choice(letters) for i in range(8))
        sub['code'] = result_str
        sub['origin'] = random.choice(lands)
        sub['destination'] = random.choice(lands)
        sub['price'] = random.randint(200,400)
        sub['depatureDate'] = '01.01.1999'
        sub['emptySeats'] = 0
        sub['plane'] = {"type": "Boeing 737", "totalSeats": 150}


        
        data.append(sub)
   
    return data  

generateshopdata()


"""
    svn = db.Column(db.String(10), primary_key = True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    adress = db.Column(db.String(50))
    postal = db.Column(db.String(10))
    location = db.Column(db.String(20))
    email = db.Column(db.String(50) , unique=True)
    password = db.Column(db.String() , unique=True)
"""


char_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
"t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
"O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9",
"!", "§", "$", "%", "&", "/", "(", ")", "=", ".", "-", ",", "@", "€", "[", "]"]




def generatePersonData():
    
    lands = ['AT', 'DE', 'AF', 'AO', 'AT', 'AN', 'AQ', 'BR']
    letters = string.ascii_lowercase
    data =[]
    for k in range(1,1000):
        
        svn = str(random.randint(1000000000,9999999999))
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        adress = "Teststraße" +str(k)
        postal = str(random.randint(1000,9999))
        location = random.choice(city_names)
        email = first_name + last_name + "@gmail.com"
        password = ""
        for k in range(0,10):
            password = ''.join(random.choice(letters) for i in range(8))
        print((svn, first_name,last_name, adress, postal, location,email, password))
        registration((svn, first_name,last_name, adress, postal, location,email, password))



#generateshopdata()

