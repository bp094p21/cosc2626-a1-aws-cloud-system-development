from subs import get_subscriptions, subscribe_new, unsubscribe_music
from search import search_music
from login import login_user
from register import register_user
import json
import uuid
import ast
import boto3
from flask import Flask, jsonify, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret'

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_login = dynamodb.Table('login')
table_music = dynamodb.Table('music')
table_subscriptions = dynamodb.Table('subscriptions')
s3 = boto3.client('s3')

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Authenticate login
        user = login_user(email, password, dynamodb, api=True)
        # Success
        if user:
            # Store user data in session
            session['email'] = email
            session['username'] = user.get('user_name')
            # Update subscriptions
            session['subscriptions'] = get_subscriptions(email, dynamodb, api=True)
            # Redirect to the user account page if the login is successful
            return redirect(url_for('user_account'))
        # Fail
        else:
            error = 'Invalid email or password. Try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

# User account registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        # If email matches w/ table, show "Email already exists" on register page
        user = register_user(email, username, password, api=True)
        # New Registration successful
        if user:
            return redirect(url_for('login'))
        # Email already registered
        else:
            error = 'Email already exists.'
            return render_template('register.html', error=error)
    else:
        return render_template('register.html')

# User account page
@app.route('/account', methods=['GET', 'POST'])
def user_account():
    if request.method == 'POST':

        title = request.form['title'].strip()
        year_value = request.form['year']
        artist = request.form['artist'].strip()

        if not (title or year_value or artist):
            error_msg = "Please enter at least one value in input fields."
            return render_template('account.html', user=session, msg=error_msg)

        result = search_music(title, year_value, artist, dynamodb, api=True)
        # Results found
        if result:
            session['results'] = result
            return render_template('account.html', user=session)
        # No results found
        else:
            # If no search criteria were submitted, redirect to the search page
            error_msg = "No results were found. Please try again."
            return render_template('account.html', user=session, msg=error_msg)
    else:
        return render_template('account.html', user=session)
    
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = session['email']  # replace with the actual user's email
    title = request.form['title']
    artist = request.form['artist']
    year = request.form['year']
    
    current_subscription_titles = [x['title'] for x in session['subscriptions']]
    if title in current_subscription_titles:
        # Return error message saying already subscribed.
        error = 'You are already subscribed to ' + title + '.'
        return render_template('account.html', user=session, msg=error)

    subscribe_new(email, title, artist, year, dynamodb, api=True)
    session['subscriptions'] = get_subscriptions(email, dynamodb, api=True)
    success_msg = "Successfully subscribed to " + title + "!"
    session.pop('results', None)

    return render_template('account.html', user=session, msg=success_msg)

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = session['email']
    subscription_id = request.form['subid']
    unsubscribe_music(email, subscription_id, dynamodb, api=True)

    session['subscriptions'] = get_subscriptions(email, dynamodb, api=True)
    session.pop('results', None)

    return render_template('account.html', user=session)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    session.pop('subscriptions', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
