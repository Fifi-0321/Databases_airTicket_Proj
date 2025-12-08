from flask import Flask, render_template, request, url_for, redirect, session, flash
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'my_super_secret_key_for_AirSystem_2025'

# Set up the database connection with Localhost:
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='AirTicketReservationSystem'
)


# Homepage:
@app.route('/')
def index():
    # Login / Register / Search Flights (Public surface):
    if 'email' in session:
        role = session['role']
        if role == 'customer':
            return redirect(url_for('customer_home'))
        elif role == 'agent':
            return redirect(url_for('agent_home'))
        elif role == 'staff':
            return redirect(url_for('staff_home'))
    return render_template('index.html')


# Login page:
@app.route('/login')
def login():
    return render_template('login.html')


# Registration page:
@app.route('/register')
def register():
    return render_template('register.html')


# Login Authorization:
@app.route('/loginAuth', methods=['POST'])
def loginAuth():
    role = request.form['role']
    email = request.form['email']
    password = hashlib.md5(request.form['password'].encode()).hexdigest() # Use md5 in hashlib to hash user passwords

    cursor = conn.cursor()
    user = None

    if role == 'customer':
        query = "SELECT * FROM customer WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

    elif role == 'agent':
        query = "SELECT * FROM booking_agent WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

    elif role == 'staff':
        query = "SELECT * FROM airline_staff WHERE username = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()


    if user:
        session['email'] = email
        session['role'] = role

        # If the user is Airline staff，the permission list is loaded and stored in the session after successful login:
        if role == 'staff':
            perm_cursor = conn.cursor()
            perm_cursor.execute("SELECT permission_type FROM permission WHERE username = %s", (email,))
            session['permissions'] = [row[0] for row in perm_cursor.fetchall()]
            perm_cursor.close()

        cursor.close()

        if role == 'customer':
            return redirect(url_for('customer_home'))
        elif role == 'agent':
            return redirect(url_for('agent_home'))
        elif role == 'staff':
            return redirect(url_for('staff_home'))
    else:
        cursor.close()
        error = 'Invalid credentials'
        return render_template('login.html', error=error)


# Registration Authorization:
@app.route('/registerAuth', methods=['POST'])
def registerAuth():
    role = request.form['role']
    email = request.form['email']
    password = hashlib.md5(request.form['password'].encode()).hexdigest()

    cursor = conn.cursor()

    if role == 'customer':
        cursor.execute("SELECT * FROM customer WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("This customer already exists")
            return redirect(url_for('register'))

        try:
            cursor.execute("""
                INSERT INTO customer (email, password, name, building_number, street, city, state,
                    phone_number, passport_number, passport_expiration, passport_country, date_of_birth)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                email, password,
                request.form['cust_name'], request.form['building_number'], request.form['street'],
                request.form['city'], request.form['state'], request.form['phone_number'],
                request.form['passport_number'], request.form['passport_expiration'],
                request.form['passport_country'], request.form['cust_dob']
            ))
            conn.commit()
            flash("Customer registered successfully!")
        except Exception as e:
            flash("Error registering customer: " + str(e))

    elif role == 'agent':
        cursor.execute("SELECT * FROM booking_agent WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("This agent already exists")
            return redirect(url_for('register'))
        
        # Get the highest current booking_agent_id
        cursor.execute("SELECT MAX(booking_agent_id) FROM booking_agent")
        result = cursor.fetchone()
        new_booking_agent_id = result[0] + 1 if result[0] is not None else 1  # Start at 1 if no records exist
        
        try:
            cursor.execute("INSERT INTO booking_agent (email, password, booking_agent_id) VALUES (%s, %s, %s)",
                        (email, password, new_booking_agent_id))
            conn.commit()
            flash("Agent registered successfully!")
        except Exception as e:
            flash("Error registering agent: " + str(e))
    elif role == 'staff':
        cursor.execute("SELECT * FROM airline_staff WHERE username = %s", (email,))
        
        if cursor.fetchone():
            flash("This staff already exists")
            return redirect(url_for('register'))

        airline_name = request.form['airline_name'].strip()

        # Check: airline_name must not be empty
        if not airline_name:
            flash("Airline name is required for staff registration.")
            return redirect(url_for('register'))

        # Optional: verify airline name exists in the 'airline' table
        cursor.execute("SELECT * FROM airline WHERE airline_name = %s", (airline_name,))
        if cursor.fetchone() is None:
            flash(f"The airline '{airline_name}' does not exist.")
            return redirect(url_for('register'))

        try:
            cursor.execute("""
                INSERT INTO airline_staff (username, password, first_name, last_name, date_of_birth, airline_name)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                email, password,
                request.form['staff_first'], request.form['staff_last'],
                request.form['staff_dob'], airline_name
            ))
            conn.commit()
            flash("Staff registered successfully!")
        except Exception as e:
            flash("Error registering staff: " + str(e))
    
    cursor.close()
    return redirect(url_for('index'))











# Homepages for Different Use Cases:
@app.route('/customer_home')
def customer_home():
    if 'email' in session and session['role'] == 'customer':
        return render_template('customer_home.html')
    return redirect(url_for('login'))

@app.route('/agent_home')
def agent_home():
    if 'email' in session and session['role'] == 'agent':
        return render_template('agent_home.html')
    return redirect(url_for('login'))

@app.route('/staff_home')
def staff_home():
    if 'email' not in session or session['role'] != 'staff':
        return redirect(url_for('login'))

    cursor = conn.cursor()
    cursor.execute("SELECT permission_type FROM permission WHERE username = %s", (session['email'],))
    permissions = [row[0] for row in cursor.fetchall()]
    cursor.close()

    return render_template("staff_home.html", permissions=permissions)









# Public Part:

def get_airports_from_input(cursor, user_input):
    """
    Given a user input string (which may be a city name, an alias, or an airport code),
    return a list of airport codes that match the input.

    This function supports the Multi-Airport Cities / City Alias feature required in the
    anti-automation challenge. It expands an input into all relevant airport codes.

    Examples:
        "Berlin"  -> ["BER", "TXL"]
        "BER"     -> ["BER"]
        "BJ"      -> ["PEK"]   (if alias added to city_airport_map)
        "Beijing" -> ["PEK"]
        "Shanghai City" -> ["PVG"]

    Resolution order (additive):
        1. Check city_airport_map for alias match
        2. Check if input is a direct airport code
        3. Check if input matches airport_city in airport table
        (All results are combined; duplicates removed)
    """

    # No filtering if input is empty
    if not user_input:
        return None

    airports = set()

    # ---------------------------------------------------------
    # 1. Look up aliases in city_airport_map (most flexible)
    # ---------------------------------------------------------
    cursor.execute("""
        SELECT airport_name
        FROM city_airport_map
        WHERE LOWER(city_alias) = LOWER(%s)
    """, (user_input,))
    for row in cursor.fetchall():
        airports.add(row["airport_name"])

    # ---------------------------------------------------------
    # 2. Check if the input is a direct airport name (PVG, BER, FRA...)
    # ---------------------------------------------------------
    cursor.execute("""
        SELECT airport_name
        FROM airport
        WHERE LOWER(airport_name) = LOWER(%s)
    """, (user_input,))
    row = cursor.fetchone()
    if row:
        airports.add(row["airport_name"])

    # ---------------------------------------------------------
    # 3. Check if the input is a city name (airport_city column)
    # ---------------------------------------------------------
    cursor.execute("""
        SELECT airport_name
        FROM airport
        WHERE LOWER(airport_city) = LOWER(%s)
    """, (user_input,))
    for row in cursor.fetchall():
        airports.add(row["airport_name"])

    # Return None if nothing matched at all
    if not airports:
        return None

    # Convert to list for safe SQL insertion
    return list(airports)

