from flask import Flask, request, render_template
import psycopg2

## DATABASE SETUP ##
conn = psycopg2.connect(
    host="db",
    database="seqwrc",
    user="postgres",
    password="postgres"
)
cursor = conn.cursor()
cursor.auto_commit = True

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
    gear TEXT[],
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    date DATE NOT NULL,
    content TEXT NOT NULL,
    likes TEXT[],
    comments TEXT[],
    type VARCHAR(10) NOT NULL
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS shoes (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    review TEXT NOT NULL,
    date DATE NOT NULL,
    tags TEXT[]
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS blog (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    content TEXT NOT NULL,
    comments TEXT[],
    tags TEXT[]
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS contact (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    message TEXT NOT NULL
''')

# create admin user
cursor.execute('''INSERT INTO users (username, password, email, name, bio, followers, following, posts, events, gear) VALUES ('admin', 'admin', 'lawson.conallin@gmail.com', 'Admin', 'Admin user. \nUsually Run by NotLawson (lawson.conallin@gmail.com).', '{}', '{}', '{}', '{}', '{}')''')

# db functions
def get_user(username):
    cursor.execute(f'SELECT * FROM users WHERE username = {username}')
    return cursor.fetchone()
def get_user_id(user_id):
    cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')
    return cursor.fetchone()

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
    cursor.execute(f'SELECT following FROM users WHERE username = {username}')
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

app = Flask(__name__)

## MAIN/MISC ##
@app.route('/')
def main_index():
    '''
    Main page of the website.
    '''
    return render_template('index.html')

@app.route('/about')
def main_about():
    '''
    About page for SEQWRC
    '''
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def main_contact():
    '''
    Contact page for SEQWRC
    Contains a form that logs a message to the database, which can be accessed by the admin at admin_contact (/admin/contact)
    '''
    return render_template('contact.html')

@app.route('/search')
def main_search():
    '''
    Searches SEQWRC
    Mainly searches posts and users, but will also return things from Joe's Shoes
    '''
    pass

@app.route('/search/<query>')
def main_search_query(query):
    '''
    See main_search
    '''
    pass

## ACCOUNTS ##
@app.route('/login', methods=['GET', 'POST'])
def accounts_login():
    '''
    Login page for SEQWRC
    An account is only needed to post, follow, and comment on things on the website. 
    Other things don't require an account.
    '''
    pass
@app.route('/signup', methods=['GET', 'POST'])
def accounts_signup():
    '''
    Signup page for SEQWRC
    See accounts_login for more info on accounts
    '''
    pass
@app.route('/logout')
def accounts_logout():
    '''
    Signout endpoint for SEQWRC
    Redirects to main_index (/)
    '''
    pass
@app.route('/account', methods=['GET', 'POST', 'DELETE'])
def accounts_account():
    '''
    Account manager for SEQWRC
    Allows users to edit account details and delete their account
    See admin_login for more info on accounts
    '''
    pass

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
     - Date: The date the post was posted
     - Likes: A list of users who have liked the post
     - Comments: A list of comments on the post
     - Content: The content of the post. For Runs and Events, this is the description of the post.
                Can contain images and YT videos, images will be stored in a static user folder and linked via Markdown
                Can contain Markdown, but no HTML
    
    This page will display posts from users that the current user follows, aswell as all posts in a seperate tab.
    '''
    pass

@app.route('/feed/new', methods=['GET', 'POST'])
def social_new_post():
    '''
    Creates a new post
    See social_feed for more info on posts
    '''
    pass

@app.route('/feed/<post_id>', methods=['GET', 'POST'])
def social_post(post_id):
    '''
    Displays a specific post
    See social_feed for more info on posts
    '''
    pass

@app.route('/feed/<post_id>/edit', methods=['GET', 'POST', 'DELETE'])
def social_edit_post(post_id):
    '''
    Edits a post
    Also deletes a post
    See social_feed for more info on posts
    '''
    pass

@app.route('/feed/<post_id>/like', methods=['GET', 'DELETE'])
def social_like_post(post_id):
    '''
    (endpoint) Likes a post
    Also remove like from a post
    See social_feed for more info on posts
    '''
    pass

@app.route('/feed/<post_id>/comment', methods=['POST', 'DELETE'])
def social_comment_post(post_id):
    '''
    (endpoint) Comments on a post
    Also deletes a comment
    See social_feed for more info on posts
    '''
    pass

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
    pass

@app.route('/profile/<username>', methods=['GET', 'POST'])
def social_profile(username):
    '''
    Displays a specific profile
    See social_all_profiles for more info on profiles
    '''
    pass

@app.route('/profile/<username>/follow', methods=['GET', 'DELETE'])
def social_follow(username):
    '''
    (endpoint) Follows a user
    Also unfollows a user
    See social_all_profiles for more info on profiles
    '''
    pass

@app.route('/profile/me/edit', methods=['GET', 'POST'])
def social_edit_profile():
    '''
    Edits your profile
    See social_all_profiles for more info on profiles
    '''
    pass

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
    pass
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
    pass

@app.route('/joe/shoes/<shoe_id>')
def joe_shoe(shoe_id):
    '''
    Displays a specific shoe
    See joe_shoes for more info on shoes
    '''
    pass

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
    pass

@app.route('/joe/blog/<post_id>')
def joe_post(post_id):
    '''
    Displays a specific post
    See joe_blog for more info on posts
    '''
    pass

@app.route('/joe/blog/<post_id>/comment', methods=['POST', 'DELETE'])
def joe_comment_post(post_id):
    '''
    (endpoint) Comments on a post
    Also edits a comment
    Also deletes a comment
    See joe_blog for more info on posts
    '''
    pass

## ADMIN ##
@app.route('/admin', methods=['GET', 'POST'])
def admin_admin():
    '''
    Admin page for SEQWRC
    This section allows for admins to view and control users accounts, posts, the contact form and Joe's Shoes
    '''
    pass

@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    '''
    Displays all users
    See main_login for more info on accounts
    '''
    pass

@app.route('/admin/users/<username>', methods=['GET', 'POST'])
def admin_user(username):
    '''
    Displays a specific user
    See main_login for more info on accounts
    '''
    pass

@app.route('/admin/users/<username>/edit', methods=['GET', 'POST', 'DELETE'])
def admin_edit_user(username):
    '''
    Edits a user
    Also deletes a user
    See main_login for more info on accounts
    '''
    pass

@app.route('/admin/posts', methods=['GET', 'POST'])
def admin_posts():
    '''
    Displays all posts
    See social_feed for more info on posts
    '''
    pass

@app.route('/admin/posts/<post_id>', methods=['GET', 'POST', 'DELETE'])
def admin_post(post_id):
    '''
    Displays a specific post
    See social_feed for more info on posts
    '''
    pass

@app.route('/admin/posts/<post_id>/edit', methods=['GET', 'POST', 'DELETE'])
def admin_edit_post(post_id):
    '''
    Edits a post on behalf of the user
    Also deletes a post
    See social_feed for more info on posts
    '''
    pass

@app.route('/admin/joe')
def admin_joe():
    '''
    Joe's Shoes Dashboard
    Link to each subpage, and show engagement stats
    See joe_shoes and joe_blog for more info on each part
    '''
    pass

@app.route('/admin/joe/shoes')
def admin_joe_shoes():
    '''
    Shows all shoes in the database
    See joe_shoes for more info on shoes
    '''
    pass

@app.route('/admin/joe/shoes/new', methods=['GET', 'POST'])
def admin_joe_new_shoe():
    '''
    Creates a new shoe
    See joe_shoes for more info on shoes
    '''
    pass

@app.route('/admin/joe/shoes/<shoe_id>', methods=['GET', 'POST', 'DELETE'])
def admin_joe_shoe(shoe_id):
    '''
    Displays a specific shoe
    See joe_shoes for more info on shoes
    Also edits a shoe
    Also deletes a shoe
    '''
    pass

@app.route('/admin/joe/blog')
def admin_joe_blog():
    '''
    Shows all blog posts in the database
    See joe_blog for more info on posts
    '''
    pass

@app.route('/admin/joe/blog/new', methods=['GET', 'POST'])
def admin_joe_new_post():
    '''
    Creates a new post
    See joe_blog for more info on posts
    '''
    pass

@app.route('/admin/joe/blog/<post_id>', methods=['GET', 'POST', 'DELETE'])
def admin_joe_post(post_id):
    ''''
    Displays a specific post'
    See joe_blog for more info on posts
    '''
    pass

@app.route('/admin/joe/blog/<post_id>/edit', methods=['GET', 'POST', 'DELETE'])
def admin_joe_edit_post(post_id):
    '''
    Edits a post
    Also deletes a post
    See joe_blog for more info on posts
    '''
    pass

@app.route('/admin/contact')
def admin_contact():
    '''
    Shows all contact tickets from the contact form
    See main_contact for more info on the contact form
    '''
    pass

@app.route('/admin/contact/<message_id>', methods=['GET', 'DELETE'])
def admin_contact_message(message_id):
    '''
    Displays a specific message
    Also deletes a message
    See main_contact for more info on the contact form
    '''
    pass

app.run(debug=True)