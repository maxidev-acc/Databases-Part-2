from flask import Flask, render_template, session, request, redirect, url_for, flash, send_file
import time
from flask_sqlalchemy import SQLAlchemy


from db_access import Transaction, BOOKING,DB_Access,  Registration, Authentification, Ticket, USER








app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'





class SESSION():
 
    def __init__(self):
        print("Session init")
        pass

    def setUser(self, user, role):
        
        session['user'] = {"svn": user[0],"first_name":user[1], "last_name": user[2], "postal": user[3], "location":user[4], "street": user[5], "houseNr": user[6], "birthdate": user[7],"email": user[8]}
        print(session['user'])
        session['id'] = user[0]
        session['role'] = role
        session['products'] = []
        self.setItemCount()
    def getUser(self,id):
            return session['user']


    def setItemCount(self):
        count = len(session['products'])
        session['itemcount'] = count

    def getSumm(self):
        sum =0
        currentproducts = session['products']
        K = len(currentproducts)
        sum = K*100
        return sum*0.9

    def deleteItemFromCart(self,flightNo):
        
        index = 0
        for item in session['products']:
             
            if item[0] == flightNo:
                del session['products'][index]
                return 0
            index = index +1 
    def clearSessionProducts(self):
        session['products'] = []
        return session['products']


                    
Session = SESSION()







@app.route('/permissiondenied')
def permDenied():
    return render_template('permissiondenied.html')



            





@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method =="POST":
        payload = (request.form['svn'], request.form['first_name'],request.form['second_name'], request.form['postal'], request.form['location'], request.form['adress'], request.form['houseNr'], request.form['birthdate'], request.form['email'], request.form['password'])
        phone = request.form['phoneNumber']
        
        print(payload)
        res = Registration().register(payload, phone)
        if  res== True:
            return redirect(url_for('login'))
         
        else:
            flash(str(res))
    return render_template("customers/register.html")





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            credentials = (email, password)
            auth=Authentification(credentials)

            if auth.authentification() ==True:
                use = USER()
                user = USER().user("email", email)
                role = use.perm(user[0])
                print(role)
                Session.setUser(user, role)
                if session['role'] =="T":
                        return redirect(url_for('backoffice'))
                if session['role'] =="P":
                        return redirect(url_for('home'))
            else:
                flash(auth.errormessage())
                
    return render_template('login.html')


@app.route('/user', methods=('GET', 'POST'))
def user():
    if 'id' in session:
        if session['role'] =="P":
            if request.method == 'POST':

                    #payload = [request.form['SVN'], request.form['firstname'],request.form['email'],request.form['sex'],request.form['birthDate'], request.form['origin']]
                    svn = request.form['svn']
                    updateUser =USER().user("svn", svn)
                    updateUser.first_name = request.form['first_name']
                    updateUser.email = request.form['email']
                    print(updateUser.first_name)
             
                    #updateUser.origin = request.form['origin']
                    db.session.commit()
                    db.session.close()
                    time.sleep(2)
                    Session.setUser(request.form['svn'], "P")

                    flash('Sucessfully updated Profile info')
                    print("Updated user info")
                    return redirect(url_for('user'))
              
                    #return 'An error occured'  
        
            return render_template('customers/user.html')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    #session.pop('id', None)
    return redirect(url_for('login'))

#Customer routes

@app.route('/')
def index():
    if 'id' in session:
        #print("Logged in as", session['username'])
        if session['role'] =="P":
            return render_template("customers/index.html", userInfo = Session.getUser(session['id']))
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if 'id' in session:
        print("Logged in as", session['id'])
        if session['role'] =="P":
            return render_template("customers/home.html", userInfo = Session.getUser(session['id']))
    print("Not logged in")
    return redirect(url_for('login'))



@app.route('/available_flights', methods=['GET', 'POST'])
def available_flights():
    if 'id' in session:
        if session['role'] =="P":
            if request.method == 'POST':
                flightNo = request.form['flightNo']
                session['addtoCart'] = DB_Access().executeFetchOne("SELECT * FROM flights NATURAL JOIN pilots NATURAL JOIN airplane_type  NATURAL JOIN airplane_exemplar WHERE flightNo = ?", (flightNo,))
                print(session['addtoCart'])
                return redirect(url_for('booking', flightNo=flightNo))
            return render_template('customers/flights.html', fl = session['available_flights'])


    return redirect(url_for('login'))







@app.route('/booking/<flightNo>', methods=['GET', 'POST'])
def booking(flightNo):
    if 'id' in session:
        if request.method == 'POST':
                    k = request.form['flightNo']
                    print("K", k)
                    print(request.form['flightNo'])
                    newFlight = DB_Access().executeFetchOne("SELECT * FROM flights WHERE flightNo = ? ", (request.form['flightNo'],))            
                    session['products'].append(newFlight)

                    Session.setItemCount()
                    print(session['products'])
                   
                    return redirect(url_for('available_flights'))


        #print(res)            
        if session['role'] =="P":
            return render_template('customers/booking.html',  flightNo= flightNo)

    return redirect(url_for('login'))





