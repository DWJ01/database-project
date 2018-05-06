from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Page
#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

REMOTE_HOST = "https://pyecharts.github.io/assets/js"

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

@app.route('/info')
def info():
	return render_template('info.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/login')
def login():
        return render_template('login.html')

@app.route('/searchAuth', methods=['GET', 'POST'])
def searchAuth():
        source = request.form['source']
        destination = request.form['destination']
        date = request.form['date']
        cursor = conn.cursor()
        query = "SELECT flight.* FROM flight, airport as T1, airport as T2 WHERE departure_airport = T1.airport_name and arrival_airport = T2.airport_name and status = 'upcoming' and (departure_airport = %s or T1.airport_city = %s) and (arrival_airport = %s or T2.airport_city = %s) and date(departure_time) = %s"
        cursor.execute(query, (source, source, destination, destination, date))
        data = cursor.fetchall()
        cursor.close()
        error = None
        if (data):
            return render_template("search.html", data = data)
        else:
            error = "No such flight"
            return render_template("search.html", error = error)

@app.route('/statusAuth', methods=['GET', 'POST'])
def statusAuth():
        flight_num = request.form['flight number']
        time = request.form['time']
        date = request.form['date']
        cursor = conn.cursor()
        if time == "arrival":
        	query = "SELECT status FROM flight WHERE flight_num = %s and date(arrival_time) = %s"
        	cursor.execute(query, (flight_num, date))
        elif time == "departure":
        	query = "SELECT status FROM flight WHERE flight_num = %s and date(departure_time) = %s"
        	cursor.execute(query, (flight_num, date))
        data = cursor.fetchall()
        cursor.close()
        error = None
        if(data):
        	return render_template("status.html", post=data)
        else:
        	error = "No such flight"
        	return render_template("status.html", error=error)

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
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	data = cursor.fetchone()
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('staff_register.html', error = error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (username, password, f_name, l_name, dob, airline_name))
		conn.commit()
		cursor.close()
		return render_template('index.html')
        

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
		session['value'] = username
		session['password'] = password
		session['type'] = usertype
		if usertype == "Customer":
			return redirect(url_for('customer_home'))
		elif usertype == "Booking Agent":
			return redirect(url_for('agent_home'))
		elif usertype == "Airline Staff":
			cursor = conn.cursor()
			query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
			cursor.execute(query, (username))
			data = cursor.fetchone()
			airline = data['airline_name']
			session['airline'] = airline
			cursor.close()
			return redirect(url_for('staff_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username.'
		return render_template('login.html', error=error)


@app.route('/customer_home')
def customer_home():
	try:
		usertype = session['type']
		if usertype == "Customer":
			return render_template('customer_home.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/agent_home')
def agent_home():
	try:
		usertype = session['type']
		if usertype == "Booking Agent":
			return render_template('agent_home.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/staff_home')
def staff_home():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			return render_template('staff_home.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/c_view')
def c_view():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Customer":
			cursor = conn.cursor()
			query = 'SELECT airline_name, flight_num, ticket_id, departure_airport, departure_time, arrival_airport, arrival_time, price, airplane_id FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND status = "upcoming"'
			cursor.execute(query, (username))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				return render_template('c_view.html', post = data)
			else:
				error = "You do not have any flight right now. Go get some."
				return render_template('c_view.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

"""@app.route('/c_opview')
def c_opview():
	try:
		usertype = session['type']
		if usertype == "Customer":
			return render_template('c_opview.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/c_opviewAuth')
def c_opviewAuth():
	try:
		username = session['value']
		usertype = session['type']
		start = request.form['start']
		end = request.form['end']
		source = request.form['source']
		destination = request.form['destination']
		if usertype == "Customer":
			cursor = conn.cursor()
			if (source == 0) or (destination == 0):
				query = 'SELECT airline_name, flight_num, ticket_id, departure_airport, departure_time, arrival_airport, arrival_time, price, airplane_id, status FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND status = "upcoming" and (departure_time between %s and %s)'
				cursor.execute(query, (start, end))
			elif (start == 0) or (end == 0):
				query = 'SELECT airline_name, flight_num, ticket_id, departure_airport, departure_time, arrival_airport, arrival_time, price, airplane_id, status FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND status = "upcoming" and (departure_time between %s and %s)'"""



@app.route('/c_search')
def c_search():
	try:
		usertype = session['type']
		if usertype == "Customer":
			return render_template('c_search.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')


@app.route('/c_searchAuth', methods = ['GET','POST'])
def c_searchAuth():
	try:
		usertype = session['type']
		if usertype == "Customer":
			source = request.form['source']
			destination = request.form['destination']
			date = request.form['date']
			cursor = conn.cursor()
			query = "SELECT flight.* FROM flight, airport as T1, airport as T2 WHERE departure_airport = T1.airport_name and arrival_airport = T2.airport_name and status = 'upcoming' and (departure_airport = %s or T1.airport_city = %s) and (arrival_airport = %s or T2.airport_city = %s) and date(departure_time) = %s"
			cursor.execute(query, (source, source, destination, destination, date))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				return render_template('c_purchase.html', post = data)
			else:
				error = "No such flight"
				return render_template("c_search.html", error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/c_purchase')
def c_purchase():
	try:
		usertype = session['type']
		if usertype == "Customer":
			return render_template('c_purchase.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')


@app.route('/c_purchaseAuth', methods = ['GET', 'POST'])
def c_purchaseAuth():
	try:
		usertype = session['type']
		if usertype == "Customer":
			airline_name = request.form['airline name']
			flight_num = request.form['flight number']
			cursor = conn.cursor()
			query = 'SELECT ticket_id FROM ticket WHERE airline_name = %s and flight_num = %s and ticket_id not in (SELECT ticket_id from purchases)'
			cursor.execute(query, (airline_name, flight_num))
			data = cursor.fetchone()
			cursor.close()
			error = None
			if(data):
				return render_template('c_buy.html', post = data)
			else:
				error = "No ticket left"
				return render_template('c_purchase.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/c_buy')
def c_buy():
	try:
		usertype = session['type']
		if usertype == "Customer":
			return render_template('c_buy.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/c_buyAuth', methods = ['GET', 'POST'])
def c_buyAuth():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Customer":
			ticket_id = request.form['ticket id']
			cursor = conn.cursor()
			query = 'INSERT INTO purchases values (%s, %s, null, CURRENT_DATE())'
			cursor.execute(query, (ticket_id, username))
			conn.commit()
			cursor.close()
			return render_template('customer_home.html', post = "Successfully buy.")
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/c_spending')
def c_spending():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Customer":
			cursor = conn.cursor()
			query = 'SELECT sum(price) as sum FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE())'
			cursor.execute(query, (username))
			data = cursor.fetchall()
			cursor.close()
			error = None
			print(data)
			if (data):
				cursor = conn.cursor()
				query = 'SELECT month(purchase_date) as month, sum(price) as money1 FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 6 MONTH) AND CURRENT_DATE()) GROUP BY month ORDER BY month'
				cursor.execute(query, (username))
				bardata = cursor.fetchall()
				cursor.close()
				print(bardata)
				bar = Bar('Track my Spending within 6 months')
				xbar = []
				ybar =[]
				for dic in bardata:
					xbar.append(dic['month'])
					ybar.append(int(dic['money1']))
				print(xbar,ybar)
				bar.add('money',xbar,ybar)
				return render_template('c_spending.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
			else:
				error = "You have not get any ticket."
				return render_template('c_spending.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/c_sdetails')
def c_sdetails():
	return render_template('c_sdetails.html')

@app.route('/c_sdetailsAuth', methods = ['GET', 'POST'])
def c_sdetailsAuth():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Customer":
			date_start = request.form["date start"]
			date_end = request.form["date end"]
			cursor = conn.cursor()
			query = 'SELECT sum(price) as sum FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN %s AND %s)'
			cursor.execute(query, (username, date_start, date_end))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				cursor = conn.cursor()
				query = 'SELECT month(purchase_date) as month, sum(price) as money1 FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN %s AND %s) GROUP BY month ORDER BY month'
				cursor.execute(query, (username, date_start, date_end))
				bardata = cursor.fetchall()
				cursor.close()
				bar = Bar('Track my Spending in a range')
				xbar = []
				ybar =[]
				for dic in bardata:
					xbar.append(dic['month'])
					ybar.append(int(dic['money1']))
				bar.add('money',xbar,ybar)
				return render_template('c_sdetails.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
			else:
				error = "You have not get any ticket."
				return render_template('c_sdetails.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/a_view')
def a_view():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Booking Agent":
			cursor = conn.cursor()
			query = 'SELECT customer_email, airline_name, flight_num, ticket_id, departure_airport, departure_time, arrival_airport, arrival_time, price, airplane_id FROM flight natural join ticket natural join purchases natural join booking_agent WHERE email = %s AND status = "upcoming"'
			cursor.execute(query, (username))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				return render_template('a_view.html', post = data)
			else:
				error = "No flight purchased."
				return render_template('a_view.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/a_search')
def a_search():
	try:
		usertype = session['type']
		if usertype == "Booking Agent":
			return render_template('a_search.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/a_searchAuth', methods = ['GET','POST'])
def a_searchAuth():
	try:
		usertype = session['type']
		if usertype == "Booking Agent":
			source = request.form['source']
			destination = request.form['destination']
			date = request.form['date']
			cursor = conn.cursor()
			query = "SELECT flight.* FROM flight, airport as T1, airport as T2 WHERE departure_airport = T1.airport_name and arrival_airport = T2.airport_name and status = 'upcoming' and (departure_airport = %s or T1.airport_city = %s) and (arrival_airport = %s or T2.airport_city = %s) and date(departure_time) = %s"
			cursor.execute(query, (source, source, destination, destination, date))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				return render_template('a_purchase.html', post = data)
			else:
				error = "No such flight"
				return render_template("a_search.html", error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/a_purchase')
def a_purchase():
	try:
		usertype = session['type']
		if usertype == "Booking Agent":
			return render_template('a_purchase.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')
	
@app.route('/a_purchaseAuth', methods = ['GET', 'POST'])
def a_purchaseAuth():
	try:
		usertype = session['type']
		if usertype == "Booking Agent":
			airline_name = request.form['airline name']
			flight_num = request.form['flight number']
			cursor = conn.cursor()
			query = 'SELECT ticket_id FROM ticket WHERE airline_name = %s and flight_num = %s and ticket_id not in (SELECT ticket_id from purchases)'
			cursor.execute(query, (airline_name, flight_num))
			data = cursor.fetchone()
			cursor.close()
			error = None
			if(data):
				return render_template('a_buy.html', post = data)
			else:
				error = "No ticket left"
				return render_template('a_purchase.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/a_buy')
def a_buy():
	try:
		usertype = session['type']
		if usertype == "Booking Agent":
			return render_template('a_buy.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/a_buyAuth', methods = ['GET', 'POST'])
def a_buyAuth():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Booking Agent":
			cursor = conn.cursor()
			query = 'SELECT booking_agent_id FROM booking_agent WHERE email = %s'
			cursor.execute(query, (username))
			data = cursor.fetchone()
			cursor.close()
			booking_agent_id = data['booking_agent_id']
			ticket_id = request.form['ticket id']
			customer = request.form['customer']
			cursor = conn.cursor()
			query = 'INSERT INTO purchases values (%s, %s, %s, CURRENT_DATE())'
			cursor.execute(query, (ticket_id, customer, booking_agent_id))
			conn.commit()
			cursor.close()
			return render_template('agent_home.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/a_commission')
def a_commission():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Booking Agent":
			cursor = conn.cursor()
			query = "SELECT 0.1 * sum(price) as Total, count(ticket_id) as Amount, 0.1 * sum(price)/count(ticket_id) as Average FROM purchases natural join ticket natural join flight natural join booking_agent WHERE email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE())"
			cursor.execute(query, (username))
			data = cursor.fetchone()
			conn.commit()
			cursor.close()
			error = None
			if(data):
				return render_template('a_commission.html', post = data)
			else:
				error = "Nothing"
				return render_template('a_commission.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/a_commissiondetail')
def a_commissiondetail():
	try:
		usertype = session['type']
		if usertype == "Booking Agent":
			return render_template('a_commissiondetail.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/a_commissiondetailAuth', methods = ['GET', 'POST'])
def a_commissiondetailAuth():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Booking Agent":
			start = request.form['start']
			end = request.form['end']
			cursor = conn.cursor()
			query = "SELECT 0.1 * sum(price) as Total, count(ticket_id) as Amount FROM purchases natural join ticket natural join flight natural join booking_agent WHERE email = %s AND (purchase_date BETWEEN %s AND %s)"
			cursor.execute(query, (username, start, end))
			data = cursor.fetchone()
			conn.commit()
			cursor.close()
			error = None
			if(data):
				return render_template('a_commissiondetail.html', post = data)
			else:
				error = "Nothing"
				return render_template('a_commissiondetail.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/a_top')
def a_top():
	try:
		usertype = session['type']
		if usertype == "Booking Agent":
			return render_template('a_top.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/a_topmonth')
def a_topmonth():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Booking Agent":
			cursor = conn.cursor()
			query = "SELECT customer_email as email, count(ticket_id) as num FROM purchases, booking_agent WHERE purchases.booking_agent_id = booking_agent.booking_agent_id AND email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 6 MONTH) AND CURRENT_DATE())  GROUP BY customer_email ORDER BY count(ticket_id) DESC LIMIT 5"
			cursor.execute(query, (username))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				bar = Bar('View top Customers in the past 6 months')
				xbar = []
				ybar =[]
				for dic in data:
					xbar.append(dic['email'])
					ybar.append(int(dic['num']))
				bar.add('ticket number',xbar,ybar)
				return render_template('a_topmonth.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
			else:
				error = "No customer"
				return render_template('a_topmonth.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/a_topyear')
def a_topyear():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Booking Agent":
			cursor = conn.cursor()
			query = "SELECT customer_email as email, sum(price) * 0.1 as commission FROM purchases, booking_agent, flight, ticket WHERE purchases.booking_agent_id = booking_agent.booking_agent_id AND ticket.ticket_id = purchases.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()) GROUP BY customer_email ORDER BY sum(price) * 0.1 DESC LIMIT 5"
			cursor.execute(query, (username))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				bar = Bar('View top Customers in the last year')
				xbar = []
				ybar =[]
				for dic in data:
					xbar.append(dic['email'])
					ybar.append(int(dic['commission']))
				bar.add('commission',xbar,ybar)
				return render_template('a_topyear.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
			else:
				error = "No customer"
				return render_template('a_topyear.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')



@app.route('/s_view')
def s_view():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Airline Staff":
			cursor = conn.cursor()
			query = "SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, airplane_id FROM airline_staff natural join flight WHERE username = %s AND status = 'upcoming' AND (departure_time BETWEEN CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(),INTERVAL 1 MONTH))"
			cursor.execute(query, (username))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				return render_template('s_view.html', post = data)
			else:
				error = "There is no flight for my airline in the next 30 days."
				return render_template('c_view.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_viewflight')
def s_viewflight():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			return render_template('s_viewflight.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')
	
@app.route('/s_viewflightAuth', methods = ['GET', 'POST'])
def s_viewflightAuth():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			airline_name = request.form['airline name']
			flight_num = request.form['flight number']
			cursor = conn.cursor()
			query = 'SELECT ticket_id FROM ticket WHERE airline_name = %s and flight_num = %s and ticket_id not in (SELECT ticket_id from purchases)'
			cursor.execute(query, (airline_name, flight_num))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if(data):
				return render_template('a_buy.html', post = data)
			else:
				error = "No ticket left"
				return render_template('a_purchase.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_customer')
def s_customer():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			return render_template('s_customer.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route("/s_customerAuth", methods = ['GET', 'POST'])
def s_customerAuth():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Airline Staff":
			flight_num = request.form['flight number']
			cursor = conn.cursor()
			query = 'SELECT email, name FROM (flight natural join ticket natural join purchases natural join airline_staff) as T, customer WHERE T.customer_email = customer.email AND username = %s AND flight.flight_num = %s'
			cursor.execute(query, (username, flight_num))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if(data):
				return render_template('s_customer.html', post = data)
			else:
				error = "No customers"
				return render_template('s_customer.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_cflight')
def s_cflight():
	try:
		usertype = session['type']
		airline = session['airline']
		if usertype == "Airline Staff":
			cursor = conn.cursor()
			query = "SELECT flight.* FROM flight where airline_name = %s and (departure_time BETWEEN CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(),INTERVAL 1 MONTH)) and status = 'upcoming'"
			cursor.execute(query, (airline))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				return render_template('s_cflight.html', post = data)
			else:
				error = "No flights"
				return render_template('s_cflight.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_cflightAuth', methods = ['GET', 'POST'])
def s_cflightAuth():
	try:
		usertype = session['type']
		airline = session['airline']
		if usertype == "Airline Staff":
			flight_num = request.form['flight number']
			departure_airport = request.form['departure airport']
			departure_time = request.form['departure time']
			arrival_airport = request.form['arrival airport']
			arrival_time = request.form['arrival time']
			price = request.form['price']
			status = request.form['status']
			airplane_id = request.form['airplane id']
			cursor = conn.cursor()
			query = 'SELECT flight.* FROM flight WHERE airline_name = %s and flight_num = %s'
			cursor.execute(query, (airline, flight_num))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				error = "The flight already exists"
				return render_template('s_cflight.html', error = error)
			else:
				try:
					cursor = conn.cursor()
					query = 'insert into flight values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
					cursor.execute(query, (airline, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id))
					conn.commit()
					cursor.close()
					cursor = conn.cursor()
					query = "SELECT flight.* FROM flight where airline_name = %s and (departure_time BETWEEN CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(),INTERVAL 1 MONTH)) and status = 'upcoming'"
					cursor.execute(query, (airline))
					data = cursor.fetchall()
					cursor.close()
					return render_template('s_cflight.html', message = "Successfully Insert.", post = data)
				except:
					error = "Pay attention to the constraint!"
					return render_template('s_cflight.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_change')
def s_change():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			return render_template('s_change.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_changeAuth', methods = ['GET', 'POST'])
def s_changeAuth():
	try:
		usertype = session['type']
		airline = session['airline']
		if usertype == "Airline Staff":
			flight_num = request.form['flight number']
			status = request.form['status']
			cursor = conn.cursor()
			query = 'SELECT flight.* FROM flight where airline_name = %s and flight_num = %s'
			cursor.execute (query, (airline, flight_num))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				cursor = conn.cursor()
				query = 'UPDATE flight SET status = %s WHERE airline_name = %s and flight_num = %s'
				cursor.execute(query, (status, airline, flight_num))
				conn.commit()
				cursor.close()
				return render_template('s_change.html', post = "Update Successfully")
			else:
				error = "No such flight"
				return render_template('s_change.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_airplane')
def s_airplane():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			return render_template('s_airplane.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_airplaneAuth', methods = ['GET', 'POST'])
def s_airplaneAuth():
	try:
		usertype = session['type']
		airline = session['airline']
		if usertype == "Airline Staff":
			airplane_id = request.form['airplane id']
			seats = request.form['seats']
			cursor = conn.cursor()
			query = 'SELECT airplane.* FROM airplane WHERE airline_name = %s and airplane_id = %s'
			cursor.execute(query, (airline, airplane_id))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if(data):
				error = "The airplane already exists."
				return render_template('s_airplane.html', error = error)
			else:
				cursor = conn.cursor()
				query = 'insert into airplane values (%s, %s, %s)'
				cursor.execute(query, (airline, airplane_id, seats))
				conn.commit()
				cursor.close()
				cursor = conn.cursor()
				query = 'SELECT airplane.* FROM airplane WHERE airline_name = %s'
				cursor.execute(query, (airline))
				data = cursor.fetchall()
				cursor.close()
				return render_template('s_airplane.html', post = data)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_airport')
def s_airport():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			return render_template('s_airport.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_airportAuth', methods = ['GET', 'POST'])
def s_airportAuth():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			airport_name = request.form['airport name']
			airport_city = request.form['airport city']
			cursor = conn.cursor()
			query = 'SELECT airport.* FROM airport WHERE airport_name = %s'
			cursor.execute(query, (airport_name))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				error = "This airport already exists."
				return render_template('s_airport.html', error = error)
			else:
				cursor = conn.cursor()
				query = 'insert into airport values (%s, %s)'
				cursor.execute(query, (airport_name, airport_city))
				conn.commit()
				cursor.close()
				return render_template('s_airport.html', post = "Successfully Inserted")
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_agent')
def s_agent():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			return render_template('s_agent.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_agentsalemonth')
def s_agentsalemonth():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			cursor = conn.cursor()
			query = "SELECT email, booking_agent_id, count(ticket_id) as Total FROM purchases natural join booking_agent WHERE (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE()) GROUP BY email  ORDER BY count(ticket_id) DESC LIMIT 5"
			cursor.execute(query)
			data = cursor.fetchall()
			cursor.close()
			error = None
			if(data):
				return render_template('s_agentsalemonth.html', post = data)
			else:
				error = "Not enought booking agent"
				return render_template('s_agentsalemonth.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_agentsaleyear')
def s_agentsaleyear():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			cursor = conn.cursor()
			query = "SELECT email, booking_agent_id, count(ticket_id) as Total FROM purchases natural join booking_agent WHERE (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()) GROUP BY email  ORDER BY count(ticket_id) DESC LIMIT 5"
			cursor.execute(query)
			data = cursor.fetchall()
			cursor.close()
			error = None
			if(data):
				return render_template('s_agentsaleyear.html', post = data)
			else:
				error = "Not enought booking agent"
				return render_template('s_agentsaleyear.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_agentcommission')
def s_agentcommission():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			cursor = conn.cursor()
			query = "SELECT email, booking_agent_id, sum(price) * 0.1 as Commission FROM ticket natural join flight natural join purchases natural join booking_agent WHERE (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()) GROUP BY email  ORDER BY sum(price) * 0.1 DESC LIMIT 5"
			cursor.execute(query)
			data = cursor.fetchall()
			cursor.close()
			error = None
			if(data):
				return render_template('s_agentcommission.html', post = data)
			else:
				error = "Not enought booking agent"
				return render_template('s_agentcommission.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_fcustomer')
def s_fcustomer():
	try:
		usertype = session['type']
		airline = session['airline']
		if usertype == "Airline Staff":
			cursor = conn.cursor()
			query = "SELECT email, name, count(ticket_id) as Total FROM ticket natural join purchases as T, customer WHERE airline_name = %s and T.customer_email = customer.email and (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()) GROUP BY email  ORDER BY count(ticket_id) DESC LIMIT 1"
			cursor.execute(query, (airline))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if(data):
				return render_template('s_fcustomer.html', post = data)
			else:
				error = "Not enought customer"
				return render_template('s_fcustomer.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_particular')
def s_particular():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			return render_template('s_particular.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_particularAuth', methods = ['GET', 'POST'])
def s_particularAuth():
	try:
		usertype = session['type']
		airline = session['airline']
		if usertype == "Airline Staff":
			customer_email = request.form['customer']
			cursor = conn.cursor()
			query = "SELECT flight.* FROM flight natural join ticket natural join purchases WHERE customer_email = %s and airline_name = %s"
			cursor.execute(query, (customer_email, airline))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if(data):
				return render_template('s_particular.html', post = data)
			else:
				error = "Taking no flight of this airline"
				return render_template('s_particular.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')


@app.route('/s_report')
def s_report():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Airline Staff":

			return render_template('s_report.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_rdates')
def s_rdates():
	return render_template('s_rdates.html')

@app.route('/s_rdatesAuth', methods = ['GET', 'POST'])
def s_rdatesAuth():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			start = request.form['start']
			end = request.form['end']
			cursor = conn.cursor()
			query = 'SELECT count(ticket_id) as num FROM purchases WHERE purchase_date BETWEEN %s AND %s'
			cursor.execute(query, (start, end))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if(data):
				cursor = conn.cursor()
				query = 'SELECT month(purchase_date) as month, count(ticket_id) as num FROM purchases WHERE purchase_date BETWEEN %s AND %s GROUP BY month ORDER BY month'
				cursor.execute(query, (start, end))
				bardata = cursor.fetchall()
				cursor.close()
				xbar = []
				ybar = []
				for dic in bardata:
					xbar.append(dic['month'])
					ybar.append(int(dic['num']))
				bar = Bar('View report in a range')
				bar.add('number of tickets', xbar, ybar)
				return render_template('s_rdates.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
			else:
				error = "No ticket is sold out."
				return render_template('s_rdates.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_ryear')
def s_ryear():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			cursor = conn.cursor()
			query = 'SELECT count(ticket_id) as num FROM purchases WHERE purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()'
			cursor.execute(query)
			data = cursor.fetchall()
			cursor.close()
			error = None
			if(data):
				cursor = conn.cursor()
				query = 'SELECT month(purchase_date) as month, count(ticket_id) as num FROM purchases WHERE purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE() GROUP BY month ORDER BY month'
				cursor.execute(query)
				bardata = cursor.fetchall()
				cursor.close()
				xbar = []
				ybar = []
				for dic in bardata:
					xbar.append(dic['month'])
					ybar.append(int(dic['num']))
				bar = Bar('View report last year')
				bar.add('number of tickets', xbar, ybar)
				return render_template('s_ryear.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
			else:
				error = "No ticket is sold out."
				return render_template('s_ryear.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_rmonth')
def s_rmonth():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			cursor = conn.cursor()
			query = 'SELECT count(ticket_id) as num FROM purchases WHERE purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE()'
			cursor.execute(query)
			data = cursor.fetchall()
			cursor.close()
			error = None
			if(data):
				return render_template('s_rmonth.html', post = data)
			else:
				error = "No ticket is sold out."
				return render_template('s_rmonth.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_compare')
def s_compare():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Airline Staff":
			return render_template('s_compare.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_compareyear')
def s_compareyear():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			cursor = conn.cursor()
			query = 'SELECT sum(price) FROM purchases, ticket, flight WHERE purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND booking_agent_id is null AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE())'
			cursor.execute(query)
			direct = cursor.fetchone()
			cursor.close()
			cursor = conn.cursor()
			query = 'SELECT sum(price) FROM purchases, ticket, flight WHERE purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND booking_agent_id is not null AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE())'
			cursor.execute(query)
			indirect = cursor.fetchone()
			cursor.close()
			error = None
			xpie = ['direct sale', 'indirect sale']
			ypie = []
			print(direct, indirect)
			for key in direct:
				if direct[key] == None:
					ypie.append(0)
				else:
					ypie.append(int(direct[key]))
			for key in indirect:
				if indirect[key] == None:
					ypie.append(0)
				else:
					ypie.append(int(indirect[key]))
			pie = Pie('Revenue in last year')
			pie.add('',xpie,ypie,is_label_show = True)
			return render_template('s_compareyear.html', myechart = pie.render_embed(), host = REMOTE_HOST, script_list=pie.get_js_dependencies())
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_comparemonth')
def s_comparemonth():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			cursor = conn.cursor()
			query = 'SELECT sum(price) FROM purchases, ticket, flight WHERE purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND booking_agent_id is null AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE())'
			cursor.execute(query)
			direct = cursor.fetchone()
			cursor.close()
			cursor = conn.cursor()
			query = 'SELECT sum(price) FROM purchases, ticket, flight WHERE purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND booking_agent_id is not null AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE())'
			cursor.execute(query)
			indirect = cursor.fetchone()
			cursor.close()
			error = None
			xpie = ['direct sale', 'indirect sale']
			ypie = []
			for key in direct:
				if direct[key] == None:
					ypie.append(0)
				else:
					ypie.append(int(direct[key]))
			for key in indirect:
				if indirect[key] == None:
					ypie.append(0)
				else:
					ypie.append(int(indirect[key]))
			pie = Pie('Revenue in last month')
			pie.add('',xpie,ypie,is_label_show = True)
			return render_template('s_comparemonth.html', myechart = pie.render_embed(), host = REMOTE_HOST, script_list=pie.get_js_dependencies())
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_destination')
def s_destination():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Airline Staff":
			return render_template('s_destination.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_destinationmonth')
def s_destinationmonth():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			cursor = conn.cursor()
			query = "SELECT airport_city, count(ticket_id) as Total FROM purchases natural join ticket natural join flight, airport WHERE airport_name = arrival_airport and (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 3 MONTH) AND CURRENT_DATE()) GROUP BY airport_city ORDER BY count(ticket_id) DESC LIMIT 3"
			cursor.execute(query)
			data = cursor.fetchall()
			cursor.close()
			error = None
			if(data):
				return render_template('s_destinationmonth.html', post = data)
			else:
				error = "No such place"
				return render_template('s_destinationmonth.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/s_destinationyear')
def s_destinationyear():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			cursor = conn.cursor()
			query = "SELECT airport_city, count(ticket_id) as Total FROM purchases natural join ticket natural join flight, airport WHERE airport_name = arrival_airport and (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()) GROUP BY airport_city ORDER BY count(ticket_id) DESC LIMIT 3"
			cursor.execute(query)
			data = cursor.fetchall()
			cursor.close()
			error = None
			if(data):
				return render_template('s_destinationyear.html', post = data)
			else:
				error = "No such place"
				return render_template('s_destinationyear.html', error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')



@app.route('/staff_logout')
def staff_logout():
	try:
		usertype = session['type']
		if usertype == "Airline Staff":
			session.pop('value')
			session.pop('password')
			session.pop('type')
			session.pop('airline')
			return redirect('/')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')
	

@app.route('/customer_logout')
def customer_logout():
	try:
		usertype = session['type']
		if usertype == "Customer":
			session.pop('value')
			session.pop('password')
			session.pop('type')
			return redirect('/')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')


@app.route('/agent_logout')
def agent_logout():
	try:
		usertype = session['type']
		if usertype == "Booking Agent":
			session.pop('value')
			session.pop('password')
			session.pop('type')
			return redirect('/')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