# Public Search for Upcoming Flight:
from datetime import datetime
@app.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
    flights = None

    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Validate dates
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.')
            return render_template('search_flights.html', flights=None)

        if start_date_obj > end_date_obj:
            flash('Start date cannot be after end date.')
            return render_template('search_flights.html', flights=None)

        cursor = conn.cursor(dictionary=True)

        # NEW: expand city/alias/airport to airport list
        source_airports = get_airports_from_input(cursor, source)
        dest_airports = get_airports_from_input(cursor, destination)

        if not source_airports:
            flash("No airports found matching origin.")
            return render_template('search_flights.html', flights=None)

        if not dest_airports:
            flash("No airports found matching destination.")
            return render_template('search_flights.html', flights=None)

        # Build SQL using FIND_IN_SET() to avoid dynamic IN (...)
        query = """
            SELECT f.*
            FROM flight f
            WHERE FIND_IN_SET(f.departure_airport, %s)
              AND FIND_IN_SET(f.arrival_airport, %s)
              AND DATE(f.departure_time) BETWEEN %s AND %s
        """

        params = [
            ",".join(source_airports),
            ",".join(dest_airports),
            start_date_obj,
            end_date_obj,
        ]

        cursor.execute(query, params)
        flights = cursor.fetchall()
        cursor.close()

    return render_template('search_flights.html', flights=flights)



# [NEW] Public Lookup of Flight Status:
@app.route('/check_flight_status', methods=['GET', 'POST'])
def check_flight_status():
    flight_info = None
    error = None

    if request.method == 'POST':
        airline = request.form.get('airline_name', '').strip()
        flight_num = request.form.get('flight_num', '').strip()

        if not airline or not flight_num:
            error = "Airline and flight number are required."
        else:
            cursor = conn.cursor(dictionary=True)
            # Search for Upcoming flights in default:
            query = """
                SELECT airline_name, flight_num, departure_airport, arrival_airport,
                       departure_time, arrival_time, status
                FROM flight
                WHERE airline_name = %s AND flight_num = %s
            """
            cursor.execute(query, (airline, flight_num))
            flight_info = cursor.fetchone()
            cursor.close()

            if not flight_info:
                error = "No such flight found."

    return render_template('check_flight_status.html',
                           flight=flight_info,
                           error=error)






# Customer Part:

# Customer 1 -- Search for flights and Purchase tickets:
# [New]: Add `purchase_authorization_customer` page to let customer double-check and confirm purchase
@app.route('/purchase_authorization_customer', methods=['POST'])
def purchase_authorization_customer():
    if 'email' not in session or session['role'] != 'customer':
        return redirect(url_for('login'))

    airline = request.form.get('airline')
    flight_num = request.form.get('flight_num')

    if not airline or not flight_num:
        flash("Missing flight information.")
        return redirect(url_for('search_flights'))

    cursor = conn.cursor(dictionary=True)

    # Step 1: Search for flight information
    cursor.execute("""
        SELECT f.airline_name, f.flight_num, f.departure_airport, f.arrival_airport,
               f.departure_time, f.arrival_time, f.price, f.status
        FROM flight f
        WHERE f.airline_name = %s AND f.flight_num = %s
    """, (airline, flight_num))
    flight = cursor.fetchone()

    if not flight:
        cursor.close()
        flash("Flight not found.")
        return redirect(url_for('search_flights'))

    # Step 2: Check whether Repeat Purchase
    cursor.execute("""
        SELECT COUNT(*) AS cnt
        FROM ticket t
        JOIN purchases p ON t.ticket_id = p.ticket_id
        WHERE t.airline_name = %s
          AND t.flight_num = %s
          AND p.customer_email = %s
    """, (airline, flight_num, session['email']))
    row = cursor.fetchone()

    # Close uniformly as all queries have been completed:
    cursor.close()

    has_purchased = row['cnt'] > 0 if row else False

    return render_template(
        'purchase_authorization_customer.html',
        flight=flight,
        has_purchased=has_purchased
    )


@app.route('/purchase_ticket', methods=['POST'])
def purchase_ticket():
    if 'email' not in session or session['role'] != 'customer':
        return redirect(url_for('login'))

    # Step0: Search for flights - share the same page with the public and get search result from "search_flights":
    airline = request.form.get('airline')
    flight_num = request.form.get('flight_num')
    password = request.form.get('password')

    cursor = conn.cursor()

    # [New] Step 1: verify customer password again (purchase authorization)
    cursor.execute("SELECT password FROM customer WHERE email = %s", (session['email'],))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        flash("User not found.")
        return redirect(url_for('login'))

    stored_hash = row[0]

    input_hash = hashlib.md5(password.encode()).hexdigest() if password else None

    # If wrong password - fail to purchase and back to the search page:
    if not password or input_hash != stored_hash:
        cursor.close()
        flash("Purchase authorization failed: incorrect password!")
        return redirect(url_for('search_flights'))

    # Step 2: Check if the flight is sold out
    cursor.execute("""
        SELECT a.seats
        FROM flight f JOIN airplane a ON f.airline_name = a.airline_name AND f.airplane_id = a.airplane_id
        WHERE f.airline_name = %s AND f.flight_num = %s
    """, (airline, flight_num))
    result = cursor.fetchone()
    if not result:
        flash("Flight not found.")
        return redirect(url_for('purchase_ticket'))

    max_seats = result[0]

    # Count how many tickets have been sold for this flight
    cursor.execute("""
        SELECT COUNT(*) FROM ticket
        WHERE airline_name = %s AND flight_num = %s
    """, (airline, flight_num))
    sold = cursor.fetchone()[0]

    if sold >= max_seats:
        flash('Sold out! No more tickets available for this flight.')
        cursor.close()
        return redirect(url_for('purchase_ticket'))

    # Step 3: Create new ticket (generate ticket_id)
    cursor.execute("SELECT MAX(ticket_id) FROM ticket")
    max_id = cursor.fetchone()[0]
    ticket_id = 1 if max_id is None else max_id + 1

    # Step 4: Insert new ticket
    insert_ticket = "INSERT INTO ticket (ticket_id, airline_name, flight_num) VALUES (%s, %s, %s)"
    cursor.execute(insert_ticket, (ticket_id, airline, flight_num))

    # Step 5: Insert into purchases
    insert_purchase = """
        INSERT INTO purchases (ticket_id, customer_email, purchase_date)
        VALUES (%s, %s, CURDATE())
    """
    cursor.execute(insert_purchase, (ticket_id, session['email']))

    conn.commit()
    cursor.close()

    flash('Ticket purchased successfully!')
    return redirect(url_for('customer_home'))


# Customer 2 -- Review Purchased Flights:
# [Revise]: Add on filters(date ranges, origin, and destination)
from datetime import datetime
@app.route('/view_customer_flights', methods=['GET'])
def view_customer_flights():
    # Ensure user is logged in and is a customer
    if 'email' not in session or session.get('role') != 'customer':
        return redirect(url_for('login'))

    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    origin_input = request.args.get('origin', '').strip()
    destination_input = request.args.get('destination', '').strip()
    show = request.args.get('show', '').strip()

    cursor = conn.cursor(dictionary=True)

    # Base query
    base_query = """
        SELECT f.*
        FROM flight f
        JOIN ticket t ON f.airline_name = t.airline_name
                     AND f.flight_num = t.flight_num
        JOIN purchases p ON t.ticket_id = p.ticket_id
        WHERE p.customer_email = %s
    """
    params = [session['email']]

    # Default View: show only upcoming flights
    if show not in ('all', 'past'):
        base_query += " AND DATE(f.departure_time) >= CURDATE() "
    elif show == 'past':
        base_query += " AND DATE(f.departure_time) < CURDATE() "

    # Date range filters
    if start_date_str:
        base_query += " AND DATE(f.departure_time) >= %s "
        params.append(start_date_str)

    if end_date_str:
        base_query += " AND DATE(f.departure_time) <= %s "
        params.append(end_date_str)

    # ================================
    # NEW: City Alias / Multi-Airport Support
    # ================================
    origin_airports = get_airports_from_input(cursor, origin_input)
    destination_airports = get_airports_from_input(cursor, destination_input)

    # Origin filter
    if origin_input and origin_airports:
        placeholder = ",".join(["%s"] * len(origin_airports))
        base_query += f" AND f.departure_airport IN ({placeholder}) "
        params.extend(origin_airports)

    # Destination filter
    if destination_input and destination_airports:
        placeholder = ",".join(["%s"] * len(destination_airports))
        base_query += f" AND f.arrival_airport IN ({placeholder}) "
        params.extend(destination_airports)

    # Sort results
    base_query += " ORDER BY f.departure_time ASC "

    # Execute
    cursor.execute(base_query, tuple(params))
    flights = cursor.fetchall()
    cursor.close()

    return render_template(
        'view_customer_flights.html',
        flights=flights,
        start_date=start_date_str,
        end_date=end_date_str,
        origin=origin_input,
        destination=destination_input,
        show=show or 'upcoming'
    )