@app.route('/flights_search', methods=['GET', 'POST'])
def flights_search():
    if 'id' in session:
        if session['role'] =="P":
            availableAirports = DB_Access().executeFetchAll("SELECT * from flights")
            

            if request.method == 'POST':
                from_ = request.form['from']
                to_ = request.form['to']
                search_results = []
                
                results = DB_Access().executeFetchAll("SELECT * FROM flights NATURAL JOIN pilots NATURAL JOIN personen WHERE depatureAirport = ? AND destinationAirport = ? ", (from_, to_)) 
                print(results)                                                          


                session["available_flights"] = results
                print(session['available_flights'])
                return redirect(url_for('available_flights'))        

        return render_template('customers/flight_search.html', airports = availableAirports )             
    
    return 'You are not logged in'







@app.route('/shop', methods=['GET','POST'])
def shop():
    if 'id' in session:

        if session['role'] =="P":
            print(session['role'])
            if request.method == 'POST':
                print(request.method)
                if "flightNo" in request.form:
                    print(request.form)
                    id =request.form['flightNo']
                    print(id)
                    Session.deleteItemFromCart(id)
                    Session.setItemCount()
                    return render_template('customers/shop.html', total = Session.getSumm())
                else:
                    print("Someting else")

        return render_template('customers/shop.html', total = Session.getSumm())
    return 'Not logged in'


@app.route('/transaction', methods=['GET','POST'])
def transaction():
    if 'id' in session:
        if request.method == "POST":
                    print("Attempting transaction")
                    n =Transaction()
                    if n.verify("8668-8514-3799-5729", "656") != False:
                        passNo = DB_Access().executeFetchSingle("SELECT passNo FROM passenger WHERE svn = ?", (session['id'],))
                        print(passNo)
                        BOOKING( session['products'], passNo)  
                        Session.clearSessionProducts()
                        Session.setItemCount()

                        return redirect(url_for('history'))
        return redirect(url_for('history'))




@app.route('/history', methods=['GET', 'POST'])
def history():
    if 'id' in session:
        passNo = DB_Access().executeFetchSingle("SELECT passNo FROM passenger WHERE svn = ?", (session['id'],))
        hist = DB_Access().executeFetchAll("SELECT * FROM bookings NATURAL JOIN flights WHERE passNo =?", (passNo,))
        print(hist)
        if session['role'] =="P":
            
            if request.method == "POST":
                return redirect(url_for('printTicket', id=request.form['bookingID']))


            
            return render_template("customers/history.html", history= hist )


    print("Not logged in")
    return render_template("login.html")




@app.route('/history/<id>', methods= ['GET', 'POST'])
def printTicket(id):
    if 'id' in session:
        if session['role'] =="P":

            data = DB_Access().executeFetchOne("SELECT * FROM bookings NATURAL JOIN passenger NATURAL JOIN flights NATURAL join personen  WHERE bookingNo =?", (id,)) 
            print("Printer")
            print(data)
            newTicket = Ticket()
            newTicket.content(data)
            name = str(data[0])+".pdf"
            newTicket.output(dest='S').encode('latin-1', 'ignore')
            newTicket.output(name)
            return send_file(name, as_attachment=True, download_name= name)

    print("Not logged in")
    return render_template("login.html")









#BACKOFFICE ROUTES

@app.route('/backoffice')
def backoffice():
    if 'id' in session:
        if session['role'] =="T":
            #print("Logged in as", session['username'])
            return render_template("backoffice/backoffice.html", userInfo = Session.getUser(session['id']))
    print("Not logged in")
    return render_template("login.html")


@app.route('/backoffice/user', methods=('GET', 'POST'))
def userBackoffice():
    if 'id' in session:
        if session['role'] =="T":
        #user = Person.query.filter_by(svn=session['ID']).first()
        #userIn1 = [{user.svn, user.first_name, user.email, user.sex, user.birthDate, user.origin}]
        #print(userIn1)
            if request.method == 'POST':
                try:
                    svn = request.form['SVN']
                    payload = [request.form['SVN'], request.form['firstname'],request.form['email'],request.form['sex'],request.form['birthDate'], request.form['origin']]
                    updateUser =USER().user("svn", svn)
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
            
        return render_template('backoffice/userBackoffice.html', userInfo = Session.getUser(session['id']))

    return 'You are not logged in'

@app.route('/backoffice/blackbox')
def blackbox():
    if 'id' in session:
        if session['role'] =="T":
            return render_template('backoffice/blackbox.html', id = id)
        else:
            return redirect(url_for('permDenied'))





if __name__ =='__main__':
    app.run(debug=True)

