from flask import Flask, request, render_template
import json
import psycopg2
'''
from psycopg2.extras import Json
from psycopg2.extensions import register_adapter

register_adapter(dict, Json)

conn = psycopg2.connect(
    dbname="seqwrc",
    user="postgres",
    password="tipping",
    host="db"
)
conn.autocommit = True
cursor = conn.cursor()

# Check for tables
try:
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT, name TEXT, flags TEXT[])")
except psycopg2.errors.DuplicateTable:
    pass

try:
    cursor.execute("CREATE TABLE posts (id TEXT, author TEXT, date TEXT, content TEXT, comments TEXT[])")
except psycopg2.errors.DuplicateTable:
    pass

# Create admin user
cursor.execute("SELECT * FROM users WHERE username='admin'")
if cursor.fetchone() is None:
    cursor.execute("INSERT INTO users (username, password, name, flags, children) VALUES ('admin', 'admin', 'Admin', ARRAY ['admin'], ARRAY []::text[])")

# DB Functions
def db_create_user(username, password, name, flags = []):
    cursor.execute("INSERT INTO users (username, password, name, flags, children) VALUES (%s, %s, %s, %s::text[], %s::text[])", (username, password, name, flags, children))

TOKENS = {}

def auth(request):
    token = request.cookies.get('token')
    if token is None:
        return False
    try: username = TOKENS[token]
    except KeyError: return False
    return username

def get_user(username):
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    return user

def create_user(username, password, name, flags = [], children = []):
    cursor.execute("INSERT INTO users (username, password, name, flags, children) VALUES (%s, %s, %s, %s::text[], %s::text[])", (username, password, name, flags, children))

'''
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/members")
def members():
    return "Members"

@app.route("/members/<string:name>")
def getMember(name):
    return name

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    else:
        return 'You are probably using GET'


app.run(debug=True)

