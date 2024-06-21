import os
from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()

@app.route('/')
def index():
    return render_template('index.html')
# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC0e99256697bbcea8c4a142f9bab25523'
    TWILIO_SYNC_SERVICE_SID = 'ISa109dd2c9e372aefa8f92b7d4a5c5997'
    TWILIO_API_KEY = 'SKed9389b1aa6180e3708381275dbfb6f9'
    TWILIO_API_SECRET = '8ioBl5lAE4QCYRA8svC0kkhwUJKPfWM2'

    username = request.args.get('username', fake.user_name())
    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())
# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad = request.form['text']
    with open('workfile.txt', 'w') as f:
        f.write(text_from_notepad)
    path_to_store = "workfile.txt"
    return send_file(path_to_store, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0')