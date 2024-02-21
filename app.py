from flask import Flask, render_template, session, request, redirect, url_for, flash
import time
from flask_sqlalchemy import SQLAlchemy



#dev data
flight_data = [{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "AT", "destination": "DE", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}}, {"ID":2,"code": "ER45if", "price": 345.99, "departureDate": "2016/02/11", "origin": "MUA", "destination": "LAX", "emptySeats": 52, "plane": {"type": "Boeing 777", "totalSeats": 300}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}}]
shop_data = [{"ID":1, "code": "ER38sd","price": 100,},{"ID":2, "code": "ER38sd","price": 300,},{"ID":3, "code": "ER38sd","price": 300,} ]


user_ = {"name":"Maximilian", "email": "admin@test.at","sex": "M", "birthDate": "1999/03/20", "origin": "AT", "SVN": "5039 290399", "role":"T",}
userIn = [{"name":"Maximilian", "email": "admin@test.at","sex": "M", "birthDate": "1999/03/20", "origin": "AT", "SVN": "5039 290399", "role":"T",}]


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

class Person(db.Model):
    svn = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    sex = db.Column(db.String(200))
    birthDate = db.Column(db.String(200))
    origin = db.Column(db.String(10))
    

def getUser(id):
        user = Person.query.filter_by(svn=id).first()
        session['user'] = [{"name":user.first_name, "email": user.email,"sex": user.sex, "birthDate": user.birthDate, "origin": user.origin, "SVN": user.svn, "role":"T",}]
        return session['user']



def getItemCount():
    k = len(session['products'])
    return k



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        try:
            
            email = request.form.get('email')
            password = request.form.get('password')
            print(email)
            user = Person.query.filter_by(email=email).first()
            print(user.email)
            print(user.first_name)
            session['id'] = user.svn
            session['role'] = "P"
            session['products'] =shop_data

            print(session['role'])
            if session['role'] =="T":
                return redirect(url_for('backoffice'))
            if session['role'] =="P":
                return redirect(url_for('home'))
        except:
            return 'error'

    return render_template('login.html')


@app.route('/user', methods=('GET', 'POST'))
def user():
    if 'id' in session:
        if request.method == 'POST':
            if request.method == 'POST':
                try:
                    payload = [request.form['SVN'], request.form['firstname'],request.form['email'],request.form['sex'],request.form['birthDate'], request.form['origin']]
                    updateUser =Person.query.filter_by(svn=request.form['SVN']).first()
                    updateUser.first_name = request.form['firstname']
                    updateUser.email = request.form['email']
                    updateUser.sex = request.form['sex']
                    updateUser.birthDate = request.form['birthDate']
                    updateUser.origin = request.form['origin']
                    db.session.commit()
                    flash('Sucess')
                    print("Updated user info")
                    return redirect(url_for('user'))
                except:
                    return 'An error occured'  
        if session['role'] =="P":
            return render_template('customers/user.html', userInfo = getUser(session['id']), itemCount = getItemCount())
    return 'You are not logged in'


@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('login'))

#Customer routes

@app.route('/')
def index():
    if 'id' in session:
        print("Logged in as", session['username'])
        if session['role'] =="P":
            return render_template("customers/index.html", userInfo = getUser(session['id']), itemCount = getItemCount())
    print("Not logged in")
    return render_template("login.html")


@app.route('/home')
def home():
    if 'id' in session:
        print("Logged in as", session['id'])
        if session['role'] =="P":
            return render_template("customers/home.html", userInfo = getUser(session['id']), itemCount = getItemCount())
    print("Not logged in")
    return render_template("login.html")



@app.route('/flights', methods=['GET', 'POST'])
def flights():
    if 'id' in session:
        if session['role'] =="P":
            if request.method == 'POST':
                id = request.form['ID']
                print(id)
                


                return redirect(url_for('booking', id=id))
            return render_template('customers/flights.html', fl = flight_data, itemCount = getItemCount())             
    return 'You are not logged in'

@app.route('/booking/<id>')
def booking(id):
    if 'id' in session:

        if session['role'] =="P":
            return render_template('customers/booking.html',  userInfo = getUser(session['id']), itemCount = getItemCount())


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if 'id' in session:

        if session['role'] =="P":
            if request.method == 'POST':
                if request.form['ID']:
                    id = request.form['ID']
                    currentproducts = session['products']
                    print(id)
                    print(currentproducts)
                    for prod in currentproducts:
                        print(prod['ID'])
                        
                        if int(prod['ID']) == int(id):
                            for i in range(len(currentproducts)):
                                if str(currentproducts[i]['ID']) == str(id):
                                    del currentproducts[i]
                                    break
 
# printing result
                        print ("List after deletion of dictionary : " +  str(currentproducts))
                    
                    print(currentproducts)
                    return render_template('customers/shop.html', products= session['products'], userInfo = getUser(session['id']), itemCount = getItemCount())
                else:
                    print("Someting else")

            return render_template('customers/shop.html', products= session['products'], userInfo = getUser(session['id']), itemCount = getItemCount())




#BACKOFFICE ROUTES

@app.route('/backoffice')
def backoffice():
    if 'id' in session:
        if session['role'] =="T":
            print("Logged in as", session['username'])
            return render_template("backoffice/backoffice.html", userInfo = getUser(session['id']))
    print("Not logged in")
    return render_template("login.html")


@app.route('/backoffice/user', methods=('GET', 'POST'))
def userBackoffice():
    if 'id' in session:
        #user = Person.query.filter_by(svn=session['ID']).first()
        #userIn1 = [{user.svn, user.first_name, user.email, user.sex, user.birthDate, user.origin}]
        #print(userIn1)
        if request.method == 'POST':
            try:
                payload = [request.form['SVN'], request.form['firstname'],request.form['email'],request.form['sex'],request.form['birthDate'], request.form['origin']]
                updateUser =Person.query.filter_by(svn=request.form['SVN']).first()
                updateUser.first_name = request.form['firstname']
                updateUser.email = request.form['email']
                updateUser.sex = request.form['sex']
                updateUser.birthDate = request.form['birthDate']
                updateUser.origin = request.form['origin']
                db.session.commit()
                flash('Sucess')
                print("Updated user info")
                return redirect(url_for('userBackoffice'))

            except:
                return 'An error occured'
        if session['role'] =="T":
            return render_template('backoffice/userBackoffice.html', userInfo = getUser(session['id']))

    return 'You are not logged in'

@app.route('/backoffice/blackbox')
def blackbox():
    if 'ID' in session:
        if session['role'] =="T":
            return render_template('backoffice/blackbox.html', id = id)
        else:
            return 'Permission denied'






if __name__ =='__main__':
    app.run(debug=True)
