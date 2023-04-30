from flask import Flask, render_template, request, jsonify, redirect, url_for, g, session
app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route('/')
def login_page():
    session['authenticated'] = False
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    if email == 'shayan@gmail.com' and password == '12345':
        # successful login, redirect to home page
        session['authenticated'] = True
        return redirect(url_for('home_page'))
    else:
        # login failed, return error message
        error = 'Invalid email or password'
        # Render template with error variable
        return render_template('login.html', error=error)
        
@app.route('/home')
def home_page():
    if session.get('authenticated'):
        return "This is the home page"
    else:
        return "User is not authenticated"

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug = True)