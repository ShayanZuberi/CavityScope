#import flask
from flask import Flask, render_template, request, jsonify, redirect, url_for, g, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import cv2
#importing numpy
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
    # Convert the image to the LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Define the color ranges for cavity detection
    color_ranges = [
        # Dark Brown/Black
        (np.array([0, 0, 0], dtype=np.uint8), np.array([40, 128, 128], dtype=np.uint8)),
        
        # Light Brown
        (np.array([20, 40, 100], dtype=np.uint8), np.array([40, 170, 180], dtype=np.uint8)),
        
        # Yellowish/Brownish
        (np.array([0, 100, 120], dtype=np.uint8), np.array([30, 170, 190], dtype=np.uint8)),
        
        # Dark Gray/Black
        (np.array([0, 0, 0], dtype=np.uint8), np.array([40, 40, 40], dtype=np.uint8)),
        
        # Unnatural Color Contrast (Low Intensity)
        (np.array([0, 0, 0], dtype=np.uint8), np.array([255, 255, 50], dtype=np.uint8)),
        
        # Greenish
        (np.array([0, 50, 0], dtype=np.uint8), np.array([60, 255, 60], dtype=np.uint8)),
        
        # Bluish
        (np.array([0, 0, 50], dtype=np.uint8), np.array([60, 60, 255], dtype=np.uint8))
    ]
    
    # Create an empty mask
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    
    # Apply color thresholding for each color range
    for lower_color, upper_color in color_ranges:
        color_mask = cv2.inRange(lab, lower_color, upper_color)
        mask = cv2.bitwise_or(mask, color_mask)
    
    # Apply morphological operations to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Find contours of the cavity areas
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw rectangles around the cavity areas on the original image
    img_with_rectangles = img.copy()
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(img_with_rectangles, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return img_with_rectangles







if __name__ == '__main__':
    app.run(debug = True)