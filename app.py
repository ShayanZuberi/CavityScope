from flask import Flask, render_template, request, jsonify, redirect, url_for, g, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import cv2
import numpy as np
import base64
app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cavityscope.db"
db = SQLAlchemy(app)

class CavityReport(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.String(50), nullable = False)
    findings = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f" {self.id} - {self.user_email} - {self.findings}"

@app.route('/')
def login_page():
    session['authenticated'] = False
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    if email == 'shayan@gmail.com' and password == 'shayan#strongPassword12345':
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
        return render_template("home.html")
    else:
        return "User is not authenticated"

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login_page'))

@app.route('/process_image', methods=['POST'])
def process_image():
  # Get the image file from the POST request
  image_file = request.files['image']
  image_data = image_file.read()
  img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
  processed_img = detect_cavity(img)
  retval, buffer_img = cv2.imencode('.jpg', processed_img)
  response = {'image': base64.b64encode(buffer_img).decode('utf-8')} 
  return jsonify(response)

def detect_cavity(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply a median blur to reduce noise
    gray = cv2.medianBlur(gray, 5)

    # Apply adaptive thresholding
    threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate over contours and identify cavities
    for cnt in contours:
        # Ignore small contours
        if cv2.contourArea(cnt) < 500:
            continue

        # Check if the contour is inside the tooth area
        mask = np.zeros(gray.shape, np.uint8)
        cv2.drawContours(mask, [cnt], -1, 255, -1)
        masked_gray = cv2.bitwise_and(gray, mask)
        avg_color = np.mean(masked_gray)
        if avg_color > 300:
            continue

        # Draw a bounding box around the cavity
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    return img



if __name__ == '__main__':
    app.run(debug = True)