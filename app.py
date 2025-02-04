from flask import Flask, jsonify, render_template
from flask_cors import CORS
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)

# Initialize an empty data variable
data = {}

def fetch_data():
    global data
    print("Fetching data from API...")  # Debugging line
    try:
        response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        response.raise_for_status()
        data = response.json()
        print("Data fetched successfully!")  # Debugging line
    except Exception as e:
        print(f"Error fetching data: {e}")  # Debugging line

# Schedule the fetch_data function to run every 15 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_data, 'interval', minutes=15)
scheduler.start()

# Fetch data immediately when the server starts
fetch_data()

@app.route('/')
def index():
    # Render the index.html file from the templates folder
    return render_template('index.html')

@app.route('/data')
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
