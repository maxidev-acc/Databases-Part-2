from flask import Flask, render_template, session, request, redirect, url_for, flash, send_file
import time, random, string
from flask_sqlalchemy import SQLAlchemy
from tools import Ticket
from setup import generateshopdata
import os
from tools import Transaction
from db_access import registration, authentification




#global vars for Dev
shop_data = generateshopdata()
flight_data = shop_data
history_ = shop_data[1:5]






app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



class Person(db.Model):
    svn = db.Column(db.String(10), primary_key = True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    adress = db.Column(db.String(50))
    postal = db.Column(db.String(10))
    location = db.Column(db.String(20))
    email = db.Column(db.String(50) , unique=True)
    password = db.Column(db.String() , unique=True)




def getUser(id):
        user = Person.query.filter_by(svn=id).first()
        session['user'] = [{"name":user.first_name, "email": user.email, "SVN": user.svn}]
        return session['user']



def getItemCount():
    k = len(session['products'])
    return k


def getSumm():
        sum =0
        currentproducts = session['products']
        for i in range(len(currentproducts)):
                sum =sum + int(currentproducts[i]['price'])
 
        return sum*0.9



def deleteItemFromCart(id):
        tempP = session['products']
        for prod in tempP:
            print(prod['ID'])
                        
            if int(prod['ID']) == int(id):
                for i in range(len(tempP)):
                    if str(tempP[i]['ID']) == str(id):
                        print(tempP[i])
                        del tempP[i]
                        session['products'] = tempP
                        print ("List after deletion of dictionary : " +  str(session['products']))
                        return 0
 


def createSession(user, role):
    


    session['id'] = user.svn
    session['role'] = role
    session['products'] = []
                    





@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method =="POST":
        payload = (request.form['svn'], request.form['first_name'],request.form['second_name'],request.form['adress'],request.form['postal'],request.form['location'],request.form['email'], request.form['password'])
        print(payload)
        
        if registration(payload) == True:
            
            #user = Person.query.filter_by(svn=payload[0]).first()
            print(user)
            #createSession(user, "P")
            #äreturn redirect(url_for('home'))
            return 'Sucesss'
        else:
            return("An error occured")
    return render_template("customers/register.html")





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        
            email = request.form.get('email')
            password = request.form.get('password')
         
            #user = Person.query.filter_by(email=email).first()
            credentials = (email, password)
            
            id = authentification(credentials)
          
    
            if id != False:
                user = Person.query.filter_by(svn=id).first()

                createSession(user, "P")
            
                if session['role'] =="T":
                    return redirect(url_for('backoffice'))
                if session['role'] =="P":
                    return redirect(url_for('home'))
            flash('Error')


    return render_template('login.html')


@app.route('/user', methods=('GET', 'POST'))
def user():
    if 'id' in session:
        if session['role'] =="P":
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
                    time.sleep(2)
                    flash('Sucessfully updated Profile info')
                    print("Updated user info")
                    return redirect(url_for('user'))
                except:
                    return 'An error occured'  
        
            return render_template('customers/user.html', userInfo = getUser(session['id']), itemCount = getItemCount())
    return 'You are not logged in'


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



@app.route('/available_flights', methods=['GET', 'POST'])
def available_flights():
    if 'id' in session:
        if session['role'] =="P":
            if request.method == 'POST':
                id = request.form['ID']
                print(id)
                return redirect(url_for('booking', id=id))
            return render_template('customers/flights.html', fl = session['available_flights'], itemCount = getItemCount())             
    return 'You are not logged in'


@app.route('/flights_search', methods=['GET', 'POST'])
def flights_search():
    if 'id' in session:
        if session['role'] =="P":
            if request.method == 'POST':
                from_ = request.form['from']
                to_ = request.form['to']
                search_results = []
                
                for k in flight_data: 
                    if k['origin'] == from_ and k['destination'] == to_:
                        search_results.append(k)
                session["available_flights"] = search_results
                print(session['available_flights'])
                return redirect(url_for('available_flights',itemCount = getItemCount()))        
    
        return render_template('customers/flight_search.html', itemCount = getItemCount())             
    
    return 'You are not logged in'




@app.route('/booking/<id>', methods=['GET', 'POST'])
def booking(id):
    if 'id' in session:
        if request.method == 'POST':

            for sub in flight_data: 
                if str(sub['ID']) == str(id):
                    res = sub
                    print(res)
                    temp = session['products']
                    print(type(temp))
                    temp.append(res)
                    session['products'] = temp
                    print(session['products'])
                    break
            return redirect(url_for('available_flights'))


        #print(res)            
        if session['role'] =="P":
            return render_template('customers/booking.html',  userInfo = getUser(session['id']), itemCount = getItemCount(), id= id)


@app.route('/shop', methods=['GET','POST'])
def shop():
    if 'id' in session:

        if session['role'] =="P":
            print(session['role'])
            if request.method == 'POST':
                print(request.method)
                if "ID" in request.form:
                    print(request.form)
                    id =request.form['ID']
                    print(id)
                    deleteItemFromCart(id)
                    return render_template('customers/shop.html', products= session['products'], userInfo = getUser(session['id']), itemCount = getItemCount(), total = getSumm())
                else:
                    print("Someting else")

        return render_template('customers/shop.html', products= session['products'], userInfo = getUser(session['id']), itemCount = getItemCount(), total = getSumm())

@app.route('/transaction', methods=['GET','POST'])
def transaction():
    if 'id' in session:
        if request.method == "POST":
                    print("Attempting transaction")
                    n =Transaction()
                    if n.verify("8668-8514-3799-5729", "656") != False:
                        time.sleep(4)
                        

                        #hier logik buchung in Datenbank eintragen  
                        session['products'] = []
                        return render_template('customers/shop.html', products= session['products'], userInfo = getUser(session['id']), itemCount = getItemCount(), total = getSumm())
        return redirect(url_for('history'))


@app.route('/history/<id>', methods= ['GET', 'POST'])
def printTicket(id):
    if 'id' in session:
        if session['role'] =="P":
            print("Printer")
            newTicket = Ticket()
            newTicket.content("AUT", "DE", "01.01.1999", "EAR1-Q3","Maximilian","Mustermann", "100-100" , "02.02.1999")
            name = "Ticket1.pdf"
            newTicket.output(dest='S').encode('latin-1', 'ignore')
            newTicket.output(name)
            return send_file("Ticket1.pdf", as_attachment=True, download_name='ticket.pdf')

    print("Not logged in")
    return render_template("login.html")



@app.route('/history', methods=['GET', 'POST'])
def history():
    if 'id' in session:
        if session['role'] =="P":
            if request.method == "POST":
                return redirect(url_for('printTicket', id="1test"))


            
            return render_template("customers/history.html", history=history_ )



    print("Not logged in")
    return render_template("login.html")




#BACKOFFICE ROUTES

@app.route('/backoffice')
def backoffice():
    if 'id' in session:
        if session['role'] =="T":
            #print("Logged in as", session['username'])
            return render_template("backoffice/backoffice.html", userInfo = getUser(session['id']))
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