# Customer 3 -- Review spending:
# [Revise]: Default showing the monthly spending in last 12 months and bar chart for last 6 months
from datetime import date, timedelta
import io, base64
import matplotlib.pyplot as plt

@app.route('/customer_spending', methods=['GET', 'POST'])
def customer_spending():
    if 'email' not in session or session['role'] != 'customer':
        return redirect(url_for('login'))

    cursor = conn.cursor(dictionary=True)

    today = date.today() # Keep track of the current date
    default_start = today - timedelta(days=365)
    default_end = today

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not start_date or start_date.strip() == '':
            start_date = default_start.strftime('%Y-%m-%d')
        if not end_date or end_date.strip() == '':
            end_date = default_end.strftime('%Y-%m-%d')

        use_last_six_for_chart = False
    else:
        start_date = default_start.strftime('%Y-%m-%d')
        end_date = default_end.strftime('%Y-%m-%d')
        use_last_six_for_chart = True

    # Total spending:
    total_query = """
        SELECT SUM(f.price) AS total_spent
        FROM purchases p
        JOIN ticket t
            ON p.ticket_id = t.ticket_id
        JOIN flight f
            ON t.airline_name = f.airline_name
           AND t.flight_num   = f.flight_num
        WHERE p.customer_email = %s
          AND p.purchase_date BETWEEN %s AND %s
    """
    cursor.execute(total_query, (session['email'], start_date, end_date))
    total_row = cursor.fetchone()
    total_spent = float(total_row['total_spent']) if total_row and total_row['total_spent'] else 0.0

    # Monthly spending:
    monthly_query = """
        SELECT DATE_FORMAT(p.purchase_date, '%Y-%m') AS month,
               SUM(f.price) AS total
        FROM purchases p
        JOIN ticket t
            ON p.ticket_id = t.ticket_id
        JOIN flight f
            ON t.airline_name = f.airline_name
           AND t.flight_num   = f.flight_num
        WHERE p.customer_email = %s
          AND p.purchase_date BETWEEN %s AND %s
        GROUP BY month
        ORDER BY month ASC
    """

    cursor.execute(monthly_query, (session['email'], start_date, end_date))
    monthly_spending = cursor.fetchall()


    # Generate Bar Chart:
    chart_url = None
    if monthly_spending:
        if use_last_six_for_chart and len(monthly_spending) > 6:
            data_for_chart = monthly_spending[-6:]
        else:
            data_for_chart = monthly_spending

        months = [row['month'] for row in data_for_chart]
        amounts = [row['total'] for row in data_for_chart]

        img = io.BytesIO()
        plt.figure(figsize=(10, 6))
        plt.bar(months, amounts, color='steelblue')
        plt.xlabel('Month')
        plt.ylabel('Amount Spent ($)')
        plt.title('Monthly Spending')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        chart_url = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()

    cursor.close()

    return render_template(
        'customer_spending.html',
        total_spent=total_spent,
        monthly_spending=monthly_spending,
        start_date=start_date,
        end_date=end_date,
        chart_url=chart_url
    )













# Booking Agent Part:

# Agent 1 -- Search for flights and Purchase tickets:
# [New]: Add `purchase_authorization_agent` page to let agent double-check and confirm purchase
@app.route('/purchase_authorization_agent', methods=['POST'])
def purchase_authorization_agent():
    if 'email' not in session or session.get('role') != 'agent':
        return redirect(url_for('login'))

    airline = request.form.get('airline')
    flight_num = request.form.get('flight_num')
    customer_email = request.form.get('customer_email')

    if not airline or not flight_num or not customer_email:
        flash("Missing flight or customer information.")
        return redirect(url_for('search_flights'))

    cursor = conn.cursor(dictionary=True)

    # Step 1: Check if the agent is working for this airline
    cursor.execute("""
        SELECT airline_name
        FROM booking_agent_work_for
        WHERE email = %s
    """, (session['email'],))
    rows = cursor.fetchall()

    if not rows:
        cursor.close()
        flash("You are not currently working for any airline, so you cannot purchase tickets.")
        return redirect(url_for('search_flights'))

    allowed_airlines = {r['airline_name'] for r in rows}
    if airline not in allowed_airlines:
        cursor.close()
        flash("You do not work for the selected airline.")
        return redirect(url_for('search_flights'))

    # Step 2: Check flight information (display on confirmation page)
    cursor.execute("""
        SELECT f.airline_name, f.flight_num,
               f.departure_airport, f.arrival_airport,
               f.departure_time, f.arrival_time,
               f.price, f.status
        FROM flight f
        WHERE f.airline_name = %s AND f.flight_num = %s
    """, (airline, flight_num))
    flight = cursor.fetchone()

    if not flight:
        cursor.close()
        flash("Flight not found.")
        return redirect(url_for('search_flights'))

    # Step 3: Check whether this customer has already purchased this flight
    cursor.execute("""
        SELECT COUNT(*) AS cnt
        FROM ticket t
        JOIN purchases p ON t.ticket_id = p.ticket_id
        WHERE t.airline_name = %s
          AND t.flight_num = %s
          AND p.customer_email = %s
    """, (airline, flight_num, customer_email))
    row = cursor.fetchone()
    cursor.close()

    has_purchased = row['cnt'] > 0 if row else False

    return render_template(
        'purchase_authorization_agent.html',
        flight=flight,
        has_purchased=has_purchased,
        customer_email=customer_email
    )


