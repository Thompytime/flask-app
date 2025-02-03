from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize an empty data variable
data = {}

def fetch_data():
    global data
    print("Fetching data from API...")
    try:
        # Replace with your API URL
        response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        print("Data fetched successfully!")
    except Exception as e:
        print(f"Error fetching data: {e}")

# Schedule the fetch_data function to run every 30 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_data, 'interval', seconds=30)
scheduler.start()

# Fetch data immediately when the server starts
fetch_data()

@app.route('/data')
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)