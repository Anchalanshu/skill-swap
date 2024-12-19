from flask import Flask, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash  # For hashing passwords
import mysql.connector
import sqlite3
import bcrypt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')

# Database connection setup using values from .env file
conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB")
)
cursor = conn.cursor()



# Route for form page
@app.route('/')
def form():
    return render_template('form.html')

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        skills = request.form['skills']
        purpose = request.form['purpose']
        contact = request.form['contact']
        profile_picture = request.form['profile_picture']
        email = request.form['email']
        password = request.form['password']

        # Check if the email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            error_message = "Email already registered!"
            return render_template('form.html', error=error_message)

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert into the database
        query = "INSERT INTO users (name, skills, purpose, contact, profile_picture, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (name, skills, purpose, contact, profile_picture, email, hashed_password)
        cursor.execute(query, values)
        conn.commit()

        return redirect('/landing')  # Redirect to the landing page
    return render_template('form.html')  # Render your registration page

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None  # Variable to hold error message
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Fetch the user from the database based on email
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[7].encode('utf-8')):  # user[7] is the hashed password
            # Login successful, redirect to landing page or wherever needed
            return redirect('/landing')
        else:
            error_message = "Login failed, check your email or password. Retry"  # Set the error message
    
    return render_template('login.html', error_message=error_message)  # Pass the error message to the template




# Route for landing page with search and filters
@app.route('/landing', methods=['GET'])
def landing():
    query = request.args.get('query', '').strip()
    filter_selected = request.args.getlist('filter')  # Get selected filters
    
    # Prepare the base query
    base_query = "SELECT * FROM users WHERE 1=1"  # Start with a true condition
    conditions = []
    params = []

    # Check if there's a search query
    if query:
        conditions.append(
            "(LOWER(TRIM(name)) LIKE LOWER(TRIM(%s)) OR "
            "LOWER(TRIM(skills)) LIKE LOWER(TRIM(%s)) OR "
            "LOWER(TRIM(purpose)) LIKE LOWER(TRIM(%s)))"
        )
        params.extend(['%' + query + '%'] * 3)

    # Add filter conditions if any filters are selected
    if filter_selected:
        for filter_item in filter_selected:
            if filter_item == 'hackathon':
                conditions.append("LOWER(TRIM(skills)) LIKE '%hackathon%' OR LOWER(TRIM(purpose)) LIKE '%hackathon%'")
            elif filter_item == 'project':
                conditions.append("LOWER(TRIM(skills)) LIKE '%project%' OR LOWER(TRIM(purpose)) LIKE '%project%'")
            elif filter_item == 'skill_up':
                conditions.append("LOWER(TRIM(skills)) LIKE '%skill up%' OR LOWER(TRIM(purpose)) LIKE '%skill up%'")
            elif filter_item == 'web_development':
                conditions.append("LOWER(TRIM(skills)) LIKE '%web development%'")
            elif filter_item == 'aiml':
                # Updated condition to include 'artificial intelligence' and 'machine learning'
                conditions.append(
                    "LOWER(TRIM(skills)) LIKE '%aiml%' OR "
                    "LOWER(TRIM(skills)) LIKE '%artificial intelligence%' OR "
                    "LOWER(TRIM(skills)) LIKE '%machine learning%' OR "
                    "LOWER(TRIM(purpose)) LIKE '%aiml%' OR "
                    "LOWER(TRIM(purpose)) LIKE '%artificial intelligence%' OR "
                    "LOWER(TRIM(purpose)) LIKE '%machine learning%'"
                )

    # Combine conditions and execute the query
    if conditions:
        filter_query = " AND ".join(conditions)
        
        if query:
            cursor.execute(
                f"{base_query} AND ({filter_query})", params
            )
        else:
            cursor.execute(
                f"{base_query} AND ({filter_query})"
            )
        user_data = cursor.fetchall()
    else:
        # If there were no conditions, return an empty list
        user_data = []

    return render_template('landing.html', users=user_data)


# Route for collaborate page
@app.route('/collaborate', methods=['GET'])
def collaborate():
    query = request.args.get('query', '').strip()
    filter_selected = request.args.getlist('filter')  # Get selected filters

    return render_template('collaborate.html')

# Route for code_board
@app.route('/code_board', methods=['GET'])
def code_board():
    query = request.args.get('query', '').strip()
    filter_selected = request.args.getlist('filter')  # Get selected filters

    return render_template('code_board.html')

# Route for skill_swap
@app.route('/skill_swap', methods=['GET'])
def skill_swap():
    query = request.args.get('query', '').strip()
    filter_selected = request.args.getlist('filter')  # Get selected filters

    return render_template('skill_swap.html')



@app.route('/users')
def users():
    cursor.execute("SELECT id, name, skills, purpose, contact, profile_picture, email, password FROM users")
    user_data = cursor.fetchall()
    print(user_data)  # Print the fetched user data to the console
    return render_template('users.html', users=user_data)




# Route for search functionality
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    if query:
        cursor.execute(
            "SELECT * FROM users WHERE "
            "LOWER(TRIM(name)) LIKE LOWER(TRIM(%s)) OR "
            "LOWER(TRIM(skills)) LIKE LOWER(TRIM(%s)) OR "
            "LOWER(TRIM(purpose)) LIKE LOWER(TRIM(%s))",
            ('%' + query + '%', '%' + query + '%', '%' + query + '%')
        )
        user_data = cursor.fetchall()
        return render_template('landing.html', users=user_data)  # Pass users to the landing page
    return redirect('/landing')

if __name__ == '__main__':
    app.run(debug=True)