@app.route('/purchase_ticket_agent', methods=['GET', 'POST'])
def purchase_ticket_agent():
    if 'email' not in session or session['role'] != 'agent':
        return redirect(url_for('login'))

    if request.method == 'GET':
        return redirect(url_for('search_flights'))

    airline = request.form.get('airline')
    flight_num = request.form.get('flight_num')
    customer_email = request.form.get('customer_email')
    password = request.form.get('password') 

    cursor = conn.cursor()

    # Step 0: Verify agent password again (purchase authorization)
    cursor.execute("""
        SELECT password
        FROM booking_agent
        WHERE email = %s
    """, (session['email'],))
    pwd_row = cursor.fetchone()
    if not pwd_row:
        cursor.close()
        flash("Invalid agent account.")
        return redirect(url_for('login'))

    stored_hash = pwd_row[0]
    input_hash = hashlib.md5(password.encode()).hexdigest() if password else None
    if not password or input_hash != stored_hash:
        cursor.close()
        flash("Purchase authorization failed: incorrect password!")
        return redirect(url_for('search_flights'))

    # Step 1: Fetch all airlines the agent works for
    cursor.execute("""
        SELECT airline_name
        FROM booking_agent_work_for
        WHERE email = %s
    """, (session['email'],))
    rows = cursor.fetchall()

    if not rows:
        flash("You are not currently working for any airline, so you cannot purchase tickets.")
        cursor.close()
        return redirect(url_for('search_flights'))

    # Step 2: Check if selected airline is in the list
    allowed_airlines = {r[0] for r in rows}
    if airline not in allowed_airlines:
        flash("You do not work for the selected airline.")
        cursor.close()
        return redirect(url_for('purchase_ticket_agent'))

    # Step 3: Check if flight exists and seats available
    cursor.execute("""
        SELECT a.seats
        FROM flight f
        JOIN airplane a ON f.airline_name = a.airline_name AND f.airplane_id = a.airplane_id
        WHERE f.airline_name = %s AND f.flight_num = %s
    """, (airline, flight_num,))
    result = cursor.fetchone()
    if not result:
        flash("Flight not found.")
        cursor.close()
        return redirect(url_for('purchase_ticket_agent'))

    max_seats = result[0]

    # Step 4: Check tickets sold
    cursor.execute("""
        SELECT COUNT(*) FROM ticket
        WHERE airline_name = %s AND flight_num = %s
    """, (airline, flight_num,))
    sold = cursor.fetchone()[0]

    if sold >= max_seats:
        flash('Sold out! No more tickets available for this flight.')
        cursor.close()
        return redirect(url_for('purchase_ticket_agent'))

    # Step 5: Generate new ticket ID
    cursor.execute("SELECT MAX(ticket_id) FROM ticket")
    max_id = cursor.fetchone()[0]
    ticket_id = 1 if max_id is None else max_id + 1

    # Step 6: Insert new ticket
    cursor.execute("INSERT INTO ticket (ticket_id, airline_name, flight_num) VALUES (%s, %s, %s)",
                   (ticket_id, airline, flight_num))

    # Step 7: Get booking_agent_id from email
    cursor.execute("SELECT booking_agent_id FROM booking_agent WHERE email = %s", (session['email'],))
    agent_row = cursor.fetchone()
    if not agent_row:
        flash("Invalid agent account.")
        cursor.close()
        return redirect(url_for('purchase_ticket_agent'))

    booking_agent_id = agent_row[0]

    # Step 8: Insert into purchases table
    cursor.execute("""
        INSERT INTO purchases (ticket_id, customer_email, booking_agent_id, purchase_date)
        VALUES (%s, %s, %s, CURDATE())
    """, (ticket_id, customer_email, booking_agent_id))

    conn.commit()
    cursor.close()

    flash('Ticket purchased successfully!')
    return redirect(url_for('agent_home'))



# Agent 2 -- View Purchased flights:
@app.route('/view_agent_flights', methods=['GET', 'POST'])
def view_agent_flights():
    if 'email' not in session or session['role'] != 'agent':
        return redirect(url_for('login'))

    cursor = conn.cursor(dictionary=True)

    # Get filters from form
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    source = request.form.get('source')
    destination = request.form.get('destination')

    # Base query
    query = """
        SELECT f.*
        FROM flight f
        JOIN ticket t ON f.flight_num = t.flight_num AND f.airline_name = t.airline_name
        JOIN purchases p ON t.ticket_id = p.ticket_id
        JOIN booking_agent b ON b.booking_agent_id = p.booking_agent_id
        JOIN airport a1 ON f.departure_airport = a1.airport_name
        JOIN airport a2 ON f.arrival_airport = a2.airport_name
        WHERE b.email = %s
    """

    params = [session['email']]

    # Add filters dynamically
    if start_date:
        query += " AND DATE(f.departure_time) >= %s"
        params.append(start_date)
    if end_date:
        query += " AND DATE(f.departure_time) <= %s"
        params.append(end_date)
    if source:
        query += " AND (a1.airport_name = %s OR a1.airport_city = %s)"
        params.extend([source, source])
    if destination:
        query += " AND (a2.airport_name = %s OR a2.airport_city = %s)"
        params.extend([destination, destination])

    query += " ORDER BY f.departure_time DESC"

    cursor.execute(query, params)
    flights = cursor.fetchall()
    cursor.close()

    return render_template('view_agent_flights.html',
                           flights=flights,
                           start_date=start_date,
                           end_date=end_date,
                           source=source,
                           destination=destination)



# Agent 3 -- View my commission:
from datetime import datetime, timedelta
@app.route('/agent_commission', methods=['GET', 'POST'])
def agent_commission():
    if 'email' not in session or session['role'] != 'agent':
        return redirect(url_for('login'))

    cursor = conn.cursor()

    today = datetime.now().date()
    default_start = today - timedelta(days=30)

    if request.method == 'POST':
        start_date = request.form.get('start_date') or default_start.strftime('%Y-%m-%d')
        end_date = request.form.get('end_date') or today.strftime('%Y-%m-%d')
    else:
        start_date = default_start.strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')

    # Get list of airlines the agent works for
    cursor.execute("""
        SELECT airline_name
        FROM booking_agent_work_for
        WHERE email = %s
    """, (session['email'],))
    airlines = [row[0] for row in cursor.fetchall()]

    if not airlines:
        flash("You are not associated with any airline.")
        return render_template('agent_commission.html',
                               total_commission=0,
                               avg_commission=0,
                               total_tickets=0,
                               start_date=start_date,
                               end_date=end_date)

    airline_placeholders = ','.join(['%s'] * len(airlines))
    params = [session['email'], start_date, end_date] + airlines

    # Total commission in date range for these airlines
    total_query = f"""
        SELECT SUM(f.price * 0.1)
        FROM purchases p
        JOIN ticket t ON p.ticket_id = t.ticket_id
        JOIN flight f ON t.airline_name = f.airline_name AND t.flight_num = f.flight_num
        JOIN booking_agent ba ON p.booking_agent_id = ba.booking_agent_id
        WHERE ba.email = %s
        AND p.purchase_date BETWEEN %s AND %s
        AND f.airline_name IN ({airline_placeholders})
    """
    cursor.execute(total_query, params)
    total_commission = cursor.fetchone()[0] or 0

    # Average commission per ticket
    avg_query = f"""
        SELECT AVG(f.price * 0.1)
        FROM purchases p
        JOIN ticket t ON p.ticket_id = t.ticket_id
        JOIN flight f ON t.airline_name = f.airline_name AND t.flight_num = f.flight_num
        JOIN booking_agent ba ON p.booking_agent_id = ba.booking_agent_id
        WHERE ba.email = %s
        AND p.purchase_date BETWEEN %s AND %s
        AND f.airline_name IN ({airline_placeholders})
    """
    cursor.execute(avg_query, params)
    avg_commission = cursor.fetchone()[0] or 0

    # Total number of tickets sold
    count_query = f"""
        SELECT COUNT(*)
        FROM purchases p
        JOIN ticket t ON p.ticket_id = t.ticket_id
        JOIN flight f ON t.airline_name = f.airline_name AND t.flight_num = f.flight_num
        JOIN booking_agent ba ON p.booking_agent_id = ba.booking_agent_id
        WHERE ba.email = %s
        AND p.purchase_date BETWEEN %s AND %s
        AND f.airline_name IN ({airline_placeholders})
    """
    cursor.execute(count_query, params)
    total_tickets = cursor.fetchone()[0]

    cursor.close()

    return render_template('agent_commission.html',
                           total_commission=total_commission,
                           avg_commission=avg_commission,
                           total_tickets=total_tickets,
                           start_date=start_date,
                           end_date=end_date)



# Agent 4 -- View Top Customers:
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64

