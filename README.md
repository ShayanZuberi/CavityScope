# CavityScope
CavityScope is a Python Flask app for detecting dental cavities and mal-positioned teeth. The app processes images of teeth using OpenCV and machine learning techniques to provide an accurate assessment of dental health. CavityScope is designed to be fast, accurate, and user-friendly, with a simple GUI that allows users to upload images and receive a detailed report on the extent of damage caused by cavities.

# Features
CavityScope provides the following features:

Dental cavity detection: The app uses machine learning models and image processing techniques to detect dental cavities with high accuracy.
Mal-positioned teeth detection: CavityScope can also detect mal-positioned teeth and suggest whether the subject would be a good case for using braces.
Damage quantification: The app quantifies the extent of damage caused by cavities and provides a report with findings.
Report generation: CavityScope generates a report in a text file, providing a detailed description of the findings and quantifying the extent of damage.
Friendly GUI: The app has a simple, user-friendly interface that allows users to easily upload images and receive reports.

# Getting started
To get started with CavityScope, you'll need to:

Clone the repo: git clone git@github.com:ShayanZuberi/CavityScope.git
Install the necessary dependencies: pip install -r requirements.txt
Start the Flask app: flask run
Navigate to http://localhost:5000 in your web browser.
Once you've started the app, you'll be able to upload images of teeth and receive a detailed report on dental health.

# Limitations
CavityScope has been trained on a specific dataset of dental images, and its accuracy may vary when applied to images outside of this dataset. Additionally, while the app can detect dental cavities with high accuracy, it is not a replacement for a dental professional's diagnosis and should be used for informational purposes only.

# Contributing
If you'd like to contribute to CavityScope, feel free to submit a pull request with your changes. We welcome contributions from all developers, and we'll be happy to review your changes and merge them into the main branch if they meet our standards.
