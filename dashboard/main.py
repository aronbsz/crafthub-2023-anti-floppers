from flask import Flask, request, jsonify, render_template
from google.cloud import bigquery

app = Flask(__name__)

# Initialize the BigQuery client
client = bigquery.Client(project="vernal-signal-387115")

@app.route('/messages', methods=['POST'])
def add_message():
    data = request.get_json()
    query = """
        INSERT INTO `vernal-signal-387115.fraud_test.chrome_extension_messages` (EVENT_TIME, SOURCE, MESSAGE_ID, FRAUD_SCORE, USER_ID)
        VALUES ('{}', '{}', '{}', {}, '{}')
    """.format(
        data['EVENT_TIME'],
        data['SOURCE'],
        data['MESSAGE_ID'],
        data['FRAUD_SCORE'],
        data['USER_ID']
    )
    client.query(query)

    return jsonify({'message': 'New message added to the database'}), 201

@app.route('/messages', methods=['GET'])
def get_messages():
    query = """
        SELECT *
        FROM `vernal-signal-387115.fraud_test.chrome_extension_messages`
    """
    result = client.query(query)

    messages = []
    for row in result:
        message = {
            'EVENT_TIME': row['EVENT_TIME'],
            'SOURCE': row['SOURCE'],
            'MESSAGE_ID': row['MESSAGE_ID'],
            'FRAUD_SCORE': row['FRAUD_SCORE'],
            'USER_ID': row['USER_ID']
        }
        messages.append(message)

    return render_template('page.html', messages=messages)

if __name__ == "__main__":
    app.run(debug=True)