@app.route('/view_top_customers')
def view_top_customers():
    if 'email' not in session or session['role'] != 'agent':
        return redirect(url_for('login'))

    cursor = conn.cursor(dictionary=True)

    # Get agent ID
    cursor.execute("SELECT booking_agent_id FROM booking_agent WHERE email = %s", (session['email'],))
    agent_info = cursor.fetchone()
    if not agent_info:
        flash("Agent not found.")
        cursor.close()
        return redirect(url_for('agent_home'))

    agent_id = agent_info['booking_agent_id']

    # 1. Top 5 customers by tickets (last 6 months)
    six_months_ago = datetime.now() - timedelta(days=180)
    cursor.execute("""
        SELECT p.customer_email, COUNT(*) AS ticket_count
        FROM purchases p
        WHERE p.booking_agent_id = %s AND p.purchase_date >= %s
        GROUP BY p.customer_email
        ORDER BY ticket_count DESC
        LIMIT 5
    """, (agent_id, six_months_ago))
    top_customers_tickets = cursor.fetchall()

    # 2. Top 5 customers by commission (last year)
    one_year_ago = datetime.now() - timedelta(days=365)
    cursor.execute("""
        SELECT p.customer_email, ROUND(SUM(f.price * 0.1), 2) AS total_commission
        FROM purchases p
        JOIN ticket t ON p.ticket_id = t.ticket_id
        JOIN flight f ON t.airline_name = f.airline_name AND t.flight_num = f.flight_num
        WHERE p.booking_agent_id = %s AND p.purchase_date >= %s
        GROUP BY p.customer_email
        ORDER BY total_commission DESC
        LIMIT 5
    """, (agent_id, one_year_ago))
    top_customers_commission = cursor.fetchall()

    cursor.close()

    def create_chart(labels, values, title, ylabel, color):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(labels, values, color=color)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')

    # Prepare chart data
    ticket_labels = [row['customer_email'] for row in top_customers_tickets]
    ticket_counts = [row['ticket_count'] for row in top_customers_tickets]
    ticket_chart = create_chart(ticket_labels, ticket_counts, "Top 5 Customers by Tickets", "Tickets", "skyblue")

    commission_labels = [row['customer_email'] for row in top_customers_commission]
    commission_values = [row['total_commission'] for row in top_customers_commission]
    commission_chart = create_chart(commission_labels, commission_values, "Top 5 Customers by Commission", "Commission (CNY)", "lightcoral")

    return render_template('agent_top_customers.html',
                           top_customers_tickets=top_customers_tickets,
                           top_customers_commission=top_customers_commission,
                           ticket_chart=ticket_chart,
                           commission_chart=commission_chart)














# Airline Staff Part:

# Staff 1 -- View My Flights:
# Step 1: View all flights for the airline the staff works for
@app.route('/staff_view_flights', methods=['GET', 'POST'])
def staff_view_flights():
    if 'email' not in session or session['role'] != 'staff':
        return redirect(url_for('login'))

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT airline_name FROM airline_staff WHERE username = %s", (session['email'],))
    airline_name = cursor.fetchone()['airline_name']

    # Get filters
    from datetime import datetime, timedelta
    today = datetime.today()

    start_date_raw = request.form.get('start_date')
    end_date_raw = request.form.get('end_date')
    source = request.form.get('source')
    destination = request.form.get('destination')
    time_filter = request.form.get('time_filter')

    # Default date range: show all flights in next 30 days
    if not start_date_raw:
        start_date = today
    else:
        start_date = datetime.strptime(start_date_raw, '%Y-%m-%d')

    if not end_date_raw:
        end_date = today + timedelta(days=30)
    else:
        end_date = datetime.strptime(end_date_raw, '%Y-%m-%d')

    is_default_view = (
        not start_date_raw and
        not end_date_raw and
        not source and
        not destination and
        (not time_filter or time_filter == 'all')
    )

    # Build base query
    query = """
        SELECT * FROM flight
        WHERE airline_name = %s
        AND departure_time BETWEEN %s AND %s
    """
    params = [airline_name, start_date, end_date]

    if source:
        query += " AND (departure_airport LIKE %s OR departure_airport IN (SELECT airport_name FROM airport WHERE airport_city LIKE %s))"
        params.extend([f'%{source}%', f'%{source}%'])

    if destination:
        query += " AND (arrival_airport LIKE %s OR arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city LIKE %s))"
        params.extend([f'%{destination}%', f'%{destination}%'])

    # Apply time filter
    if time_filter == 'future':
        query += " AND departure_time > NOW()"
    elif time_filter == 'past':
        query += " AND departure_time < NOW()"

    query += " ORDER BY departure_time ASC"

    cursor.execute(query, tuple(params))
    flights = cursor.fetchall()
    cursor.close()

    return render_template(
        'staff_view_flights.html',
        flights=flights,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        source=source or '',
        destination=destination or '',
        time_filter=time_filter or '',
        is_default_view=is_default_view
    )

