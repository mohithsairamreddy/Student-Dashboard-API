from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
import os
import logging
import time
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)
REDASH_API_KEY = os.getenv('REDASH_API_KEY', 'pGeiV72zVfRn8ZpUWSNATVl24jDdOybYBBIAKkiS')
REDASH_BASE_URL = 'https://viz-data-dashboard.ei-insights.study'
@app.route('/')
def dashboard():
    return render_template('dashboard.html')
@app.route('/api/student-data')
def get_student_data():
    start_time = time.time()
    response_data = {'error': 'Unknown error', '_latency': 0}
    status_code = 500
    
    try:
        query_id = '1283'
        results_url = f'{REDASH_BASE_URL}/api/queries/{query_id}/results.json'
        
        headers = {
            'Authorization': f'Key {REDASH_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(results_url, headers=headers, timeout=10)
        end_time = time.time()
        latency = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            if 'query_result' in data and 'data' in data['query_result'] and 'rows' in data['query_result']['data']:
                response_data = data['query_result']['data']['rows'][0]
                response_data['_latency'] = latency
                status_code = 200
            else:
                response_data = {'error': 'Invalid data format', '_latency': latency}
        else:
            response_data = {
                'error': 'Unable to fetch data from the server. Please try again later.',
                '_latency': latency
            }
            
    except requests.ConnectionError:
        response_data = {
            'error': 'Please check your internet connection and try again.',
            '_latency': time.time() - start_time
        }
    except requests.Timeout:
        response_data = {
            'error': 'The request timed out. Please try again.',
            '_latency': time.time() - start_time
        }
    except Exception as e:
        response_data = {
            'error': 'An unexpected error occurred. Please try again later.',
            '_latency': time.time() - start_time
        }
        logging.error(f"Unexpected error: {str(e)}")
    
    return jsonify(response_data), status_code
if __name__ == '__main__':
    app.run(debug=True)