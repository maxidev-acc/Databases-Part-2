from flask import Flask, render_template, session, request, redirect, url_for, flash
import time

flight_data = [{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}}, {"ID":2,"code": "ER45if", "price": 345.99, "departureDate": "2016/02/11", "origin": "MUA", "destination": "LAX", "emptySeats": 52, "plane": {"type": "Boeing 777", "totalSeats": 300}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}},{"ID":1, "code": "ER38sd","price": 400, "departureDate": "2016/03/20", "origin": "MUA", "destination": "SFO", "emptySeats": 0, "plane": {"type": "Boeing 737", "totalSeats": 150}}]

userIn = [{"name":"Maximilian", "email": "admin@test.at","sex": "M", "birthDate": "1999/03/20", "origin": "DE", "SVN": "5039 290399",}]

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        print("Logged in as", session['username'])
        return render_template("index.html", user =user)
    print("Not logged in")
    return render_template("login.html")
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #if request.form['username'] == 'Admin@test.com' and request.form['password'] == 'admin':
        print("Admin logged in")
        session['username'] = request.form['username']
        return redirect(url_for('index'))
        #else:
         #   return ''' Invalid User Name'''


    return render_template('login.html')



@app.route('/user', methods=('GET', 'POST'))
def user():
    if 'username' in session:
        if request.method == 'POST':
            firstname = request.form['firstname']
            sex = request.form['sex']
            print(firstname)


            if firstname:
                flash("Scucesss")
                time.sleep(2)
            return redirect(url_for('index'))
            
        return render_template('user.html', userInfo = userIn)

     


    return 'You are not logged in'

@app.route('/flights')
def flights():
    if 'username' in session:
        return render_template('flights.html', fl = flight_data)
    return 'You are not logged in'






@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ =='__main__':
    app.run(debug=True)