# Step 2: View customers on a specific flight
@app.route('/staff_view_customers')
def staff_view_customers():
    if 'email' not in session or session['role'] != 'staff':
        return redirect(url_for('login'))

    airline = request.args.get('airline')
    flight_num = request.args.get('flight_num')

    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT DISTINCT c.name, c.email
        FROM customer c
        JOIN purchases p ON c.email = p.customer_email
        JOIN ticket t ON p.ticket_id = t.ticket_id
        WHERE t.airline_name = %s AND t.flight_num = %s
    """
    cursor.execute(query, (airline, flight_num))
    customers = cursor.fetchall()
    cursor.close()

    return render_template('staff_view_customers.html', customers=customers, flight_num=flight_num)





# Staff 2 -- Create New Flights [Admin ONLY]:
@app.route('/staff_create_flight', methods=['GET', 'POST'])
def staff_create_flight():
    if 'email' not in session or session['role'] != 'staff':
        return redirect(url_for('login'))

    cursor = conn.cursor()

    # Get airline of the staff
    query = "SELECT airline_name FROM airline_staff WHERE username = %s"
    cursor.execute(query, (session['email'],))
    result = cursor.fetchone()
    if not result:
        flash("Invalid staff session.")
        return redirect(url_for('login'))
    airline_name = result[0]

    # Check permission
    permission_query = "SELECT * FROM permission WHERE username = %s AND permission_type = 'Admin'"
    cursor.execute(permission_query, (session['email'],))
    is_admin = cursor.fetchone() is not None

    if not is_admin:
        flash("Unauthorized: Admin permission required to create flights.")
        return redirect(url_for('staff_home'))

    if request.method == 'POST':
        flight_num = request.form['flight_num']
        departure_airport = request.form['departure_airport']
        departure_time = request.form['departure_time']
        arrival_airport = request.form['arrival_airport']
        arrival_time = request.form['arrival_time']
        price = request.form['price']
        status = request.form['status']
        airplane_id = request.form['airplane_id']

        insert_query = """
            INSERT INTO flight (airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(insert_query, (airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id))
            conn.commit()
            flash('Flight created successfully!')
            return redirect(url_for('staff_create_flight'))
        except Exception as e:
            flash('Error: Could not create flight. ' + str(e))

    # Show upcoming flights operated by this airline in the next 30 days
    flights_query = """
        SELECT * FROM flight
        WHERE airline_name = %s AND departure_time >= NOW() AND departure_time <= DATE_ADD(NOW(), INTERVAL 30 DAY)
        ORDER BY departure_time
    """
    cursor.execute(flights_query, (airline_name,))
    upcoming_flights = cursor.fetchall()
    cursor.close()

    return render_template('staff_create_flight.html', flights=upcoming_flights)



# Staff 3 -- Add New Airplanes [Admin ONLY]:
@app.route('/staff_add_airplane', methods=['GET', 'POST'])
def staff_add_airplane():
    if 'email' not in session or session['role'] != 'staff':
        return redirect(url_for('login'))

    cursor = conn.cursor()

    cursor.execute(
        "SELECT airline_name FROM airline_staff WHERE username = %s",
        (session['email'],)
    )
    result = cursor.fetchone()
    if not result:
        cursor.close()
        flash("Airline staff not found.")
        return redirect(url_for('staff_home'))

    airline_name = result[0]

    # Check Admin permission
    cursor.execute(
        "SELECT * FROM permission WHERE username = %s AND permission_type = 'Admin'",
        (session['email'],)
    )
    is_admin = cursor.fetchone() is not None

    if not is_admin:
        cursor.close()
        flash("Unauthorized: Admin permission required to add airplanes.")
        return redirect(url_for('staff_home'))


    if request.method == 'POST':
        airplane_id = request.form['airplane_id']
        seats = request.form['seats']

        insert_query = """
            INSERT INTO airplane (airline_name, airplane_id, seats)
            VALUES (%s, %s, %s)
        """
        try:
            cursor.execute(insert_query, (airline_name, airplane_id, seats))
            conn.commit()
            flash('Airplane added successfully!')
        except Exception as e:
            print("Error inserting airplane:", e)
            flash('Error: Could not add airplane.')

        cursor.close()
        return redirect(url_for('staff_add_airplane'))

    # Show existing airplanes for this airline
    cursor.execute(
        """
        SELECT airplane_id, seats
        FROM airplane
        WHERE airline_name = %s
        ORDER BY airplane_id
        """,
        (airline_name,)
    )
    airplanes = cursor.fetchall()
    cursor.close()

    return render_template(
        'staff_add_airplane.html',
        is_admin=True,
        airplanes=airplanes,
        airline_name=airline_name
    )


# Staff 4 -- Add New Airport [Admin ONLY]:
@app.route('/staff_add_airport', methods=['GET', 'POST'])
def staff_add_airport():
    if 'email' not in session or session['role'] != 'staff':
        return redirect(url_for('login'))

    cursor = conn.cursor()

    # Get airline of the staff
    cursor.execute(
        "SELECT airline_name FROM airline_staff WHERE username = %s",
        (session['email'],)
    )
    result = cursor.fetchone()
    if not result:
        cursor.close()
        flash("Airline staff not found.")
        return redirect(url_for('staff_home'))
    airline_name = result[0]

    # Check Admin permission
    cursor.execute(
        "SELECT * FROM permission WHERE username = %s AND permission_type = 'Admin'",
        (session['email'],)
    )
    is_admin = cursor.fetchone() is not None

    if not is_admin:
        cursor.close()
        flash("Unauthorized: Admin permission required to add airports.")
        return redirect(url_for('staff_home'))

    if request.method == 'POST':
        airport_name = request.form['airport_name']
        airport_city = request.form['airport_city']

        try:
            cursor.execute(
                "INSERT INTO airport (airport_name, airport_city) VALUES (%s, %s)",
                (airport_name, airport_city)
            )
            conn.commit()
            flash("Airport added successfully!")
        except Exception as e:
            flash("Error adding airport: " + str(e))
        cursor.close()
        return redirect(url_for('staff_add_airport'))

    # Show existing airports
    cursor.execute("SELECT * FROM airport ORDER BY airport_name")
    airports = cursor.fetchall()
    cursor.close()

    return render_template(
        "staff_add_airport.html",
        airports=airports,
        is_admin=True,
        airline_name=airline_name
    )






# Staff 5 -- Update Status of Flights [Operator ONLY]:
@app.route('/staff_change_status', methods=['GET', 'POST'])
def staff_change_status():
    if 'email' not in session or session['role'] != 'staff':
        return redirect(url_for('login'))

    cursor = conn.cursor()

    # Get airline the staff belongs to
    cursor.execute(
        "SELECT airline_name FROM airline_staff WHERE username = %s",
        (session['email'],)
    )
    result = cursor.fetchone()
    if not result:
        cursor.close()
        flash("Staff not associated with any airline.")
        return redirect(url_for('staff_home'))
    airline_name = result[0]

    # Check if user has Operator permission
    cursor.execute(
        "SELECT * FROM permission WHERE username = %s AND permission_type = 'Operator'",
        (session['email'],)
    )
    is_operator = cursor.fetchone() is not None

    if not is_operator:
        cursor.close()
        flash("Unauthorized: Operator permission required to change flight status.")
        return redirect(url_for('staff_home'))

    # Handle form submission
    if request.method == 'POST':
        key = request.form['flight_key']
        new_status = request.form['new_status']

        try:
            flight_num, departure_time_str = key.split('|', 1)

            from datetime import datetime
            departure_time = datetime.strptime(departure_time_str, '%Y-%m-%d %H:%M:%S')

            cursor.execute(
                """
                UPDATE flight
                SET status = %s
                WHERE airline_name = %s
                  AND flight_num = %s
                  AND departure_time = %s
                """,
                (new_status, airline_name, flight_num, departure_time)
            )
            conn.commit()

            if cursor.rowcount == 0:
                flash("No matching flight found to update.")
            else:
                flash("Flight status updated successfully.")
        except Exception as e:
            print("Error updating flight status:", e)
            flash("Error updating flight status: " + str(e))

        cursor.close()
        return redirect(url_for('staff_change_status'))

    # On GET, show all future flights for this airline
    cursor.execute(
        """
        SELECT flight_num,
               departure_airport,
               arrival_airport,
               departure_time,
               arrival_time,
               status
        FROM flight
        WHERE airline_name = %s
          AND departure_time >= NOW()
        ORDER BY departure_time ASC
        """,
        (airline_name,)
    )
    flights = cursor.fetchall()
    cursor.close()

    return render_template(
        "staff_change_status.html",
        flights=flights,
        airline_name=airline_name,
        is_operator=is_operator
    )







# Staff 6 -- View all agents:
from datetime import datetime, timedelta

@app.route('/staff_view_agents')
def staff_view_agents():
    if 'email' not in session or session['role'] != 'staff':
        return redirect(url_for('login'))

    cursor = conn.cursor(dictionary=True)

    # Get the airline the current staff belongs to
    cursor.execute("SELECT airline_name FROM airline_staff WHERE username = %s", (session['email'],))
    result = cursor.fetchone()
    if not result:
        flash("No airline found for this staff member.")
        return redirect(url_for('staff_home'))
    airline_name = result['airline_name']

    today = datetime.today()
    one_month_ago = today - timedelta(days=30)
    one_year_ago = today - timedelta(days=365)

    # 1. Top 5 agents by ticket sales in the past month
    cursor.execute("""
        SELECT ba.email, COUNT(*) AS tickets_sold
        FROM purchases p
        JOIN booking_agent ba ON p.booking_agent_id = ba.booking_agent_id
        JOIN ticket t ON p.ticket_id = t.ticket_id
        JOIN booking_agent_work_for baf ON ba.email = baf.email
        WHERE p.purchase_date >= %s AND t.airline_name = %s AND baf.airline_name = %s
        GROUP BY ba.email
        ORDER BY tickets_sold DESC
        LIMIT 5
    """, (one_month_ago, airline_name, airline_name))
    top_month_sales = cursor.fetchall()

    # 2. Top 5 agents by ticket sales in the past year
    cursor.execute("""
        SELECT ba.email, COUNT(*) AS tickets_sold
        FROM purchases p
        JOIN booking_agent ba ON p.booking_agent_id = ba.booking_agent_id
        JOIN ticket t ON p.ticket_id = t.ticket_id
        JOIN booking_agent_work_for baf ON ba.email = baf.email
        WHERE p.purchase_date >= %s AND t.airline_name = %s AND baf.airline_name = %s
        GROUP BY ba.email
        ORDER BY tickets_sold DESC
        LIMIT 5
    """, (one_year_ago, airline_name, airline_name))
    top_year_sales = cursor.fetchall()

    # 3. Top 5 agents by commission in the past month
    cursor.execute("""
        SELECT ba.email, SUM(f.price * 0.1) AS total_commission
        FROM purchases p
        JOIN ticket t ON p.ticket_id = t.ticket_id
        JOIN flight f
          ON t.flight_num = f.flight_num
         AND t.airline_name = f.airline_name
        JOIN booking_agent ba ON p.booking_agent_id = ba.booking_agent_id
        JOIN booking_agent_work_for baf ON ba.email = baf.email
        WHERE p.purchase_date >= %s
          AND f.airline_name = %s
          AND baf.airline_name = %s
        GROUP BY ba.email
        ORDER BY total_commission DESC
        LIMIT 5
    """, (one_month_ago, airline_name, airline_name))
    top_month_commission = cursor.fetchall()

    # 4. Top 5 agents by commission in the past year
    cursor.execute("""
        SELECT ba.email, SUM(f.price * 0.1) AS total_commission
        FROM purchases p
        JOIN ticket t ON p.ticket_id = t.ticket_id
        JOIN flight f ON t.flight_num = f.flight_num AND t.airline_name = f.airline_name
        JOIN booking_agent ba ON p.booking_agent_id = ba.booking_agent_id
        JOIN booking_agent_work_for baf ON ba.email = baf.email
        WHERE p.purchase_date >= %s AND f.airline_name = %s AND baf.airline_name = %s
        GROUP BY ba.email
        ORDER BY total_commission DESC
        LIMIT 5
    """, (one_year_ago, airline_name, airline_name))
    top_year_commission = cursor.fetchall()

    cursor.close()


    return render_template(
        'staff_view_agents.html',
        top_month_sales=top_month_sales,
        top_year_sales=top_year_sales,
        top_year_commission=top_year_commission,
        top_month_commission=top_month_commission,
        airline_name=airline_name
    )





# Staff 7 -- View Frequent customers:
@app.route('/staff_frequent_customers', methods=['GET', 'POST'])
def staff_frequent_customers():
    if 'email' not in session or session['role'] != 'staff':
        return redirect(url_for('login'))

    cursor = conn.cursor(dictionary=True)

    # Step 1: Get staff's airline
    cursor.execute("SELECT airline_name FROM airline_staff WHERE username = %s", (session['email'],))
    result = cursor.fetchone()
    if not result:
        flash("Airline staff not associated with any airline.")
        return redirect(url_for('staff_home'))
    airline_name = result['airline_name']

    # Step 2: Get all top customers with same max ticket count
    top_customer_query = """
        SELECT p.customer_email, COUNT(*) AS ticket_count
        FROM purchases p
        JOIN ticket t ON p.ticket_id = t.ticket_id
        WHERE t.airline_name = %s
        AND p.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        GROUP BY p.customer_email
        HAVING ticket_count = (
            SELECT MAX(ticket_counts.ticket_count)
            FROM (
                SELECT p.customer_email, COUNT(*) AS ticket_count
                FROM purchases p
                JOIN ticket t ON p.ticket_id = t.ticket_id
                WHERE t.airline_name = %s
                AND p.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
                GROUP BY p.customer_email
            ) AS ticket_counts
        )
    """
    cursor.execute(top_customer_query, (airline_name, airline_name))
    top_customers = cursor.fetchall()

    # Step 3: Handle search for specific customer's flights
    customer_flights = []
    if request.method == 'POST':
        customer_email = request.form['customer_email']
        cursor.execute("""
            SELECT f.*
            FROM flight f
            JOIN ticket t ON f.airline_name = t.airline_name AND f.flight_num = t.flight_num
            JOIN purchases p ON t.ticket_id = p.ticket_id
            WHERE p.customer_email = %s AND f.airline_name = %s
            ORDER BY f.departure_time DESC
        """, (customer_email, airline_name))
        customer_flights = cursor.fetchall()

    cursor.close()
    return render_template("staff_frequent_customers.html",
                           top_customers=top_customers,
                           customer_flights=customer_flights)





# Staff 8 -- View Monthly Sales(Tickets sold) Report:
@app.route('/staff_reports', methods=['GET', 'POST'])
def staff_reports():
    if 'email' not in session or session['role'] != 'staff':
        return redirect(url_for('login'))

    cursor = conn.cursor(dictionary=True)

    # Get staff's airline
    cursor.execute("SELECT airline_name FROM airline_staff WHERE username = %s", (session['email'],))
    result = cursor.fetchone()
    if not result:
        flash("No airline found for staff.")
        return redirect(url_for('staff_home'))

    airline_name = result['airline_name']
    today = datetime.today()

    # Set default dates first
    start_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')

    # Priority 1: use form inputs (manual)
    if request.method == 'POST':
        if request.form.get('start_date'):
            start_date = request.form['start_date']
        if request.form.get('end_date'):
            end_date = request.form['end_date']
    # Priority 2: override with preset only if NOT a POST
    elif request.method == 'GET':
        preset = request.args.get("preset")
        if preset == "last30":
            start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        elif preset == "last_year":
            start_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')

    # Fetch total ticket count
    cursor.execute("""
        SELECT COUNT(*) AS total_tickets
        FROM purchases p
        JOIN ticket t ON p.ticket_id = t.ticket_id
        WHERE t.airline_name = %s
        AND p.purchase_date BETWEEN %s AND %s
    """, (airline_name, start_date, end_date))
    total_tickets = cursor.fetchone()['total_tickets']

    # Month-wise breakdown
    cursor.execute("""
        SELECT DATE_FORMAT(p.purchase_date, '%Y-%m') AS month, COUNT(*) AS ticket_count
        FROM purchases p
        JOIN ticket t ON p.ticket_id = t.ticket_id
        WHERE t.airline_name = %s
        AND p.purchase_date BETWEEN %s AND %s
        GROUP BY month
        ORDER BY month ASC
    """, (airline_name, start_date, end_date))
    rows = cursor.fetchall()

    months = [row['month'] for row in rows]
    ticket_counts = [row['ticket_count'] for row in rows]

    cursor.close()

    # Plot chart
    img = io.BytesIO()
    plt.figure(figsize=(10, 6))
    plt.bar(months, ticket_counts, color='skyblue')
    plt.xlabel('Month')
    plt.ylabel('Tickets Sold')
    plt.title(f'Ticket Sales from {start_date} to {end_date}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return render_template("staff_reports.html",
                           total_tickets=total_tickets,
                           start_date=start_date,
                           end_date=end_date,
                           months=months,
                           ticket_counts=ticket_counts,
                           chart_url=chart_url)




# Staff 9 -- Delay vs. on-time statistics:

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta
from flask import render_template, session, redirect, url_for, flash

@app.route('/staff_delay_vs_ontime')
def staff_delay_vs_ontime():
    """
    Show analytics: Delay vs. On-time statistics for the staff's airline.
    - Last 30 days: #on-time vs #delayed flights
    - Last 1 year:  #on-time vs #delayed flights
    A flight is considered 'delayed' if flight.status = 'delayed',
    and 'on-time' otherwise.
    """
    if 'email' not in session or session.get('role') != 'staff':
        return redirect(url_for('login'))

    cursor = conn.cursor(dictionary=True)

    # Get the airline name of current staff
    cursor.execute(
        "SELECT airline_name FROM airline_staff WHERE username = %s",
        (session['email'],)
    )
    result = cursor.fetchone()
    if not result:
        cursor.close()
        flash("No airline found for this staff.")
        return redirect(url_for('staff_home'))

    airline_name = result['airline_name']

    now = datetime.now()
    last_month = now - timedelta(days=30)
    last_year = now - timedelta(days=365)

    # Helper SQL: count delayed vs on-time flights in a time window
    # delayed: status = 'delayed'
    # on-time: status NOT IN ('delayed')
    sql_delay_stats = """
        SELECT
            SUM(CASE WHEN status = 'delayed' THEN 1 ELSE 0 END) AS delayed_count,
            SUM(CASE WHEN status <> 'delayed' OR status IS NULL THEN 1 ELSE 0 END) AS ontime_count
        FROM flight f
        WHERE f.airline_name = %s
          AND f.departure_time >= %s
    """

    # ---- Last Month stats ----
    cursor.execute(sql_delay_stats, (airline_name, last_month))
    last_month_stats = cursor.fetchone() or {'delayed_count': 0, 'ontime_count': 0}

    # ---- Last Year stats ----
    cursor.execute(sql_delay_stats, (airline_name, last_year))
    last_year_stats = cursor.fetchone() or {'delayed_count': 0, 'ontime_count': 0}

    cursor.close()

    lm_delayed = int(last_month_stats.get('delayed_count') or 0)
    lm_ontime = int(last_month_stats.get('ontime_count') or 0)
    ly_delayed = int(last_year_stats.get('delayed_count') or 0)
    ly_ontime = int(last_year_stats.get('ontime_count') or 0)

    last_month_stats['delayed_count'] = lm_delayed
    last_month_stats['ontime_count'] = lm_ontime
    last_year_stats['delayed_count'] = ly_delayed
    last_year_stats['ontime_count'] = ly_ontime

    # Helper to create bar chart encoded as base64
    def create_bar_chart(labels, values, title, ylabel):
        values = [int(v) for v in values]

        fig, ax = plt.subplots(figsize=(6, 4))
        colors = ['lightcoral', 'lightgreen']
        bars = ax.bar(labels, values, color=colors)
        ax.set_title(title)
        ax.set_ylabel(ylabel)

        max_val = max(values) if values else 0

        if max_val > 0:
            ax.set_ylim(0, max_val * 1.25)

        for bar, v in zip(bars, values):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + max_val * 0.03,  
                str(v),
                ha='center',
                va='bottom',              
                fontsize=9,
                color='black'
            )

        plt.tight_layout()

        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Create charts only if there is at least one flight in the period
    lastmonth_chart = None
    if lm_delayed + lm_ontime > 0:
        lastmonth_chart = create_bar_chart(
            labels=['Delayed', 'On-time'],
            values=[lm_delayed, lm_ontime],
            title='Delay vs On-time (Last 30 Days)',
            ylabel='Number of Flights'
        )

    lastyear_chart = None
    if ly_delayed + ly_ontime > 0:
        lastyear_chart = create_bar_chart(
            labels=['Delayed', 'On-time'],
            values=[ly_delayed, ly_ontime],
            title='Delay vs On-time (Last 1 Year)',
            ylabel='Number of Flights'
        )

    return render_template(
        'staff_delay_vs_ontime.html',
        airline_name=airline_name,
        last_month_stats=last_month_stats,
        last_year_stats=last_year_stats,
        lastmonth_chart=lastmonth_chart,
        lastyear_chart=lastyear_chart
    )



