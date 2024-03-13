from flask import Flask, render_template, session, request, redirect, url_for, flash, send_file
import time
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from tools import Transaction, BOOKING,DB_Access,  Registration, Authentification, Ticket, USER, BLACKBOX_CHECKOUT, CANCEL_BOOKING
import shutil






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

    def ActiveSessionPasseneger(self):
        if 'id' in session:
            if session['role'] == "PASSENGER":
                return True
        else:
            return False
    
    def ActiveSessionEmployee(self):
        if 'id' in session:
            if session['role'] != "PASSENGER":
                return True
        else:
            return False

                    

#global session var 
Session = SESSION()




@app.route('/permissiondenied')
def permDenied():
    return render_template('permissiondenied.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            print("Attempting authentification")
            email = request.form.get('email')
            password = request.form.get('password')
            credentials = (email, password)
            auth=Authentification(credentials)
            
            if auth.authentification() ==True:
                active_user = USER()
                global Session
                Session= SESSION()
                user_data = active_user.user("email", email)
                permission = active_user.perm(user_data[0])
                Session.setUser(user_data, permission)

                if Session.ActiveSessionEmployee():
                        return redirect(url_for('backoffice'))
                
                if Session.ActiveSessionPasseneger():
                        return redirect(url_for('home'))
            else:
                flash(auth.errormessage())
                
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


            
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







@app.route('/user', methods=('GET', 'POST'))
def user():
    if  Session.ActiveSessionPasseneger():
            if request.method == 'POST':
    
                    data = request.form
                    svn = session['id']
                    USER().update_user(svn, data)
                    user = DB_Access().executeFetchOne("SELECT * from personen WHERE svn =?", (svn, ))
                    Session.setUser(user, session['role'])                  
                    flash('Sucessfully updated Profile info')
                    print("Updated user info")
                    return redirect(url_for('user'))
              
                    
        
            return render_template('customers/user.html')
    
    if Session.ActiveSessionEmployee():
            
            if request.method == 'POST':
                    data = request.form
                    svn = session['id']
                    USER().update_user(svn, data)
                    user = DB_Access().executeFetchOne("SELECT * from personen WHERE svn =?", (svn, ))
                    Session.setUser(user, session['role'])                  
                    flash('Sucessfully updated Profile info')
                    print("Updated user info")
                    return redirect(url_for('user'))   



             
            return render_template('customers/user.html')
    return redirect(url_for('login'))




@app.route('/')
def index():
    if Session.ActiveSessionPasseneger():
            return render_template("customers/index.html")
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if Session.ActiveSessionPasseneger():
        return render_template("customers/home.html", userInfo = Session.getUser(session['id']))
   
    return redirect(url_for('login'))


@app.route('/available_flights', methods=['GET', 'POST'])
def available_flights():
    if Session.ActiveSessionPasseneger():
            if request.method == 'POST':
                flightNo = request.form['flightNo']
                session['addtoCart'] = DB_Access().executeFetchOne("SELECT * FROM flights NATURAL JOIN pilots NATURAL JOIN airplane_type  NATURAL JOIN airplane_exemplar WHERE flightNo = ?", (flightNo,))
                print(session['addtoCart'])
                return redirect(url_for('booking', flightNo=flightNo))
            
            return render_template('customers/flights.html', fl = session['available_flights'])


    return redirect(url_for('login'))


@app.route('/booking/<flightNo>', methods=['GET', 'POST'])
def booking(flightNo):
    if Session.ActiveSessionPasseneger():
        if request.method == 'POST':
                    newFlight = DB_Access().executeFetchOne("SELECT * FROM flights WHERE flightNo = ? ", (request.form['flightNo'],))            
                    session['products'].append(newFlight)
                    Session.setItemCount()
                    return redirect(url_for('shop'))
         
     
        return render_template('customers/booking.html',  flightNo= flightNo)

    return redirect(url_for('login'))


@app.route('/flights_search', methods=['GET', 'POST'])
def flights_search():
    if Session.ActiveSessionPasseneger():

            if request.method == 'POST':
                from_ = request.form['from']
                to_ = request.form['to']
                today = str(datetime.now())
                results = DB_Access().executeFetchAll("SELECT * FROM flights NATURAL JOIN pilots NATURAL JOIN personen WHERE depatureAirport = ? AND destinationAirport = ? AND depaturetime > ? ", (from_, to_, today)) 
                session["available_flights"] = results
                
                return redirect(url_for('available_flights'))        

            return render_template('customers/flight_search.html' )             
    
    return 'You are not logged in'


@app.route('/shop', methods=['GET','POST'])
def shop():
    if Session.ActiveSessionPasseneger():
        
            if request.method == 'POST':
                if "flightNo" in request.form:
                    id =request.form['flightNo']
                    Session.deleteItemFromCart(id)
                    Session.setItemCount()
                    return render_template('customers/shop.html', total = Session.getSumm())

            return render_template('customers/shop.html', total = Session.getSumm())
    
    return redirect(url_for('login'))


@app.route('/transaction', methods=['GET','POST'])
def transaction():
    if Session.ActiveSessionPasseneger():
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
    if Session.ActiveSessionPasseneger():
        passNo = DB_Access().executeFetchSingle("SELECT passNo FROM passenger WHERE svn = ?", (session['id'],))
        hist = DB_Access().executeFetchAll("SELECT * FROM bookings NATURAL JOIN flights WHERE passNo =? ORDER BY depaturetime DESC", (passNo,))
        tod = str(datetime.now())
        return render_template("customers/history.html", history= hist , today = tod)


    print("Not logged in")
    return render_template("login.html")


@app.route('/cancel_booking/<id>', methods=['GET','POST'])
def cancel_booking(id):
    if Session.ActiveSessionPasseneger():
        if request.method == "POST":
                    print("Attempting cancelation")
                    print(id)
                    CANCEL_BOOKING(id)
                        

                    return redirect(url_for('history'))
        return redirect(url_for('history'))



@app.route('/history/<id>', methods= ['GET', 'POST'])
def printTicket(id):
    if Session.ActiveSessionPasseneger():

            data = DB_Access().executeFetchOne("SELECT * FROM bookings NATURAL JOIN passenger NATURAL JOIN flights NATURAL join personen  WHERE bookingNo =?", (id,)) 
            print("Printer")
            print(data)
            newTicket = Ticket()
            newTicket.content(data)
            name = str(data[0])+".pdf"
            newTicket.output(dest='S').encode('latin-1', 'ignore')
            newTicket.output(name)
            relative = "tickets/"+name                  
            shutil.move(name , relative )
            return send_file(relative, as_attachment=True, download_name= name)


    return render_template("login.html")









#BACKOFFICE ROUTES
#svn = 1000077152 
@app.route('/backoffice')
def backoffice():
    if Session.ActiveSessionEmployee():
            return render_template("backoffice/backoffice.html", userInfo = Session.getUser(session['id']))
    return render_template("login.html")









@app.route('/backoffice/blackbox/return',methods= ['GET', 'POST'])
def blackbox_return():
    if Session.ActiveSessionEmployee():
            
            ub = BLACKBOX_CHECKOUT().user_blackboxes(session['id'])
            if request.method == "POST":
                id = request.form['id']
                print(id)
                BLACKBOX_CHECKOUT().return_blackbox(id)
                ub = BLACKBOX_CHECKOUT().user_blackboxes(session['id'])
                return render_template('backoffice/blackbox_return.html', user_boxes = ub )


            return render_template('backoffice/blackbox_return.html', user_boxes = ub)
    else:
            return redirect(url_for('permDenied'))




@app.route('/backoffice/blackbox/checkout',methods= ['GET', 'POST'])
def blackbox_checkout():
    if Session.ActiveSessionEmployee():
            
            ab = BLACKBOX_CHECKOUT().available_blackboxes()
            blackboxids = BLACKBOX_CHECKOUT().blackbox_ids()
            if request.method == "POST":
                id = request.form['id']
                print(id)
                BLACKBOX_CHECKOUT().checkout(session['id'], id)
                ab = BLACKBOX_CHECKOUT().available_blackboxes()
                blackboxids = BLACKBOX_CHECKOUT().blackbox_ids()
                return render_template('backoffice/blackbox_checkout.html', available_boxes = ab, ids = blackboxids)


            return render_template('backoffice/blackbox_checkout.html', available_boxes = ab, ids = blackboxids)
    else:
            return redirect(url_for('permDenied'))





@app.route('/backoffice/flights/')
def employee_flights():
    if Session.ActiveSessionEmployee():
            pilotid = DB_Access().executeFetchSingle("SELECT pilot_no FROM pilots WHERE svn = ?",(session['id'], ))
            fl = DB_Access().executeFetchAll("SELECT * FROM flights WHERE pilot_no = ?", (pilotid,))
            k = str(datetime.now())
            print(k)
            return render_template("backoffice/employee_flights.html", date = k, flights = fl)
    else:
            return redirect(url_for('permDenied'))





if __name__ =='__main__':
    app.run(debug=True)

