from flask import Flask, request
import csv
import os

app = Flask(__name__)

# Global variable to store the initial balance
initial_balance = None

# Path to the CSV file where data will be stored
csv_file_path = '../bots/action_log.csv'

'''
Usage of set_initial balance:
Json body:
{
    'initial_balance': 1000
}
'''

@app.route('/set_initial_balance', methods=['POST'])
def set_initial_balance():
    global initial_balance
    initial_balance = request.json.get('initial_balance', 0)
    return f"Initial balance set to {initial_balance}"

'''
Usage of log_Action:
Json Body:
{
    'action': 'buy',
    'time': '2023-12-05 10:00:00',
    'investment_type': 'short_term',
    'amount': 100,
    'total_balance': 1000,
    'currency_rate': 0.5
}
'''

@app.route('/log_action', methods=['POST'])
def log_action():
    global initial_balance
    data = request.json

    # Calculate the balance difference
    if initial_balance is not None:
        balance_difference = float(data['total_balance']) - float(initial_balance)
        data['balance_difference'] = balance_difference
    else:
        data['balance_difference'] = 'initial_balance_not_set'

    # Check if the file exists. If not, create it with the header
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writeheader()

    # Write the data to the CSV file
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writerow(data)

    return "Action logged successfully"

if __name__ == '__main__':
    app.run(debug=True, port=8111)