# Staff 10 -- View Top Destination from purchased flights:
@app.route('/staff_top_destinations')
def staff_top_destinations():    
    if 'email' not in session or session['role'] != 'staff':
        return redirect(url_for('login')) 
    
    cursor=conn.cursor(dictionary = True) 
    
    # Get staff's airline
    cursor.execute("SELECT airline_name FROM airline_staff WHERE username = %s", (session['email'],))
    result = cursor.fetchone()
    if not result:
        flash("No airline found for staff.")
        return redirect(url_for('staff_home'))

    airline_name = result['airline_name']
    
    # Top 3 destinations
    query_destinations = """
        SELECT a.airport_city, COUNT(a.airport_city) AS destination_count
        FROM purchases p 
            JOIN ticket t ON p.ticket_id = t.ticket_id
            JOIN flight f ON t.flight_num = f.flight_num AND f.airline_name = t.airline_name
            JOIN airport a ON f.arrival_airport = a.airport_name
        WHERE p.purchase_date >= %s AND f.airline_name = %s
        GROUP BY a.airport_city
        ORDER BY destination_count DESC
        LIMIT 3
    """

    # 3 months
    three_months_ago = datetime.now() - timedelta(days=90)
    cursor.execute(query_destinations, (three_months_ago, airline_name))
    top_destinations_last3months = cursor.fetchall()

    # Last year
    last_year = datetime.now() - timedelta(days=365)
    cursor.execute(query_destinations, (last_year, airline_name))
    top_destinations_lastyear = cursor.fetchall()
    
    cursor.close()
    return render_template("staff_top_destinations.html",
                           top_destinations_last3months = top_destinations_last3months,
                           top_destinations_lastyear = top_destinations_lastyear)




