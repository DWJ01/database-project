#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)


#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       port = 8889,
                       password='root',
                       db='airport_project',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
        return render_template('login.html')

@app.route('/info')
def info():
        return render_template('info.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/searchAuth', methods=['GET', 'POST'])
def searchAuth():
        source = request.form['source']
        destination = request.form['destination']
        date = request.form['date']
        cursor = conn.cursor()
        query = "select airline_name, flight_num from flight where departure_airport = %s and arrival_airport = %s and date(departure_time) = %s"
        cursor.execute(query, (source, destination, date))
        data = cursor.fetchall()
        cursor.close()
        error = None
        if (data):
                return render_template("search.html", post = data)
        else:
                error = "No such flight"
                return render_template("search.html", error = error)

@app.route('/statusAuth', methods=['GET', 'POST'])
def statusAuth():
        flight_num = request.form['flight number']
        date = request.form['arrival/departure date']
        cursor = conn.cursor()
        query = ""

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	usertype = request.form['usertype']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	if usertype == "Customer":
		query = 'SELECT * FROM customer WHERE email = %s and password = %s'
		cursor.execute(query, (username, password))
	elif usertype == "Booking Agent":
		query = 'SELECT * FROM booking_agent WHERE email = %s and password = %s'
		cursor.execute(query, (username, password))
	elif usertype == "Airline Staff":
		query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
		cursor.execute(query, (username, password))
    #stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		if usertype == "Customer":
			session['customer'] = username
			return redirect(url_for('customer_home'))
		elif usertype == "Booking Agent":
			session['booking_agent'] = username
			return redirect(url_for('agent_home'))
		elif usertype == "Airline Staff":
			session['airline_staff'] = username
			return redirect(url_for('staff_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

@app.route('/customer_home')
def customer_home():
	username = session['customer']
	return render_template('customer_home.html')

@app.route('/agent_home')
def agent_home():
	username = session['booking_agent']
	return render_template('agent_home.html')

@app.route('/staff_home')
def staff_home():
	username = session['airline_staff']
	return render_template('staff_home.html')

@app.route('/customer_register')
def customer_register():
	return render_template('customer_register.html')

@app.route('/agent_register')
def agent_register():
	return render_template('agent_register.html')

@app.route('/staff_register')
def staff_register():
	return render_template('staff_register.html')

@app.route('/c_register', methods=['GET', 'POST'])
def c_register():
	#grabs information from the forms
	email = request.form['email']
	name = request.form['name']
	password = request.form['password']
	b_number = request.form['building number']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone_num = request.form['phone number']
	pass_num = request.form['passport number']
	pass_exp = request.form['passport expiration']
	pass_country = request.form['passport country']
	dob = request.form['date of birth']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute(query, (email))
	
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('customer_register.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (email, name, password, b_number, street, city, state, phone_num, pass_num, pass_exp, pass_country, dob))
		conn.commit()
		cursor.close()
		return render_template('index.html')




@app.route('/a_register', methods=['GET', 'POST'])
def a_register():
	email = request.form['email']
	password = request.form['password']
	agent_id = request.form['booking agent id']
	cursor = conn.cursor()
	query = 'SELECT * FROM booking_agent WHERE email = %s'
	cursor.execute(query, (email))
	data = cursor.fetchone()
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('agent_register.html', error = error)
	else:
		ins = 'INSERT INTO booking_agent VALUES(%s, %s, %s)'
		cursor.execute(ins, (email, password, agent_id))
		conn.commit()
		cursor.close()
		return render_template('index.html')


	

@app.route('/s_register', methods=['GET', 'POST'])
def s_register():
	username = request.form['username']
	password = request.form['password']
	f_name = request.form['first name']
	l_name = request.form['last name']
	dob = request.form['date of birth']
	airline_name = request.form['airline name']
	cursor= conn.cursor()
	query_1 = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query_1, (username))
	data_1 = cursor.fetchone()
	query_2 = 'SELECT * FROM airline_staff WHERE airline_name = %s'
	cursor.execute(query_2, (airline_name))
	data_2 = cursor.fetchall()
	error = None
	if(data_1):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('staff_register.html', error = error)
	elif(not data_2):
		#If the previous query returns data, then user exists
		error = "There is no such airline"
		return render_template('staff_register.html', error = error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (username, password, f_name, l_name, dob, airline_name))
		conn.commit()
		cursor.close()
		return render_template('index.html')




@app.route('/staff_logout')
def staff_logout():
	session.pop('airline_staff')
	return redirect('/')

@app.route('/customer_logout')
def customer_logout():
        session.pop('customer')
        return redirect('/')

@app.route('/agent_logout')
def agent_logout():
        session.pop('booking_agent')
        return redirect('/')
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
