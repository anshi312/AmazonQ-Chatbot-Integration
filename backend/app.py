from flask import Flask, request, jsonify
import boto3
from flask_cors import CORS
import uuid
import json

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

# AWS credentials and Q App ID
ACCESS_KEY = 'XXXX'
SECRET_KEY = 'XXXXX'
APP_ID = 'XXXX'

# Initialize Q Business client
client = boto3.client(
    'qbusiness',
    region_name='us-west-2',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

###################################################
# @app.route('/chat', methods=['POST'])
# def chat():
#     print("Chat route hit")
#     try:
#         user_input = request.json.get('message')
#         print("User input:", user_input)

#         # Anonymous mode, no conversationId or userId
#         response = client.chat_sync(
#             applicationId=APP_ID,
#             userMessage=user_input
#         )

#         print("Raw response:", response)
#         print("Response type:", type(response))

#         # Safely extract system message
#         if isinstance(response, dict):
#             system_message = response.get('systemMessage')
#             if system_message and isinstance(system_message, dict):
#                 reply = system_message.get('content', '[No content]')
#             else:
#                 reply = '[No systemMessage in response]'
#         else:
#             reply = f"[Amazon Q returned unexpected string: {response}]"

#         print("Q reply:", reply)
#         return jsonify({'reply': reply})

#     except Exception as e:
#         print("Error in /chat:", e)
#         return jsonify({'reply': 'Backend error: ' + str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True, silent=True)
        if not isinstance(data, dict):
            return jsonify({'reply': 'Invalid request format'}), 400

        user_input = data.get('message', '')
        print("User input:", user_input)

        response = client.chat_sync(
            applicationId=APP_ID,
            userMessage=user_input
        )

        print("=== DEBUG: type(response) ===", type(response))
        print("=== DEBUG: response ===", response)

        if isinstance(response, dict):
            print("✓ Response is a dict.")
            reply = response.get('systemMessage') or '[No systemMessage in response]'
        elif isinstance(response, str):
            print("✓ Response is a string.")
            reply = f"[Raw string response from Q]: {response}"
        else:
            reply = f"[Unexpected response type: {type(response)}]"

        return jsonify({'reply': reply})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'reply': 'Backend error: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