# [不一定需要] Staff 11 -- Grant Permissions [? Admin ONLY]:
@app.route('/staff_grant_permission', methods=['GET', 'POST'])
def staff_grant_permission():
    if 'email' not in session or session['role'] != 'staff':
        return redirect(url_for('login'))

    cursor = conn.cursor()

    # Get current staff's airline
    cursor.execute("SELECT airline_name FROM airline_staff WHERE username = %s", (session['email'],))
    current_staff_airline = cursor.fetchone()
    if not current_staff_airline:
        flash("Your airline could not be found.")
        cursor.close()
        return redirect(url_for('staff_home'))

    airline_name = current_staff_airline[0]

    if request.method == 'POST':
        username = request.form['username']
        permission = request.form['permission']

        # Step 1: Verify that the user exists
        cursor.execute("SELECT airline_name FROM airline_staff WHERE username = %s", (username,))
        staff_info = cursor.fetchone()

        if not staff_info:
            flash("The username does not exist in the system.")
            cursor.close()
            return redirect(url_for('staff_grant_permission'))

        staff_airline_name = staff_info[0]

        # Step 2: Confirm they work for the same airline
        if airline_name != staff_airline_name:
            flash("You can only grant permissions to staff within your own airline.")
            cursor.close()
            return redirect(url_for('staff_grant_permission'))

        # Step 3: Ensure they don't already have permission
        cursor.execute("SELECT * FROM permission WHERE username = %s", (username,))
        if cursor.fetchone():
            flash("This staff member already has a permission assigned.")
            cursor.close()
            return redirect(url_for('staff_grant_permission'))

        # Step 4: Insert permission
        if permission not in ['Admin', 'Operator']:
            flash("Invalid permission type.")
            cursor.close()
            return redirect(url_for('staff_grant_permission'))

        try:
            cursor.execute("INSERT INTO permission (username, permission_type) VALUES (%s, %s)", (username, permission))
            conn.commit()
            flash("Permission granted successfully!")
        except:
            flash("Error: Granting permission failed.")

        cursor.close()
        return redirect(url_for('staff_grant_permission'))

    cursor.close()
    return render_template('staff_grant_permission.html')

 

# Staff 12 -- Add Booking Agents [Admin ONLY]:
@app.route('/staff_add_agent', methods=['GET', 'POST'])
def staff_add_agent():
    if 'email' not in session or session['role'] != 'staff':
        return redirect(url_for('login'))

    cursor = conn.cursor()

    # 1. Get the airline of the current staff
    cursor.execute("SELECT airline_name FROM airline_staff WHERE username = %s", (session['email'],))
    result = cursor.fetchone()
    if not result:
        flash("Your airline could not be found.")
        cursor.close()
        return redirect(url_for('staff_home'))

    airline_name = result[0]

    # 2. Check if current staff has Admin permission
    cursor.execute("SELECT permission_type FROM permission WHERE username = %s", (session['email'],))
    permissions = [row[0] for row in cursor.fetchall()]
    if 'Admin' not in permissions:
        flash("You do not have permission to add booking agents.")
        cursor.close()
        return redirect(url_for('staff_home'))

    if request.method == 'POST':
        agent_email = request.form['email']

        # 3. Check if the agent exists
        cursor.execute("SELECT * FROM booking_agent WHERE email = %s", (agent_email,))
        if not cursor.fetchone():
            flash("This agent does not exist in the system.")
            cursor.close()
            return redirect(url_for('staff_add_agent'))

        # 4. Check if agent already works for this airline
        cursor.execute("""
            SELECT * FROM booking_agent_work_for
            WHERE email = %s AND airline_name = %s
        """, (agent_email, airline_name))
        if cursor.fetchone():
            flash("This agent already works for your airline.")
            cursor.close()
            return redirect(url_for('staff_add_agent'))

        # 5. Assign agent to airline
        try:
            cursor.execute("""
                INSERT INTO booking_agent_work_for (email, airline_name)
                VALUES (%s, %s)
            """, (agent_email, airline_name))
            conn.commit()
            flash("Booking agent successfully added to your airline!")
        except Exception as e:
            flash(f"Error: Could not add agent. {str(e)}")

        cursor.close()
        return redirect(url_for('staff_add_agent'))

    cursor.close()
    return render_template('staff_add_agent.html')


# [City Alias]
# [Perform server-side validation of all inputs]
      
    
@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('role', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run('127.0.0.1',5001, debug=True)