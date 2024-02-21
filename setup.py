import random, string

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