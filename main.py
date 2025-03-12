from flask import Flask, request, render_template, make_response, redirect
import psycopg2, json
import sys, os, time
from datetime import datetime
from datetime import timezone, timedelta

## GET FLAGS ##
args = sys.argv[1:]
if 'local' in args:
    LOCAL = True
else:
    LOCAL = False
if 'debug' in args:
    DEBUG = True
else:
    DEBUG = False

## DATABASE SETUP ##
if LOCAL == False:
    from psycopg2.extras import Json
    from psycopg2.extensions import register_adapter
    register_adapter(dict, Json)
    conn = psycopg2.connect(
        host="db",
        database="seqwrc",
        user="postgres",
        password="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    

    # create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL UNIQUE,
        name VARCHAR(50) NOT NULL,
        bio TEXT,
        followers TEXT[],
        following TEXT[],
        posts TEXT[],
        events TEXT[],
        gear json
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        title VARCHAR(50) NOT NULL,
        date DATE NOT NULL,
        content json NOT NULL,
        likes TEXT[],
        comments TEXT[],
        type VARCHAR(10) NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS shoes (
        id SERIAL PRIMARY KEY,
        brand VARCHAR(50) NOT NULL,
        model VARCHAR(50) NOT NULL,
        review TEXT NOT NULL,
        date DATE NOT NULL,
        tags TEXT[]
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS blog (
        id SERIAL PRIMARY KEY,
        title VARCHAR(50) NOT NULL,
        date DATE NOT NULL,
        content TEXT NOT NULL,
        comments TEXT[],
        tags TEXT[]
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contact (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL,
        message TEXT NOT NULL
    )
    ''')

    # create admin user
    try: cursor.execute('''INSERT INTO users (username, password, email, name, bio, followers, following, posts, events, gear) VALUES ('admin', 'admin', 'lawson.conallin@gmail.com', 'Admin', 'Admin user. \nUsually Run by NotLawson (lawson.conallin@gmail.com).', '{}', '{}', '{}', '{}', '{}')''')
    except: pass # user already exists, ignore

# db functions
def get_user(username):
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    return cursor.fetchone()
def get_user_id(user_id):
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchone()
def create_user(username, password, email, name):
    cursor.execute("INSERT INTO users (username, password, email, name, bio, followers, following, posts, events, gear) VALUES (%s, %s, %s, %s, '', '{}', '{}', '{}', '{}', '{}')", (username, password, email, name))
def delete_user(id):
    cursor.execute(f'DELETE FROM users WHERE id = {id}')

def get_post(post_id):
    cursor.execute(f'SELECT * FROM posts WHERE id = {post_id}')
    return cursor.fetchone()
def get_posts(user_id):
    cursor.execute(f'SELECT * FROM posts WHERE user_id = {user_id}')
    return cursor.fetchall()
def get_all_posts():
    cursor.execute('''
    SELECT sub.*
    FROM (SELECT * 
          FROM posts 
          ORDER BY date DESC
          LIMIT 100
         ) sub
    ORDER BY date ASC;
    ''')
    return cursor.fetchall()
def get_following_posts(username):
    cursor.execute('SELECT following FROM users WHERE username = %s', (username,))
    following = cursor.fetchone()[0]
    cursor.execute('''
    SELECT sub.*
    FROM (SELECT * 
          FROM posts
          WHERE user_id = ANY(%s)
          ORDER BY date DESC
          LIMIT 100
         ) sub
    ORDER BY date ASC;
    ''', (following,))
    return cursor.fetchall()


## APP SETUP ##
app = Flask(__name__)
TOKENS = {}

def auth(request):
    token = request.cookies.get('token')
    if token is None:
        return False
    try: id = TOKENS[token]
    except KeyError: return False
    return id


## MAIN/MISC ##
def main_not_built():
    return render_template('not_built.html')

@app.route('/')
def main_index():
    '''
    Main page of the website.
    '''
    id=auth(request)
    if id == False:
        return render_template('index.html')
    else:
        user = get_user_id(id)
        return render_template('index.html', user=user)

@app.route('/about')
def main_about():
    '''
    About page for SEQWRC
    '''
    id=auth(request)
    if id == False:
        return render_template('about.html')
    else:
        user = get_user_id(id)
        return render_template('about.html', user=user)


@app.route('/contact', methods=['GET', 'POST'])
def main_contact():
    '''
    Contact page for SEQWRC
    Contains a form that logs a message to the database, which can be accessed by the admin at admin_contact (/admin/contact)
    '''
    id=auth(request)
    if id == False:
        user = None
    else:
        user = get_user_id(id)

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        cursor.execute(f"INSERT INTO contact (name, email, message) VALUES ('{name}', '{email}', '{message}')")
        return render_template('contact.html', message_good=message, user=user)
    return render_template('contact.html', user=user)

@app.route('/search')
def main_search():
    '''
    Searches SEQWRC
    Mainly searches posts and users, but will also return things from Joe's Shoes
    '''
    return main_not_built()

@app.route('/search/<query>')
def main_search_query(query):
    '''
    See main_search
    '''
    return main_not_built()

## ACCOUNTS ##
@app.route('/login', methods=['GET', 'POST'])
def accounts_login():
    '''
    Login page for SEQWRC
    An account is only needed to post, follow, and comment on things on the website. 
    Other things don't require an account.
    '''
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = get_user(username) # get user object from the database
        if user == None: # username not in database
            return render_template('login.html', message_bad="User not found")
        if user[2] == password:
            # logged in
            token = os.urandom(16).hex()  # gen user id
            TOKENS[token] = user[0] # add to token store along with userId

            url = request.args.get('next', '/') # get the redirect url
            resp = make_response(redirect(url))
            resp.set_cookie('token', token) # set cookie
            return resp
        return render_template('login.html', message_bad="Incorrect password") # incorrect password
    return render_template('login.html') # login page

@app.route('/signup', methods=['GET', 'POST'])
def accounts_signup():
    '''
    Signup page for SEQWRC
    See accounts_login for more info on accounts
    '''
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        try: 
            create_user(username, password, email, name)
            return redirect('/login')
        except:
            return render_template('signup.html', message_bad="User already exists")
    return render_template('signup.html')

@app.route('/logout')
def accounts_logout():
    '''
    Signout endpoint for SEQWRC
    Redirects to main_index (/)
    '''
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', expires=0)
    return resp

@app.route('/account', methods=['GET', 'POST', 'DELETE'])
def accounts_account():
    '''
    Account manager for SEQWRC
    Allows users to edit account details and delete their account
    See admin_login for more info on accounts
    '''
    id = auth(request)
    if id == False:
        return redirect('/login?next=/account')
    user = get_user_id(id)
    if user == None:
        return redirect('/login?next=/account')
    
    if request.method == "DELETE":
        # (endpoint)
        delete_user(id)
        return "done"
    if request.method == "POST":
        # edit account
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']

        cursor.execute(f"UPDATE users SET username = '{username}', password = '{password}', email = '{email}', name = '{name}' WHERE id = {id}")
        user = get_user_id(id)
        return render_template('account.html', user=user, message_good="Account updated")
    return render_template('account.html', user=user)

## SOCIAL ##
@app.route('/feed')
def social_feed():
    '''
    Social feed for SEQWRC
    There are 3 different types of posts:
     - Run: Contains metadata such as distance, time, pace etc.
     - Event: Contains metadata such as location, date, time, etc.
     - Post: Contains text and images
    All posts have the following metadata:
     - User: The user who posted the post
     - Title: The title of the post
     - Date: The date the post was posted
     - Likes: A list of users who have liked the post
     - Comments: A list of comments on the post
     - Content: The content of the post.
    
    This page will display posts from users that the current user follows, aswell as all posts in a seperate tab.
    '''
    id = auth(request)
    if id == False:
        return redirect('/login?next=/feed')
    user = get_user_id(id)
    if user == None:
        return redirect('/login?next=/feed')
    
    posts = get_following_posts(user[1])
    if posts==None:
        posts = []
    all_posts = get_all_posts()
    if all_posts==None:
        all_posts = ()
    return render_template('feed.html', user=user, posts=posts, all=all_posts, get_user_id=get_user_id, json=json, str=str)

@app.route('/feed/new', methods=['GET', 'POST'])
def social_new_post():
    '''
    Creates a new post
    See social_feed for more info on posts
    '''
    id = auth(request)
    if id == False:
        return redirect('/login?next=/feed')
    user = get_user_id(id)
    if user == None:
        return redirect('/login?next=/feed')
    
    if request.method == "POST":
        title = request.form['title']
        type = request.form['type']
        if type=="post":
            data = {
                "content":request.form['content']
            }
            
        elif type=="run":
            distance = request.form['distance']
            hours = request.form['hours']
            minutes = request.form['minutes']
            seconds = request.form['seconds']
            hours_in_mins = int(hours)*60
            mins_in_seconds = (int(minutes)+hours_in_mins)*60
            time = mins_in_seconds + int(seconds)
            pace_in_seconds = int(time/float(distance))
            pace_in_mins = str(int(pace_in_seconds/60)).split(".")
            pace_in_mins[0] = int(pace_in_mins[0])
            if len(pace_in_mins) == 1:
                pace_in_mins[1] = 0
            else:
                pace_in_mins[1] = 60/int(pace_in_mins[1])
            
            pace = f'{pace_in_mins[0]}:{pace_in_mins[1]}'
            time = f'{hours}:{minutes}:{seconds}'
            description = request.form['description']
            data = {
                "distance": distance,
                "time": time,
                "pace": pace,
                "description": description
            }
        elif type=="event":
            date = request.form['date']
            location = request.form['location']
            description = request.form['description']

            data = {
                "date": date,
                "location": location,
                "description": description
            }

        date = datetime.now(timezone(timedelta(hours=10))).strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO posts (user_id, title, date, content, likes, comments, type) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user[0], title, date, json.dumps(data), '{}', '{}', type))
        return redirect(f'/feed')

    return render_template("new_post.html", user=user)

@app.route('/feed/<post_id>', methods=['GET', 'POST'])
def social_post(post_id):
    '''
    Displays a specific post
    See social_feed for more info on posts
    '''
    
    return main_not_built()

@app.route('/feed/<post_id>/edit', methods=['GET', 'POST', 'DELETE'])
def social_edit_post(post_id):
    '''
    Edits a post
    Also deletes a post
    See social_feed for more info on posts
    '''
    return main_not_built()

@app.route('/feed/<post_id>/like', methods=['GET', 'DELETE'])
def social_like_post(post_id):
    '''
    (endpoint) Likes a post
    Also remove like from a post
    See social_feed for more info on posts
    '''
    return main_not_built()

@app.route('/feed/<post_id>/comment', methods=['POST', 'DELETE'])
def social_comment_post(post_id):
    '''
    (endpoint) Comments on a post
    Also deletes a comment
    See social_feed for more info on posts
    '''
    return main_not_built()

@app.route('/profile', methods=['GET', 'POST'])
def social_all_profiles():
    '''
    Profiles
    Profiles are user facing accounts for the other users. They contain the following metadata:
     - Username: The username of the user
     - Name: The name of the user
     - Bio: The bio of the user. This can contain Markdown, but no HTML. This cannot contain images or videos
     - Profile Picture: The profile picture of the user. This will be stored in a static user folder
     - Followers: A list of users who follow the user
     - Following: A list of users who the user follows
     - Posts: A list of posts by the user. This includes Runs and Events
     - Gear: A list of gear that the user uses. This includes shoes
        - Name: The name of the shoe
        - Brand: The brand of the shoe
        - Model: The model of the shoe
        - Distance: The distance the shoe has been used for
        - Date: The date the shoe was added
        - Retired: Whether the shoe has been retired or not
     - Events: A list of events that the user has participated in (NOT CREATED: SEE Posts)

    This page will display diplay a search bar, current followers/following, recomended users
    '''
    return main_not_built()

@app.route('/profile/<username>', methods=['GET', 'POST'])
def social_profile(username):
    '''
    Displays a specific profile
    See social_all_profiles for more info on profiles
    '''
    return main_not_built()

@app.route('/profile/<username>/follow', methods=['GET', 'DELETE'])
def social_follow(username):
    '''
    (endpoint) Follows a user
    Also unfollows a user
    See social_all_profiles for more info on profiles
    '''
    return main_not_built()

@app.route('/profile/me/edit', methods=['GET', 'POST'])
def social_edit_profile():
    '''
    Edits your profile
    See social_all_profiles for more info on profiles
    '''
    return main_not_built()

## JOE'S SHOES ##
@app.route('/joe')
def joe_index():
    '''
    Joe's Shoes
    Joe's Shoes is a blog and shoe database by Joe
    It is made of 2 parts
     - Shoes: A database of shoes that Joe has reviewed
     - Blog: A blog of Joe's running experiences, tips, and tricks
    
    This page will display the latest blog post and the latest shoe review, aswell as links to each subpage
    See joe_shoes and joe_blog for more info on each part
    '''
    return main_not_built()
@app.route('/joe/shoes')
def joe_shoes():
    '''
    Shoe Database
    Joe's shoe database contains the following metadata:
     - Brand: The brand of the shoe
     - Model: The model of the shoe
     - Review: The review of the shoe. This can contain Markdown, but no HTML. This may contain images, 
       which will be stored in a static /static/joe/shoes/<shoe_id>/ folder and linked via Markdown
     - Date: The date the shoe was added
     - Tags: A list of tags for the shoe. This can be used to filter shoes. Some tags may include: road, trail, daily, etc.

    This page will display all shoes in the database, as well as a search and filtering feature
    '''
    return main_not_built()

@app.route('/joe/shoes/<shoe_id>')
def joe_shoe(shoe_id):
    '''
    Displays a specific shoe
    See joe_shoes for more info on shoes
    '''
    return main_not_built()

@app.route('/joe/blog')
def joe_blog():
    '''
    Blog
    Joe's blog contains the following metadata:
     - Title: The title of the blog post
     - Date: The date the blog post was posted
     - Content: The content of the blog post. This can contain Markdown, but no HTML. This may contain images, 
       which will be stored in a static /static/joe/blog/<post_id>/ folder and linked via Markdown
     - Comments: A list of comments on the blog post
     - Tags: A list of tags for the blog post. This can be used to filter posts. Some tags may include: tips, experience, etc.

    This page will display all blog posts in the database, as well as a search and filtering feature
    '''
    return main_not_built()

@app.route('/joe/blog/<post_id>')
def joe_post(post_id):
    '''
    Displays a specific post
    See joe_blog for more info on posts
    '''
    return main_not_built()

@app.route('/joe/blog/<post_id>/comment', methods=['POST', 'DELETE'])
def joe_comment_post(post_id):
    '''
    (endpoint) Comments on a post
    Also edits a comment
    Also deletes a comment
    See joe_blog for more info on posts
    '''
    return main_not_built()

## ADMIN ##
@app.route('/admin', methods=['GET', 'POST'])
def admin_admin():
    '''
    Admin page for SEQWRC
    This section allows for admins to view and control users accounts, posts, the contact form and Joe's Shoes
    '''
    return main_not_built()

@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    '''
    Displays all users
    See main_login for more info on accounts
    '''
    return main_not_built()

@app.route('/admin/users/<username>', methods=['GET', 'POST'])
def admin_user(username):
    '''
    Displays a specific user
    See main_login for more info on accounts
    '''
    return main_not_built()

@app.route('/admin/users/<username>/edit', methods=['GET', 'POST', 'DELETE'])
def admin_edit_user(username):
    '''
    Edits a user
    Also deletes a user
    See main_login for more info on accounts
    '''
    return main_not_built()

@app.route('/admin/posts', methods=['GET', 'POST'])
def admin_posts():
    '''
    Displays all posts
    See social_feed for more info on posts
    '''
    return main_not_built()

@app.route('/admin/posts/<post_id>', methods=['GET', 'POST', 'DELETE'])
def admin_post(post_id):
    '''
    Displays a specific post
    See social_feed for more info on posts
    '''
    return main_not_built()

@app.route('/admin/posts/<post_id>/edit', methods=['GET', 'POST', 'DELETE'])
def admin_edit_post(post_id):
    '''
    Edits a post on behalf of the user
    Also deletes a post
    See social_feed for more info on posts
    '''
    return main_not_built()

@app.route('/admin/joe')
def admin_joe():
    '''
    Joe's Shoes Dashboard
    Link to each subpage, and show engagement stats
    See joe_shoes and joe_blog for more info on each part
    '''
    return main_not_built()

@app.route('/admin/joe/shoes')
def admin_joe_shoes():
    '''
    Shows all shoes in the database
    See joe_shoes for more info on shoes
    '''
    return main_not_built()

@app.route('/admin/joe/shoes/new', methods=['GET', 'POST'])
def admin_joe_new_shoe():
    '''
    Creates a new shoe
    See joe_shoes for more info on shoes
    '''
    return main_not_built()

@app.route('/admin/joe/shoes/<shoe_id>', methods=['GET', 'POST', 'DELETE'])
def admin_joe_shoe(shoe_id):
    '''
    Displays a specific shoe
    See joe_shoes for more info on shoes
    Also edits a shoe
    Also deletes a shoe
    '''
    return main_not_built()

@app.route('/admin/joe/blog')
def admin_joe_blog():
    '''
    Shows all blog posts in the database
    See joe_blog for more info on posts
    '''
    return main_not_built()

@app.route('/admin/joe/blog/new', methods=['GET', 'POST'])
def admin_joe_new_post():
    '''
    Creates a new post
    See joe_blog for more info on posts
    '''
    return main_not_built()

@app.route('/admin/joe/blog/<post_id>', methods=['GET', 'POST', 'DELETE'])
def admin_joe_post(post_id):
    ''''
    Displays a specific post'
    See joe_blog for more info on posts
    '''
    return main_not_built()

@app.route('/admin/joe/blog/<post_id>/edit', methods=['GET', 'POST', 'DELETE'])
def admin_joe_edit_post(post_id):
    '''
    Edits a post
    Also deletes a post
    See joe_blog for more info on posts
    '''
    return main_not_built()

@app.route('/admin/contact')
def admin_contact():
    '''
    Shows all contact tickets from the contact form
    See main_contact for more info on the contact form
    '''
    return main_not_built()

@app.route('/admin/contact/<message_id>', methods=['GET', 'DELETE'])
def admin_contact_message(message_id):
    '''
    Displays a specific message
    Also deletes a message
    See main_contact for more info on the contact form
    '''
    return main_not_built()

app.run("0.0.0.0", 8000, debug=True)